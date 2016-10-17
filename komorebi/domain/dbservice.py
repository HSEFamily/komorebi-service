from abc import abstractmethod
from jujuq import Query


class DBService:
    def __init__(self, **kwargs):
        self.config = kwargs

    @abstractmethod
    def save_user(self, user):
        pass

    @abstractmethod
    def update_user(self, user):
        pass

    @abstractmethod
    def create_club(self, club, owner_id):
        pass

    @abstractmethod
    def update_club(self, club):
        pass

    @abstractmethod
    def find_user(self, user_id):
        pass

    @abstractmethod
    def delete_user(self, user_id):
        pass

    @abstractmethod
    def delete_club(self, club_id):
        pass

    @abstractmethod
    def find_club_members(self, club_id):
        pass

    @abstractmethod
    def find_user_clubs(self, user_id):
        pass

    @abstractmethod
    def add_user_movie(self, user_id, movie):
        pass

    @abstractmethod
    def rate_movie(self, user_id, movie_id, movie_rate):
        pass

    @abstractmethod
    def find_user_movies(self, user_id):
        pass

    @abstractmethod
    def delete_user_movie(self, user_id, movie_id):
        pass

    @abstractmethod
    def persist_message(self, message):
        pass


class DBServiceImpl(DBService):
    def save_user(self, user):
        with Query.construct(**self.config) as _q:
            _last_id = _q.table('users') \
                .save(**user) \
                .returning('id') \
                .fetch_one()
            user["id"] = _last_id['id']
            _q.commit()
        return user

    def update_user(self, user):
        _user_id = user['id']
        del user['id']
        with Query.construct(**self.config) as _q:
            _q.table('users') \
                .update(**user).where('id = {}'.format(_user_id)) \
                .exec()
            _q.commit()
        user['id'] = _user_id
        return user

    def find_user(self, user_id):
        with Query.construct(**self.config) as _q:
            _user = _q.table('users') \
                .find() \
                .where('id = {}'.format(user_id)) \
                .fetch_one()
            _q.commit()
        return dict(_user)

    def delete_user(self, user_id):
        with Query.construct(**self.config) as _q:
            _q.table('users') \
                .delete() \
                .where('id = {}'.format(user_id)) \
                .exec()
            _q.commit()

    def create_club(self, club, owner_id):
        with Query.construct(**self.config) as _q:
            club_id = _q.table('clubs') \
                .save(**club) \
                .returning('id') \
                .fetch_one()['id']
            _q.table('users_clubs').save(
                user_id=owner_id,
                club_id=club_id,
                user_role='owner'
            ).exec()
            club['id'] = club_id
            _q.commit()
        return club

    def update_club(self, club):
        with Query.construct(**self.config) as _q:
            _q.table('clubs') \
                .update(**club).where('id = {}'.format(club['id'])) \
                .exec() \
                .commit()
        return club

    def delete_club(self, club_id):
        with Query.construct(**self.config) as _q:
            _q.table('users_clubs') \
                .delete() \
                .where('club_id = {}'.format(club_id)) \
                .exec()
            _q.table('clubs') \
                .delete() \
                .where('id = {}'.format(club_id))\
                .exec()
            _q.commit()

    def find_club_members(self, club_id):
        with Query.construct(**self.config) as _q:
            _members = _q.table('users_clubs').find('users.id as id',
                                                    'first_name',
                                                    'last_name',
                                                    'email',
                                                    'username',
                                                    'password',
                                                    'gender',
                                                    'birthday'
                                                    ) \
                .join('users', {'user_id': 'id'}) \
                .where('users_clubs.club_id = {}'.format(club_id)) \
                .fetch_all()
            _q.commit()
        return [dict(_mem) for _mem in _members]

    def find_user_clubs(self, user_id):
        with Query.construct(**self.config) as _q:
            _clubs = _q.table('users_clubs') \
                .find('clubs.*').join('clubs', {'club_id': 'id'}) \
                .where('users_clubs.user_id = {}'.format(user_id)) \
                .fetch_all()
            _q.commit()
        return [dict(_club) for _club in _clubs]

    def persist_message(self, message):
        with Query.construct(**self.config) as _q:
            _id = _q.table('chat_messages') \
                .save(**message) \
                .returning('id') \
                .fetch_one()['id']
            message['id'] = _id
            _q.commit()
        return message

    def add_user_movie(self, user_id, movie):
        with Query.construct(**self.config) as _q:
            _movie = {
                'id': movie['id'],
                'name': movie['name'],
                'year': movie['year'],
                'description': movie['description'],
                'tagline': movie['tagline'],
                'duration': movie['duration'],
                'genre': movie['genre'],
                'country': movie['country'],
                'picture': movie['picture'],
            }
            # Save movie
            _q.table('movies').save_if_not_exists('id = {}'.format(movie['id']), **_movie).exec()
            # Add movie to user library
            _q.table('users_movies').save(user_id=user_id,
                                          movie_id=movie['id'],
                                          status='non_watched'
                                          ).exec()
            _crew = {
                'director': movie['director'],
                'composer': movie['composer'],
                'editor': movie['editor'],
                'operator': movie['operator'],
                'screenwriter': movie['script'],
                'producer': movie['producers'],
                'actor': movie['cast']
            }
            for _crew_role, _crew_mems in _crew.items():
                if _crew_mems is None:
                    continue
                if isinstance(_crew_mems, list):
                    for _person in _crew_mems:
                        if _person is None:
                            continue
                        _q.table('persons').save_if_not_exists('id = {}'.format(_person['id']), **_person).exec()
                        # Add producers, screenwriters
                        if _crew_role != 'actor':
                            _q.table('crew_movies') \
                                .save_if_not_exists(
                                'crew_id = {0} AND movie_id = {1}'.format(_person['id'], movie['id']),
                                crew_id=_person['id'],
                                movie_id=movie['id'],
                                crew_role=_crew_role) \
                                .exec()
                        # Add actors
                        else:
                            _q.table('cast_movies') \
                                .save_if_not_exists(
                                'actor_id = {0} AND movie_id = {1}'.format(_person['id'], movie['id']),
                                actor_id=_person['id'],
                                movie_id=movie['id']) \
                                .exec()
                # Add director, composer, editor, operator
                else:
                    _q.table('persons').save_if_not_exists('id = {}'.format(_crew_mems['id']), **_crew_mems).exec()
                    _q.table('crew_movies') \
                        .save_if_not_exists('crew_id = {0} AND movie_id = {1}'.format(_crew_mems['id'], movie['id']),
                                            crew_id=_crew_mems['id'],
                                            movie_id=movie['id'],
                                            crew_role=_crew_role) \
                        .exec()
            _q.commit()

    def rate_movie(self, user_id, movie_id, movie_rate):
        with Query.construct(**self.config) as _q:
            _q.table('users_movies') \
                .update(**movie_rate)\
                .where('user_id = {0} AND movie_id = {1}'.format(user_id, movie_id)) \
                .exec() \
                .commit()

    def delete_user_movie(self, user_id, movie_id):
        with Query.construct(**self.config) as _q:
            _q.table('users_movies') \
                .delete() \
                .where('user_id = {0} AND movie_id = {1}'.format(user_id, movie_id)) \
                .exec() \
                .commit()

    def find_user_movies(self, user_id):
        with Query.construct(**self.config) as _q:
            _movies = _q.raw('SELECT * FROM find_user_movies({0})'.format(user_id)) \
                .fetch_all()
            _q.commit()
        return [dict(_movie) for _movie in _movies]
