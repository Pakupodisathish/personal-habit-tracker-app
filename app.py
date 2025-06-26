import streamlit as st
import datetime
import pandas as pd
import habit_component # Your custom component
from streamlit_oauth import OAuth2Component # <-- Import the new library
import base64
import json

# --- 1. Login Configuration using the new library ---
# This uses st.secrets to securely load your credentials.
CLIENT_ID = st.secrets.auth.client_id
CLIENT_SECRET = st.secrets.auth.client_secret
AUTHORIZE_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
# IMPORTANT: This URI now matches your deployed application.
REDIRECT_URI = "https://personal-habit-tracker-app-krvmn7pnh8jmm4dvabbtge.streamlit.app/"

# Create an OAuth2Component instance
oauth2_component = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_ENDPOINT, TOKEN_ENDPOINT, TOKEN_ENDPOINT, TOKEN_ENDPOINT)

st.title("Personal Habit Tracker")

# --- 2. New Login Check ---
# Check if a token exists in the session state
if 'token' not in st.session_state:
    # If not, show the authorization button
    result = oauth2_component.authorize_button(
        name="Login with Google",
        icon="https://www.google.com/favicon.ico",
        redirect_uri=REDIRECT_URI,
        scope="openid email profile",
        key="google",
        extras_params={"prompt": "consent", "access_type": "offline"},
    )
    # If a result is returned, it means the user has authorized.
    # We store the token in the session state and rerun the app.
    if result:
        st.session_state.token = result.get('token')
        st.rerun()
    st.stop()
else:
    # If a token exists, the user is logged in.
    token_str = st.session_state['token']['id_token']
    # Decode the token to get user info
    try:
        payload = token_str.split('.')[1]
        payload += '=' * (-len(payload) % 4)
        user_info = json.loads(base64.b64decode(payload))
        st.write(f"Welcome, {user_info.get('name', 'User')}!")
    except Exception as e:
        st.write("Welcome, User!")
        print(f"Error decoding token: {e}")

    if st.button("Logout"):
        del st.session_state.token
        st.rerun()

# --- Your Existing App Code (remains the same) ---

# Initialising session state
if "habits" not in st.session_state:
    st.session_state.habits = []
if "habits_status" not in st.session_state:
    st.session_state.habits_status = {}

today = datetime.date.today().isoformat()
if today not in st.session_state.habits_status:
    st.session_state.habits_status[today] = {habit: False for habit in st.session_state.habits}

# Adding new habit
st.subheader("Add new habit:")
with st.form("new_habit_form", clear_on_submit=True):
    new_habit = st.text_input("Add new habit:")
    add_habit = st.form_submit_button("Add habit")
    if add_habit and new_habit.strip():
        if new_habit not in st.session_state.habits:
            st.session_state.habits.append(new_habit)
            st.session_state.habits_status[today][new_habit] = False
            st.success(f"New habit: {new_habit} added successfully")
            st.rerun()
        else:
            st.warning(f"{new_habit} already exists!")

# Delete habit
if st.session_state.habits:
    st.subheader("Delete habit")
    habit_to_delete = st.selectbox("Choose a habit to delete:", st.session_state.habits, key="delete_select")
    if st.button("Delete Habit"):
        st.session_state.habits.remove(habit_to_delete)
        for day in st.session_state.habits_status:
            st.session_state.habits_status[day].pop(habit_to_delete, None)
        st.session_state.just_deleted_a_habit = True
        st.write(f"Deleted habit: {habit_to_delete}")
        st.rerun()

# Daily CheckList (React)
st.subheader(f"Today's habits {today}")
if not st.session_state.habits:
    st.info("No habits Yet. Add some above!")
else:
    habits_for_component = list(st.session_state.habits)
    completed_habits_for_component = [
        habit for habit, done in st.session_state.habits_status[today].items() if done
    ]

    updated_completed = habit_component.habitCheckList(
        habits=habits_for_component,
        completed_habits=completed_habits_for_component,
        key="habit_checklist_key"
    )
    
    if st.session_state.pop('just_deleted_a_habit', False):
        pass
    elif updated_completed is not None and set(completed_habits_for_component) != set(updated_completed):
        for habit in st.session_state.habits:
            st.session_state.habits_status[today][habit] = habit in updated_completed
        st.rerun()

    total_completed = sum(st.session_state.habits_status[today].get(habit, False) for habit in st.session_state.habits)
    total_habits = len(st.session_state.habits)
    if total_habits > 0:
        st.success(f"Progress: {total_completed}/{total_habits} habits Completed Today! ({total_completed/total_habits*100:.0f}%)")
        st.write("Great, keep going!")
    else:
        st.info("No habits to track progress for.")

# Habit history
st.subheader("Habit Completion History (last 7 Days)")
all_days = sorted(st.session_state.habits_status.keys(), reverse=True)
recent_days = []
for day_str in all_days:
    day_date = datetime.date.fromisoformat(day_str)
    if day_date <= datetime.date.today():
        recent_days.append(day_str)
        if len(recent_days) >= 7:
            break

if recent_days and st.session_state.habits:
    data = []
    for habit in st.session_state.habits:
        row = {"Habit": habit}
        for day in recent_days:
            status = st.session_state.habits_status.get(day, {}).get(habit, False)
            row[day] = "✅" if status else "❌"
        data.append(row)
    
    if data:
        df = pd.DataFrame(data)
        st.table(df.set_index("Habit"))
else:
    st.info("No history yet. Start tracking your habits!")