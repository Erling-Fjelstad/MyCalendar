import datetime
import time

import streamlit as st

import db

def update_event(
    event: dict
):
    props = event.get("extendedProps", {}) or {}

    event_title = event.get("title")
    title = st.text_input(
        label="Update title:",
        value=event_title
    )

    event_description = props.get("description")
    description = st.text_input(
        label="Update description:",
        value=event_description
    )

    event_date = datetime.datetime.fromisoformat(event.get("start")).date()
    date = st.date_input(
        label="Update date",
        value=event_date
    )

    event_all_day = event.get("allDay")
    all_day = st.toggle(
        label="All day?",
        value=event_all_day,
        key="all_day_update"
    )

    if not all_day:
        raw_start = event.get("start")
        if isinstance(raw_start, str):
            start_dt = datetime.datetime.fromisoformat(raw_start.replace("Z", "+00:00"))
        else:
            start_dt = raw_start  

        raw_end = event.get("end")
        if raw_end is None:
            end_dt = start_dt + datetime.timedelta(hours=1)  
        elif isinstance(raw_end, str):
            end_dt = datetime.datetime.fromisoformat(raw_end.replace("Z", "+00:00"))
        else:
            end_dt = raw_end

        start = st.time_input(
            label="Update start time:",
            value=start_dt.time()
        )

        end   = st.time_input(
            label="Update end time:",
            value=end_dt.time()
        )

    if all_day:
        start_dt = datetime.datetime.combine(date, datetime.time(0, 0, 0)).isoformat()
        end_dt = datetime.datetime.combine(date, datetime.time(23, 59, 59)).isoformat()

    else:
        start_dt = datetime.datetime.combine(date, start).isoformat()
        end_dt = datetime.datetime.combine(date, end).isoformat()

        if end_dt <= start_dt:
            st.error("End time must be after start time")
            return

    if props.get("type") == "task":
        event_status = props.get("status")
        index_by_status = {"Todo": 0, "In progress": 1, "Done": 2}

        status = st.selectbox(
            label="Status",
            options=["Todo", "In progress", "Done"],
            index=index_by_status.get(event_status, 0),
            key="status_update"
        )
    
    event_id = props.get("id")

    if st.button(label="UPDATE", type="primary"):
        if props.get("type") == "task":
            db.update_task(
                task_id=event_id,
                title=title,
                description=description,
                all_day=all_day,
                start=start_dt,
                end=end_dt,
                status=status
            )
            st.success("Task updated")
            time.sleep(1)
            st.rerun()
        
        elif props.get("type") == "lecture":
            db.update_lecture(
                lecture_id=event_id,
                course=title,
                description=description,
                all_day=all_day,
                start=start_dt,
                end=end_dt
            )
            st.success("Lecture updated")
            time.sleep(1)
            st.rerun()
        
        elif props.get("type") == "exercise":
            db.update_exercise(
                exercise_id=event_id,
                course=title,
                description=description,
                all_day=all_day,
                start=start_dt,
                end=end_dt
            )
            st.success("Exercise updated")
            time.sleep(1)
            st.rerun()
        
        else:
            st.error("Cannot update event")