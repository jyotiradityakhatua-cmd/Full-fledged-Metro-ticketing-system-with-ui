from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt
from database import create_tables, get_connection
from auth import get_current_user, SECRET_KEY, ALGORITHM
from models import (
    list_stations, 
    get_station_distance, 
    get_fare, 
    get_balance, 
    update_balance, 
    create_user,
    insert_station, 
    insert_fare
)
import ticket
from config import DEFAULT_BALANCE
from ticket import  book_ticket
from database import create_tables, get_connection




app = FastAPI(title="Metro Ticketing System API")

@app.on_event("startup")
def startup_event():
    create_user()
    insert_station()
    insert_fare()



@app.post("/auth/register", tags=["Auth"])
def register(username: str, password: str):
    conn = get_connection()
    try:
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return {"message": "User registered successfully"}
    except Exception:
        raise HTTPException(status_code=400, detail="Username already exists")
    finally:
        conn.close()

@app.post("/auth/login", tags=["Auth"])
def login(username: str, password: str):
    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode({"sub": str(user["id"])}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/metro/stations", dependencies=[Depends(get_current_user)])
def list_stations():
    conn = get_connection()
    stations = conn.execute("SELECT name, distance FROM stations").fetchall()
    conn.close()
    return {"stations": [dict(s) for s in stations]}

@app.get("/user/balance", tags=["User"])
def get_user_balance(user_id: int = Depends(get_current_user)):
    balance = get_balance(user_id)
    if balance is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"balance": balance}

@app.post("/ticket/book", tags=["Ticket"])

def book_tickets(source: str, destination: str, user_id: int = Depends(get_current_user)):
    return {"message":book_ticket( source, destination, user_id)}
    # result = ticket.book_ticket(source, destination, user_id)
    
    # if "Booked" in result:
    #     return {"status": "Success", "details": result}
    # else:
    #     raise HTTPException(status_code=400, detail=result)


    # distance = calculate_distance(source, destination)
    # conn = get_connection()
    # fare_row = conn.execute("SELECT price FROM fares WHERE ? BETWEEN min_km AND max_km", (distance,)).fetchone()
    
    # if not fare_row:
    #     raise HTTPException(status_code=400, detail="Fare mapping not found for this distance")
    
    # fare = fare_row["price"]


    # user = conn.execute("SELECT balance FROM users WHERE id = ?", (user_id,)).fetchone()
    # if user["balance"] < fare:
    #     raise HTTPException(status_code=400, detail=f"Insufficient balance. Fare: {fare}, Balance: {user['balance']}")

    # new_balance = user["balance"] - fare
    # conn.execute("UPDATE users SET balance = ? WHERE id = ?", (new_balance, user_id))
    # conn.commit()
    # conn.close()

    # return {
    #     "message": "Ticket Booked Successfully",
    #     "details": {
    #         "from": source,
    #         "to": destination,
    #         "distance_km": distance,
    #         "fare_charged": fare,
    #         "remaining_balance": new_balance
    #     }
    # }


@app.post("/admin/setup", tags=["Admin"])
def setup_system():
    conn = get_connection()

    stations = [("Station A", 0), ("Station B", 10), ("Station C", 25), ("Station D", 60), ("Station E", 120)]
    conn.executemany("INSERT OR IGNORE INTO stations (name, distance) VALUES (?,?)", stations)

    fares = [(0, 20, 20), (21, 50, 50), (51, 100, 100), (101, 1000, 150)]
    conn.executemany("INSERT OR IGNORE INTO fares (min_km, max_km, price) VALUES (?,?,?)", fares)
    conn.commit()
    conn.close()
    return {"message": "System stations and fares initialized"}
    

@app.put("/user/balance", tags=["User"])
def update_user_balance(amount: float, user_id: int = Depends(get_current_user)):
    balance = get_balance(user_id)
    if balance is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_balance = balance + amount
    update_balance(user_id, new_balance)
    return {"message": "Balance updated successfully", "new_balance": new_balance}




