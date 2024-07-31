from flask import render_template, redirect,\
     session, url_for, flash

from werkzeug.security import check_password_hash

from . import main
from .forms import LoginForm
from .. import redis


@main.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' not in session and 'is_authenticated' not in session:
        session['username'] = 'Anonimous'
        session['is_authenticated'] = False
        session['user_id'] = None

    username = session['username']
    is_authenticated = session['is_authenticated']

    form = LoginForm()

    users_keys = redis.keys('user:*')
    users_keys_str = [user_key.decode() for user_key in users_keys]
    # словарь с полями и значениями в bytes
    dict_users = {user_key.decode(): redis.hgetall(user_key) for user_key in users_keys}
    dict_str = {} # словарь со всеми ключами, полями и значениями в string
    for i in users_keys_str:
        dict_str[i] = {user_field.decode(): dict_users[i][user_field].decode()
                       for user_field in dict_users[i].keys()}

    users_usernames = [dict_str[i]['username'] for i in users_keys_str]
    print('users_usernames: ', users_usernames)
    dict_id_usernames = {id: dict_str[id]['username'] for id in users_keys_str}
    print('dict_id_usernames: ', dict_id_usernames)

    if form.validate_on_submit():
        username = form.data['username']
        password = form.data['password']

        if username not in dict_id_usernames.values():
            flash('no such username')
            print('no such username')
        else:
            for id in dict_id_usernames.keys():
                if dict_id_usernames[id] == username:
                    username_id = id
                    break

            if not check_password_hash(redis.hget(username_id, 'password_hash').decode(), password):
                flash('incorrect password')
                print('incorrect password')

            elif check_password_hash(redis.hget(username_id, 'password_hash').decode(), password):
                session['username'] = username
                session['is_authenticated'] = True
                session['user_id'] = username_id
                flash('Authorization success')
                print('Authorization success')
                next = url_for('main.index')
                print('url: ', next)
                return redirect(next)
            else:
                flash('Authorization failed')
                print('Authorization failed')

    return render_template('login.html', form=form,
                           username=username, is_authenticated=is_authenticated)


@main.route('/logout')
def logout():
    session['username'] = 'Anonymous'
    session['is_authenticated'] = None
    session['user_id'] = None
    username = session['username']
    is_authenticated = session['is_authenticated']
    return render_template('logout.html',
                           username=username, is_authenticated=is_authenticated)
