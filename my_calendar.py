import streamlit as st
from streamlit_calendar import calendar
import db

def my_calendar():
    calendar_options = {
        "editable": True,
        "selectable": True,
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "timeGridDay,timeGridWeek",
        },
        "slotMinTime": "06:00:00",
        "slotMaxTime": "18:00:00",
        "initialView": "timeGridWeek",
        "firstDay": 1,
    }

    db.init_db()
    tasks_list = db.get_tasks_as_objects()
    lectures_list = db.get_lectures_as_objects()

    calendar_events = []

    TASK_BG = "#B8E0D2"     
    TASK_BORDER = "#6BBFA5"
    TASK_TEXT = "#103D33"

    LEC_BG = "#C7D3FF"      
    LEC_BORDER = "#7E9BFF"
    LEC_TEXT = "#0F1B3D"

    for task in tasks_list:
        calendar_events.append({
            "title": task.title,
            "allDay": task.all_day,
            "start": task.start.isoformat(),
            "end": task.end.isoformat(),
            "extendedProps": {
                "description": task.description,
                "status": task.status
            },
            "display": "auto",
            "backgroundColor": TASK_BG,
            "borderColor": TASK_BORDER,
            "textColor": TASK_TEXT,
        })

    for lecture in lectures_list:
        calendar_events.append({
            "title": lecture.course,
            "allDay": lecture.all_day,
            "start": lecture.start.isoformat(),
            "end": lecture.end.isoformat(),
            "extendedProps": {
                "description": lecture.description,
            },
            "display": "auto",
            "backgroundColor": LEC_BG,
            "borderColor": LEC_BORDER,
            "textColor": LEC_TEXT,
        })

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
        key='calendar', 
    )

    if cal_state and "eventClick" in cal_state:
        ev = cal_state["eventClick"]["event"]
        title = ev.get("title")
        props = ev.get("extendedProps", {}) or {}

        with st.container(border=True):  
            st.markdown(f"**{title}**")
            if props.get("description"):
                st.write(props["description"])
            if props.get("status"):
                st.write(f"Status: {props['status']}")