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

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"After slash input start as: YYYY-MM-DD<br/>"
        f"/api/v1.0/<start_date><br/>"
        f"After each slash, first input a start and end date (in that order)as: YYYY-MM-DD<br/>"
        f"/api/v1.0/<start_date>/<end_date>"
    )

#################################################
#Precipitation route
#################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #pull the final date and the date for filtering in the past year
    end_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    filter_date= dt.datetime.strptime(end_date, '%Y-%m-%d') - dt.timedelta(days=366)

 
    #Query for both the date and the precipition    
    prcp_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > filter_date).\
        filter(Measurement.prcp.isnot(None)).\
        order_by(Measurement.date.asc()).all()

    session.close()

    #convert the all data query to a df    
    prcp_df = pd.DataFrame(prcp_data)
    prcp_df.columns=['date','precipitation']

    prcp_dict = prcp_df.groupby('date')['precipitation'].apply(list).to_dict()
   
    return jsonify(prcp_dict)

#################################################
#Station route
#################################################
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #query for all stations in the dataset
    results = session.query(Station.name).all()
    
    session.close()
    
     # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

#################################################
#Tobs route
#################################################
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #pull the final date and the date for filtering in the past year
    end_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    filter_date= dt.datetime.strptime(end_date, '%Y-%m-%d') - dt.timedelta(days=366)
    
    #pull the most active station name
    most_active_query = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()
    most_active = most_active_query[0]
    
    #query both the date and temperature observations
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active).\
        filter(Measurement.date > filter_date).\
        filter(Measurement.tobs.isnot(None)).\
        order_by(Measurement.date.asc()).all()

    session.close()

    #convert the all data query to a df 
    tobs = list(np.ravel(results))

    return jsonify(tobs)


#################################################
#Start route
#################################################
@app.route("/api/v1.0/<start_date>")
def start(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #query the min, max and average based on the start input
    values = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    session.close()
 
    value_list = list(np.ravel(values))
#extra steps to make the output look nice and clearly itdentify each value
    tmin=value_list[0]
    tmax=value_list[1]
    tavg=value_list[2]

    output=(f"The min temperature from the starting date {start_date} is {tmin}, the max temperature is {tmax}, and the average is {tavg}.")

    return jsonify(output)

#################################################
#Start/End route
#################################################    
@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)
#query the min, max and average based on the start and end input
    values = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()

    session.close()
 
    value_list = list(np.ravel(values))
    
#extra steps to make the output look nice and clearly itdentify each value
    tmin=value_list[0]
    tmax=value_list[1]
    tavg=value_list[2]

    output=(f"The min temperature from the starting date {start_date} to the end date {end_date} is {tmin}, the max temperature is {tmax}, and the average is {tavg}.")

    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)