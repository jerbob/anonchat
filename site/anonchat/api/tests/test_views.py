"""Test that API endpoints return the correct data."""

from api.tests import JSONRequestMixin

from django.test import TestCase


VALID_USERNAME = 'Kenobi'
VALID_MESSAGE = 'Hello there.'


class RegisterUserViewTest(JSONRequestMixin, TestCase):
    """Test the /api/register endpoint."""

    def test_valid_registration(self: TestCase) -> None:
        """Ensure that valid registrations are accepted."""
        status, response = self.post(
            '/api/register',
            {'username': VALID_USERNAME},
        )
        self.assertEqual(status, 200)
        self.assertTrue(response.get('success'))

    def test_invalid_json(self: TestCase) -> None:
        """Ensure that invalid JSON data is denied."""
        status, response = self.post('/api/register', '')
        self.assertEqual(response, {
            'success': False,
            'error': 'You supplied incorrect data.'
        })

    def test_deny_multiple_registration(self: TestCase) -> None:
        """Ensure that registrations by logged-in users are denied."""
        self.post('/api/register', {'username': VALID_USERNAME})
        status, response = self.post(
            '/api/register',
            {'username': VALID_USERNAME}
        )
        self.assertEqual(response, {
            'success': False,
            'error': 'You are already registered.'
        })

    def test_username_out_of_bounds(self: TestCase) -> None:
        """Ensure that username lengths outside 1 - 100 are denied."""
        for username in ('', 'R' + 'E' * 100):
            status, response = self.post(
                '/api/register',
                {'username': username}
            )
            self.assertEqual(response, {
                'success': False,
                'error': 'Username length must be between 1 and 100.'
            })


class PostMessageViewTest(JSONRequestMixin, TestCase):
    """Test the /rooms/*/post endpoint."""

    def setUp(self: TestCase) -> None:
        """Register a user and room before all tests."""
        status, response = self.post(
            '/api/register',
            {'username': VALID_USERNAME}
        )
        slug = response['slug']
        self.room = f'/api/rooms/{slug}/post'

    def test_successful_message(self: TestCase) -> None:
        """Ensure that valid messages are accepted."""
        status, response = self.post(
            self.room,
            {'content': VALID_MESSAGE}
        )
        self.assertEqual(response, {
            'success': True,
            'message': {
                'content': VALID_MESSAGE,
                'author': VALID_USERNAME
            }
        })

    def test_content_out_of_bounds(self: TestCase) -> None:
        """Ensure that content lengths outside 1 - 256 are denied."""
        for content in ('', 'Hell' + 'o' * 247 + ' there'):
            status, response = self.post(self.room, {'content': content})
            self.assertEqual(response, {
                'success': False,
                'error': 'Content length must be between 1 and 256.'
            })

    def test_user_not_registered(self: TestCase) -> None:
        """Ensure that unregistered users cannot send messages."""
        self.client.cookies.clear()
        status, response = self.post(
            self.room,
            {'content': VALID_MESSAGE}
        )
        self.assertEqual(response, {
            'success': False,
            'error': 'You are not registered.'
        })

    def test_room_does_not_exist(self: TestCase) -> None:
        """Ensure that messages sent to nonexistent rooms are denied."""
        status, response = self.post(
            '/api/rooms/snail/post',
            {'content': VALID_MESSAGE}
        )
        self.assertEqual(response, {
            'success': False,
            'error': 'That room does not exist.'
        })
