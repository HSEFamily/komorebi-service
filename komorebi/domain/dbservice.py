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
    def create_club(self, club):
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

    def create_club(self, club):
        pass

    def delete_club(self, club_id):
        Query.construct(tb='clubs', **self.config)\
            .delete()\
            .where('id = {}'.format(club_id))\
            .exec()
