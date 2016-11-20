import json
from flask import Blueprint, request

from service import controller

user_service = Blueprint("user_service", __name__)

def setRoutes():
    setUserRoutes()
    setClubRoutes()
    setClubsRoutes()
    setMoviesRoutes()

def setUserRoutes():
    @user_service.route('/user/new', methods=['POST'])
    def new_user():
        user_dict = request.get_json()
        user = controller.save_user(user_dict)
        return 'Success'

    @user_service.route('/user/auth', methods=['POST'])
    def auth_user():
        credentials = request.get_json()
        username = credentials['user_name']
        password = credentials['password']
        token = controller.auth_user(username, password)
        return token   

    @user_service.route('/user/<int:id>', methods=['GET'])
    def find_user(id):
        token = request.args.get('sectoken', '')
        user = controller.find_user(token, id)
        return 'Success'

    @user_service.route('/user/<int:id>', methods=['PUT'])
    def update_user(id):
        token = request.args.get('sectoken', '')
        user_dict = request.get_json()
        controller.update_user(token, id, user_dict)
        return 'Success'

    @user_service.route('/user/<int:id>', methods=['DELETE'])
    def delete_user(id):
        token = request.args.get('sectoken', '')
        controller.delete_user(token, id)
        return 'Success'

    @user_service.route('/user/<int:user_id>/movie/<int:movie_id>', methods=['POST'])
    def watch_movie(user_id, movie_id):
        token = request.args.get('sectoken', '')
        controller.watch_movie(token, user_id, movie_id)
        return 'Success'

    @user_service.route('/user/<int:user_id>/movie/<int:movie_id>', methods=['DELETE'])
    def unwatch_movie(user_id, movie_id):
        token = request.args.get('sectoken', '')
        controller.unwatch_movie(token, user_id, movie_id)
        return 'Success'

    @user_service.route('/user/<int:user_id>/movie/<int:movie_id>', methods=['PUT'])
    def set_review(user_id, movie_id):
        token = request.args.get('sectoken', '')
        review_dict = request.get_json()
        controller.set_review(token, user_id, movie_id, review_dict)
        return 'Success'

    @user_service.route('/user/<int:user_id>/movies', methods=['GET'])
    def get_user_movies(user_id):
        token = request.args.get('sectoken', '')
        movies = controller.get_user_movies(token, user_id)
        return 'Success'

    @user_service.route('/user/<int:user_id>/club', methods=['POST'])
    def create_club(user_id):
        token = request.args.get('sectoken', '')
        club_dict = request.get_json()
        controller.create_club(token, user_id, club_dict)
        return 'Success'

    @user_service.route('/user/<int:user_id>/clubs', methods=['GET'])
    def get_user_clubs(user_id):
        token = request.args.get('sectoken', '')
        clubs = controller.get_user_clubs(token, user_id)
        return 'Success'

def setClubRoutes():
    @user_service.route('/club/<int:id>', methods=['PUT'])
    def update_club(id):
        club_dict = request.get_json()
        controller.update_club(id, club_dict)
        return 'Success'

    @user_service.route('/club/<int:id>', methods=['DELETE'])
    def delete_club(id):
        controller.delete_club(id)
        return 'Success'

    @user_service.route('/club/<int:club_id>/member/<int:member_id>', methods=['PUT'])
    def add_club_member(club_id, member_id):
        controller.add_club_member(club_id, member_id)
        return 'Success'

    @user_service.route('/club/<int:club_id>/member/<int:member_id>', methods=['DELETE'])
    def delete_club_member(club_id, member_id):
        controller.delete_club_member(club_id, member_id)
        return 'Success'

    @user_service.route('/club/<int:id>/members', methods=['GET'])
    def get_club_members(id):
        users = controller.get_club_members(id)
        return 'Success'

def setClubsRoutes():
    @user_service.route('/clubs', methods=['GET'])
    def find_clubs():
        sq = request.args.get('sq', '')
        clubs = controller.find_clubs(sq)
        return 'Success'

def setMoviesRoutes():
    @user_service.route('/movies', methods=['GET'])
    def find_movies():
        sq = request.args.get('sq', '')
        movies = controller.find_movies(sq)
        return 'Success'

setRoutes()
