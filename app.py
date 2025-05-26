import streamlit as st 
import datetime 
import pandas as pd
from habit_component.habit_component import habitCheckList
import authlib


st.title("Personal Habit Tracker")
#app login  
if not st.user.is_logged_in:
    if st.button("Login In With Google"):
        st.login()
    st.stop()
if st.button("logout"):
    st.logout()

#initialising session state
if "habits" not in st.session_state:
    st.session_state.habits=[]
if "habits_status" not in st.session_state:
    st.session_state.habits_status={}
today=datetime.date.today().isoformat()
if today not in st.session_state.habits_status:
     st.session_state.habits_status[today]={habit:False for habit in st.session_state.habits}

#adding new habit 
st.subheader("add new habit:")
with st.form("new_habit_form"):
    new_habit=st.text_input("add new habit:")
    add_habit=st.form_submit_button("add habit")
    if add_habit and new_habit.strip():
        if new_habit not in st.session_state.habits:
            st.session_state.habits.append(new_habit)
            st.session_state.habits_status[today][new_habit]=False 
            st.success(f"new habit:{new_habit}added successfully")
        else:
            st.warning(f"{new_habit} already exists!")

#delete habit 
if st.session_state.habits:
    st.subheader("delete habit")
    habit_to_delete=st.selectbox("habit to delete:",st.session_state.habits)
    if st.button("delete habit"):
        st.session_state.habits.remove(habit_to_delete)
        for day in st.session_state.habits_status:
           st.session_state.habits_status[day].pop(habit_to_delete,None)
        st.write(f"deleted habit:{habit_to_delete}")

#Daily CheckList(React)
st.subheader(f"Todays habits {today}")
st.write("Current habits:", st.session_state.habits)
if not st.session_state.habits:
    st.info("No habits Yet.Add some above!")
else:
    completed_habits=[habit for habit,done in st.session_state.habits_status[today].items() if done]
    updated_completed=habitCheckList(st.session_state.habits,completed_habits)
    if updated_completed is not None:
        for habit in st.session_state.habits:
           st.session_state.habits_status[today][habit]=habit in updated_completed

    total_completed=sum(st.session_state.habits_status[today][habit]  for habit in st.session_state.habits)
    total_habits=len(st.session_state.habits)
    st.success(f"Progress:{total_completed/total_habits} habits Completed Today!")
    st.write("great keep going!")


#habit history
st.subheader("Habit Completion History (last 7 Days)")
history_days=sorted(st.session_state.habits_status.keys(),reverse=True)
if history_days and st.session_state.habits:
    data=[]
    for habit in st.session_state.habits:
        row={"Habit":habit}
        for day in st.session_state.habits_status:
            status=st.session_state.habits_status[day].get(habit,False)
            row[day]="✅" if status else "❌"
        data.append(row)
    df=pd.DataFrame(data)
    st.table(df)
else:
    st.info("No history yet. Start tracking your habits!")
