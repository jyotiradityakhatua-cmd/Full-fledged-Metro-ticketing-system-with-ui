from database import get_connection
from database import create_tables
from datetime import datetime, timedelta
from to_indian_time import to_indian_time


def create_user():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = 1")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (id, balance) VALUES (?, ?)",
                       (1, 100.0))
        conn.commit()
    conn.close()


def get_balance(user_id: int):  
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchall()
    # conn.close()
    # print(result)
    # print(result[0][0])
    return result[0][0] if result else None



def update_balance(user_id: int, balance: float):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (balance, user_id))
    conn.commit()
    conn.close()


def insert_station():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM stations")
    count = cursor.fetchone()[0]

    if count == 0:
        stations=[("Station A",0),
                  ("Station B",10),
                  ("Station C", 25),
                  ("Station D", 60),
                  ("Station E", 120)
        ]


        cursor.executemany("INSERT INTO stations (name, distance) VALUES (?,?)",stations)

    conn.commit()
    conn.close()

def get_station_distance(name):
    conn = get_connection()
    cursor= conn.cursor()


    cursor.execute("SELECT distance FROM stations WHERE name = ?",(name,))
    result= cursor.fetchone()


    conn.close()
    return result[0] if result else None


def list_stations():
    conn= get_connection()
    cursor= conn.cursor()

    cursor.execute("SELECT name FROM stations")
    stations= cursor.fetchall()

    conn.close()
    return[s[0] for s in stations]

def insert_fare():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM fares")
    count = cursor.fetchone()[0]

    if count == 0:
        fares = [
            (0, 20, 20),
            (21, 50, 50),
            (51, 100, 100),
            (101, 1000, 150)
        ]

        cursor.executemany(
            "INSERT INTO fares (min_km, max_km, price) VALUES (?,?,?)",
            fares
        )

    conn.commit()
    conn.close()


def get_fare(distance):
    conn = get_connection()
    cursor= conn.cursor()

    cursor.execute(""" SELECT price FROM fares WHERE ? BETWEEN min_km and max_km """,(distance,))

    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None

def create_ticket_record(user_id, source, destination, distance, fare):
    conn = get_connection()
    cursor = conn.cursor()
    
   
    cursor.execute('''CREATE TABLE IF NOT EXISTS tickets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        source TEXT,
                        destination TEXT,
                        distance REAL,
                        fare INTEGER,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )''')


# def add_ticket(user_id, source, destination, distance, fare):
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#         INSERT INTO tickets (user_id, source, destination, distance, fare)
#         VALUES (?, ?, ?, ?, ?)
#     """, (user_id, source, destination, distance, fare))

#     conn.commit()
#     conn.close()

#     def get_ticket_history(user_id: int):
#         conn = get_connection()
#         cursor = conn.cursor()

#     cursor.execute("""
#         SELECT source, destination, distance, fare, timestamp
#         FROM tickets
#         WHERE user_id = ?
#         ORDER BY timestamp DESC
#     """, (user_id,))

#     rows = cursor.fetchall()
#     conn.close()

#     return [
#         {
#             "source": r[0],
#             "destination": r[1],
#             "distance_km": r[2],
#             "fare": r[3],
#             "timestamp": r[4]
#         }
#         for r in rows
#     ]

def add_ticket(user_id, source, destination, distance, fare):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tickets (user_id, source, destination, distance, fare)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, source, destination, distance, fare))

    conn.commit()
    conn.close()



def get_ticket_history(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT source, destination, distance, fare, timestamp
        FROM tickets
        WHERE user_id = ?
        ORDER BY timestamp DESC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return [
    {
        "source": r[0],
        "destination": r[1],
        "distance_km": r[2],
        "fare": r[3],
        "timestamp": to_indian_time(r[4])
    }
    for r in rows
]
def insert_station():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM stations")
    count = cursor.fetchone()[0]

    if count == 0:
        stations = [
            ("Station A", 0),
            ("Station B", 10),
            ("Station C", 25),
            ("Station D", 60),
            ("Station E", 120)
        ]

        cursor.executemany(
            "INSERT INTO stations (name, distance) VALUES (?, ?)",
            stations
        )

        conn.commit()

    conn.close()