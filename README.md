# 🌐 Master Hub  

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)  |
![Flask](https://img.shields.io/badge/Flask-Framework-lightgrey)  |
![License](https://img.shields.io/badge/License-MIT-green)  

Master Hub is a **Flask-based web application** that combines multiple mini-apps into a single hub.  
It allows you to explore weather, stock prices, cryptocurrencies, COVID-19 data, and more — all in one place.  

![Home Page Screenshot](https://github.com/PrathamSinghal001/Master-Hub/blob/94157f66fe13d62f282b7f66bfea40bfcc6aed6b/masterhub_logo.png)

---

## 📌 Apps Included
- 🌦 **Weather App** → Get real-time weather information by latitude & longitude.  
- 📈 **Stock Monitor App** → Track live stock prices and percentage changes.  
- 💰 **Crypto App** → Monitor live cryptocurrency data.  
- 🦠 **COVID-19 Resource App** → View updated COVID-19 statistics per country.  
- 📅 (Coming soon) **Calendar Sync App** → Sync and manage events with Google/Outlook calendars.  
- 🎥 (Coming soon) Movies, Books, Sports Scoreboard, Recipe Finder, and more.  

---

## 🚀 Features
- 🔐 User authentication (Login & Register).  
- 📱 Responsive UI with **Bootstrap 4**.  
- ⚡ Real-time data fetched via external APIs.  
- 🗂 Modular architecture (each app is a separate route).  
- 📊 SQLite database for user management.  

---

## 🛠️ Tech Stack
- **Backend:** Python, Flask  
- **Frontend:** HTML5, CSS3, Bootstrap, Jinja2  
- **Database:** SQLite (default)  
- **APIs Used:**  
  - [Open Meteo API](https://open-meteo.com/) → Weather  
  - [Alpha Vantage](https://www.alphavantage.co/) / Yahoo Finance → Stock  
  - [CoinGecko API](https://www.coingecko.com/en/api) → Crypto  
  - [disease.sh API](https://disease.sh/) → COVID-19  
  - [Google Calendar API](https://developers.google.com/calendar) → Calendar Sync  

---

## 📂 Project Structure
```bash
Master-Hub/
│── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── auth.py
│   │   ├── forms.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── books.html
│   │   ├── calendar_sync.html
│   │   ├── covid19.html
│   │   ├── crypto.html
│   │   ├── flight_tracker.html
│   │   ├── gen_ai.html
│   │   ├── ghibli_art.html
│   │   ├── login.html
│   │   ├── movies.html
│   │   ├── profile.html
│   │   ├── recipe_finder.html
│   │   ├── register.html
│   │   ├── sports_scoreboard.html
│   │   ├── stock_monitor.html
│   │   ├── weather.html
│   ├── static/
│       ├── css/style.css
│       ├── js/script.js
│       ├── img/masterhub.png
│── instance/
│   ├── masterhub.db   ← local SQLite DB (ignored in .gitignore)
│── run.py
│── requirements.txt
│── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/PrathamSinghal001/Master-Hub.git
cd master-hub
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
```

Activate:
- Windows → `venv\Scripts\activate`  
- Linux/Mac → `source venv/bin/activate`

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the App
```bash
flask run
```
or
```bash
python run.py
```

👉 Open in browser: [http://127.0.0.1:5000](http://127.0.0.1:5000)  

---

## 📊 Example Screenshots  

- **Home Page**
  ![Home Page Screenshot](https://github.com/PrathamSinghal001/Master-Hub/blob/420df1f87d0c46335410f94cb59f176b6547c93b/Screenshot_25-9-2025_175551_127.0.0.1.jpeg)
- **Covid-19 App**  
  ![Covid-19 Screenshot](https://github.com/PrathamSinghal001/Master-Hub/blob/0155bc601fbd74a46cd3bc51a237935258d95f3c/Screenshot_25-9-2025_175244_127.0.0.1.jpeg)  

- **Books App**  
  ![Books Screenshot](https://github.com/PrathamSinghal001/Master-Hub/blob/84a418d79aec5f355d5513f6c81323d9a8f70e56/Screenshot_25-9-2025_174716_127.0.0.1.jpeg)  

- **Crypto App**  
  ![Crypto Screenshot](https://github.com/PrathamSinghal001/Master-Hub/blob/84a418d79aec5f355d5513f6c81323d9a8f70e56/Screenshot_25-9-2025_17467_127.0.0.1.jpeg)  

---

## 🔐 Database Notes
- Default database: **SQLite** (`instance/masterhub.db`).  
- ⚠️ **Do not upload your production database with user data to GitHub.**  
- Add this to `.gitignore`:  
  ```gitignore
  instance/
  *.db
  ```

Instead, share:
- Database schema (`models.py` or migrations).  
- A seed script for test/demo data.  

---

## 🤝 Contributing
Contributions are welcome!  

1. Fork the repo  
2. Create a new branch (`git checkout -b feature-name`)  
3. Commit your changes (`git commit -m 'Add new feature'`)  
4. Push to your branch (`git push origin feature-name`)  
5. Create a Pull Request  

---

## 📜 License
This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute it with proper attribution.  

---

👨‍💻 Author: **Pratham Singhal**  
🔗 [LinkedIn](http://www.linkedin.com/in/pratham-singhal001) |
🔗 [GitHub](https://github.com/PrathamSinghal001) | 
🔗 [X](https://x.com/prathamsinghal0)  
