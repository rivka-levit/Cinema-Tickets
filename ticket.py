from purchase import Seat, User
from random import choice
from string import ascii_letters, digits
from fpdf import FPDF


class Ticket:
    """
    Generates a Pdf file that contains the digital ticket user has purchased,
    with his name, number of the seat, id of the thicket and the price.
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

        pdf.output(self.filepath)

