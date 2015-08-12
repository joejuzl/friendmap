from unittest.mock import patch, MagicMock
from friendmap.controller import (add_user, get_users, get_all_connections,
                                  get_friends, add_friend)

__author__ = 'joejuzl'

from unittest import TestCase


class ControllerTest(TestCase):

    @patch('friendmap.controller.User')
    def test_add_user_calls_create_user_and_returns_username(self, mock_user_class):
        mock_user_class.objects.create_user.return_value = MagicMock(username='joe')

        actual = add_user(username='joe', password='password')
        expected = 'joe'

        mock_user_class.objects.create_user.assert_called_with(username='joe', password='password')
        self.assertEquals(actual, expected)

    def test_add_user_throws_exception_on_none_input(self):
        self.assertRaises(ValueError, add_user)

    @patch('friendmap.controller.User')
    def test_get_users_returns_correct_users(self, mock_user_class):
        mock_user_class.objects.all.return_value = [MagicMock(username='joe'), MagicMock(username='john'),
                                                    MagicMock(username='james'), MagicMock(username='ben')]
        actual = get_users(username='jo')
        expected = ['joe', 'john']

        self.assertListEqual(actual, expected)

    @patch('friendmap.controller.User')
    def test_get_users_handles_no_users(self, mock_user_class):
        mock_user_class.objects.all.return_value = []
        actual = get_users(username='jo')
        expected = []

        self.assertListEqual(actual, expected)

    def test_get_users_throws_exception_for_none(self):
        self.assertRaises(ValueError, get_users)

    @patch('friendmap.controller.User')
    @patch('friendmap.controller.Friend')
    def test_get_all_connections_returns(self, mock_friend_class, mock_user_class):
        mock_user_class.objects.all.return_value = [MagicMock(username='joe'), MagicMock(username='john'),
                                                    MagicMock(username='james'), MagicMock(username='ben')]
        mock_friend_class.objects.friends.side_effect = ([MagicMock(username='ben')],
                                                         [MagicMock(username='joe'), MagicMock(username='james')],
                                                         [],
                                                         [MagicMock(username='james')])
        actual = get_all_connections()
        expected = [{'username': 'joe',
                     'friends': ['ben']},
                    {'username': 'john',
                     'friends': ['joe', 'james']},
                    {'username': 'james',
                    'friends': []},
                    {'username': 'ben',
                     'friends': ['james']}]

        self.assertListEqual(actual, expected)

    @patch('friendmap.controller.User')
    def test_get_all_connections_handles_no_users(self, mock_user_class):
        mock_user_class.objects.all.return_value = []

        actual = get_all_connections()
        expected = []

        self.assertListEqual(actual, expected)

    @patch('friendmap.controller.Friend')
    def test_get_friends_returns(self, mock_friend_class):
        mock_friend_class.objects.friends.return_value = [MagicMock(username='john'),
                                                          MagicMock(username='james'), MagicMock(username='ben')]
        mock_user = MagicMock()
        actual = get_friends(user=mock_user)
        expected = ['john', 'james', 'ben']

        self.assertListEqual(actual, expected)
        mock_friend_class.objects.friends.assert_called_with(mock_user)

    @patch('friendmap.controller.Friend')
    def test_get_friends_returns_empty_list_for_no_friends(self, mock_friend_class):
        mock_friend_class.objects.friends.return_value = []
        actual = get_friends(user=MagicMock())
        expected = []
        self.assertListEqual(actual, expected)

    def test_get_friends_raise_value_error(self):
        self.assertRaises(ValueError, get_friends)


    @patch('friendmap.controller.User')
    @patch('friendmap.controller.Friend')
    def test_add_friend_calls_correct_methods(self, mock_friend_class, mock_user_class):
        mock_friend_user = MagicMock()
        mock_relationship = MagicMock()
        mock_user = MagicMock
        mock_user_class.objects.all().filter.return_value = [mock_friend_user]
        mock_friend_class.objects.add_friend.return_value = mock_relationship

        add_friend(mock_user, 'joe')

        mock_user_class.objects.all().filter.assert_called_with(username='joe')
        mock_friend_class.objects.add_friend.assert_called_with(mock_user, mock_friend_user)
        mock_relationship.accept.assert_called_with()

    def test_add_friend_throws_exception_for_none(self):
        self.assertRaises(ValueError, add_friend())