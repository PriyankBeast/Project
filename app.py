from flask import Flask, render_template
import pickle
import random
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import os

app = Flask(__name__)

# Load the model
model = pickle.load(open('model.pkl', 'rb'))

# Helper function to generate random weather
def generate_weather(month):
    weather_conditions = {
        'Jan': 'Cold',
        'Feb': 'Mild',
        'Mar': 'Warm',
        'Apr': 'Hot',
        'May': 'Hot',
        'Jun': 'Rainy',
        'Jul': 'Rainy',
        'Aug': 'Rainy',
        'Sep': 'Warm',
        'Oct': 'Mild',
        'Nov': 'Cold',
        'Dec': 'Cold'
    }
    return weather_conditions.get(month, 'Mild')

# Home Page Route
@app.route('/')
def index():
    current_time = datetime.now()
    
    # Extract hour, day, month, and year
    current_hour = current_time.hour
    current_day = current_time.day
    current_month = current_time.month
    current_year = current_time.year

    # Generate random hours for off-peak and peak
    peak_hours = f"{random.randint(12, 16)} to {random.randint(17, 22)}"
    off_peak_hours = f"{random.randint(0, 5)} to {random.randint(6, 11)}"

    # Predict pricing based on hour, day, month, year
    current_price = model.predict([[current_hour, current_day, current_month, current_year]])[0]
    
    # Generate upcoming prices (next 5 hours)
    upcoming_prices = [
       float( model.predict([[current_hour + i, current_day, current_month, current_year]])[0] )
        for i in range(1, 6)
    ]

    # Generate random notifications
    notifications = [
        "You can use AC from 22 hours",
        "Switch to solar energy from 14 hours to 18 hours",
        "Charge your vehicle at 23 hours"
    ]
    notification = random.choice(notifications)

    # Get weather based on the month
    weather = generate_weather(current_time.strftime("%b"))

    return render_template('index.html', 
                           date=current_time.strftime("%Y-%m-%d"), 
                           time=current_time.strftime("%H:%M:%S"),
                           weather=weather,
                           peak_hours=peak_hours,
                           off_peak_hours=off_peak_hours,
                           current_price=current_price,
                           upcoming_prices=upcoming_prices,
                           notification=notification)

# Report Page Route
@app.route('/report')
def report():
    # Generate random data for graphs
    daily_data = np.random.uniform(10, 20, 24)
    weekly_data = np.random.uniform(10, 20, 14)
    monthly_data = np.random.uniform(300, 500, 6)

    # Calculate costs
    weekly_cost = np.sum(weekly_data) * 40
    monthly_costs = monthly_data * 40

    # Generate daily graph
    plt.figure()
    plt.hist(daily_data, bins=24)
    plt.title("Electricity Pricing (Last 24 hours)")
    plt.xlabel("Hours")
    plt.ylabel("Price (Rs)")
    plt.savefig('static/daily_graph.png')
    plt.close()

    # Generate weekly graph
    plt.figure()
    plt.plot(weekly_data)
    plt.title("Electricity Usage (Last 14 days)")
    plt.xlabel("Days")
    plt.ylabel("Usage (KWH)")
    plt.savefig('static/weekly_graph.png')
    plt.close()

    # Generate monthly graph
    plt.figure()
    plt.bar(range(1, 7), monthly_data)
    plt.title("Electricity Usage (Last 6 months)")
    plt.xlabel("Months")
    plt.ylabel("Usage (KWH)")
    plt.savefig('static/monthly_graph.png')
    plt.close()
    saved_energy = round(random.uniform(0, 2), 2)
    return render_template('report.html', 
                           daily_message=f"Today you saved up to {saved_energy} KWH energy", 
                           weekly_cost=f"Total cost for this week: Rs {weekly_cost:.2f}",
                           monthly_costs=monthly_costs,
                           enumerate=enumerate)
if __name__ == "__main__":
    app.run(port=8000, debug=True)
