# import streamlit as st
# import requests
# from datetime import datetime, timedelta




# API_URL = "http://localhost:8000"  
# st.set_page_config(page_title="Metro Ticketing System", layout="wide")

# if st.button("Test Backend"):
#     try:
#         res = requests.get(f"{API_URL}/metro/stations")
#         st.success(f"Backend reachable! Found {len(res.json()['stations'])} stations")
#     except requests.exceptions.ConnectionError:
#         st.error(f"Cannot connect to backend at {API_URL}")


# if "token" not in st.session_state:
#     st.session_state.token = None
# if "username" not in st.session_state:
#     st.session_state.username = ""

# def get_headers():
#     return {"Authorization": f"Bearer {st.session_state.token}"} if st.session_state.token else {}


# def to_indian_time(timestamp: str):
#     try:
#         dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
#         ist_time = dt + timedelta(hours=5, minutes=30)
#         return ist_time.strftime("%d %b %Y, %I:%M %p")
#     except:
#         return timestamp


# def register_user():
#     username = st.session_state.reg_username
#     password = st.session_state.reg_password
#     if not username or not password:
#         st.error("Please provide both username and password")
#         return
#     try:
#         res = requests.post(f"{API_URL}/auth/register", params={"username": username, "password": password})
#         res.raise_for_status()
#         st.success("Registration successful! Please log in.")
#     except requests.exceptions.HTTPError:
#         st.error("Username already exists")
#     except requests.exceptions.ConnectionError:
#         st.error(f"Cannot connect to backend at {API_URL}")

# def login_user():
#     username = st.session_state.login_username
#     password = st.session_state.login_password
#     try:
#         res = requests.post(f"{API_URL}/auth/login", json={"username": username, "password": password})
#         res.raise_for_status()
#         st.session_state.token = res.json()["access_token"]
#         st.session_state.username = username
#         st.success("Login successful!")
#     except requests.exceptions.ConnectionError:
#         st.error(f"Cannot connect to backend at {API_URL}")
#     except requests.exceptions.HTTPError:
#         st.error("Invalid username or password")


# if not st.session_state.token:
#     st.title("Welcome to Metro Ticketing System")
#     auth_tab = st.tabs(["Login", "Register"])


#     with auth_tab[0]:
#         st.subheader("Login")
#         st.text_input("Username", key="login_username")
#         st.text_input("Password", key="login_password", type="password")
#         st.button("Login", on_click=login_user)


#     with auth_tab[1]:
#         st.subheader("Register")
#         st.text_input("Username", key="reg_username")
#         st.text_input("Password", key="reg_password", type="password")
#         st.button("Register", on_click=register_user)


# else:
#     st.title(f"Metro Ticketing Dashboard — {st.session_state.username}")
#     headers = get_headers()

  
#     dashboard_tabs = st.tabs(["Balance", "Book Ticket", "Ticket History"])


#     with dashboard_tabs[0]:
#         st.subheader("Your Balance")
#         try:
#             res = requests.get(f"{API_URL}/user/balance", headers=headers)
#             balance = res.json()["balance"]
#             st.metric("Current Balance", f"₹{balance}")
#         except:
#             st.error("Could not fetch balance")

#         st.subheader("Add Balance")
#         topup_amount = st.number_input("Amount to add", min_value=0, step=10)
#         if st.button("Top-Up Balance"):
#             try:
#                 res = requests.put(f"{API_URL}/user/balance", params={"amount": topup_amount}, headers=headers)
#                 st.success(f"Balance updated! New balance: ₹{res.json()['new_balance']}")
#             except:
#                 st.error("Failed to update balance")


#     with dashboard_tabs[1]:
#       st.subheader("Book a Ticket")

#     try:
#         res = requests.get(f"{API_URL}/metro/stations", headers=headers)
#         stations = [s["name"] for s in res.json().get("stations", [])]
#     except requests.exceptions.RequestException:
#         stations = []
#         st.error("Could not fetch stations")

#     col1, col2 = st.columns(2)
#     with col1:
#         source = st.selectbox("Source Station", stations)
#     with col2:
#         destination = st.selectbox("Destination Station", stations)

