import json
from flask import Blueprint, request

from service import controller

user_service = Blueprint("user_service", __name__)


@user_service.route('/hello')
def greet():
    return 'Hello, user!'


@user_service.route('/user', methods=['POST'])
def new_user():
    user_dict = request.get_json()
    user = controller.save_user(user_dict)


@user_service.route('/user/auth', methods=['POST'])
def auth_user():
    # TODO
    pass


@user_service.route('/user', methods=['PUT'])
def update_user():
    user_dict = request.get_json()
    controller.update_user(user_dict)


@user_service.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    controller.delete_user(id)


@user_service.route('/user/<int:id>', methods=['GET'])
def find_user(id):
    user = controller.find_user(id)
    return 'Success'


@user_service.route('/club', methods=['POST'])
def create_club():
    json_params = request.get_json()
    club = json_params['club']
    owner_id = json_params['owner_id']
    controller.create_club(club, owner_id)


@user_service.route('/club', methods=['PUT'])
def update_club():
    club = request.get_json()
    controller.update_club(club)


@user_service.route('/club/<int:id>', methods=['DELETE'])
def delete_club(id):
    controller.delete_user(id)


@user_service.route('/club/<int:id>/members', methods=['GET'])
def find_club_members(id):
    members = controller.find_club_members(id)
    return 'Success'
