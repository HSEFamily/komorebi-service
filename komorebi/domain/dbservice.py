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

    def persist_message(self, message):
        q = Query.construct(**self.config)
        return q.table('chat_messages')\
            .save(**message)\
            .returning('id')\
            .fetch_one()
