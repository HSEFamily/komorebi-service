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
    def delete_user(self, user):
        pass

    @abstractmethod
    def delete_club(self, club):
        pass


class DBServiceImpl(DBService):

    def save_user(self, user):
        _q = Query.construct(**self.config).save(user)
        _last_id = _q.exec().fetch_one()
        user["id"] = _last_id
        return user

    def update_user(self, user):
        Query.construct(tb='users', **self.config)\
            .update(user)\
            .exec()
        return user

    def create_club(self, club):
        pass

    def find_user(self, user_id):
        return Query.construct(tb='users', **self.config)\
            .find()\
            .where('id = {}'.format(user_id))\
            .fetch_one()

    def delete_user(self, user_id):
        Query.construct(tb='users', **self.config)\
            .delete()\
            .where('id = {}'.format(user_id))\
            .exec()

    def delete_club(self, club_id):
        Query.construct(tb='clubs', **self.config)\
            .delete()\
            .where('id = {}'.format(club_id))\
            .exec()
