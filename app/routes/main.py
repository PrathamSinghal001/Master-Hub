from flask import Blueprint, render_template, session, url_for, Response, redirect, flash, request
from app import db
from app.models import User 
import requests
import google.generativeai as genai
from PIL import Image
from io import BytesIO 
import base64
import os
import clients


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')


# 1. Weather App
@main_bp.route('/weather', methods=['GET', 'POST'])
def weather():
    # Check if user is logged in
    if "user_id" not in session:
        flash("You must be logged in to access this app.", "Danger")
        return redirect(url_for("auth.login"))

    temperature = None
    wind_speed = None
    lat= None
    lon = None

    # Handle form submission
    if request.method == "POST":
        lat = request.form.get('lat')
        lon = request.form.get('lon')

        # Only call API if both latitude and longitude are provided
        if lat and lon:
            try:
                lat = float(lat)
                lon = float(lon)
            except ValueError:
                flash("Please enter valid numbers for latitude and longitude.", "Danger")
                return render_template("weather.html")

            # Fetch weather data from Open-Meteo
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m"
            # url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                if 'current' in data:
                    temperature = f"{data['current']['temperature_2m']} °C"
                    wind_speed = f"{data['current']['wind_speed_10m']} m/s"
                else:
                    flash("Weather data is not available for the given coordinates.", "Warning")
            else:
                flash(f"Failed to retrieve data: {response.status_code}", "Danger")

    return render_template("weather.html", temperature=temperature, wind_speed=wind_speed, lat=lat, lon=lon)


# 2. Crypto App
@main_bp.route('/crypto', methods=['GET', 'POST'])
def crypto():
    if "user_id" not in session:
        flash("You must be logged in to access this app.", "Danger")
        return redirect(url_for("auth.login"))

    API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    API_KEY = os.getenv('COINMARKETCAP_API_KEY')

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY
    }

    if request.method == 'POST':
        symbol = request.form.get('symbol', '').strip().upper()

        if not symbol:
            flash("Please enter a cryptocurrency symbol (e.g., BTC).", "Warning")
            return render_template('crypto.html')

        params = {
            'symbol': symbol,
            'convert': 'USD'
        }

        try:
            response = requests.get(API_URL, headers=headers, params=params)
            data = response.json()

            crypto = data.get("data", {}).get(symbol)

            if crypto:
                name = crypto['name']
                price = crypto['quote']['USD']['price']
                market_cap = crypto['quote']['USD']['market_cap']
                percent_change_24h = crypto['quote']['USD']['percent_change_24h']

                return render_template(
                    'crypto.html',
                    name=name,
                    symbol=symbol,
                    price=price,
                    market_cap=market_cap,
                    percent_change_24h=percent_change_24h
                )
            else:
                flash("❌ No data found for the given cryptocurrency symbol.", "Danger")

        except requests.exceptions.RequestException as e:
            flash(f"⚠️ Unable to fetch data right now. Please check your internet connection or try again later.", "Danger")

    # For GET request or errors, show empty form
    return render_template('crypto.html')


# 3. Movies App
@main_bp.route('/movies', methods=["GET", "POST"])
def movies():
    if "user_id" not in session:
        flash("You must be logged in to access this app.", "Danger")
        return redirect(url_for("auth.login"))

    movie_data = None
    if request.method == 'POST':
        title = request.form.get('title')
        if not title:
            flash("Please enter a movie title.", "Warning")
        else:
            API_KEY = os.getenv('MOVIES_API_KEY')
            url = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
            try:
                response = requests.get(url)
                data = response.json()
                if data.get("Response") == "True":
                    movie_data = data
                else:
                    flash("Movie not found!", "Danger")
            except Exception as e:
                flash(f"⚠️ Unable to connect to the server. Please check your internet connection.", "Danger")

    return render_template("movies.html", movie=movie_data)


