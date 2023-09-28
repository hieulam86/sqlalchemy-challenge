# Part 2: Design Your Climate App

# Import the dependencies
import numpy as np
import datetime as dt
from sqlalchemy import func
from sqlalchemy.orm import Session
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create an app
app = Flask(__name__)

# Define what to do when a user hits the index route
app.route('/')
def home():
    return(
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


app.route("/api/v1.0/precipitation")
def precipitation():
    # Create a session
    session = Session(engine)
    
    # Calculate the date one year ago from the most recent date
    most_recent_data = "2017-08-23"
    one_year_ago_date = get_one_year_ago_date(most_recent_data)

    #Query to retrieve precipitation data for the last year
    precipitation_data = session.query(Measurement.date, Measurement.precipitation).\
        filter(Measurement.date >= one_year_ago_date).all()
    
    # Convert the query results to a dictionary
    precipitation_dict = {date: precipitation for date, precipitation in precipitation_data}
    return jsonify(precipitation_dict)

