import datetime
import time

import streamlit as st

import db
from task import Task
from lecture import Lecture


def add_object(
    event: str | None,
    title: str,
    description: str,
    date: datetime.date,
    all_day: bool,
    repeat_weekly: bool,
    repeat_weeks: int = 1,
    start: datetime.time | None = None,
    end: datetime.time | None = None,
    status: str = "Todo"
):
    if not event or not title or not description or not date:
        st.error("You have not filled out the required fields")
        return

    if all_day:
        start_dt = datetime.datetime.combine(date, datetime.time(0, 0, 0))
        end_dt = datetime.datetime.combine(date, datetime.time(23, 59, 59))

    else:
        if not start or not end:
            st.error("Please select start and end time")
            return
        
        start_dt = datetime.datetime.combine(date, start)
        end_dt = datetime.datetime.combine(date, end)

        if end_dt <= start_dt:
            st.error("End time must be after start time")
            return

    if event == "Task":
        if repeat_weekly:
            for i in range(int(repeat_weeks)):
                delta = datetime.timedelta(weeks=i)
                task = Task(
                    title=title.strip(),
                    description=description.strip(),
                    all_day=all_day,
                    start=start_dt + delta,
                    end=end_dt + delta,
                    status=status
                )
                db.insert_task(task)

            st.success(f"Task added (weekly x {int(repeat_weeks)})")
            time.sleep(1)
            st.rerun()

        else:
            task = Task(
                title=title.strip(),
                description=description.strip(),
                all_day=all_day,
                start=start_dt,
                end=end_dt,
                status=status
            )
            db.insert_task(task)
            st.success("Task added")
            time.sleep(1)
            st.rerun()

    elif event == "Lecture":
        if repeat_weekly:
            for i in range(int(repeat_weeks)):
                delta = datetime.timedelta(weeks=i)
                lecture = Lecture(     
                    course=title.strip(),
                    description=description.strip(),
                    all_day=all_day,
                    start=start_dt + delta,
                    end=end_dt + delta
                )
                db.insert_lecture(lecture)

            st.success(f"Lecture added (weekly x {int(repeat_weeks)})")
            time.sleep(1)
            st.rerun()

        else:
            lecture = Lecture(     
                course=title.strip(),
                description=description.strip(),
                all_day=all_day,
                start=start_dt,
                end=end_dt
            )
            db.insert_lecture(lecture)
            st.success("Lecture added")
            time.sleep(1)
            st.rerun()

    else:
        st.error("Unknown event type")

def add_events():
    event = st.selectbox(
        label="Event:",
        options=["Task", "Lecture"],
        index=None,
        placeholder="Select event type"
    )

    event_title = st.text_input(
        label="Title:", 
        placeholder="Title for this event"
    )

    event_description = st.text_input(
        label="Description:", 
        placeholder="Describe this event"
    )

    event_date = st.date_input(
        label="Select the date for the event",
        value=datetime.date.today(),
        min_value=datetime.date.today()
    )

    event_all_day = st.toggle(
        label="All day?", 
        value=False,
        key="all_day_add"
    )

    if not event_all_day:
        event_start = st.time_input(
            label="Start time:",
            value=datetime.time(9, 0)
        )
    
        event_end = st.time_input(
            label="End time:",
            value=datetime.time(12, 0)
        )

    event_status = None
    if event == "Task":
        event_status = st.selectbox(
            label="Status",
            options=["Todo", "In progress", "Done"],
            index=0,
            key="status_add"
        )
    
    repeat_weekly = st.toggle(
        label="Repeat weekly?", 
        value=False,
        key="repeat_weekly_add"
    )

    repeat_weeks = 1
    if repeat_weekly:
        repeat_weeks = st.number_input(
            label="Number of weeks:",
            value=10,
            min_value=2,
            step=1
        )

    if st.button(label="ADD", type="primary"):
        add_object(
            event=event,
            title=event_title,
            description=event_description,
            date=event_date,
            all_day=event_all_day,
            start=None if event_all_day else event_start,
            end=None if event_all_day else event_end,
            status=event_status,
            repeat_weekly=repeat_weekly,
            repeat_weeks=repeat_weeks
        )