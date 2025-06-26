# Personal Habit Tracker

A modern and interactive habit tracking application built with Python, Streamlit, and a custom React component. This app allows users to add, track, and manage their daily habits with a clean and user-friendly interface.

# Login Page 
![Habit Tracker Screenshot](https://github.com/Pakupodisathish/personal-habit-tracker-app/blob/main/interface_screenshot_1.png?raw=true)

# Add Habit Section 
![Habit Tracker Homepage Without Habits](https://github.com/Pakupodisathish/personal-habit-tracker-app/blob/main/interface_screenshot_2.png?raw=true)

# Without Habits 
![Habit Tracker Hompage Without Habits](https://github.com/Pakupodisathish/personal-habit-tracker-app/blob/main/interface_screenshot_3.png?raw=true)

# HabitCheckList Component After Adding Habits
![Habit Tracker Homepage Habit CheckList](https://github.com/Pakupodisathish/personal-habit-tracker-app/blob/main/interface_screenshot_4.png?raw=true)_

# History Table After Adding Habits
![Habit Tracker Homepage History Table](https://github.com/Pakupodisathish/personal-habit-tracker-app/blob/main/interface_screenshot_5.png?raw=true)

### 🔴 Live Demo

**[Click here to try the live application!](https://personal-habit-tracker-app-krvmn7pnh8jmm4dvabbtge.streamlit.app/)**

---

## Key Features

* **Custom Interactive UI:** A beautiful checklist component built with React for a smooth user experience.
* **Dynamic Habit Management:** Easily add new habits or delete old ones.
* **Daily Progress Tracking:** Instantly see your completion percentage for the day.
* **7-Day History View:** A clear table shows your consistency over the last week.
* **Secure Google Login:** Uses OAuth 2.0 to ensure each user's habit list is private to their session.
* **Responsive Design:** Looks great on both desktop and mobile devices.

---

## Technologies Used

| Category     | Technology                        |
|--------------|-----------------------------------|
| **Backend** | Python, Streamlit                 |
| **Frontend** | React.js, CSS                     |
| **Data** | Pandas                            |
| **Auth** | streamlit-oauth, Google OAuth 2.0 |
| **Deployment**| Streamlit Community Cloud         |

---

## Local Setup and Installation

To run this project on your local machine, please follow these steps:

### Prerequisites

* Python 3.8+
* Node.js and npm

### 1. Clone the Repository

```bash
git clone [https://github.com/Pakupodisathish/personal-habit-tracker-app.git](https://github.com/Pakupodisathish/personal-habit-tracker-app.git)
cd personal-habit-tracker-app
```

### 2. Set Up the Python Environment

It is recommended to use a virtual environment.

```bash
# Create and activate a virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install the required Python libraries
pip install -r requirements.txt
```

### 3. Set Up the React Frontend

You need to build the static frontend files that Streamlit will serve.

```bash
# Navigate to the frontend directory
cd frontend/my_app

# Install npm dependencies
npm install

# Create the production build
npm run build

# Navigate back to the root project directory
cd ../..
```

### 4. Configure Your Credentials

The application uses Google Login, which requires API keys.

1.  Create a folder named `.streamlit` in the root of your project directory.
2.  Inside the `.streamlit` folder, create a file named `secrets.toml`.
3.  Add your Google OAuth credentials to the file in the following format:
    ```toml
    [auth]
    client_id = "YOUR_GOOGLE_CLIENT_ID"
    client_secret = "YOUR_GOOGLE_CLIENT_SECRET"
    ```

### 5. Run the Application

Now you can run the Streamlit app from the root project directory.

```bash
streamlit run app.py
```

The application should now be running locally at `http://localhost:8501`.

---