# 4. Sport Score Board App
@main_bp.route('/sports-scoreboard', methods=["GET", "POST"])
def sports_scoreboard():
    if "user_id" not in session:
        flash("You must be logged in to access this app.", "Danger")
        return redirect(url_for("auth.login"))

    team_data = None  # unified object to pass to template

    if request.method == 'POST':
        team_name = request.form.get('team_name')
        if not team_name:
            flash("Please enter a team name.", "Warning")
        else:
            API_KEY = os.getenv('SPORTS_API_KEY')
            try:
                # 1. Search team
                url_team = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/searchteams.php?t={team_name}"
                response = requests.get(url_team)
                data = response.json()

                if data.get('teams'):
                    team = data['teams'][0]
                    id_team = team.get('idTeam')

                    # 2. Get players
                    url_players = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/lookup_all_players.php?id={id_team}"
                    players = requests.get(url_players).json().get('player', [])

                    # 3. Get recent matches
                    url_recent = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/eventslast.php?id={id_team}"
                    matches = requests.get(url_recent).json().get('results', [])

                    # Add winner to each match
                    for match in matches:
                        home = match.get('strHomeTeam')
                        away = match.get('strAwayTeam')
                        hs = match.get('intHomeScore')
                        ascore = match.get('intAwayScore')
                        try:
                            if hs is not None and ascore is not None:
                                hs = int(hs)
                                ascore = int(ascore)
                                if hs > ascore:
                                    match['winner'] = home
                                elif ascore > hs:
                                    match['winner'] = away
                                else:
                                    match['winner'] = "Draw"
                            else:
                                match['winner'] = "Unknown"
                        except:
                            match['winner'] = "Error"

                    # Package all data into one object
                    team_data = {
                        "info": team,
                        "players": players,
                        "recent_matches": matches
                    }

                else:
                    flash("Team not found!", "Danger")
            except Exception as e:
                flash(f"⚠️ Unable to connect to the server. Please check your internet connection.", "Danger")

    return render_template("sports_scoreboard.html", team_data=team_data)


# 5. Flight Tracker App
@main_bp.route('/flight-tracker', methods=["GET","POST"])
def flight_tracker():
    if "user_id" not in session:
        flash("You must be logged in to access this app.", "Danger")
        return redirect(url_for("auth.login"))
    
    API_KEY = os.getenv('FLIGHT_TRACKER_API_KEY')
    BASE_URL = 'http://api.aviationstack.com/v1/flights'

    flight_data = None
    if request.method == 'POST':
        flight_number = request.form.get('flight_number')
        if flight_number:
            # Try searching by flight_iata
            url = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}&flight_iata={flight_number}"
            response = requests.get(url)
            print("API Response:", response.json())  # Debug print

            if response.status_code == 200:
                data = response.json()
                flights = data.get('data', [])
                if flights:
                    flight_data = flights[0]
                else:
                    # No flights found, try another parameter or show message
                    flash("No flight information found for that flight number.", "Warning")
            else:
                flash(f"API Error: {response.status_code}", "Danger")
        else:
            flash("Please enter a flight number.", "Warning")

    return render_template('flight_tracker.html', flight_data=flight_data)


