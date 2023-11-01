import streamlit as st
import ephem
import datetime
import os
import base64
import streamlit_analytics
from dotenv import load_dotenv

#### Configuration
st.set_page_config(
   page_title="Closest",
   page_icon="🌌"
   )

# Do not display header
hide_header = """
            <style>
            header {visibility: hidden;}
            </style>
"""

# Do not display footer
hide_footer = """
            <style>
            footer {visibility: hidden;}
            </style>
"""

st.markdown(hide_header, unsafe_allow_html=True)
st.markdown(hide_footer, unsafe_allow_html=True) 

#### Configuration functions

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
    background-repeat: no-repeat;
    background-position: center center;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

def custom_style(title_text):
    style = """
        <style>
        .custom-title {
            font-family: 'Saira Condensed', sans-serif;
            font-size: 30px;
            text-align: center;
        }
        </style>
    """

    return f'{style} <div class="custom-title">{title_text}</div>'

# Include the Google Fonts link for custom_style
st.markdown("""
    <link href="https://fonts.bunny.net/css?family=Saira Condensed&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

#### Calculation functions
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

#### APP
load_dotenv()
weather = os.getenv("WEATHER")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logo_path = f"{BASE_DIR}/img/logo_url_corner_wide.png"

st.image(logo_path, use_column_width=True)

container = st.container()

today = st.checkbox('Today')

if not today:
    query = st.date_input(":calendar: Date", None, min_value=datetime.date(1900, 1, 1), max_value=datetime.date(2100, 12, 31))

streamlit_analytics.start_tracking()

if st.button("Calculate", type="primary"):
    if today:
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
        container.image(f"{BASE_DIR}/img/{str.lower(closest_planet)}_wide_opaque.png", use_column_width=True)
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
            container.image(f"{BASE_DIR}/img/{str.lower(closest_planet)}_wide_opaque.png", use_column_width=True)
            container.markdown(custom_style(f"<b>{closest_planet}</b>!"), unsafe_allow_html=True)
        else:
            container.error("Please select a date.")

simple_bg = st.toggle('Simple background')

if simple_bg:
    st.markdown("""<style>
                .stApp {
                background-image: linear-gradient(180deg, #020e40, #0e1118ff, #0e1118ff, #0e1118ff, #0e1118ff, #0e1118ff, #0e1118ff, #0e1118ff, #891c5f);
                }
                </style>""", unsafe_allow_html=True
                )
else: 
    set_background(f"{BASE_DIR}/img/bg.jpeg")

streamlit_analytics.stop_tracking(unsafe_password=weather)

st.markdown("<span style='color: #891c5f;'><strong>Author: <br> <a href='https://github.com/jlnetosci' style='color: #891c5f;'>João L. Neto</a> <br> <a href='mailto:closest.app.contact@gmail.com' style='color: #891c5f;'>Contact Me</a></strong></span>", unsafe_allow_html=True)
