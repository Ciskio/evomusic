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


# books = read_booking()

calendar_events = [
    {
        "title": "Francesco",
        "start": "2023-09-18T08:30:00",
        "end": "2023-09-18T10:30:00",
    },
    {
        "title": "Evoband1",
        "start": "2023-09-18T17:30:00",
        "end": "2023-09-18T19:30:00",
    },
]

calendar = calendar(events=read_booking(), options=calendar_options)

# if st.button("Add event"):

  # Get the event details from the user.
#   event_title = st.text_input("Event title:")
#   event_start = st.date_input("Event start:")
#   event_end = st.date_input("Event end:")


st.write(calendar)





# calendar_events = [
    # {
    #     "title": "Event 1",
    #     "start": "2023-09-17T08:30:00",
    #     "end": "2023-09-17T10:30:00",
    #     # "resourceId": "a",
    # },

# ]