# 6. Books App
@main_bp.route('/books', methods=["GET","POST"])
def books():
    if "user_id" not in session:
        flash("You must be logged in to access this app.", "Danger")
        return redirect(url_for("auth.login"))
    
    book_results = []
    if request.method == 'POST':
        book_name = request.form.get('book_name')
        if not book_name:
            flash("Please enter a book name or title.", "warning")
        else:
            try:
                url = f"https://www.googleapis.com/books/v1/volumes?q={book_name}"
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                if 'items' not in data or len(data['items']) == 0:
                    flash("No books found for the given query.", "warning")
                else:
                    for item in data['items'][:]:  # Show all books
                        volume_info = item.get('volumeInfo', {})
                        book = {
                            'title': volume_info.get('title', 'N/A'),
                            'authors': ", ".join(volume_info.get('authors', ['N/A'])),
                            'publisher': volume_info.get('publisher', 'N/A'),
                            'publishedDate': volume_info.get('publishedDate', 'N/A'),
                            'description': volume_info.get('description', 'No description available.'),
                            'pageCount': volume_info.get('pageCount', 'N/A'),
                            'categories': ", ".join(volume_info.get('categories', ['N/A'])),
                            'averageRating': volume_info.get('averageRating', 'N/A'),
                            'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', None)
                        }
                        book_results.append(book)

            except requests.exceptions.HTTPError as http_err:
                flash(f"HTTP error occurred: {http_err}", "danger")
            except requests.exceptions.ConnectionError:
                flash("Network error. Please check your connection.", "danger")
            except requests.exceptions.Timeout:
                flash("Request timed out.", "danger")
            except Exception as err:
                flash(f"⚠️ Something went wrong while finding the books. Please try again later.", "Danger")

    return render_template('books.html', books=book_results)


