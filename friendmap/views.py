from json import (dumps, loads)
from django.contrib.auth import (authenticate, logout, login)
from django.http import (HttpResponse)
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import (csrf_exempt)
from friendmap.controller import (add_user, get_users, get_friends, add_friend, get_all_connections)


@csrf_exempt
def users(request):
    if request.method == 'GET':
        username = request.GET.get('username', None)
        if username:
            response = get_users(username=username)
        else:
            response = []
        return HttpResponse(dumps(response))
    elif request.method == 'POST':
        username = _get_post_param(param='username', request=request)
        password = _get_post_param(param='password', request=request)
        response = add_user(username=username, password=password)
        return HttpResponse(dumps(response))

@csrf_exempt
def friends(request):
    if request.user is None:
        return HttpResponse(status=401)
    if request.method == 'GET':
        response = get_friends(user=request.user)
        return HttpResponse(dumps(response))
    elif request.method == 'POST':
        friend_name = _get_post_param(param='username', request=request)
        add_friend(user=request.user, friend_name=friend_name)
        return HttpResponse(status=200)

@csrf_exempt
def whoami(request):
    if request.user is None:
        return HttpResponse(status=401)
    else:
        response = request.user.username
        return HttpResponse(dumps(response))


@csrf_exempt
def all_connections(request):
    if request.user.is_superuser:
        response = get_all_connections()
        return HttpResponse(dumps(response))
    else:
        return HttpResponse(status=401)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = _get_post_param(param='username', request=request)
        password = _get_post_param(param='password', request=request)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse(username)
            else:
                return HttpResponse(status=401)
        else:
                return HttpResponse(status=400)


@csrf_exempt
def logout_user(request):
    logout(request)
    return HttpResponse(status=200)


def login_form(request):
    context = {'data': 'none'}
    return render_to_response('login.html', locals(), context_instance=RequestContext(request))


def friend_page(request):
    context = {'data': 'none'}
    return render_to_response('friend_page.html', locals(), context_instance=RequestContext(request))


def admin_page(request):
    context = {'data': 'none'}
    return render_to_response('admin_page.html', locals(), context_instance=RequestContext(request))


def _get_post_param(param=None, request=None):
    try:
        body = request.body.decode('utf-8')
        data = loads(body)
        return data.get(param, '')
    except ValueError:
        return None