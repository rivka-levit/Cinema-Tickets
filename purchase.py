import sqlite3
from random import choice
from string import ascii_letters, digits
from fpdf import FPDF


class Seat:
    """
    Occupies the seat if it is free
    """
    def __init__(self, seat_id: str, database: str = 'cinema.db') -> None:
        self.database = database
        self.seat_id = seat_id
        self.price = self._get_price(self.seat_id)

    def _get_price(self, seat_id: str) -> float:
        """
        Get price of the seat from database
        :return: the price
        """
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT "price" FROM 'Seat' WHERE "seat_id" == ?
            """, [seat_id])
        res = cursor.fetchall()
        connection.close()
        return float(*res[0])

    def is_free(self) -> bool:
        """
        Check if the seat is not taken yet
        :return: boolean value
        """
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT "taken" FROM 'Seat' WHERE "seat_id" == ?
            """, [self.seat_id])
        res = cursor.fetchall()
        connection.close()
        return res[0][0] == 0

    def occupy(self) -> None:
        """
        Set the seat to occupied in the database. So that nobody could buy it again
        """
        connection = sqlite3.connect(self.database)
        connection.execute("""
            UPDATE "Seat" SET "taken" = 1 WHERE "seat_id" = ?
            """, [self.seat_id])
        connection.commit()
        connection.close()


class Card:
    """
    Hold and validate all the information about user card
    """
    def __init__(self, type_card: str, number: int, cvc: int, holder: str,
                 database: str = 'banking.db') -> None:
        self.type_card = type_card
        self.number = number
        self.cvc = cvc
        self.holder = holder
        self.database = database

    def validate(self, price: float) -> bool:
        """
        Validates all the parameters of the card and if the balance is enough
        to buy the ticket
        :return: boolean value
        """
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
    """
    Makes the purchase of a seat using the card of the user
    """
    def __init__(self, name: str) -> None:
        self.name = name

    @staticmethod
    def choose_seat(seat: Seat) -> Seat:
        if seat.is_free():
            return seat
        while not seat.is_free():
            print('Seat is taken!')
            seat = Seat(input('Enter another seat number: '))
        return seat

    def buy(self, seat: Seat, card: Card):
        """
        Make the purchase of a ticket. Sets the seat to occupied and change
        the balance on the card
        """
        if not card.validate(seat.price):
            return "There's a problem with your card"
        seat.occupy()
        card_balance = self._get_card_balance(card)
        self._update_balance(seat, card, card_balance)
        Ticket(self, seat).to_pdf()
        return 'Purchase successful!'

    @staticmethod
    def _update_balance(seat: Seat, card: Card, card_balance: float) -> None:
        """
        Subtract the price of the seat and set new card balance after the purchase
        """
        new_balance = card_balance - seat.price
        connection = sqlite3.connect(card.database)
        connection.execute("""
            UPDATE "Card" SET "balance" = ? WHERE "number" == ?
        """, [new_balance, card.number])
        connection.commit()
        connection.close()

    @staticmethod
    def _get_card_balance(card: Card) -> float:
        """
        Get card balance of the user that he has before the purchase
        :return: the balance on the card
        """
        connection = sqlite3.connect(card.database)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT "balance" FROM "Card" WHERE "number" == ?
            """, [card.number])
        card_balance = cursor.fetchall()[0][0]
        connection.commit()
        connection.close()
        return card_balance


class Ticket:
    """
    Generates a Pdf file that contains the digital ticket that user has
    purchased, with his name, number of the seat, id of the thicket and
    the price.
    """
    filepath = 'ticket.pdf'

    def __init__(self, user: User, seat: Seat):
        self.id = ''.join([choice(ascii_letters + digits) for _ in range(8)])
        self.user = user
        self.seat = seat

    def to_pdf(self):
        """Generate and save the Pdf to the file"""

        pdf = FPDF(orientation='P', unit='pt', format='A4')
        pdf.add_page()

        # Add the title

        pdf.set_font(family='Helvetica', size=32, style='B')
        pdf.cell(w=0, h=80, txt="Your Digital Ticket", border=1, align='C', ln=1)

        # Add the data of the user and the ticket

        data = [('Name:', self.user.name), ('Ticket ID:', self.id),
                ('Price:', self.seat.price), ('Seat number:', self.seat.seat_id)]

        for label, value in data:
            pdf.set_font(family='Helvetica', size=18, style='B')
            pdf.cell(w=150, h=35, txt=label, border=1)
            pdf.set_font(family='Helvetica', size=12)
            pdf.cell(w=389, h=35, txt=f'{value}', border=1, ln=1)

            pdf.cell(w=539, h=5, txt='', border=0, ln=1)

        # Write the pdf file

        pdf.output(self.filepath)