# 7. Recipe Finder App
@main_bp.route('/recipe-finder', methods=["GET","POST"])
def recipe_finder():
    if "user_id" not in session:
        flash("You must be logged in to access this app.", "Danger")
        return redirect(url_for("auth.login"))
    
    SPOONACULAR_API_KEY = os.getenv('SPOONACULAR_API_KEY')
    recipes = []
    error = None
    if request.method == 'POST':
        ingredients = request.form.get('ingredients', '')
        diet = request.form.get('diet', '')
        intolerances = request.form.get('intolerances', '')

        # Build API URL
        url = "https://api.spoonacular.com/recipes/complexSearch"
        params = {
            "apiKey": SPOONACULAR_API_KEY,
            "includeIngredients": ingredients,
            "diet": diet,
            "intolerances": intolerances,
            "number": 10
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            recipes = data.get('results', [])
            if not recipes:
                error = "No recipes found for given inputs."
        except Exception as e:
            error = f"⚠️ Something went wrong while fetching data. Please try again."

    return render_template('recipe_finder.html', recipes=recipes, error=error)


# 8. Stock Monitor App
@main_bp.route('/stock-monitor', methods=["GET","POST"])
def stock_monitor():
    if "user_id" not in session:
        flash("You must be logged in to access this app.", "Danger")
        return redirect(url_for("auth.login"))
    
    API_KEY = os.getenv('STOCK_API_KEY') 
    stock_data = None
    if request.method == 'POST':
        symbol = request.form.get('symbol', '').upper().strip()

        if not symbol:
            flash("Please enter a stock symbol.", "warning")
            return redirect(url_for('stock'))

        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={API_KEY}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if "Error Message" in data:
                flash("Invalid API call or stock symbol. Please try again.", "danger")
            elif "Note" in data:
                flash("API call limit reached. Please wait and try again later.", "warning")
            else:
                # Find the time series key dynamically
                time_series_key = next((k for k in data if "Time Series" in k), None)

                if not time_series_key:
                    flash("No time series data found.", "danger")
                else:
                    time_series = data[time_series_key]
                    latest_timestamp = sorted(time_series.keys())[-1]
                    latest_data = time_series[latest_timestamp]

                    stock_data = {
                        'symbol': symbol,
                        'timestamp': latest_timestamp,
                        'open': latest_data['1. open'],
                        'high': latest_data['2. high'],
                        'low': latest_data['3. low'],
                        'close': latest_data['4. close'],
                        'volume': latest_data['5. volume']
                    }

        except requests.exceptions.RequestException as e:
            flash(f"⚠️ Unable to connect to the server. Please check your internet connection.", "danger")
        except Exception as e:
            flash(f"⚠️ Something went wrong while fetching data. Please try again.", "danger")

    return render_template('stock_monitor.html', stock_data=stock_data)


# 9. Covid-19 Resource App
@main_bp.route('/covid19', methods=["GET","POST"])
def covid19():
    if "user_id" not in session:
        flash("You must be logged in to access this app.", "Danger")
        return redirect(url_for("auth.login"))
    
    stats = None
    country = None

    if request.method == "POST":
        country = request.form.get("country")

        if country:
            url = f"https://disease.sh/v3/covid-19/countries/{country}?strict=true"
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()

                stats = {
                    "Country": data.get("country", "N/A"),
                    "Total Cases": data.get("cases", "N/A"),
                    "Today's Cases": data.get("todayCases", "N/A"),
                    "Total Deaths": data.get("deaths", "N/A"),
                    "Today's Deaths": data.get("todayDeaths", "N/A"),
                    "Recovered": data.get("recovered", "N/A"),
                    "Active": data.get("active", "N/A"),
                    "Critical": data.get("critical", "N/A"),
                    "Cases per Million": data.get("casesPerOneMillion", "N/A"),
                    "Deaths per Million": data.get("deathsPerOneMillion", "N/A"),
                    "Population": data.get("population", "N/A"),
                }

            except requests.exceptions.RequestException as err:
                flash("⚠️ Something went wrong while fetching data. Please try again.", "Danger")
        else:
            flash("Please enter a country name.", "Darning")
    return render_template('covid19.html', country=country, stats=stats)


# 10. Calendar SYNC App
@main_bp.route('/calendar-sync', methods=["GET","POST"])
def calendar_sync():
    return render_template('calendar_sync.html')


# 11. Ghibli Art App
@main_bp.route('/ghibli', methods=["GET","POST"])
def ghibli_art():
    if "user_id" not in session:
        flash("You must be logged in to access this app.", "Danger")
        return redirect(url_for("auth.login"))
    
    API_KEY = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=API_KEY)

    generation_text = None
    image_data_url = None

    if request.method == "POST":
        prompt = request.form.get("prompt")
        image_file = request.files.get("image")
    
        if not prompt or not image_file:
            flash("Please provide a prompt.", "Warning")
            return redirect(url_for("main.ghibli_art"))
    
        try:
            input_image = Image.open(image_file.stream)
    
            response = client.generate_content(
                model="gemini-pro-vision",
                contents=[prompt, input_image],
                generation_config=genai.GenerationConfig(
                    candidate_count=1
                )
            )
    
            for part in response.candidates[0].content.parts:
                if hasattr(part, "text") and part.text:
                    generation_text = part.text
                elif hasattr(part, "inline_data") and part.inline_data:
                    generated_image = Image.open(BytesIO(part.inline_data.data))
                    buffer = BytesIO()
                    generated_image.save(buffer, format="PNG")
                    encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
                    image_data_url = f"data:image/png;base64,{encoded_image}"
    
        except Exception:
            flash("⚠️ Something went wrong while generating the image. Please try again later.", "danger")
    
    return render_template("ghibli_art.html", image_data_url=image_data_url, generation_text=generation_text)


# 12. Gen AI App
@main_bp.route('/genai', methods=["GET","POST"])
def gen_ai():

    if "user_id" not in session:
        flash("You must be logged in to access this app.", "Danger")
        return redirect(url_for("auth.login"))
    
    # NOTE: Replace this with an environment variable in production
    API_KEY = os.getenv('GHIBLI_API_KEY')
    
    # Configure the GenAI client (no need for genai.Client)
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")  # Use valid model name like "gemini-pro" or "gemini-1.5-flash"
    
    prompt = None
    response_text = None
    
    if request.method == "POST":
        prompt = request.form.get("prompt", "").strip()
    
        if not prompt:
            flash("Please provide a prompt.", "Warning")
        else:
            try:
                response = model.generate_content(prompt)
                response_text = response.text  # Safely get the output text
            except Exception:
                # ✅ Do not expose internal errors to users
                flash("⚠️ Something went wrong while generating the response. Please try again later.", "Danger")
    
    return render_template("gen_ai.html", prompt=prompt, response=response_text)
   

# APP COMPLETED 