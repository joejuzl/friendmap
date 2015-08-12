from json import loads, dumps
from django.test import TestCase

__author__ = 'joejuzl'


class FunctionalTest(TestCase):

    def test_create_and_find_user(self):
        self._add_user(username='joe')
        self._add_user(username='john')
        self._add_user(username='ben')
        users = self._get_users(username='jo')
        self.assertEquals(users, ['joe', 'john'])

    def test_add_and_get_friends(self):
        self._add_user(username='joe')
        self._add_user(username='john')
        self._add_user(username='ben')  # use a damn loop
        self._add_user(username='bob')
        self._login(username='joe', password='password')
        self._add_friend(username='john')
        self._add_friend(username='bob')
        friends = self._get_friends()
        self.assertEquals(friends, ['john', 'bob'])

    def test_login_and_whoami(self):
        self._add_user(username='joe')
        self._login(username='joe', password='password')
        response = self._whoami()
        self.assertEquals(response, 'joe')

    def test_logout(self):
        self._add_user(username='joe')
        self._login(username='joe', password='password')
        response1 = self._whoami()
        self._logout()
        response2 = self._whoami()
        self.assertEquals(response1, 'joe')
        self.assertEquals(response2, '')

    def _add_user(self, username=None):
        response = self.client.post('/user/', data=dumps({
            'username': username,
            'password': 'password'
        }), content_type="application/json")
        actual = _get_content(response)
        self.assertEquals(actual, username)

    def _get_users(self, username=None):
        response = self.client.get('/users?username={}'.format(username))
        return _get_content(response)

    def _login(self, username=None, password=None):
        self.client.post('/login_user/', data=dumps({
            'username': username,
            'password': password
        }), content_type="application/json")

    def _logout(self):
        self.client.post('/logout_user/')

    def _add_friend(self, username=None):
        self.client.post('/friend/', data=dumps({
            'username': username,
        }), content_type="application/json")

    def _get_friends(self):
        response = self.client.get('/friend/')
        return _get_content(response)


    def _whoami(self):
        response = self.client.get('/whoami/')
        return _get_content(response)


def _get_content(response=None):
    return loads(str(response.content, encoding='utf8'))