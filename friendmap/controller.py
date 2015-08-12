from django.contrib.auth.models import (User)
from friendship.models import Friend

__author__ = 'joejuzl'


def add_user(username=None, password=None):
    if not username or not password:
        raise ValueError
    user = User.objects.create_user(username=username, password=password)
    return user.username


def get_users(username=None):
    if not username:
        raise ValueError
    all_users = User.objects.all()
    filtered_users = _filter_by_name(users=all_users, username=username)
    return [user.username for user in filtered_users]


def get_all_connections():
    all_users = User.objects.all()
    data = []
    for user in all_users:
        data.append({
            'username': user.username,
            'friends': [friend.username for friend in Friend.objects.friends(user)]
        })
    return data


def get_friends(user=None):
    if not user:
        raise ValueError
    friends = Friend.objects.friends(user)
    return [user.username for user in friends]


def add_friend(user=None, friend_name=None):
    if not user or not friend_name:
        raise ValueError
    friend_user = User.objects.all().filter(username=friend_name)[0]
    new_relationship = Friend.objects.add_friend(user, friend_user)
    new_relationship.accept()


def _filter_by_name(users=None, username=None):
    return [user for user in users if _is_match(username=user.username, partial_username=username)]


def _is_match(username=None, partial_username=None):
    if partial_username == username[:len(partial_username)]:
            return True
    return False
