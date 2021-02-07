import csv
import io
import logging
from datetime import datetime, timedelta, date
import hug
import xlsxwriter
from peewee import fn, DoesNotExist, IntegrityError

from access_control.access_control import UserRoles, token_key_authentication
from config import config
from db.directives import PeeweeSession
from db.model import TimeSlot, Appointment, Booking, SlotCode, User
from secret_token.secret_token import get_random_string, get_secret_token, hash_pw

log = logging.getLogger('api')


@hug.format.content_type('text/comma-separated-values')
def format_as_csv(data, request=None, response=None):
    return data


@hug.get("/next_free_slots", requires=token_key_authentication)
def next_free_slots(db: PeeweeSession, user: hug.directives.user, at_datetime: hug.types.text = None):
    """
    SELECT t.start_date_time, count(a.time_slot_id)
FROM appointment a
         JOIN timeslot t ON a.time_slot_id = t.id
WHERE a.booked IS false
  AND a.claim_token ISNULL
  AND t.start_date_time > NOW()
GROUP BY t.start_date_time
ORDER BY t.start_date_time
    """
    with db.atomic():
        # @formatter:off
        if at_datetime is not None:
            now = datetime.fromisoformat(at_datetime).replace(tzinfo=None)
        else:
            now = datetime.now(tz=config.Settings.tz).replace(tzinfo=None)
        slots = TimeSlot \
            .select(TimeSlot.start_date_time, TimeSlot.length_min,
                    fn.count(Appointment.time_slot).alias("free_appointments")) \
            .join(Appointment) \
            .where(
                (TimeSlot.start_date_time > now) &
                (Appointment.claim_token.is_null() | (Appointment.claimed_at +
                                                      timedelta(
                                                          minutes=config.Settings.claim_timeout_min) < now)) &
                (Appointment.booked == False)
            ) \
            .group_by(TimeSlot.start_date_time, TimeSlot.length_min) \
            .order_by(TimeSlot.start_date_time) \
            .limit(config.Settings.num_display_slots)
        # @formatter:on
        return {
            "slots": [{
                "startDateTime": slot.start_date_time,
                "freeAppointments": slot.free_appointments,
                "timeSlotLength": slot.length_min
            } for slot in slots
            ],
            "coupons": user.coupons
        }


@hug.get("/claim_appointment", requires=token_key_authentication)
def claim_appointment(db: PeeweeSession, start_date_time: hug.types.text, user: hug.directives.user):
    """
    UPDATE appointment app
    SET claim_token = 'claimed'
    WHERE app.id
          IN (
              SELECT a.id FROM appointment a
                                 JOIN timeslot t on a.time_slot_id = t.id
              WHERE t.start_date_time = '2020-03-25 08:30:00.000000'
                AND a.claim_token isnull
                AND NOT a.booked
              LIMIT 1
              )
    RETURNING *
    """
    with db.atomic():
        try:
            if user.role != UserRoles.ANON:
                assert user.coupons > 0
            start_date_time_object = datetime.fromisoformat(start_date_time)
            now = datetime.now(tz=config.Settings.tz).replace(tzinfo=None)
            if start_date_time_object < now:
                raise ValueError("Can't claim an appointment in the past")
            time_slot = TimeSlot.get(
                TimeSlot.start_date_time == start_date_time_object)
            appointment = Appointment.select() \
                .where(
                (Appointment.time_slot == time_slot) &
                (Appointment.booked == False) &
                (Appointment.claim_token.is_null() | (Appointment.claimed_at +
                                                      timedelta(
                                                          minutes=config.Settings.claim_timeout_min) < now))
            ) \
                .order_by(Appointment.claim_token.desc()) \
                .get()
            appointment.claim_token = get_random_string(32)
            appointment.claimed_at = now
            appointment.save()
            return appointment.claim_token
        except DoesNotExist as e:
            raise hug.HTTPGone
        except ValueError as e:
            raise hug.HTTPBadRequest
        except AssertionError as e:
            raise hug.HTTPBadRequest


