from datetime import datetime, timedelta

def to_indian_time(timestamp: str) -> str:
   

    try:
        dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    except Exception:
        return timestamp  

    ist_time = dt + timedelta(hours=5, minutes=30)

    return ist_time.strftime("%d %b %Y, %I:%M %p")