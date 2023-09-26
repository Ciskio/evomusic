import pandas as pd
import datetime
import numpy as np

import streamlit as st
from streamlit_calendar import calendar
from streamlit_gsheets import GSheetsConnection



# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=60)
def load_data():
    conn = st.experimental_connection("gsheets", type=GSheetsConnection)
    data = conn.read(worksheet="Bookings")
    names = data["Name"].dropna().to_list()
    starts = data["Start"].dropna().to_list()
    ends = data["End"].dropna().to_list()
    values = {"Name": names, "Start": starts, "End": ends}
    df = pd.DataFrame(values)
    return df, conn

def clean_db_old(df):
    now = np.datetime64('now')
    df["End"] = pd.to_datetime(df["End"])
    new_df = df[~(df['End'] > now)]
    return new_df

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


def book_slot(slot_title, slot_day, slot_start, slot_end, df, conn):
    slot_book = [
        slot_title,
        f"{slot_day}T{slot_start}",
        f"{slot_day}T{slot_end}"
    ]
    df.loc[len(df)] = slot_book
    st.write(df)
    conn.update(worksheet="Bookings", data=df)
    st.cache_data.clear()
    st.experimental_rerun()


def check_past(input_day):
    """Check if today is > than the input day

    :param input_day: day to test
    :return: True if the tested day is in the past, False otherwise
    """
    # passed_day = datetime.datetime.strptime(f"{input_day[:4]}-{input_day[5:7]}-{input_day[8:]}", "%Y/%m/%d").date()
    today = datetime.date.today()
    if today > input_day:
        return True
    return False

def check_overlap(first_inter,second_inter):
    for f,s in ((first_inter,second_inter), (second_inter,first_inter)):
        #will check both ways
        for time in (f["starting_time"], f["ending_time"]):
            if s["starting_time"] < time < s["ending_time"]:
                return True
    else:
        return False

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


df, conn = load_data()
calendar = calendar(events=read_booking(df), options=calendar_options)

st.write(calendar)


with st.form(key="new_book"):
    st.write("Book a slot")

  # Get the event details from the user.
    slot_title = st.text_input("Your name or band name:")
    slot_day = st.date_input("Day to select:")
    slot_start = st.time_input("Hour to start:")
    slot_end = st.time_input("Hour to end:")

    booking = st.form_submit_button("Book")

if booking:
    booking_in_the_past = check_past(slot_day)

    # TODO check that there are no overlapping bookings
    # TODO automatically remove old bookings
    if not booking_in_the_past:
        # df = clean_db_old(df)
        book_slot(slot_title, slot_day, slot_start, slot_end, df, conn)
        

    else:
        st.write("You can't book in the past")