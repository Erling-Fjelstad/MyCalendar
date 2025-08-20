import streamlit as st
from streamlit_calendar import calendar

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

calendar_events = [
    {
        "title": "Event 1",
        "start": "2025-08-21T08:30:00",
        "end": "2025-08-21T10:30:00",
    },
]

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


