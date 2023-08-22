from flask import Flask, jsonify, g
import numpy as np
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

app = Flask(__name__)

# Creating a Connection to the SQLite database
database_path = "Resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{database_path}")

# Database tables into classes
Base = automap_base()
Base.prepare(engine, reflect=True)
Station = Base.classes.station
Measurement = Base.classes.measurement

# Function to create a session 
def get_session():
    if 'session' not in g:
        g.session = Session(engine)
    return g.session

# Calculating the date from one year from the last date
def calculate_dates():
    session = get_session()
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = datetime.strptime(most_recent_date, '%Y-%m-%d') - timedelta(days=365)
    return most_recent_date, one_year_ago

# Define the homepage text or Routes
@app.route("/")
def home():
    return (
        f"Welcome to the Climate App!<br/>"
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = get_session()
    most_recent_date, one_year_ago = calculate_dates()
    
    # Create Query to get the last 12 months of precipitation data
    last_year_precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()
    
    # Converting the query result to a dictionary
    precipitation_dict = {date: prcp for date, prcp in last_year_precipitation}
    
    return jsonify(precipitation_dict)

# Stations route
@app.route("/api/v1.0/stations")
def stations():
    session = get_session()
    
    # Query to get the list of stations
    station_list = session.query(Station.station).all()
    
    # Convert the query result to a list
    stations = list(np.ravel(station_list))
    
    return jsonify(stations)

# Temperature observations route
@app.route("/api/v1.0/tobs")
def tobs():
    session = get_session()
    most_recent_date, one_year_ago = calculate_dates()
    
    # Query to get the most active station (first station in the list)
    active_station = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()[0]
    
    # Creating Query to get the temperature observations for the most active station - last 12 months
    temperature_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == active_station).\
        filter(Measurement.date >= one_year_ago).all()
    
    # Convert the query result to a list of dictionaries
    tobs_data = [{'date': date, 'temperature': temp} for date, temp in temperature_data]
    
    return jsonify(tobs_data)

# Temperature statistics route
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats(start, end=None):
    session = get_session()
    
    # Creating Query to calculate temperature statistics for the specified date range
    if end is None:
        temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
    else:
        temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Converting the query result to dictionary
    stats_dict = {
        "start_date": start,
        "end_date": end,
        "min_temperature": temp_stats[0][0],
        "avg_temperature": temp_stats[0][1],
        "max_temperature": temp_stats[0][2]
    }

    return jsonify(stats_dict)

# Close the session after each request
@app.teardown_request
def teardown_request(exception=None):
    session = g.pop('session', None)
    if session is not None:
        session.close()

if __name__ == "__main__":
    app.run(debug=True)