#     if st.button("Book Ticket"):
#         if source == destination:
#             st.warning("Source and destination cannot be the same")
#         else:
#             try:
#                 res = requests.post(
#                     f"{API_URL}/ticket/book",
#                     json={"source": source, "destination": destination},
#                     headers=headers
#                 )

#                 if res.status_code == 200:
#                     st.success("Ticket booked successfully!")
#                 else:
#                     # Robust error handling: try JSON, fallback to text
#                     try:
#                         data = res.json()
#                         error_msg = data.get("error", "Booking failed")
#                     except requests.exceptions.JSONDecodeError:
#                         error_msg = res.text or "Booking failed"
#                     st.error(error_msg)

#             except requests.exceptions.ConnectionError:
#                 st.error(f"Cannot connect to backend at {API_URL}")

   
#     with dashboard_tabs[2]:
#         st.subheader("Ticket History")
#         try:
#             res = requests.get(f"{API_URL}/tickets", headers=headers)
#             tickets = res.json().get("data", [])
#             if tickets:
#                 for t in tickets:
#                     st.write(
#                         f"**From:** {t['source']} → **To:** {t['destination']} | "
#                         f"**Distance:** {t['distance_km']} km | "
#                         f"**Fare:** ₹{t['fare']} | "
#                         f"**Time (IST):** {to_indian_time(t['timestamp'])}"
#                     )
#             else:
#                 st.info("No tickets booked yet")
#         except requests.exceptions.ConnectionError:
#             st.error(f"Cannot connect to backend at {API_URL}")

#     with dashboard_tabs[2]:  
#         st.subheader("List of Metro Stations")
#     try:
#         res = requests.get(f"{API_URL}/metro/stations", headers=headers)
#         stations = res.json().get("stations", [])
#         if stations:
#             for s in stations:
#                 st.write(f"**Station:** {s['name']} | **Distance (km):** {s['distance']}")
#         else:
#             st.info("No stations found")
#     except requests.exceptions.ConnectionError:
#         st.error(f"Cannot connect to backend at {API_URL}")
# import streamlit as st
# import requests
# from datetime import datetime, timedelta


# API_URL = "http://localhost:8000"

# st.set_page_config(page_title="Metro Ticketing System", layout="wide")


# def init_state():
#     defaults = {
#         'token': None,
#         'username': '',
#     }
#     for k,v in defaults.items():
#         if k not in st.session_state:
#             st.session_state[k] = v

# def headers():
#     return {'Authorization': f"Bearer {st.session_state.token}"} if st.session_state.token else {}


# def api_get(path):
#     return requests.get(f"{API_URL}{path}", headers=headers(), timeout=10)


# def api_post(path, **kwargs):
#     return requests.post(f"{API_URL}{path}", headers=headers(), timeout=10, **kwargs)


# def api_put(path, **kwargs):
#     return requests.put(f"{API_URL}{path}", headers=headers(), timeout=10, **kwargs)


# def to_ist(ts):
#     try:
#         dt = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') + timedelta(hours=5, minutes=30)
#         return dt.strftime('%d %b %Y, %I:%M %p')
#     except Exception:
#         return ts


# def login(username, password):
#     res = requests.post(f"{API_URL}/auth/login", json={'username': username, 'password': password}, timeout=10)
#     res.raise_for_status()
#     data = res.json()
#     st.session_state.token = data['access_token']
#     st.session_state.username = username


# def register(username, password):
#     res = requests.post(f"{API_URL}/auth/register", params={'username': username, 'password': password}, timeout=10)
#     res.raise_for_status()


# def logout():
#     st.session_state.token = None
#     st.session_state.username = ''
#     st.rerun()

# def login_view():
#     st.title('Metro Ticketing System')
#     tab1, tab2 = st.tabs(['Login', 'Register'])

#     with tab1:
#         with st.form('login_form'):
#             u = st.text_input('Username')
#             p = st.text_input('Password', type='password')
#             submit = st.form_submit_button('Login')
#             if submit:
#                 try:
#                     login(u, p)
#                     st.success('Login successful')
#                     st.rerun()
#                 except Exception:
#                     st.error('Invalid credentials or server error')

