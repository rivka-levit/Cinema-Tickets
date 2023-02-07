import sqlite3


def create_table():
    connection = sqlite3.connect('../banking.db')
    connection.execute("""
    CREATE TABLE 'Card' (
        'type' TEXT, 
        'number' INTEGER, 
        'cvc'  INTEGER,
        'holder' TEXT,
        'balance' REAL);
    """)
    connection.commit()
    connection.close()


def insert_record(t: str, number: int, cvc: int, holder: str,
                  balance: float) -> None:
    connection = sqlite3.connect('../banking.db')
    connection.execute("""
    INSERT INTO 'Card' ('type', 'number', 'cvc', 'holder', 'balance') 
    VALUES (?, ?, ?, ?, ?)""", [t, number, cvc, holder, balance])
    connection.commit()
    connection.close()


create_table()

data = [('Master Card', 23456789, 234, 'Marry Smith', 5000.0), ('Visa', 12345678, 123, 'John Smith', 4400.0)]

if __name__ == '__main__':
    for a, b, c, d, e in data:
        insert_record(a, b, c, d, e)
