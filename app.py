import streamlit as st
import pandas as pd
import plotly.express as px

# Initialize the session state to store task dates and categories if not already done
# Update the session state initialization to include placeholders for notes and users
if 'task_dates' not in st.session_state:
    st.session_state['task_dates'] = {
        # Including empty strings for notes and empty lists for users
        "Prep for Launch Web/Brochure": ("2024-04-01", "2024-04-30", "Bottling Op", "", []),
        "Bldg design": ("2024-04-01", "2024-04-30", "Bottling Op", "", []),
        "Legal/Insurance/Contracts": ("2024-04-01", "2024-04-30", "NLC", "", []),
        "Secure Contract": ("2024-05-01", "2024-05-31", "NLC", "", []),
        "Procure Equipment": ("2024-05-01", "2024-05-31", "Bottling Op", "", []),
        "Production": ("2024-05-01", "2024-05-31", "Bottling Op", "", []),
        "Site Prep": ("2024-06-01", "2024-06-30", "Bottling Op", "", []),
        "Complete 1st Order": ("2024-06-01", "2024-06-30", "Boralis Labs", "", []),
        "Delivery Vehicle": ("2024-07-01", "2024-07-31", "NLC", "", []),
        "Pour Slab": ("2024-07-01", "2024-07-31", "Bottling Op", "", []),
        "Order Bldg": ("2024-07-01", "2024-07-31", "Bottling Op", "", []),
    }


# Function to add or update tasks in the session state with notes and users
def add_or_update_task(task_name, start_date, end_date, category, notes, users, old_task_name=None):
    if old_task_name and old_task_name in st.session_state['task_dates'] and old_task_name != task_name:
        del st.session_state['task_dates'][old_task_name]

    # Convert user input string to list of users
    users_list = [user.strip() for user in users.split(',')] if users else []

    st.session_state['task_dates'][task_name] = (start_date, end_date, category, notes, users_list)


st.title("Project Management")

with st.expander("Add or Edit Task"):
    task_to_edit = st.selectbox("Select a task to edit or add a new task:",
                                [""] + list(st.session_state['task_dates'].keys()))

    # Pre-fill form with selected task's details if editing
    if task_to_edit:
        task_details = st.session_state['task_dates'][task_to_edit]
        default_name, default_start, default_end, default_category, default_notes, default_users = task_to_edit, *task_details
        default_users_str = ', '.join(default_users)  # Convert list of users to string for display
    else:
        default_name, default_start, default_end, default_category, default_notes, default_users_str = "", "2024-01-01", "2024-01-31", "", "", ""

    task_name = st.text_input("Task Name", value=default_name)
    task_start = st.date_input("Start Date", value=pd.to_datetime(default_start))
    task_end = st.date_input("End Date", value=pd.to_datetime(default_end))
    task_category = st.text_input("Category", value=default_category)
    task_notes = st.text_area("Notes", value=default_notes)
    task_users = st.text_input("Assigned Users (comma-separated)", value=default_users_str)

    submit_button = st.button("Save Task")

    if submit_button and task_name and task_category and task_end >= task_start:
        add_or_update_task(task_name, str(task_start), str(task_end), task_category, task_notes, task_users,
                           old_task_name=task_to_edit if task_to_edit else None)
        st.success(f"Task '{task_name}' saved successfully!")

# Generate and display the updated Gantt chart with notes and users in the tooltip
events_data = [
    {
        "Task": task,
        "Start": start,
        "Finish": end,
        "Resource": category,
        "Notes": notes,
        "Users": ', '.join(users)  # Convert the list of users to a string for display
    }
    for task, (start, end, category, notes, users) in st.session_state['task_dates'].items()
]

events_df = pd.DataFrame(events_data)

# Using Plotly Express to generate the Gantt chart, specifying hover data to include notes and users
fig = px.timeline(
    events_df,
    x_start="Start",
    x_end="Finish",
    y="Task",
    color="Resource",
    title="Project Timeline",
    hover_data=["Notes", "Users"]  # Adding notes and users to the hover data
)

events_df = pd.DataFrame(events_data)
# Correctly setting up hover_data to include Notes and Users in the tooltip
fig = px.timeline(
    events_df,
    x_start="Start",
    x_end="Finish",
    y="Task",
    color="Resource",
    title="Project Timeline",
    hover_data={
        "Resource": False,  # Disables the default display of the Resource column in the tooltip
        "Notes": True,  # Enables the display of Notes in the tooltip
        "Users": True,  # Enables the display of Users in the tooltip
    }
)
st.plotly_chart(fig)