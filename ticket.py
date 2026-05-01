from models import (
    get_balance,
    update_balance,
    get_fare,
    get_station_distance,
    add_ticket,
   get_ticket_history
)
from database import get_connection

def calculate_distance(source: str, destination: str):
    src_distance = get_station_distance(source)
    dest_distance = get_station_distance(destination)

    if src_distance is None or dest_distance is None:
        return None, "Invalid station"

    if source == destination:
        return None, "Source and destination cannot be the same"

    distance = abs(dest_distance - src_distance)
    return distance, None


def process_payment(user_id: int, fare: int):
    balance = get_balance(user_id)

    if balance is None:
        return None, "User not found"

    if balance <= 0:
        return None, "No balance left"

    if balance < fare:
        return None, f"Insufficient balance. Fare: ₹{fare}, Balance: ₹{balance}"

    new_balance = balance - fare
    update_balance(user_id, new_balance)

    return new_balance, None

def book_ticket(source: str, destination: str, user_id: int):
   
    distance, error = calculate_distance(source, destination)
    if error:
        return {"success": False, "error": error}


    fare = get_fare(distance)
    if fare is None:
        return {"success": False, "error": "Fare mapping not found for this distance"}

    new_balance, error = process_payment(user_id, fare)
    if error:
        return {"success": False, "error": error}


    add_ticket(user_id, source, destination, distance, fare)


    return {
        "success": True,
        "data": {
            "source": source,
            "destination": destination,
            "distance_km": distance,
            "fare": fare,
            "remaining_balance": new_balance
        }
    }


#     add_ticket(user_id, source, destination, distance, fare)
# def book_ticket(source: str, destination: str, user_id: int):
#     distance, error = calculate_distance(source, destination)
#     if error:
#         return error

#     fare = get_fare(distance)
#     if fare is None:
#         return {"error": "Fare mapping not found for this distance"}

#     new_balance, error = process_payment(user_id, fare)
#     if error:
#         return {"error": error}

#     add_ticket(user_id, source, destination, distance, fare)

#     return {
#         "success": True,
#         "data": {
#             "source": source,
#             "destination": destination,
#             "distance_km": distance,
#             "fare": fare,
#             "remaining_balance": new_balance
#         }
#     }
# def book_ticket(source, destination, user_id):

#     conn = get_connection()
#     cursor= conn.cursor()


#     distance = ...
#     src_distance = get_station_distance(source)
#     dest_distance = get_station_distance(destination)
#     fare = ...


#     user = cursor.execute("SELECT balance FROM users WHERE id=?", (user_id,)).fetchone()

#     if user["balance"] < fare:
#         return {"success": False, "error": "Insufficient balance"}


#     new_balance = user["balance"] - fare

#     cursor.execute("UPDATE users SET balance=? WHERE id=?", (new_balance, user_id))


#     cursor.execute(
#         "INSERT INTO tickets (user_id, source, destination, distance, fare) VALUES (?, ?, ?, ?, ?)",
#         (user_id, source, destination, distance, fare)
#     )

#     conn.commit()
#     conn.close()

#     return {
#         "success": True,
#         "fare": fare,
#         "remaining_balance": new_balance
#     }

def get_user_ticket_history(username: str):
    tickets = get_ticket_history(username)

    if not tickets:
        return {"success": True, "data": [], "message": "No tickets found"}

    return {
        "success": True,
        "data": tickets
    } 