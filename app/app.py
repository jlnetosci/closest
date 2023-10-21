import streamlit as st
import ephem
import datetime
#import time as t
import os

def calculate_closest_planet(date, time):
    if time is not None:
        target_date_time = ephem.localtime(ephem.Date(f"{date} {time}"))
    else:
        target_date_time = ephem.localtime(ephem.Date(f"{date}"))

    planets = {
        'Mercury': ephem.Mercury(),
        'Venus': ephem.Venus(),
        'Mars': ephem.Mars(),
        #'Jupiter': ephem.Jupiter(),
        #'Saturn': ephem.Saturn(),
        #'Uranus': ephem.Uranus(),
        #'Neptune': ephem.Neptune()
    }

    closest_distance = float('inf')
    closest_planet = None

    for planet_name, planet in planets.items():
        planet.compute(target_date_time)
        distance = planet.earth_distance
        if distance < closest_distance:
            closest_distance = distance
            closest_planet = planet_name

    return closest_planet

def custom_style(title_text):
    style = """
        <style>
        .custom-title {
            font-family: 'Saira Condensed', sans-serif;
            font-size: 40px;
            text-align: center;
        }
        </style>
    """

    return f'{style} <div class="custom-title">{title_text}</div>'

## Include the Google Fonts link
#st.markdown("""
#    <link href="https://fonts.googleapis.com/css2?family=Saira Condensed&display=swap" rel="stylesheet">
#    """, unsafe_allow_html=True)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
logo_path = f"{BASE_DIR}/img/logo.png"

st.sidebar.image(logo_path, use_column_width=True)
st.sidebar.header("Select Date and Time")
right_now = st.sidebar.toggle('Now')

# Initialize the 'on' variable with a default value
on = False

# Define current_date and current_time here
current_date = datetime.date.today()
current_datetime = datetime.datetime.now()  # Current date and time
current_date_time = current_datetime.replace(second=0, microsecond=0)  # Round to the minute

col1, col2, col3 = st.columns([1,4,1])

if not right_now:
    date = st.sidebar.date_input(":calendar: Date", None, min_value=datetime.date(1900, 1, 1), max_value=datetime.date(2100, 12, 31))
    on = st.sidebar.checkbox('Select time')

    if on:
        time = st.sidebar.time_input(":mantelpiece_clock: Time", None, step=60)
    else:
        time = None
with col2:
    if st.sidebar.button("Calculate"):
        if right_now:
            date = current_date
            time = current_datetime.strftime("%H:%M")
            verb_tense = "is"
            closest_planet = calculate_closest_planet(date, time)
            date_formatted = date.strftime("%B %d, %Y")  # Format date as "April 22, 1987"
            st.markdown(
                custom_style(f"The closest planet to Earth on <br> {date_formatted} at {time} {verb_tense}"),
                unsafe_allow_html=True
            )

            st.image(f"{BASE_DIR}/img/{str.lower(closest_planet)}.png", use_column_width=True)
    #        st.markdown(
    #            custom_style(f'<img src="{BASE_DIR}/img/{str.lower(closest_planet)}.png" width="500">', center_image=False),
    #            unsafe_allow_html=True
    #        )

            st.markdown(custom_style(f"<b>{closest_planet}</b>!"), unsafe_allow_html=True)
        else:        
            if date:
                if on:
                    if time is not None:
                        selected_date_time = datetime.datetime.combine(date, time)
                        if selected_date_time < current_date_time:
                            verb_tense = "was"
                        elif selected_date_time == current_date_time:
                            verb_tense = "is"
                        else:
                            verb_tense = "will be"
                        closest_planet = calculate_closest_planet(date, time)
                        date_formatted = date.strftime("%B %d, %Y")  # Format date as "April 22, 1987"
                        time_formatted = time.strftime("%H:%M")  # Format time as HH:MM
                        #with st.spinner(Calculating...'):
                        #    t.sleep(1)
                        st.markdown(
                            custom_style(f"The closest planet to Earth on {date_formatted} at {time_formatted} {verb_tense}"),
                            unsafe_allow_html=True
                        )
                        st.image(f"{BASE_DIR}/img/{str.lower(closest_planet)}.png", use_column_width=True)
                        st.markdown(custom_style(f"<b>{closest_planet}</b>!"), unsafe_allow_html=True)
                    else:
                        st.error("Please select a time.")
                elif not on:
                    if date < current_date:
                        verb_tense = "was"
                    elif date == current_date:
                        verb_tense = "is"
                    else:
                        verb_tense = "will be"
                    closest_planet = calculate_closest_planet(date, time)
                    date_formatted = date.strftime("%B %d, %Y")  # Format date as "April 22, 1987"
                    #with st.spinner('Calculating...'):
                    #    t.sleep(1)
                    st.markdown(
                        custom_style(f"The closest planet to Earth on {date_formatted} {verb_tense}"),
                        unsafe_allow_html=True
                    )
                    st.image(f"{BASE_DIR}/img/{str.lower(closest_planet)}.png", use_column_width=True)
                    st.markdown(custom_style(f"<b>{closest_planet}</b>!"), unsafe_allow_html=True)
            else:
                st.error("Please select a date.")
