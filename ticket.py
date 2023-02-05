from purchase import Seat, User
from random import choice


class Ticket:
    def __init__(self, user: User, seat: Seat):
        self.id = self._get_id()
        self.user = user
        self.seat = seat

    @staticmethod
    def _get_id():
        let = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        res = ''
        for i in range(8):
            res = res + choice(let)
        return res

    def to_pdf(self):
        pass