#     with tab2:
#         with st.form('register_form'):
#             u = st.text_input('Username', key='reg_u')
#             p = st.text_input('Password', type='password', key='reg_p')
#             submit = st.form_submit_button('Register')
#             if submit:
#                 try:
#                     register(u, p)
#                     st.success('Registration successful')
#                 except Exception:
#                     st.error('Registration failed')


# def balance_tab():
#     st.subheader('Wallet')
#     try:
#         res = api_get('/user/balance')
#         bal = res.json().get('balance', 0)
#         st.metric('Balance', f'₹{bal}')
#     except Exception:
#         st.error('Failed to fetch balance')
#         bal = 0

#     with st.form('add_money_form'):
#         amount = st.number_input('Add Balance', min_value=1, step=10)
#         submit = st.form_submit_button('Add Money')
#         if submit:
#             try:
#                 res = api_put('/user/balance', params={'amount': amount})
#                 st.success(f"New Balance: ₹{res.json().get('new_balance')}")
#                 st.rerun()
#             except Exception:
#                 st.error('Update failed')


# def booking_tab():
#     try:
#         res = api_get('/metro/stations')
#         stations = [s['name'] for s in res.json().get('stations', [])]
#     except Exception:
#         stations = []
#         st.error('Failed to load stations')

#     if not stations:
#         return

#     with st.form('book_form'):
#         c1, c2 = st.columns(2)
#         with c1:
#             src = st.selectbox('Source', stations)
#         with c2:
#             dst = st.selectbox('Destination', stations)
#         submit = st.form_submit_button('Book Ticket')
#         if submit:
#             if src == dst:
#                 st.warning('Choose different stations')
#             else:
#                 try:
#                     res = api_post('/ticket/book', json={'source': src, 'destination': dst})
#                     if res.status_code == 200:
#                         st.success("Ticket booked!")
#                         print("Ticket booked successfully:", res.json())
#                         # st.show_spinner("ticket booked")
#                         st.rerun()
#                     else:
#                         st.error(res.json().get('detail', 'Booking failed'))
#                 except Exception:
#                     st.error('Booking failed')
# def load_stations():
#     try:
#         res = api_get('/metro/stations')
#         if res.status_code == 200:
#             stations = [s['name'] for s in res.json().get('stations', [])]
#             return stations
#         else:
#             st.error("Failed to load stations")
#             return []
#     except Exception as e:
#         st.error(f"Error: {str(e)}")
#         return []
# def process_booking(src, dst):
#     try:
#         res = api_post('/ticket/book', json={'source': src, 'destination': dst})
#         if res.status_code == 200:
        
#             st.success("Ticket successfully booked!")
#             st.balloons()  
#             print("Ticket booked successfully:", res.json())
#             st.rerun() 
#         else:
#             st.error(res.json().get('detail', 'Booking failed'))
#     except Exception as e:
#         st.error(f"Booking failed due to error: {str(e)}")


# def booking_tab():
  
#     stations = load_stations()

#     if not stations:
#         return  


#     with st.form('book_form'):
#         c1, c2 = st.columns(2)
#         with c1:
#             src = st.selectbox('Source', stations)
#         with c2:
#             dst = st.selectbox('Destination', stations)

#         submit = st.form_submit_button('Book Ticket')

#         if submit:
   
#             if src == dst:
#                 st.warning('Source and destination must be different!')
#             else:
        
#                 process_booking(src, dst)


# if __name__ == "__main__":
#     booking_tab()


# def history_tab():
#     try:
#         res = api_get('/tickets')
#         tickets = res.json().get('data', [])
#         if not tickets:
#             st.info('No tickets yet')
#         for t in tickets:
#             st.write(f"{t['source']} → {t['destination']} | ₹{t['fare']} | {to_ist(t['timestamp'])}")
#     except Exception:
#         st.error('Failed to load history')


# def stations_tab():
#     try:
#         res = api_get('/metro/stations')
#         for s in res.json().get('stations', []):
#             st.write(f"{s['name']} ({s['distance']} km)")
#     except Exception:
#         st.error('Failed to fetch stations')


# def dashboard_view():
#     st.title(f"Welcome, {st.session_state.username}")
#     t1, t2, t3, t4 = st.tabs(['Balance', 'Book Ticket', 'History', 'Stations'])
#     with t1:
#         balance_tab()
#     with t2:
#         booking_tab()
#     with t3:
#         history_tab()
#     with t4:
#         stations_tab()
#     st.button('Logout', on_click=logout)


