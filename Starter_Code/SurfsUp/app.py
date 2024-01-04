# Import the dependencies.
import numpy as np
import datetime as dt
import pandas as pd
import sqlalchemy
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
Base.prepare(autoload_with=engine)

# Save references to each table
measurement_table = Base.classes.measurement
station_table = Base.classes.station

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
def welcome():
    """List all available api routes."""
    return (
        f"Welcome, <br/>"
        f"Available Routes in Climate API:<br/>"
        f"/api/v1.0/precipitations<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/end<br/>"
    )

# precipitation route
@app.route("/api/v1.0/precipitations")
def precipitations():
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Perform a query to retrieve the data and precipitation scores
    query_results = session.query(measurement_table.date, measurement_table.prcp).filter(measurement_table.date >= previous_year).all()
    precip = {date: prcp for date, prcp in query_results}
    session.close()
    return jsonify(precip)

#stations route
@app.route("/api/v1.0/stations")
def stations():
    query_results = session.query(station_table.station).all()
    stations = list(np.ravel(query_results))
    session.close()
    return jsonify(stations)

# tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    query_results = session.query(measurement_table.tobs).filter(measurement_table.station == 'USC00519281').filter(measurement_table.date >= previous_year).all()
    tobs = list(np.ravel(query_results))
    session.close()
    return jsonify(tobs)

# start route
@app.route("/api/v1.0/<start>")
# start/end route
@app.route("/api/v1.0/<start>/<end>")
def stats(start=None, end=None):
    stat_result = [func.min(measurement_table.tobs), func.max(measurement_table.tobs), func.avg(measurement_table.tobs)]
    print("\n\n", start)
    print(start, "\n\n")

    #if only start date is given
    if not end: 
        query_results = session.query(*stat_result).filter(measurement_table.date >= start).all()
        temps = list(np.ravel(query_results))
        return jsonify(temps=temps)
    
    #if start and end date is given
    query_results = session.query(*stat_result).filter(measurement_table.date >= start).filter(measurement_table.date <= end).all()
    temps = list(np.ravel(query_results))
    session.close()
    return jsonify(temps)

if __name__ == '__main__':
    app.run(debug=True)

    

    