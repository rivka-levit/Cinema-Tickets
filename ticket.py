from purchase import Seat, User
from random import choice
from string import ascii_letters, digits


class Ticket:
    def __init__(self, user: User, seat: Seat):
        self.id = self._get_id()
        self.user = user
        self.seat = seat

    @staticmethod
    def _get_id():
        res = ''
        for i in range(8):
            res = res + choice(ascii_letters + digits)
        return res

    def to_pdf(self):
        pass