# init_state()
# if st.session_state.token:
#     dashboard_view()
# else:
#     login_view()





# import streamlit as st
# import requests
# from datetime import datetime, timedelta

# API_URL = "http://localhost:8000"

# st.set_page_config(page_title="Metro Ticketing System", layout="wide")



# def init_state():
#     defaults = {
#         'token': None,
#         'username': '',
#     }
#     for k, v in defaults.items():
#         if k not in st.session_state:
#             st.session_state[k] = v



# def headers():
#     return {'Authorization': f"Bearer {st.session_state.token}"} if st.session_state.token else {}



# def api_get(path):
#     return requests.get(f"{API_URL}{path}", headers=headers(), timeout=10)


# def api_post(path, **kwargs):
#     return requests.post(f"{API_URL}{path}", headers=headers(), timeout=10, **kwargs)


# def api_put(path, **kwargs):
#     return requests.put(f"{API_URL}{path}", headers=headers(), timeout=10, **kwargs)



# def to_ist(ts):
#     try:
#         dt = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') + timedelta(hours=5, minutes=30)
#         return dt.strftime('%d %b %Y, %I:%M %p')
#     except Exception:
#         return ts



# def login(username, password):
#     res = requests.post(f"{API_URL}/auth/login", json={'username': username, 'password': password}, timeout=10)
#     res.raise_for_status()
#     data = res.json()
#     st.session_state.token = data['access_token']
#     st.session_state.username = username



# def register(username, password):
#     res = requests.post(f"{API_URL}/auth/register", params={'username': username, 'password': password}, timeout=10)
#     res.raise_for_status()



# def logout():
#     st.session_state.token = None
#     st.session_state.username = ''
#     st.rerun()



def login_view():
    st.title('Metro Ticketing System')
    tab1, tab2 = st.tabs(['Login', 'Register'])

    with tab1:
        with st.form('login_form'):
            u = st.text_input('Username')
            p = st.text_input('Password', type='password')
            submit = st.form_submit_button('Login')
            if submit:
                try:
                    login(u, p)
                    st.success('Login successful')
                    st.rerun()
                except Exception:
                    st.error('Invalid credentials or server error')

    with tab2:
        with st.form('register_form'):
            u = st.text_input('Username', key='reg_u')
            p = st.text_input('Password', type='password', key='reg_p')
            submit = st.form_submit_button('Register')
            if submit:
                try:
                    register(u, p)
                    st.success('Registration successful')
                except Exception:
                    st.error('Registration failed')



# def get_balance():
#     try:
#         res = api_get('/user/balance')
#         return res.json().get('balance', 0)
#     except Exception:
#         st.error('Failed to fetch balance')
#         return 0



# def balance_tab():
#     st.subheader('Wallet')
#     balance = get_balance()
#     st.metric('Balance', f'₹{balance}')

#     with st.form('add_money_form'):
#         amount = st.number_input('Add Balance', min_value=1, step=10)
#         submit = st.form_submit_button('Add Money')
#         if submit:
#             try:
#                 res = api_put('/user/balance', params={'amount': amount})
#                 st.success(f"New Balance: ₹{res.json().get('new_balance')}")
#                 st.rerun()
#             except Exception:
#                 st.error('Update failed')



# def load_stations():
#     try:
#         res = api_get('/metro/stations')
#         if res.status_code == 200:
#             return [s['name'] for s in res.json().get('stations', [])]
#         else:
#             st.error("Failed to load stations")
#             return []
#     except Exception as e:
#         st.error(f"Error: {str(e)}")
#         return []



# def booking_tab():
#     stations = load_stations()

#     if not stations:
#         return

#     with st.form('book_form'):
#         c1, c2 = st.columns(2)
#         with c1:
#             src = st.selectbox('Source', stations)
#         with c2:
#             dst = st.selectbox('Destination', stations)

#         submit = st.form_submit_button('Book Ticket')

