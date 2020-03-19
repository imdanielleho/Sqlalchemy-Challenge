import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

##Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect an existing database into a new model
Base = automap_base()
#reflect the tables
Base.prepare(engine, reflect=True)
#Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

## Flask setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f"Welcome To My Homepage!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"The last 12 months of precipitation data<br/>"
        f"/api/v1.0/stations<br/>"
        f"List of stations from the dataset<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Dates and temperature observations of prior year<br/>"
        f"/api/v1.0/<star><br/>"
        f"The min temp, avg temp, max temp for a given start date<br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"The min temp, avg temp, max temp for a given start-end range<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create our session (link) from Python to the DB
    session = Session(engine)
    start_query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prcp_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= start_query_date).order_by(Measurement.date).all()
    session.close()

    total_prcp = []
    for date, prcp in prcp_data:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        total_prcp.append(prcp_dict)

    return jsonify(total_prcp)

@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    station_list = session.query(Station.station).all()
    session.close()
    all_station = list(np.ravel(station_list))

    return jsonify(all_station)


@app.route("/api/v1.0/tobs")
def tob():
    session = Session(engine)
    start_query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tob_data = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= start_query_date).order_by(Measurement.date).all()
    session.close()

    all_tob = list(np.ravel(tob_data))

    return jsonify(all_tob)

@app.route("/api/v1.0/<start>")
def temp_data_start(start):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    session.close()

    all_results = list(np.ravel(results))

    return jsonify(all_results)

@app.route("/api/v1.0/<start>/<end>")
def temp_data_start_end(start,end):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    all_results = list(np.ravel(results))

    return jsonify(all_results)

if __name__ == '__main__':
    app.run(debug=True)

