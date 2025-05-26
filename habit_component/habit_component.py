import streamlit.components.v1 as components 
import os 


build_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "frontend", "my_app", "build"
))
print("Frontend build path:", build_path)
print("Exists?", os.path.exists(build_path))

habit_tracker = components.declare_component(
    "habit_tracker",
    path=build_path
)

def habitCheckList(habits,completedHabits):
    return habit_tracker(
        args=[habits,completedHabits],
        default=completedHabits,
        key="habit_tracker_app"
    )