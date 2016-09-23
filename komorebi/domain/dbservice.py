from abc import abstractmethod


class DBService:

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
    def find_user(self, **kwargs):
        pass

    @abstractmethod
    def delete_user(self, user):
        pass

    @abstractmethod
    def delete_club(self, club):
        pass


class DBServiceImpl(DBService):

    def save_user(self, user):
        pass

    def update_user(self, user):
        pass

    def create_club(self, club):
        pass

    def find_user(self, **kwargs):
        pass

    def delete_user(self, user):
        pass

    def delete_club(self, club):
        pass
