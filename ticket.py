from models import (
    get_balance,
    update_balance,
    get_fare,
    get_station_distance,
  
)


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