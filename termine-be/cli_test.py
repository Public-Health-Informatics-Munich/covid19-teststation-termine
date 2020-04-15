import csv
import io
from datetime import datetime
from typing import List, Dict, Tuple

import hug

from conftest import ADMIN, USER
from db.model import User, TimeSlot, Appointment, Booking


def parse_csv(csv_string: str) -> List[Dict]:
    return list(csv.DictReader(io.StringIO(csv_string), delimiter='\t'))




def test_get_coupon_state(testing_db):
    def get_admin_and_user_data() -> Tuple[Dict, Dict]:
        response = hug.test.cli('get_coupon_state', module='main', collect_output=True)
        out = parse_csv(response)
        a: Dict = next(a for a in out if a['name'] == ADMIN)
        u: Dict = next(a for a in out if a['name'] == USER)
        assert len(out) == 2
        return a, u
    admin_1, user_1 = get_admin_and_user_data()
    assert int(admin_1['num_bookings']) == 0
    assert int(user_1['num_bookings']) == 0
    assert int(admin_1['coupons']) == 10
    assert int(user_1['coupons']) == 10

    User.update({User.coupons: User.coupons + 11}).where(User.user_name == USER).execute()

    admin_2, user_2 = get_admin_and_user_data()
    assert int(admin_2['num_bookings']) == 0
    assert int(user_2['num_bookings']) == 0
    assert int(admin_2['coupons']) == 10
    assert int(user_2['coupons']) == 21

    Booking.create(
        surname="Mustermann",
        first_name="Marianne",
        phone="0123456789",
        office="MusterOffice",
        secret="SECRET",
        booked_by=USER,
        booked_at=datetime.now(),
        appointment=(
            Appointment.create(
                booked=True,
                time_slot=(
                    TimeSlot.create(
                        start_date_time=datetime.now(),
                        length_min=15)
                )
            )
        ),
    )
    User.update({User.coupons: User.coupons - 1}).where(User.user_name == USER).execute()

    admin_3, user_3 = get_admin_and_user_data()
    assert int(admin_3['num_bookings']) == 0
    assert int(user_3['num_bookings']) == 1
    assert int(admin_3['coupons']) == 10
    assert int(user_3['coupons']) == 20
