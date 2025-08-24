import time

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
    tasks_list = db.get_tasks()
    lectures_list = db.get_lectures()

    calendar_events = []

    TASK_BG = "#B8E0D2"     
    TASK_BORDER = "#6BBFA5"
    TASK_TEXT = "#103D33"

    LEC_BG = "#C7D3FF"      
    LEC_BORDER = "#7E9BFF"
    LEC_TEXT = "#0F1B3D"

    for task in tasks_list:
        calendar_events.append({
            "title": task.get("title"),
            "allDay": bool(task.get("all_day")),
            "start": task.get("start"),
            "end": task.get("end"),
            "extendedProps": {
                "id": task.get("id"),
                "description": task.get("description"),
                "status": task.get("status"),
                "type": "task"
            },
            "display": "auto",
            "backgroundColor": TASK_BG,
            "borderColor": TASK_BORDER,
            "textColor": TASK_TEXT,
        })

    for lecture in lectures_list:
        calendar_events.append({
            "title": lecture.get("course"),
            "allDay": bool(lecture.get("all_day")),
            "start": lecture.get("start"),
            "end": lecture.get("end"),
            "extendedProps": {
                "id": lecture.get("id"),
                "description": lecture.get("description"),
                "type": "lecture"
            },
            "display": "auto",
            "backgroundColor": LEC_BG,
            "borderColor": LEC_BORDER,
            "textColor": LEC_TEXT,
        })

    custom_css = """
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
        key="calendar", 
    )

    if cal_state and "eventClick" in cal_state:
        ev = cal_state["eventClick"]["event"]
        title = ev.get("title")
        props = ev.get("extendedProps", {}) or {}
        event_id_raw = props.get("id")
        event_id = int(event_id_raw) if event_id_raw is not None else None

        with st.container(border=True):  
            st.markdown(f"**{title}**")

            if props.get("description"):
                st.write(props.get("description"))

            if props.get("status"):
                st.write(f"Status: {props.get('status')}")

            if st.button(label="DELETE", type="primary"):
                if event_id is None:
                    st.error("Delete failed (missing id)")
                    return
                
                if props.get("type") == "task":
                    db.delete_task(task_id=event_id)
                    st.success("Task deleted")
                    time.sleep(1)
                    st.rerun()
                elif props.get("type") == "lecture":
                    db.delete_lecture(lecture_id=event_id)
                    st.success("Lecture deleted")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Delete failed")