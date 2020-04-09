import hug
from peewee import fn, DoesNotExist

from access_control.access_control import admin_authentication, UserRoles
from db.directives import PeeweeSession
from db.model import User, Booking


@hug.get("/user", requires=admin_authentication)
def get_users():
    """
    SELECT u.user_name, u.coupons, COUNT(b.id)
    FROM "user" u
    JOIN booking b ON b.booked_by = u.user_name
    GROUP BY u.user_name, u.coupons
    """
    users = User.select().order_by(User.role.desc(), User.user_name)
    return [{
        "user_name": user.user_name,
        "is_admin": user.role == UserRoles.ADMIN,
        "total_bookings": len(Booking.select().where(
            user.user_name == Booking.booked_by)),
        "coupons": user.coupons
    } for user in users]


@hug.patch("/user", requires=admin_authentication)
def put_user(db: PeeweeSession, user_name: hug.types.text, coupons: hug.types.number):
    with db.atomic():
        try:
            user = User.get(User.user_name == user_name)
            if coupons < 0:
                coupons = 0
            user.coupons = coupons
            user.save()
            return {
                "user_name": user.user_name,
                "coupons": user.coupons
            }
        except DoesNotExist as e:
            raise hug.HTTPBadRequest
        except ValueError as e:
            raise hug.HTTPBadRequest
        except AssertionError as e:
            raise hug.HTTPBadRequest