#         if submit:
#             if src == dst:
#                 st.warning('Source and destination must be different!')
#             else:
#                 try:
#                     res = api_post('/ticket/book', json={'source': src, 'destination': dst})
#                     if res.status_code == 200:
#                         st.success("Ticket booked successfully!")
#                         st.balloons() 
#                         print("Ticket booked successfully:", res.json())
#                         st.rerun()  
#                     else:
#                         st.error(res.json().get('detail', 'Booking failed'))
#                 except Exception:
#                     st.error('Booking failed')



# def history_tab():
#     try:
#         res = api_get('/tickets')
#         tickets = res.json().get('data', [])
#         if not tickets:
#             st.info('No tickets yet')
#         for t in tickets:
#             st.write(f"{t['source']} → {t['destination']} | ₹{t['fare']} | {to_ist(t['timestamp'])}")
#     except Exception:
#         st.error('Failed to load history')



# def stations_tab():
#     try:
#         res = api_get('/metro/stations')
#         for s in res.json().get('stations', []):
#             st.write(f"{s['name']} ({s['distance']} km)")
#     except Exception:
#         st.error('Failed to fetch stations')



# def dashboard_view():
#     st.title(f"Welcome, {st.session_state.username}")


#     balance = get_balance()


#     t1, t2, t3, t4 = st.tabs(['Balance', 'Book Ticket', 'History', 'Stations'])

#     with t1:
#         balance_tab()
#     with t2:
#         booking_tab()
#     with t3:
#         history_tab()
#     with t4:
#         stations_tab()


#     st.write(f"Total Balance: ₹{balance}")


#     st.button('Logout', on_click=logout)



import streamlit as st
import requests
from datetime import datetime, timedelta
import time

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Metro Ticketing System", layout="wide")