@hug.post("/book_appointment", requires=token_key_authentication)
def book_appointment(db: PeeweeSession, body: hug.types.json, user: hug.directives.user):
    with db.atomic():
        try:
            if all(key in body for key in ('claim_token', 'start_date_time', 'first_name', 'name', 'phone', 'office')):
                claim_token = body['claim_token']
                start_date_time = body['start_date_time']
                start_date_time_object = datetime.fromisoformat(
                    start_date_time)
                now = datetime.now(tz=config.Settings.tz).replace(tzinfo=None)
                if start_date_time_object < now:
                    raise ValueError("Can't claim an appointment in the past")
                time_slot = TimeSlot.get(
                    TimeSlot.start_date_time == start_date_time_object)
                appointment = Appointment.get(
                    (Appointment.time_slot == time_slot) &
                    (Appointment.booked == False) &
                    (Appointment.claim_token == claim_token)
                )
                appointment.booked = True
                appointment.claim_token = None
                appointment.claimed_at = None
                appointment.save()
                success = False
                street = body['street'] if 'street' in body else None
                street_number = body['street_number'] if 'street_number' in body else None
                post_code = body['post_code'] if 'post_code' in body else None
                city = body['city'] if 'city' in body else None
                birthday = body['birthday'] if 'birthday' in body else None
                reason = body['reason'] if 'reason' in body else None
                with db.atomic():
                    while not success:
                        secret = get_secret_token(6)
                        try:
                            SlotCode.create(
                                date=time_slot.start_date_time.date(), secret=secret)
                            success = True
                        except IntegrityError as e:  # in the offchance that we had a collision with secret codes, retry
                            pass

                booking = Booking.create(appointment=appointment, first_name=body['first_name'], surname=body['name'],
                                         phone=body['phone'], street=street,
                                         street_number=street_number,
                                         post_code=post_code, city=city, birthday=birthday,
                                         reason=reason, office=body['office'], secret=secret,
                                         booked_by=user.user_name)
                booking.save()
                if user.role != UserRoles.ANON:
                    user.coupons -= 1
                    user.save()
                return {
                    "secret": booking.secret,
                    "time_slot": time_slot.start_date_time,
                    "slot_length_min": time_slot.length_min
                }
            else:
                raise ValueError("Missing parameter")
        except DoesNotExist as e:
            raise hug.HTTPGone
        except ValueError as e:
            raise hug.HTTPBadRequest
        except AssertionError as e:
            raise hug.HTTPBadRequest


@hug.delete("/claim_token", requires=token_key_authentication)
def delete_claim_token(db: PeeweeSession, claim_token: hug.types.text):
    with db.atomic():
        try:
            appointment = Appointment.get(
                (Appointment.booked == False) &
                (Appointment.claim_token == claim_token)
            )
            appointment.claim_token = None
            appointment.claimed_at = None
            appointment.save()
        except DoesNotExist as e:
            pass
        except ValueError as e:
            pass


@hug.get("/list_for_day.csv", output=format_as_csv, requires=token_key_authentication)
def list_for_day(db: PeeweeSession, user: hug.directives.user,
                 date_of_day: hug.types.text = None):
    if not date_of_day:
        date_of_day = (date.today() + timedelta(days=1)).isoformat()
    user_name = user.user_name
    with db.atomic():
        try:
            user_role = user.role
            requested_day_object = date.fromisoformat(date_of_day)
            result = io.StringIO()
            writer = csv.DictWriter(result,
                                    fieldnames=['start_date_time', 'first_name', 'surname', 'phone', 'office', 'secret',
                                                'booked_by'])
            writer.writeheader()
            for timeslot in TimeSlot.select().where(
                    (TimeSlot.start_date_time > requested_day_object - timedelta(days=1)) &
                    (TimeSlot.start_date_time < requested_day_object + timedelta(days=1))):
                for appointment in Appointment.select().where(
                        (Appointment.time_slot == timeslot) & (Appointment.booked == True)):
                    try:
                        booking = Booking.get(
                            Booking.appointment == appointment)
                        if user_role != UserRoles.ADMIN:
                            booking = Booking.select().where((Booking.appointment == appointment) &
                                                             (Booking.booked_by == user_name)).get()

                        writer.writerow({'start_date_time': timeslot.start_date_time, 'first_name': booking.first_name,
                                         'surname': booking.surname, 'phone': booking.phone, 'office': booking.office,
                                         'secret': booking.secret, 'booked_by': booking.booked_by})
                    except DoesNotExist as e:
                        pass
            return result.getvalue().encode('utf8')
        except DoesNotExist as e:
            raise hug.HTTPGone
        except ValueError as e:
            raise hug.HTTPBadRequest


