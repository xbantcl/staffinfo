#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from flask import _app_ctx_stack


def init_db(cls=None):
    """Create database table"""
    with cls.app_context():
        db = get_db(cls)
        with cls.open_resource('schema.sql', mode='r') as f:
            print '*' * 20
            db.cursor().executescript(f.read())
        db.commit()


def get_db(cls=None):
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect(cls.config['DATABASE'])
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db

    return top.sqlite_db
