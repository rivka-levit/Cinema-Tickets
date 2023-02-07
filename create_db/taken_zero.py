import sqlite3


def taken_to_zero():
    connection = sqlite3.connect('../cinema.db')
    connection.execute("""
        UPDATE "Seat" SET "taken" = 0
    """)
    connection.commit()
    connection.close()


if __name__ == '__main__':
    taken_to_zero()
