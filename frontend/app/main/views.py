import os
import random

import redis
from flask import render_template, request, redirect,\
     session, url_for

from werkzeug.security import generate_password_hash

from . import main
from .forms import HashFieldValueForm, UserUpdateForm
from .. import redis


@main.route('/', methods=['GET', 'POST'])
def index():
    list_all_keys = redis.keys("*")
    print("all keys in byte: ", list_all_keys)

    if 'username' not in session and 'is_authenticated' not in session:
        session['username'] = 'Anonimous'
        session['is_authenticated'] = False
        session['user_id'] = None

    username = session['username']
    is_authenticated = session['is_authenticated']

    user_agent = request.headers.get('User-Agent')
    # redirect позволяет избежать повторного
    # POST запроса, поскольку по умолчанию делает GET запрос
    return render_template('index.html', user_agent=user_agent,
                           username=username, is_authenticated=is_authenticated,
                           secret=os.getenv('SECRET_KEY'))


@main.route('/add/user', methods=['GET', 'POST'])
def add_user():
    if 'username' not in session and 'is_authenticated' not in session:
        session['username'] = 'Anonimous'
        session['is_authenticated'] = False
        session['user_id'] = None

    username = session['username']
    is_authenticated = session['is_authenticated']

    if username != 'admin' or is_authenticated is not True:
        return render_template('secret_add.html',
                               username=username, is_authenticated=is_authenticated
                               )

    form = HashFieldValueForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            print(data, request.form.to_dict(), session)
            print('data.keys: ', data.keys())

            random.seed()
            pipe = redis.pipeline()
            pipe.key = f"user:{random.getrandbits(32)}"
            new_user = pipe.key
            for field in ['name', 'secondName', 'username', 'age', 'skills', 'hobby']:
                pipe.hset(pipe.key, field, data[field])
            password_hash = generate_password_hash(data['password'])
            pipe.hset(pipe.key, 'password_hash', password_hash)
            pipe.execute()
            print('pipe executed, new user: ', new_user)
            return redirect(url_for('main.success_add'))
    else:
        print('request method GET received')
    return render_template('add_user.html', form=form,
                           username=username, is_authenticated=is_authenticated,
                           secret=os.getenv('SECRET_KEY'))


@main.route('/add/success', methods=['GET'])
def success_add():
    if 'username' not in session and 'is_authenticated' not in session:
        session['username'] = 'Anonimous'
        session['is_authenticated'] = False
        session['user_id'] = None

    username = session['username']
    is_authenticated = session['is_authenticated']

    return render_template('success_add.html',
                           username=username, is_authenticated=is_authenticated,
                           secret=os.getenv('SECRET_KEY'))


@main.route('/list/users', methods=['GET'])
def list_users():
    if 'username' not in session and 'is_authenticated' not in session:
        session['username'] = 'Anonimous'
        session['is_authenticated'] = False
        session['user_id'] = None

    username = session['username']
    is_authenticated = session['is_authenticated']
    user_id = session['user_id']

    users_keys = redis.keys('user:*')
    users_keys_string = [user_key.decode() for user_key in users_keys]
    # users_keys_string_map = list(map(bytes.decode, users_keys))
    dict_users = {user_key.decode(): redis.hgetall(user_key) for user_key in users_keys}
    print('dict_users: ', dict_users)
    # print('users_keys_string: ', users_keys_string)
    # print('users_keys_string_map: ', users_keys_string_map)

    # for i in users_keys:
    #     if 'password_hash' not in redis.hgetall(i):
    #         password_hash = generate_password_hash('1234567890')
    #         redis.hset(i, 'password_hash', password_hash)
    #         print('записан password_hash для пользователя ', i)

    dict_str = {}
    for i in users_keys_string:
        # print('map: ', list(map(bytes.decode, dict_users[i].values())))
        dict_str[i] = {user_field.decode(): dict_users[i][user_field].decode()
                       for user_field in dict_users[i].keys()}
    # print('dict_str: ', dict_str)
    return render_template('list_users.html', dict_users=dict_str,
                           users_keys=users_keys_string,
                           username=username, is_authenticated=is_authenticated,
                           user_id=user_id,
                           secret=os.getenv('SECRET_KEY'))


@main.route('/update/user/<pk>', methods=['GET', 'POST'])
def update_user(pk):
    if 'username' not in session and 'is_authenticated' not in session:
        session['username'] = 'Anonimous'
        session['is_authenticated'] = False
        session['user_id'] = None

    username = session['username']
    is_authenticated = session['is_authenticated']

    if username == 'Anonimous' and is_authenticated is False:
        return render_template('secret.html',
                               username=username, is_authenticated=is_authenticated,
                               )

    form = UserUpdateForm()
    user = redis.hgetall(pk)
    user_data = {i.decode(): user[i].decode() for i in user.keys()}
    print('user_update user_data: ', user_data)

    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            print('update user form: ', data, request.form.to_dict(), session)
            print('data.keys: ', data.keys())

            pipe = redis.pipeline()
            pipe.key = pk
            for field in ['name', 'secondName', 'age', 'skills', 'hobby']:
                if data[field]:
                    pipe.hset(pipe.key, field, data[field])
            pipe.execute()

            print('pipe executed, updated user: ', pk)
            return redirect(url_for('main.success_update'))
    else:
        print('request method GET received')

    return render_template('update_user.html', pk=pk, user_data=user_data,
                           username=username, is_authenticated=is_authenticated,
                           form=form, secret=os.getenv('SECRET_KEY'))


@main.route('/update/success', methods=['GET'])
def success_update():
    if 'username' not in session and 'is_authenticated' not in session:
        session['username'] = 'Anonimous'
        session['is_authenticated'] = False
        session['user_id'] = None

    username = session['username']
    is_authenticated = session['is_authenticated']

    return render_template('success_update.html',
                           username=username, is_authenticated=is_authenticated,
                           secret=os.getenv('SECRET_KEY'))
