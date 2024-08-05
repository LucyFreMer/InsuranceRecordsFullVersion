import sqlite3


def init_db():
    conn = sqlite3.connect('insurance.db')
    cursor = conn.cursor()

    # Vytvoření tabulky insured_person
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS insured_person (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT 
        )
    ''')

    # Vytvoření tabulky insurance
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS insurance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            insured_person_id INTEGER,
            policy_name TEXT,
            start_date TEXT, 
            FOREIGN KEY (insured_person_id) REFERENCES insured_person(id)
        )    
    ''')

    # Vytvoření tabulky claims
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            insured_person_id INTEGER,
            claim_date TEXT,
            description TEXT,
            FOREIGN KEY (insured_person_id) REFERENCES insured_person(id)
        )
    ''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
