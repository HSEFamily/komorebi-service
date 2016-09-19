from abc import abstractmethod


class ADBService:

    @abstractmethod
    def save_user(self, user):
        pass

    @abstractmethod
    def update_user(self, user):
        pass

    @abstractmethod
    def delete_user(self, user):
        pass

    @abstractmethod
    def find_user(self, **kwargs):
        pass

    @abstractmethod
    def create_club(self, club):
        pass

    @abstractmethod
    def delete_club(self, club):
        pass
