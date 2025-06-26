import os
import streamlit.components.v1 as components
import streamlit as st # Added for the __main__ block

# Get the directory of the component's frontend code
# This should point to the directory containing THIS FILE (habit_component.py)
current_file_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate from habit_component.py's location UP to the project root, then DOWN to frontend/my_app/build
# Assumes habit_component.py is directly in the project root
project_root_dir = current_file_dir 
build_dir = os.path.join(project_root_dir, "frontend", "my_app", "build")


# --- Your Debugging Prints (KEEP THESE! They are very helpful for verification) ---
print(f"DEBUG from habit_component.py: current_file_dir = {current_file_dir}")
print(f"DEBUG from habit_component.py: project_root_dir (assuming current_file_dir) = {project_root_dir}")
print(f"DEBUG from habit_component.py: Calculated build_dir: {build_dir}")

if not os.path.exists(build_dir):
    print(f"ERROR from habit_component.py: build_dir DOES NOT EXIST: {build_dir}")
else:
    print(f"DEBUG from habit_component.py: build_dir EXISTS: {build_dir}")
    index_html_path = os.path.join(build_dir, "index.html")
    if not os.path.exists(index_html_path):
        print(f"ERROR from habit_component.py: index.html NOT FOUND in build_dir: {index_html_path}")
    else:
        print(f"DEBUG from habit_component.py: index.html found in build_dir: {index_html_path}")
# ----------------------------------------------------------------------------------

# Set to True if the component is being run as a release build (e.g., after npm run build).
# Set to False if the component is being run in development mode (e.g., after npm start).
_RELEASE = True # <--- ENSURE THIS IS TRUE FOR DEPLOYMENT/RELEASE BUILD

if _RELEASE:
    _component_func = components.declare_component(
        "my_habit_checklist", # Use a consistent name
        path=build_dir
    )
else:
    _component_func = components.declare_component(
        "my_app", # Use a consistent name
        url="http://localhost:3000", # Common React dev server port, adjust if yours is 3001
    )

# Wrapper function for your component
def habitCheckList(habits, completed_habits, key=None):
    """Create a new instance of "my_habit_checklist".

    Parameters
    ----------
    habits: list
        A list of habit names (strings).
    completed_habits: list
        A list of habit names (strings) that are currently completed.
    key: str or None
        An optional key that uniquely identifies this component.

    Returns
    -------
    list
        The updated list of completed habits returned from the frontend.
    """
    # Debug print for arguments passed to component
    print(f"DEBUG from habit_component.py: Arguments passed to component: habits={habits}, completed_habits={completed_habits}")

    component_value = _component_func(
        habits=habits,
        completed_habits=completed_habits,
        key=key,
        default=[] # Default should be an empty list if your component returns a list of completed habits
    )
    return component_value

# --- Optional: Add a test block to run habit_component.py directly for debugging ---
if __name__ == "__main__":
    st.subheader("Test from habit_component.py directly")
    test_habits = ["Go for a walk", "Drink water", "Read a book"]
    test_completed = ["Drink water"]

    st.write("Initial Habits:", test_habits)
    st.write("Initial Completed:", test_completed)

    # Call the component
    updated_completed_habits = habitCheckList(test_habits, test_completed, key="test_component")

    st.write("Component returned:", updated_completed_habits)
    if updated_completed_habits is not None:
        st.write("Updated completed habits:", updated_completed_habits)
    else:
        st.write("Component returned None (no interaction yet).")