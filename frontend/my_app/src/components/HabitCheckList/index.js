import React from 'react';
import "./index.css";
import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib";

// This is the traditional class-based component.
class HabitCheckList extends StreamlitComponentBase {
  // The constructor initializes the component's state based on the props received from Streamlit.
  constructor(props) {
    super(props);
    // We get the data from 'this.props.args'
    const args = this.props.args || {};
    const habits = args.habits || [];
    const completed_habits = args.completed_habits || [];
    // 'this.state' holds the data that can change over time, like which habits are checked.
    const checked = {};
    habits.forEach(habit => {
      checked[habit] = completed_habits.includes(habit);
    });
    this.state = { checked };
  }
  
  // componentDidMount is a lifecycle method that runs once after the component first renders.
  // We use it here to set the initial height of the iframe in Streamlit.
  componentDidMount() {
    Streamlit.setFrameHeight();
  }

  // componentDidUpdate runs whenever the component's props or state change.
  // We use it to sync the component if the list of habits from Python changes.
  componentDidUpdate(prevProps) {
    const prevHabits = prevProps.args.habits || [];
    const currentHabits = this.props.args.habits || [];

    if (JSON.stringify(prevHabits) !== JSON.stringify(currentHabits)) {
      const completed_habits = this.props.args.completed_habits || [];
      const checked = {};
      currentHabits.forEach(habit => {
        checked[habit] = completed_habits.includes(habit);
      });
      // We update the state and then adjust the iframe height.
      this.setState({ checked }, () => Streamlit.setFrameHeight());
    }
  }

  // This is a class method to handle toggling a habit's checked status.
  checkedHabit = (habit) => {
    // 'this.setState' is used to update the component's state.
    this.setState(
      prevState => ({
        checked: { ...prevState.checked, [habit]: !prevState.checked[habit] }
      }),
      // After the state has been updated, this callback function runs.
      () => {
        // We calculate the new list of completed habits...
        const completed = Object.keys(this.state.checked).filter(
          h => this.state.checked[h]
        );
        // ...and send it back to our Python script.
        Streamlit.setComponentValue(completed);
      }
    );
  };

  // The render method describes what the UI should look like.
  render() {
    // We get the data we need from 'this.props' and 'this.state'.
    const { habits } = this.props.args;
    const { checked } = this.state;

    if (!habits) {
      return <p>Loading habits...</p>;
    }

    return (
      <div className="checklist-container">
        <h1 className="checklist-heading">Today's Habit Checklist</h1>
        {habits.length === 0 ? (
          <p className="no-habits-text">No habits yet. Add some habits!</p>
        ) : (
          <ul className="habits-checklist-container">
            {habits.map(habit => (
              <li key={habit} onClick={() => this.checkedHabit(habit)}>
                <input
                  id={habit}
                  type="checkbox"
                  checked={checked[habit] || false}
                  readOnly
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
// We still wrap the component to connect it to Streamlit.
export default withStreamlitConnection(HabitCheckList);