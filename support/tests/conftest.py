import pytest

from authentication.models import User
from main.models import Ticket


@pytest.fixture
def usual_user(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return User.objects.create_user("UserTest@tut.by", "UserPassword")


@pytest.fixture
def support_user(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return User.objects.create_user("SupportTest@tut.by", "UserPassword", is_staff=True)


@pytest.fixture
def users_ticket_created(django_db_setup, django_db_blocker, usual_user):
    with django_db_blocker.unblock():
        return Ticket.objects.create(user=usual_user, name='Users ticket')


@pytest.fixture
def supports_ticket_created(django_db_setup, django_db_blocker, support_user):
    with django_db_blocker.unblock():
        return Ticket.objects.create(user=support_user, name='Supports ticket')
