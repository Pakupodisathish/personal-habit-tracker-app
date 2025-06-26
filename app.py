print("DEBUG from habit_component.py: File is being parsed!")
import streamlit as st
import datetime
import pandas as pd
import os 
import authlib# Keep os for potential other path needs, though not strictly needed for this version
# import authlib # Assuming authlib is still needed for your login logic
import habit_component # <--- IMPORTANT: This imports your custom component file
print(f"DEBUG from app.py: Loaded habit_component from: {habit_component.__file__}")
st.title("Personal Habit Tracker")

# App login - Note: st.user.is_logged_in and st.login/logout are often for
# Streamlit Community Cloud or specific integrations. For local dev,
# you might need to adjust or remove this if it's causing issues
# or if it's based on an old Streamlit feature.
# Streamlit has `st.experimental_user` for user info.
# This part of the code might need review if it's not working as expected.
# For now, I'll keep it as is.
if not st.user.is_logged_in:
    if st.button("Login In With Google"):
        st.login()
    st.stop()
if st.button("logout"):
    st.logout()

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
with st.form("new_habit_form",clear_on_submit=True):
    new_habit = st.text_input("Add new habit:")
    add_habit = st.form_submit_button("Add habit")
    if add_habit and new_habit.strip():
        if new_habit not in st.session_state.habits:
            st.session_state.habits.append(new_habit)
            # Ensure the new habit is added to today's status
            st.session_state.habits_status[today][new_habit] = False
            st.success(f"New habit: {new_habit} added successfully")
            st.rerun()
        else:
            st.warning(f"{new_habit} already exists!")

# Delete habit
if st.session_state.habits:
    st.subheader("Delete habit")
    habit_to_delete = st.selectbox("Habit to delete:", st.session_state.habits)
    if st.button("Delete habit"):
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
    # Prepare data for the component
    # The component expects a list of habit names for 'habits'
    # And a list of already completed habit names for 'completed_habits'
    habits_for_component = list(st.session_state.habits) # Ensure it's a list of strings
    completed_habits_for_component = [
        habit for habit, done in st.session_state.habits_status[today].items() if done
    ]
    # Call the component using the imported module
    updated_completed = habit_component.habitCheckList(
        habits_for_component,
        completed_habits_for_component,
        key="habit_checklist_key"
    )

    if st.session_state.pop('just_deleted_a_habit', False):
    # If the flag exists, we do nothing and just remove the flag.
    # This prevents the component's old state from overwriting our correct state.
         pass 
    elif updated_completed is not None and set(completed_habits_for_component) != set(updated_completed):
    # This is a normal click, so we update the state and rerun as usual.
        for habit in st.session_state.habits:
            st.session_state.habits_status[today][habit] = habit in updated_completed
        st.rerun()

    total_completed = sum(st.session_state.habits_status[today][habit] for habit in st.session_state.habits)
    total_habits = len(st.session_state.habits)
    if total_habits > 0: # Avoid division by zero
        st.success(f"Progress: {total_completed}/{total_habits} habits Completed Today! ({total_completed/total_habits*100:.0f}%)")
        st.write("Great, keep going!")
    else:
        st.info("No habits to track progress for.")


# Habit history
st.subheader("Habit Completion History (last 7 Days)")
# Get recent 7 days, excluding future dates relative to today
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
        for day in recent_days: # Iterate through recent_days, not all history
            status = st.session_state.habits_status.get(day, {}).get(habit, False)
            row[day] = "✅" if status else "❌"
        data.append(row)
    df = pd.DataFrame(data)
    st.table(df)
else:
    st.info("No history yet. Start tracking your habits!")