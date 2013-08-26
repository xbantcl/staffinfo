#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, abort, \
    request, session, redirect, flash, url_for
from moudels import sqlite as sql
import config
import ldap
import json

app = Flask(__name__)
app.config.from_object(config)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

userInfo = {}
userInfo['username'] = ''
userInfo['pingyin'] = ''
userInfo['email'] = ''
userInfo['office'] = ''
userInfo['mobile'] = ''
userInfo['team'] = ''


@app.route('/')
def show_index():
    return render_template('index.html')


@app.route('/admin', methods=['GET', 'POST'])
def operate_sqlite():
    db = sql.get_db(app)
    cx = db.execute("select * from user_info")
    result = cx.fetchall()
    return render_template('admin.html', result=result)


def get_form_data():
    userInfo['username'] = request.form['Username']
    userInfo['pingyin'] = request.form['Pingyin']
    userInfo['email'] = request.form['Email']
    userInfo['office'] = request.form['Office']
    userInfo['team'] = request.form['Team']
    userInfo['mobile'] = request.form['Mobile']


@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'POST' == request.method:
        form = request.json
        sql_field = {}
        user_info = {}
        _sql = "select * from user_info where "
        if form['username'] and str.isalpha(form['username'].encode('utf-8')):
            field = 'pingyinname'
        else:
            field = 'username'
        if form['username']:
            sql_field[field] = form['username']
        if form['email']:
            sql_field['email'] = form['email']
        if form['team']:
            sql_field['department'] = form['team']
        if form['extension']:
            sql_field['office_num'] = form['extension']
        for key, value in sql_field.items():
            _sql += "%s like '%%%s%%' and " % (key, value)
        _sql = _sql[:-4]
        if form['team'] or form['email'] or form['username'] or form['extension']:
            db = sql.get_db(app)
            cx = db.execute(_sql)
            result = cx.fetchall()
            db.close()
            count = 0
            if session.get('login_in'):
                user_info['status'] = True
            else:
                user_info['status'] = False
            for row in result:
                user_info[count] = {}
                user_info[count]['username'] = row[1]
                user_info[count]['pingyin'] = row[2]
                user_info[count]['email'] = row[3]
                user_info[count]['office'] = row[4]
                user_info[count]['mobile'] = row[5]
                user_info[count]['team'] = row[6]
                count += 1
        return json.dumps(user_info)


@app.route('/linked/<value>')
def linked(value):
    user_info = 'no'
    if value:
        if session.get('login_in'):
            _sql = "select username, pingyinname, email, office_num, mobile, \
                    department from user_info where pingyinname like '%s%%'" % value[0]
        else:
            _sql = "select username, pingyinname, email, office_num, \
                    department from user_info where pingyinname like '%s%%'" % value[0]

        db = sql.get_db(app)
        cx = db.execute(_sql)
        result = cx.fetchall()
        db.close()
        if result:
            user_info = result
    return render_template('link.html', result=user_info)


@app.route('/action', methods=['GET', 'POST'])
def action():
    if not session.get('login_in'):
        abort(401)
    if 'modify' == request.args.get('types'):
        userId = int(request.args.get('id'))
        _sql = "select username, pingyinname, email, office_num, \
                mobile, department from user_info where id=%d" % userId
        db = sql.get_db(app)
        cx = db.execute(_sql)
        result = cx.fetchone()
        db.close()
        user_info = {'Username': result[0], 'Pingyin': result[1],
        'Email': result[2], 'Office': result[3], 'Mobile': result[4], 'Team': result[5]}
        return render_template('modify.html', userid=userId, user_info=user_info)
    elif 'add' == request.args.get('types'):
        return render_template('add.html')
    elif 'delete' == request.args.get('types'):
        userId = int(request.args.get('id'))
        _sql = "delete from user_info where id=%d" % userId
        db = sql.get_db(app)
        cx = db.execute(_sql)
        db.commit()
        db.close()
        if cx:
            return redirect(url_for('operate_sqlite'))
    elif 'POST' == request.method:
        get_form_data()
        db = sql.get_db(app)
        if 'modify' == request.form['action']:
            userInfo['userid'] = request.form['userid']
            _sql = "update user_info set username='%s', pingyinname='%s', email='%s', \
                    office_num='%s', mobile='%s', department='%s' where id='%s'" % \
                        (userInfo['username'], userInfo['pingyin'], userInfo['email'],
                            userInfo['office'], userInfo['mobile'],
                            userInfo['team'], userInfo['userid'])
        elif 'add' == request.form['action']:
            _sql = "insert into user_info(username, pingyinname, email, office_num, mobile, \
                    department) values('%s', '%s', '%s', '%s', '%s', '%s')" % (userInfo['username'],
                            userInfo['pingyin'], userInfo['email'], userInfo['office'],
                            userInfo['mobile'], userInfo['team'])

        cx = db.execute(_sql)
        db.commit()
        db.close()
        if cx:
            return redirect(url_for('operate_sqlite'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        passwd = request.form['password']
        user = None
        if username in app.config['ACCESS_USER_LIST']:
            if username == 'yuanzu.tang' or username == 'gcqueryhq':
                user = username + '@hq.ta-mp.com'
            else:
                user = username + '@cd.ta-mp.com'
            try:
                conn = None
                if username == 'yuanzu.tang' or username == 'gcqueryhq':
                    conn = ldap.open(host=app.config['SZ_LDAP_SERVER'], port=int(app.config['SZ_LDAP_PORT']))
                else:
                    conn = ldap.open(host=app.config['LDAP_SERVER'], port=int(app.config['LDAP_PORT']))

                conn.simple_bind_s(user, passwd)
            except ldap.INVALID_CREDENTIALS:
                error = "Invalid username or password"
            if not error:
                session['login_in'] = True
                flash('You were logged in')
                if request.form['username'] in app.config['ADMIN_USER_LIST']:
                    return redirect(url_for('operate_sqlite'))
                else:
                    return redirect(url_for('show_index'))
        else:
            error = "Permission denied"
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('login_in', None)
    return redirect(url_for('show_index'))

if __name__ == "__main__":
    #sql.init_db(app)
    app.run(debug=True, host="0.0.0.0")