def init_state():
    defaults = {
        'token': None,
        'username': '',
        'ticket_booked': False, 
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v



def headers():
    return {'Authorization': f"Bearer {st.session_state.token}"} if st.session_state.token else {}



def api_get(path):
    return requests.get(f"{API_URL}{path}", headers=headers(), timeout=10)


def api_post(path, **kwargs):
    return requests.post(f"{API_URL}{path}", headers=headers(), timeout=10, **kwargs)


def api_put(path, **kwargs):
    return requests.put(f"{API_URL}{path}", headers=headers(), timeout=10, **kwargs)



def to_ist(ts):
    try:
        dt = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') + timedelta(hours=5, minutes=30)
        return dt.strftime('%d %b %Y, %I:%M %p')
    except Exception:
        return ts



def login(username, password):
    res = requests.post(f"{API_URL}/auth/login", json={'username': username, 'password': password}, timeout=10)
    res.raise_for_status()
    data = res.json()
    st.session_state.token = data['access_token']
    st.session_state.username = username



def register(username, password):
    res = requests.post(f"{API_URL}/auth/register", params={'username': username, 'password': password}, timeout=10)
    res.raise_for_status()
    return res.json()
    # data = res.json()
    # return data
  
    




def logout():
    st.session_state.token = None
    st.session_state.username = ''
    st.session_state.ticket_booked = False 
    # st.rerun()


def get_balance():
    try:
        res = api_get('/user/balance')
        return res.json().get('balance', 0)
    except Exception:
        st.error('Failed to fetch balance')
        return 0



def balance_tab():
    st.subheader('Wallet')
    balance = get_balance()  
    st.metric('Balance', f'₹{balance}')

    with st.form('add_money_form'):
        amount = st.number_input('Add Balance', min_value=1, step=10)
        submit = st.form_submit_button('Add Money')
        if submit:
            try:
                res = api_put('/user/balance', params={'amount': amount})
                st.success(f"New Balance: ₹{res.json().get('new_balance')}")
                st.rerun()
            except Exception:
                st.error('Update failed')



def load_stations():
    try:
        res = api_get('/metro/stations')
        if res.status_code == 200:
            return [s['name'] for s in res.json().get('stations', [])]
        else:
            st.error("Failed to load stations")
            return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []



def booking_tab():
    stations = load_stations()

    if not stations:
        return

    balance = get_balance()  


    st.write(f"**Balance**: ₹{balance}")

    with st.form('book_form'):
        c1, c2 = st.columns(2)
        with c1:
            src = st.selectbox('Source', stations)
        with c2:
            dst = st.selectbox('Destination', stations)

        submit = st.form_submit_button('Book Ticket')

        if submit:
            if src == dst:
                st.warning('Source and destination must be different!')
            else:
                try:
                    res = api_post('/ticket/book', json={'source': src, 'destination': dst})
                    if res.status_code == 200:
                       
                        st.session_state.ticket_booked = True
                        st.success("Ticket booked successfully!")
                        st.balloons()  
                        print("Ticket booked successfully:", res.json())
                        st.toast("Ticket booked successfully!")
                        time.sleep(2)
                        st.rerun()  
                    else:
                        st.error(res.json().get('detail', 'Booking failed'))
                except Exception:
                    st.error('Booking failed')



def history_tab():
    balance = get_balance()  

   
    st.write(f"**Balance**: ₹{balance}")

    try:
        res = api_get('/tickets')
        tickets = res.json().get('data', [])
        if not tickets:
            st.info('No tickets yet')
        for t in reversed(tickets):
            st.write(f"{t['source']} → {t['destination']} | ₹{t['fare']} | {to_ist(t['timestamp'])}")
    except Exception:
        st.error('Failed to load history')



def stations_tab():
    balance = get_balance()  


    st.write(f"**Balance**: ₹{balance}")

    try:
        res = api_get('/metro/stations')
        for s in res.json().get('stations', []):
            st.write(f"{s['name']} ({s['distance']} km)")
    except Exception:
        st.error('Failed to fetch stations')



# def booking_popup():
#     if st.session_state.ticket_booked:
#         with st.container():  
#             st.markdown("""
#                 <div style="background-color: green; color: white; padding: 15px; border-radius: 5px; margin-top: 20px;">
#                     <h3>Ticket Booked!</h3>
#                     <p>Your ticket has been successfully booked.</p>
#                     <button onclick="window.location.reload()">Close</button>
#                 </div>
#             """, unsafe_allow_html=True)
#             if st.button("Close Pop-up"):
#                 st.session_state.ticket_booked = False  
#                 st.experimental_rerun()  

# In your booking_popup function:
# def booking_popup():
#     if st.session_state.ticket_booked:
#         with st.container():  
#             st.markdown("""
#                 <div style="background-color: green; color: white; padding: 15px; border-radius: 5px; margin-top: 20px;">
#                     <h3>Ticket Booked!</h3>
#                     <p>Your ticket has been successfully booked.</p>
#                     <button onclick="window.location.reload()">Close</button>
#                 </div>
#             """, unsafe_allow_html=True)
#             if st.button("Close Pop-up"):
#                 st.session_state.ticket_booked = False  
#                 st.rerun()  





def booking_popup():
    if st.session_state.ticket_booked:
     
        with st.container():  
            # st.markdown("""
            #     <div style="background-color: green; color: white; padding: 15px; border-radius: 5px; margin-top: 20px;">
            #         <h3>Ticket Booked!</h3>
            #         <p>Your ticket has been successfully booked.</p>
            #     </div>
            # """, unsafe_allow_html=True)
            
        
           
            st.session_state.pop_up_time = time.time()  

           
            if time.time() - st.session_state.pop_up_time >= 7:
                st.session_state.ticket_booked = False  
                st.rerun()  

def handle_ticket_booking():
  
    st.session_state.ticket_booked = True
    st.success("Ticket booked successfully!")
    booking_popup() 

def dashboard_view():
    st.title(f"Welcome, {st.session_state.username}")


    col1, col2 = st.columns([3, 1])

    with col1:
        st.write(f"**Welcome, {st.session_state.username}**")

    with col2:

        balance = get_balance()
        st.write(f"**Total Balance**: ₹{balance}")


    booking_popup()


    t1, t2, t3, t4 = st.tabs(['Balance', 'Book Ticket', 'History', 'Stations'])

    with t1:
        balance_tab()
    with t2:
        booking_tab()
    with t3:
        history_tab()
    with t4:
        stations_tab()


    st.button('Logout', on_click=logout)

# init_state()
# if st.session_state.token:
#     dashboard_view()  
# else:
#      login_view()  

init_state()
if st.session_state.token:
    dashboard_view()
else:
    login_view()
 
