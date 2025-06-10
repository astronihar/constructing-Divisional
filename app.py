# app.py

from flask import Flask, render_template, session
from flask_session import Session
import requests
from logic.divisionalLogic import (
    get_absolute_degree, get_d1_chart, get_d3_chart, 
    get_d6_chart, get_d9_chart, get_d30_chart, get_d60_chart
)

app = Flask(__name__)
app.secret_key = 'astrosecret'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Define a safe zodiac list for lookup
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

def zodiac_index(zodiac_name):
    """Safe index fetch with fallback."""
    try:
        return ZODIAC_SIGNS.index(zodiac_name)
    except ValueError:
        raise Exception(f"Invalid zodiac sign: {zodiac_name}")

def prepare_planets_raw(planets_data):
    """Convert planets from structured API data into absolute degrees."""
    result = {}
    for planet, val in planets_data.items():
        sign_index = zodiac_index(val['zodiac'])
        degree = val['degree']
        result[planet] = get_absolute_degree(sign_index, degree)
    return result

@app.route('/')
def home():
    return '✅ Visit <a href="/charts">/charts</a> to view divisional charts.'

@app.route('/charts')
def show_charts():
    url = "http://127.0.0.1:5001/api/astronihar/d1"
    try:
        res = requests.get(url)
        data = res.json()
    except Exception as e:
        return f"⚠️ Error fetching API data: {e}"

    # Process Ascendant
    asc_data = data.get('ascendant', {})
    asc_sign_index = zodiac_index(asc_data.get('zodiac', ''))
    asc_deg = get_absolute_degree(asc_sign_index, asc_data.get('degree', 0))

    # Process Planets
    planets_raw = prepare_planets_raw(data.get('planets', {}))

    # Store in session (if needed later)
    session['asc_deg'] = asc_deg
    session['planets_raw'] = planets_raw

    # Get all charts
    d1 = get_d1_chart(planets_raw, asc_deg)
    d3 = get_d3_chart(planets_raw, asc_deg)
    d6 = get_d6_chart(planets_raw, asc_deg)
    d9 = get_d9_chart(planets_raw, asc_deg)
    d30 = get_d30_chart(planets_raw, asc_deg)
    d60 = get_d60_chart(planets_raw, asc_deg)

    return render_template(
        'partials/horoscope_charts.html',
        d1=d1, d3=d3, d6=d6, d9=d9, d30=d30, d60=d60
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)
