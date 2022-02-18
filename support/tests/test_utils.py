import pytest
from rest_framework.reverse import reverse

from rest_framework.test import APIClient

from main.models import Ticket, Message
from support.utils import parse_bool

client = APIClient()


@pytest.mark.django_db
def test_all_tickets_usual_user(usual_user, support_user):
    user_ticket = Ticket.objects.create(name='user_ticket', user=usual_user)
    Ticket.objects.create(name='staff_ticket', user=support_user)
    client.force_authenticate(usual_user)
    response = client.get(reverse('support:ticket-all'))

    # User can see only his tickets
    assert len(response.data) == 1
    assert response.data[0]['id'] == user_ticket.id


@pytest.mark.django_db
def test_all_tickets_support_user(usual_user, support_user):
    supports_ticket = Ticket.objects.create(name='staff_ticket', user=support_user)
    users_ticket = Ticket.objects.create(name='user_ticket', user=usual_user)
    client.force_authenticate(support_user)
    response = client.get(reverse('support:ticket-all'))

    # Support can see all tickets
    assert len(response.data) == 2
    assert sorted([response.data[0]['id'], response.data[1]['id']]) == sorted([supports_ticket.id, users_ticket.id])
    assert 'status' in response.data[0]


@pytest.mark.parametrize(
    'value, expected_result',
    [
        ('1', True),
        ('0', False)
     ]
)
def test_parse_bool_true(value, expected_result):
    result = parse_bool(value)

    assert result is expected_result


@pytest.mark.django_db
def test_ticket_list_view():
    response = client.get(reverse('support:ticket-all'))

    assert response.status_code == 200


@pytest.mark.django_db
def test_message_list_view_usual_user(usual_user, support_user, users_ticket_created, supports_ticket_created):
    client.force_authenticate(usual_user)
    Message.objects.create(user_id=usual_user.id, ticket_id=users_ticket_created.id, text='some text')
    Message.objects.create(user_id=support_user.id, ticket_id=supports_ticket_created.id, text='some support text')
    response = client.get(reverse('support:ticket-message', kwargs={'pk': users_ticket_created.id}))

    assert response.data[0]['user'] == usual_user.username
    # User can see only his ticket messages
    assert (client.get(reverse('support:ticket-message', kwargs={'pk': supports_ticket_created.id}))).status_code == 404


@pytest.mark.django_db
def test_message_list_view_support_user(usual_user, support_user, users_ticket_created, supports_ticket_created):
    client.force_authenticate(support_user)
    Message.objects.create(user_id=usual_user.id, ticket_id=users_ticket_created.id, text='some text')
    Message.objects.create(user_id=support_user.id, ticket_id=supports_ticket_created.id, text='some support text')
    response_support_message = client.get(reverse('support:ticket-message', kwargs={'pk': users_ticket_created.id}))
    response_user_message = client.get(reverse('support:ticket-message', kwargs={'pk': users_ticket_created.id}))

    assert response_support_message.status_code == 200
    assert response_user_message.status_code == 200


@pytest.mark.django_db
def test_create_ticket_usual_user(usual_user):
    client.force_authenticate(usual_user)

    assert len(Ticket.objects.all()) == 0
    context = {
        'name': 'users ticket',
        'description': 'some description',
        'user_id': usual_user.id
    }
    client.post(reverse('support:ticket-create'), context, format='json')
    response = client.get(reverse('support:ticket-all'))

    assert response.status_code == 200
    assert response.data[0]['user'] == usual_user.username

