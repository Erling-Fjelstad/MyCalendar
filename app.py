import streamlit as st
from streamlit_calendar import calendar
import db

calendar_options = {
    "editable": True,
    "selectable": True,
    "headerToolbar": {
        "left": "today,prev,next",
        "center": "title",
        "right": "timeGridDay,timeGridWeek",
    },
    "slotMinTime": "06:00:00",
    "slotMaxTime": "18:00:00",
    "initialView": "timeGridWeek",
}

db.init_db()
tasks_list = db.get_tasks_as_objects()

calendar_events = []

for task in tasks_list:
    calendar_events.append(
         {
            "title": task.title,
            "start": task.start,
            "end": task.end,
            "extendedProps": {
                "description": task.description,
                "status": task.status
            },
            "display": "auto",
        },
    )

custom_css="""
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
"""

cal_state = calendar(
    events=calendar_events,
    options=calendar_options,
    custom_css=custom_css,
    key='calendar', # Assign a widget key to prevent state loss
)

if cal_state and "eventClick" in cal_state:
    props = cal_state["eventClick"]["event"]["extendedProps"]
    if props.get("description"): st.write(f"Description: {props['description']}")
    if props.get("status"): st.write(f"Status: {props['status']}")
