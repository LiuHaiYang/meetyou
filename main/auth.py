# -*- coding: utf-8 -*-
from functools import wraps
from flask import request, session, flash, redirect

def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash(u"用户未登入")
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function