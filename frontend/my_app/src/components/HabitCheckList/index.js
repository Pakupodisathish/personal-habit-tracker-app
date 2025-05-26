import { Component } from "react";
import "./index.css";
import { withStreamlitConnection } from "streamlit-component-lib";

class HabitCheckList extends Component {
  constructor(props) {
    super(props);
    const habits = props.args?.[0] || [];
    const completed_habits = props.args?.[1] || [];
    const checked = {};
    habits.forEach(habit => {
      checked[habit] = completed_habits.includes(habit);
    });
    this.state = { checked };
  }

  componentDidUpdate(prevProps) {
    const habits = this.props.args?.[0] || [];
    const completed_habits = this.props.args?.[1] || [];
    const prevHabits = prevProps.args?.[0] || [];
    const prevCompleted = prevProps.args?.[1] || [];
    if (
      JSON.stringify(prevHabits) !== JSON.stringify(habits) ||
      JSON.stringify(prevCompleted) !== JSON.stringify(completed_habits)
    ) {
      const checked = {};
      habits.forEach(habit => {
        checked[habit] = completed_habits.includes(habit);
      });
      this.setState({ checked });
    }
  }

  checkedHabit = (habit) => {
    this.setState(
      prevState => ({
        checked: { ...prevState.checked, [habit]: !prevState.checked[habit] }
      }),
      () => {
        // Send updated data back to Streamlit
        if (window.Streamlit) {
          const completed = Object.keys(this.state.checked).filter(
            habit => this.state.checked[habit]
          );
          window.Streamlit.setComponentValue(completed);
        }
      }
    );
  };

  render() {
    const habits = this.props.args?.[0] || [];
    const { checked } = this.state;
    return (
      <div className="checklist-container">
        <h1 className="checklist-heading">Today's Habit Checklist</h1>
        {habits.length === 0 ? (
          <p className="no-habits-text">No habits yet. Add some habits!</p>
        ) : (
          <ul className="habits-checklist-container">
            {habits.map(habit => (
              <li key={habit}>
                <input
                  id={habit}
                  type="checkbox"
                  checked={checked[habit] || false}
                  onChange={() => this.checkedHabit(habit)}
                  className="checkbox-input"
                />
                <label className="habit-name" htmlFor={habit}>
                  {habit}
                </label>
              </li>
            ))}
          </ul>
        )}
      </div>
    );
  }
}

export default withStreamlitConnection(HabitCheckList);
