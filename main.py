from purchase import User, Seat, Card
from ticket import Ticket

user = User(input('Your full name: '))
seat = Seat(input('Preferred seat number: '))
if not seat.is_free():
    print('Seat is taken!')
else:
    card_type = input('Your card type: ')
    card_number = int(input('Your card number: '))
    card_cvc = int(input('Your card cvc: '))
    card_holder = input('Card holder name: ')

    card = Card(card_type, card_number, card_cvc, card_holder)
    if not card.validate(seat.price):
        print("There's a problem with your card")
    else:
        user.buy(seat, card)
        Ticket(user, seat).to_pdf()
        print('Purchase successful!')
