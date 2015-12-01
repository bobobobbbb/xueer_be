# coding: utf-8

from flask import jsonify, url_for, request, current_app
from flask_login import current_user
from ..models import Courses, User
from . import api
from xueer import db
from xueer.api_1_0.authentication import auth


@auth.login_required
@api.route('/courses/')  # ?string=sort&main_cat&ts_cat
def get_courses():
    """
    获取全部课程
    排序存在问题
    """
    page = request.args.get('page', 1, type=int)
    # pagination = Courses.query.order_by(Courses.comment.count()).paginate(
    pagination = Courses.query.paginate(
        # 查询对象query具有paginate属性
        page,
        per_page=current_app.config['XUEER_COURSES_PER_PAGE'],
        error_out=False
    )
    courses = pagination.items
    prev = None  # should init
    if pagination.has_prev:
        prev = url_for('api.get_courses', page=page - 1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_courses', page=page + 1, _external=True)
    return jsonify({
        'course': [course.to_json() for course in courses],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/courses/<int:id>/')
def get_course_id(id):
    """
    获取特定id课程的信息
    :param id:
    :return:
    """
    course = Courses.query.get_or_404(id)
    return jsonify(course.to_json())


@api.route('/courses/<int:id>/like/', methods=['POST', 'GET'])
def course_like(id):
    """
    向特定id的课程点赞
    :param id:
    :return:
    """
    course = Courses.query.get_or_404(id)
    user = User.query.filter_by(id=current_user.id).first()
    course.user.all().append(user)
    db.session.add(course)
    db.session.commit()
    return jsonify(course.to_json()), 200
