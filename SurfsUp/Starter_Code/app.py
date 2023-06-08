# Import the dependencies.
import numpy as np
import datetime as dt

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################


@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> and /api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data)
       to a dictionary using date as the key and prcp as the value"""

    # Query all measurements of prcp for last 12 months (queries from jupyter notebook)
    latest_date = session.query(measurement).order_by(
        measurement.id.desc()).first()
    latest_date = latest_date.date

    start_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    start_date = start_date.strftime('%Y-%m-%d')

    year_data = session.query(measurement.date, measurement.prcp).filter(
        measurement.date >= start_date).all()

    # Convert list of tuples into dictionary with date as key and prcp as value
    rain = dict(year_data)

    return jsonify(rain)


@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""

    # Query all measurements of stations and return a list of these station names (queries from jupyter notebook)
    station_list = session.query(station.station, station.name).all()
    station_list

    # convert list of tuples into dictionary
    station_list = dict(station_list)

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of temperature observations for the previous year."""

    # Query the dates and temperature observations of the most-active station for the previous year of data.
    # Calculate the date one year from the last date in data set.
    start_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    start_date = start_date.strftime('%Y-%m-%d')

    most_active_stations = session.query(measurement.station, func.count(measurement.station)).\
        order_by(func.count(measurement.station).desc()).\
        group_by(measurement.station).all()

    most_active_station = most_active_stations[0][0]

    year_data_most_active = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date >= start_date).\
        filter(measurement.station == most_active_station).all()

    # Return a JSON list of temperature observations for the previous year.
    year_data_most_active = dict(year_data_most_active)

    return jsonify(year_data_most_active)


@app.route("/api/v1.0/<start>" and "/api/v1.0/<start>/<end>")
def start_end():

"""Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start 
or start-end range For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date. 
For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive."""


if __name__ == '__main__':
    app.run(debug=True)
