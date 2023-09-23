import streamlit as st
from streamlit_calendar import calendar

def read_booking():
    with open("bookings.txt", "r") as my_bookings:
        bookings = my_bookings.read().split("\n\n")[:-1]
    dict_values = [value.split(" ") for value in bookings]
    dict_keys = ["title", "start", "end"]
    all_bookings = []
    for i in dict_values:
        booking = []
        counter = 0
        for j in i:
            if j[:-1] not in dict_keys:
                booking.append((dict_keys[counter], j[:-1]))
                counter += 1
        book_dict = dict(booking)
        all_bookings.append(book_dict)

    return all_bookings


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


calendar = calendar(events=read_booking(), options=calendar_options)
st.write(calendar)


if st.button("Add event"):

  # Get the event details from the user.
    event_title = st.text_input("Your name or band name:")
    event_day = st.date_input("Day to select:")
    event_start = st.time_input("Hour to start:")
    event_end = st.time_input("Hour to end:")

