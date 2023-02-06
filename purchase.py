import sqlite3
from ticket import Ticket


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

    def is_free(self) -> bool:
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("""
                SELECT "taken" FROM 'Seat' WHERE "seat_id" == ?
                """, [self.seat_id])
        res = cursor.fetchall()
        connection.close()
        return res[0][0] == 0

    def occupy(self) -> None:
        connection = sqlite3.connect(self.database)
        connection.execute("""
        UPDATE "Seat" SET "taken" = 1 WHERE "seat_id" = ?
        """, [self.seat_id])
        connection.commit()
        connection.close()


class Card:
    def __init__(self, type_card: str, number: int, cvc: int, holder: str,
                 database: str = 'banking.db') -> None:
        self.type_card = type_card
        self.number = number
        self.cvc = cvc
        self.holder = holder
        self.database = database

    def validate(self, price: float) -> bool:
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        try:
            cursor.execute("""
                    SELECT "type", "cvc", "holder", "balance" FROM 'Card' 
                    WHERE "number" == ?
                    """, [self.number])
            res = cursor.fetchall()[0]
        except IndexError:
            return False
        connection.close()
        return res[0] == self.type_card and res[1] == self.cvc \
            and res[2] == self.holder and res[3] >= price


class User:
    def __init__(self, name: str) -> None:
        self.name = name

    def buy(self, seat: Seat, card: Card):
        seat.occupy()
        card_balance = self._get_card_balance(card)
        self._update_balance(seat, card, card_balance)
        Ticket(self, seat).to_pdf()

    @staticmethod
    def _update_balance(seat: Seat, card: Card, card_balance: float) -> None:
        new_balance = card_balance - seat.price
        connection = sqlite3.connect(card.database)
        connection.execute("""
            UPDATE "Card" SET "balance" = ? WHERE "number" == ?
        """, [new_balance, card.number])
        connection.commit()
        connection.close()

    @staticmethod
    def _get_card_balance(card: Card) -> float:
        connection = sqlite3.connect(card.database)
        cursor = connection.cursor()
        cursor.execute("""
        SELECT "balance" FROM "Card" WHERE "number" == ?
        """, [card.number])
        res = cursor.fetchall()[0][0]
        connection.commit()
        connection.close()
        return res
