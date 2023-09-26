import pandas as pd

import streamlit as st
from streamlit_calendar import calendar
from streamlit_gsheets import GSheetsConnection

def read_booking(df):

    all_bookings = []
    for row in df.itertuples():

        book_dict = {
            "title": row.Name,
            "start": row.Start,
            "end":   row.End,
            }
        all_bookings.append(book_dict)

    return all_bookings


# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=60)
def load_data():
    conn = st.experimental_connection("gsheets", type=GSheetsConnection)
    data = conn.read(spreadsheet="Evomusic", worksheet='Bookings')
    return data


def book_slot(slot_title, slot_day, slot_start, slot_end, df):
    slot_book = [
        slot_title,
        f"{slot_day}T{slot_start}",
        f"{slot_day}T{slot_end}"
    ]
    df.loc[len(df)] = slot_book
    st.write(df)
    # csv_url = st.secrets["public_gsheets_url"].replace("/edit#gid=", "/export?format=csv&gid=")
    # st.write(csv_url)
    #df.to_csv(st.secrets["public_gsheets_url"])


calendar_options = {
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "timeGridDay,timeGridWeek",
    },
    "dayHeaderFormat": {
      "weekday": "short",
       "day": "numeric", 
       "month": "numeric", 
       "omitCommas": True,
    },
    "slotMinTime": "06:00:00",
    "slotMaxTime": "21:00:00",
    "initialView": "timeGridWeek",
    "allDaySlot": False,
    "weekends": False,
}


df = load_data()
# for row in df.itertuples():
#     st.write(f"{row.Name} has a :{row.Start}:")

calendar = calendar(events=read_booking(df), options=calendar_options)
st.write(calendar)


# if st.button("Add event"):
with st.form(key="new_book"):
    st.write("Book a slot")

  # Get the event details from the user.
    slot_title = st.text_input("Your name or band name:")
    slot_day = st.date_input("Day to select:")
    slot_start = st.time_input("Hour to start:")
    slot_end = st.time_input("Hour to end:")
    st.write(f"title: {slot_title}")
    st.write(f"day: {slot_day}")
    st.write(f"start: {slot_start}")
    st.write(f"end: {slot_end}")

    booking = st.form_submit_button("Book")

if booking:
    book_slot(slot_title, slot_day, slot_start, slot_end, df)
