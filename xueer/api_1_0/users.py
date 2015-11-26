# coding: utf-8

from flask import current_app, request, url_for, jsonify
from . import api
from ..models import User
from .. import app


@app.route('/users/<int:id>')
def get_user_id(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())
