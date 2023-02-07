from purchase import User, Seat, Card

user = User(input('Your full name: '))
seat = user.choose_seat(Seat(input('Preferred seat number: ')))
if seat:
    card_type = input('Your card type: ')
    card_number = int(input('Your card number: '))
    card_cvc = int(input('Your card cvc: '))
    card_holder = input('Card holder name: ')

    card = Card(card_type, card_number, card_cvc, card_holder)

    print(user.buy(seat, card))
