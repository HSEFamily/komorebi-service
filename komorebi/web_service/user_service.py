from flask import Blueprint

user_service = Blueprint("user_service", __name__)


@user_service.route('/user')
def find_user_by_id():
    pass

