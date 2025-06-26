// src/index.js - MINIMALIST VERSION FOR STREAMLITCOMPONENTBASE
import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import HabitCheckList from "./components/HabitCheckList"; // Your root component

// StreamlitComponentBase handles Streamlit.setComponentReady() and Streamlit.events.addEventListener
// automatically when the component mounts. We just need to render the root React component.

const rootElement = document.getElementById('root');

if (rootElement) {
  ReactDOM.render(
    <React.StrictMode>
      <HabitCheckList /> {/* Streamlit automatically injects args as props.args */}
    </React.StrictMode>,
    rootElement
  );
} else {
  console.error("index.js: Root element with ID 'root' not found!");
}