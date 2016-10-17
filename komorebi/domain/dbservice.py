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
    def rate_movie(self, movie_rate):
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
        _q = Query.construct(**self.config)\
            .table('users')\
            .save(**user)\
            .returning('id')
        _last_id = _q.fetch_one()
        user["id"] = _last_id[0]
        return user

    def update_user(self, user):
        _user_id = user['id']
        del user['id']
        Query.construct(**self.config)\
            .table('users')\
            .update(**user).where('id = {}'.format(_user_id))\
            .exec()
        user['id'] = _user_id
        return user

    def find_user(self, user_id):
        return Query.construct(**self.config)\
            .table('users')\
            .find()\
            .where('id = {}'.format(user_id))\
            .fetch_one()

    def delete_user(self, user_id):
        Query.construct(**self.config)\
            .table('users')\
            .delete()\
            .where('id = {}'.format(user_id))\
            .exec()

    def create_club(self, club, owner_id):
        q = Query.construct(**self.config)
        club_id = q.table('clubs')\
            .save(**club)\
            .returning('id')\
            .fetch_one()['id']
        q.table('users_clubs').save(
            user_id=owner_id,
            club_id=club_id,
            user_role='owner'
        ).exec()
        club['id'] = club_id
        return club

    def update_club(self, club):
        q = Query.construct(**self.config)
        q.table('clubs').update(**club).where('id = {}'.format(club['id']))
        q.exec()
        return club

    def delete_club(self, club_id):
        q = Query.construct(**self.config)
        q.table('users_clubs')\
            .delete()\
            .where('club_id = {}'.format(club_id))\
            .exec()
        q.table('clubs')\
            .delete()\
            .where('id = {}'.format(club_id))

    def find_club_members(self, club_id):
        q = Query.construct(**self.config)
        q.table('users_clubs').find('users.id as id',
                                    'first_name',
                                    'last_name',
                                    'email',
                                    'user_name',
                                    'password')\
            .join('users', {'user_id': 'id'}).where('users_clubs.club_id = {}'.format(club_id))
        return q.fetch_all()

    def find_user_clubs(self, user_id):
        return Query.construct(**self.config)\
            .table('users_clubs')\
            .find('clubs.*').join('clubs', {'club_id': 'id'})\
            .where('users_clubs.user_id = {}'.format(user_id))\
            .fetch_all()

    def persist_message(self, message):
        q = Query.construct(**self.config)
        return q.table('chat_messages')\
            .save(**message)\
            .returning('id')\
            .fetch_one()

    # TODO: add test for add_movie()
    def add_user_movie(self, user_id, movie):
        q = Query.construct(**self.config)
        q.begin().exec()
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
        q.table('movies').save_if_not_exists('id = {}'.format(movie['id']), **_movie).exec()
        # Add movie to user library
        q.table('users_movies').save(user_id=user_id,
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
                    q.table('persons').save_if_not_exists('id = {}'.format(_person['id']), **_person).exec()
                    # Add producers, screenwriters
                    if _crew_role != 'actor':
                        q.table('crew_movies')\
                            .save_if_not_exists('crew_id = {0} AND movie_id = {1}'.format(_person['id'], movie['id']),
                                                crew_id=_person['id'],
                                                movie_id=movie['id'],
                                                crew_role=_crew_role)\
                            .exec()
                    # Add actors
                    else:
                        q.table('cast_movies') \
                            .save_if_not_exists('actor_id = {0} AND movie_id = {1}'.format(_person['id'], movie['id']),
                                                actor_id=_person['id'],
                                                movie_id=movie['id']) \
                            .exec()
            # Add director, composer, editor, operator
            else:
                q.table('persons').save_if_not_exists('id = {}'.format(_crew_mems['id']), **_crew_mems).exec()
                q.table('crew_movies') \
                    .save_if_not_exists('crew_id = {0} AND movie_id = {1}'.format(_crew_mems['id'], movie['id']),
                                        crew_id=_crew_mems['id'],
                                        movie_id=movie['id'],
                                        crew_role=_crew_role) \
                    .exec()
        q.commit().exec()

    def rate_movie(self, movie_rate):
        Query.construct(**self.config)\
            .table('users_movies')\
            .update(**movie_rate)\
            .exec()

    def delete_user_movie(self, user_id, movie_id):
        q = Query.construct(**self.config)
        q.table('users_movies')\
            .delete()\
            .where('user_id = {0} AND movie_id = {1}'.format(user_id, movie_id))\
            .exec()

    def find_user_movies(self, user_id):
        q = Query.construct(**self.config)
        return q.raw('SELECT * FROM find_user_movies({0})'.format(user_id))\
            .fetch_all()


