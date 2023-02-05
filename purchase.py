import sqlite3


class Seat:
    def __init__(self, seat_id: str, database: str = 'cinema.db') -> None:
        self.database = database
        self.seat_id = seat_id
        self.price = self._get_price(self.seat_id)

    def _get_price(self, seat_id: str) -> float:
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("""
                SELECT "price" FROM 'Seat' WHERE "seat_id" == ?
                """, [seat_id])
        res = cursor.fetchall()
        connection.close()
        return float(*res[0])

    def is_free(self, seat_id: str) -> bool:
        pass

    def occupy(self, seat_id: str) -> None:
        pass


class Card:
    def __init__(self, type_card: str, number: str, cvc: str, holder: str,
                 database: str = 'banking.db') -> None:
        self.type_card = type_card
        self.number = number
        self.cvc = cvc
        self.holder = holder
        self.database = database

    def validate(self, price: float) -> bool:
        pass


class User:
    def __init__(self, name: str) -> None:
        self.name = name

    def buy(self, seat: Seat, card: Card):
        pass
