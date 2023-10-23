import streamlit as st
import ephem
import datetime
import os
import base64

def calculate_closest_planet(date, time=None):
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
            font-size: 35px;
            text-align: center;
        }
        </style>
    """

    return f'{style} <div class="custom-title">{title_text}</div>'

# Include the Google Fonts link
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Saira Condensed&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logo_path = f"{BASE_DIR}/img/logo_url_wide.png"

st.image(logo_path, use_column_width=True)

container = st.container()

right_now = st.toggle('Today')

if not right_now:
    query = st.date_input(":calendar: Date", None, min_value=datetime.date(1900, 1, 1), max_value=datetime.date(2100, 12, 31))

if st.button("Calculate"):
    if right_now:
        query = datetime.date.today()
        closest_planet = calculate_closest_planet(query)
        verb_tense = "is"
        # transform date to chosen format 
        date_formatted = query.strftime("%B %-d, %Y")  # Format date as "Month day, year"
        # display information
        container.markdown(
            custom_style(f"The closest planet to Earth <br> on {date_formatted} {verb_tense}"),
            unsafe_allow_html=True
            )
        container.image(f"{BASE_DIR}/img/{str.lower(closest_planet)}_wide.png", use_column_width=True)
        container.markdown(custom_style(f"<b>{closest_planet}</b>!"), unsafe_allow_html=True)
    else:
        if query:
            # determine closest planet
            closest_planet = calculate_closest_planet(query)
            
            # define verb tense 
            if query < datetime.date.today():
                verb_tense = "was"
            elif query == datetime.date.today():
                verb_tense = "is"
            else:
                verb_tense = "will be"

            # transform date to chosen format 
            date_formatted = query.strftime("%B %-d, %Y")  # Format date as "Month day, year"

            # display information
            container.markdown(
                custom_style(f"The closest planet to Earth <br> on {date_formatted} {verb_tense}"),
                unsafe_allow_html=True
                )
            container.image(f"{BASE_DIR}/img/{str.lower(closest_planet)}_wide.png", use_column_width=True)
            container.markdown(custom_style(f"<b>{closest_planet}</b>!"), unsafe_allow_html=True)
        else:
            container.error("Please select a date.")


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background(f"{BASE_DIR}/img/bg.png")