@hug.format.content_type('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
def format_as_xlsx(data, request=None, response=None):
    return data


@hug.get("/booking_list.xlsx", output=format_as_xlsx, requires=token_key_authentication)
def list_for_day(db: PeeweeSession,
                 user: hug.directives.user,
                 start_date: hug.types.text,
                 end_date: hug.types.text):
    user_name = user.user_name
    with db.atomic():
        try:
            user_role = user.role
            start_day_object = date.fromisoformat(start_date)
            end_day_object = date.fromisoformat(end_date)
            result = io.BytesIO()
            workbook = xlsxwriter.Workbook(result)
            worksheet = workbook.add_worksheet()
            bold = workbook.add_format({'bold': 1})
            date_format = workbook.add_format({'num_format': 'dd.mm.yyyy'})
            time_format = workbook.add_format({'num_format': 'hh:mm'})
            worksheet.set_column('A:A', 15)
            worksheet.set_column('B:B', 8)
            worksheet.set_column('C:C', 18)
            worksheet.set_column('D:D', 15)
            worksheet.set_column('E:E', 18)
            worksheet.set_column('F:F', 15)
            worksheet.set_column('G:G', 15)
            worksheet.set_column('H:H', 15)
            worksheet.set_column('I:I', 15)
            worksheet.set_column('J:J', 15)
            worksheet.set_column('K:K', 15)
            worksheet.set_column('L:L', 15)
            worksheet.set_column('M:M', 15)
            worksheet.set_column('N:N', 15)
            worksheet.set_column('O:O', 15)
            worksheet.write('A1', 'Termin', bold)
            worksheet.write('B1', 'Uhrzeit', bold)
            worksheet.write('C1', 'Vorname', bold)
            worksheet.write('D1', 'Nachname', bold)
            worksheet.write('E1', 'Telefon', bold)
            worksheet.write('F1', 'Straße', bold)
            worksheet.write('G1', 'Hausnummer', bold)
            worksheet.write('H1', 'PLZ', bold)
            worksheet.write('I1', 'Stadt', bold)
            worksheet.write('J1', 'Geburtdatum', bold)
            worksheet.write('K1', 'Risikokategorie 1', bold)
            worksheet.write('L1', 'Berechtigungscode', bold)
            worksheet.write('M1', 'Behörde', bold)
            worksheet.write('N1', 'Gebucht von', bold)
            worksheet.write('O1', 'Gebucht am', bold)
            row = 1
            col = 0
            for timeslot in TimeSlot.select().where(
                (TimeSlot.start_date_time >= start_day_object) &
                (TimeSlot.start_date_time < end_day_object + timedelta(days=1))).order_by(
                    TimeSlot.start_date_time.desc()):
                for appointment in Appointment.select().where(
                        (Appointment.time_slot == timeslot) & (Appointment.booked == True)):
                    try:
                        booking = Booking.get(
                            Booking.appointment == appointment)
                        if user_role != UserRoles.ADMIN:
                            booking = Booking.select().where((Booking.appointment == appointment) &
                                                             (Booking.booked_by == user_name)).get()

                        worksheet.write_datetime(
                            row, col, timeslot.start_date_time, date_format)
                        worksheet.write_datetime(
                            row, col + 1, timeslot.start_date_time, time_format)
                        worksheet.write_string(
                            row, col + 2, booking.first_name)
                        worksheet.write_string(row, col + 3, booking.surname)
                        worksheet.write_string(row, col + 4, booking.phone)
                        worksheet.write_string(
                            row, col + 5, booking.street if booking.street is not None else "")
                        worksheet.write_string(
                            row, col + 6, booking.street_number if booking.street_number is not None else "")
                        worksheet.write_string(
                            row, col + 7, booking.post_code if booking.post_code is not None else "")
                        worksheet.write_string(
                            row, col + 8, booking.city if booking.city is not None else "")
                        if booking.birthday is None:
                            worksheet.write_string(row, col + 9, "")
                        else:
                            worksheet.write_datetime(
                                row, col + 9, booking.birthday, date_format)
                        worksheet.write_string(
                            row, col + 10, booking.reason if booking.reason is not None else "")
                        worksheet.write_string(row, col + 11, booking.secret)
                        worksheet.write_string(row, col + 12, booking.office)
                        worksheet.write_string(
                            row, col + 13, booking.booked_by)
                        worksheet.write_datetime(
                            row, col + 14, booking.booked_at, date_format)
                        row += 1
                    except DoesNotExist as e:
                        pass
            workbook.close()
            result.flush()
            return result.getvalue()
        except DoesNotExist as e:
            raise hug.HTTPGone
        except ValueError as e:
            raise hug.HTTPBadRequest


@hug.get("/booked", requires=token_key_authentication)
def booked(db: PeeweeSession, user: hug.directives.user, start_date: hug.types.text,
           end_date: hug.types.text):
    user_name = user.user_name
    with db.atomic():
        try:
            user_role = user.role
            start_day_object = date.fromisoformat(start_date)
            end_day_object = date.fromisoformat(end_date)
            if user_role != UserRoles.ADMIN:
                start_day_object = date.fromisoformat('2021-01-01') #FIXME: hack to show users all their bookings
                end_day_object = date.fromisoformat('2022-12-31') #FIXME: hack to show users all their bookings
            bookings = []
            for timeslot in TimeSlot.select().where((TimeSlot.start_date_time >= start_day_object) &
                                                    (TimeSlot.start_date_time < end_day_object + timedelta(days=1))) \
                    .order_by(TimeSlot.start_date_time.desc()):
                for appointment in Appointment.select().where(
                        (Appointment.time_slot == timeslot) & (Appointment.booked == True)):
                    try:
                        booking = Booking.get(
                            Booking.appointment == appointment)
                        if user_role != UserRoles.ADMIN:
                            booking = Booking.select().where((Booking.appointment == appointment) &
                                                             (Booking.booked_by == user_name)).get()
                        bookings.append({'start_date_time': timeslot.start_date_time, 'first_name': booking.first_name,
                                         'surname': booking.surname, 'phone': booking.phone, 'office': booking.office,
                                         'secret': booking.secret, 'booked_by': booking.booked_by,
                                         'booked_at': booking.booked_at, 'booking_id': booking.get_id()})
                    except DoesNotExist as e:
                        pass
            return bookings
        except DoesNotExist as e:
            raise hug.HTTPGone
        except ValueError as e:
            raise hug.HTTPBadRequest


@hug.delete("/booking", requires=token_key_authentication)
def delete_booking(db: PeeweeSession, user: hug.directives.user, booking_id: hug.types.text):
    if user.role != UserRoles.ANON:
        with db.atomic():
            try:
                booking = Booking.get_by_id(booking_id)
                if user.role == UserRoles.USER and booking.booked_by != user.user_name:
                    return hug.HTTP_METHOD_NOT_ALLOWED
                appointment = booking.appointment
                appointment.booked = False
                appointment.save()
                booking.delete_instance()
            except DoesNotExist as e:
                raise hug.HTTP_NOT_FOUND
        user.coupons += 1
        user.save()
        return {"booking_id": booking_id, "deleted": "successful"}
    else:
        raise hug.HTTP_METHOD_NOT_ALLOWED


@hug.patch("/user", requires=token_key_authentication)
def patch_user(db: PeeweeSession,
               body: hug.types.json,
               user: hug.directives.user):
    old_user_password = body["old_user_password"]
    new_user_password = body["new_user_password"]
    new_user_password_confirm = body["new_user_password_confirm"]
    if new_user_password != new_user_password_confirm:
        raise hug.HTTPBadRequest
    with db.atomic():
        try:
            if user.password != hash_pw(user.user_name, user.salt, old_user_password):
                raise hug.HTTPBadRequest
            salt = get_random_string(2)
            secret_password = new_user_password
            hashed_password = hash_pw(user.user_name, salt, secret_password)
            user.salt = salt
            user.password = hashed_password
            user.save()
            log.info(f"updated {user.user_name}'s pw.")
            return "updated"
        except DoesNotExist as e:
            raise hug.HTTPBadRequest
        except ValueError as e:
            raise hug.HTTPBadRequest
