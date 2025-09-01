import streamlit as st

from my_calendar import my_calendar
from add_events import add_events


st.title("My Calendar")

my_calendar()

add_event = st.toggle(
    label="Add event?",
    value=False,
    key="add_event"
)

if add_event:
    add_events()