import sqlite3


def create_table():
    connection = sqlite3.connect('../cinema.db')
    connection.execute("""
    CREATE TABLE 'Seat' (
        'seat_id' TEXT, 
        'taken' INTEGER, 
        'price' REAL );
    """)
    connection.commit()
    connection.close()


def insert_record(seat_id: str, taken: int, price: float) -> None:
    connection = sqlite3.connect('../cinema.db')
    connection.execute("""
    INSERT INTO 'Seat' ('seat_id', 'taken', 'price') 
    VALUES (?, ?, ?)""", [seat_id, taken, price])
    connection.commit()
    connection.close()


create_table()

data = [('A1', 0, 120.0), ('A2', 1, 100.0), ('A3', 0, 120.0),
        ('B1', 0, 100.0), ('B2', 1, 150.0), ('B3', 0, 120.0)]

if __name__ == '__main__':
    for s, t, p in data:
        insert_record(s, t, p)
