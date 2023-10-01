# Part 2: Design Your Climate App

# Import the dependencies
import numpy as np
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create an app
app = Flask(__name__)

# Flask Routes
@app.route('/')
def home():
    """List all available API routes"""
    return(
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create a session
    session = Session(engine)
    
    # # Calculate the date one year ago from the most recent date
    # most_recent_data = "2017-08-23"
    # one_year_ago_date = get_one_year_ago_date(most_recent_data)

    # Query to retrieve precipitation data for the last year
    prcp_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2017-08-23").all()
    
    session.close()
    
    # Convert the query results to a dictionary
    all_prcp = []
    for date, prcp in prcp_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp

        all_prcp.append(prcp_dict)
        return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create a session
    session = Session(engine)

    # Query all Stations
    stations_data = session.query(Station.station, Station.name).all()
    return jsonify(stations_data)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create a session
    session = Session(engine)

    # Query the dates and temperature observations of the most-active station for the previous year of data
    tobs_data = session.query(Measurement.date, Measurement.tobs, Measurement.prcp).\
                    filter(Measurement.date >= "2017-08-23").\
                    filter(Measurement.station=="USC00519281").all()
    
    session.close()

    # Convert the list to Dictionary
    all_tobs = []
    # Create a dictionary 
    for prcp, date, tobs in tobs_data:
        tobs_dict = {}
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs

        all_tobs.append(tobs_dict)
    
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start_date_tobs(start):
    # Create a session
    session = Session(engine)

    # Calculate TMIN, TAVG, and TMAX for all dates greater than or equal to the start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    session.close()

   # Create a dictionary from the row data and append to a list of start_date_tobs
   start_date_tobs = []
   for min_temp, avg_temp, max_temp in results:
        start_date_tobs_dict = {
            "min_temp": min_temp,
            "avg_temp": avg_temp,
            "max_temp": max_temp
        }
        start_date_tobs.append(start_date_tobs_dict)
   return jsonify(start_date_tobs)   

@app.route("/api/v1.0/<start>/<end>")
def start_end_date_tobs(start, end):
    # Create a session
    session = Session(engine)

    # Return a list of min, avg and max tobs for start and end dates
    #Query all tobs
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of start_end_date_tobs
    start_end_tobs = []
    for min_temp, avg_temp, max_temp in results:
        start_end_tobs_dict = {
            "min_temp": min_temp,
            "avg_temp": avg_temp,
            "max_temp": max_temp
        }
        start_end_tobs.append(start_end_tobs_dict) 

    return jsonify(start_end_tobs)

if __name__ == "__main__":
    app.run(debug=True)
    

