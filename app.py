import datetime as dt
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)
Base = automap_base()
Base.prepare(autoload_with=engine, reflect=True)

session = Session(engine)
app = Flask(__name__)


@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"start and end date: Year-Month-Day<br/>"
        f"/api/v1.0/start/end<br/>"
        )

Measurement = Base.classes.measurement
Station = Base.classes.station

one_year_before = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   

@app.route("/api/v1.0/precipitation")
def precipitation():
    result = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_before).all()
    precipitation_d = {date: prcp for date, prcp in result}
    return jsonify(precipitation_d)

@app.route("/api/v1.0/stations")
def stations():
    list_station = session.query(Station.station).all()
    station_d = list(np.ravel(list_station))
    return jsonify(station_d)

@app.route("/api/v1.0/tobs")
def tobs():
    most_active = session.query(Measurement.tobs, Measurement.date)\
    .filter(Measurement.station == "USC00519281")\
    .filter(Measurement.date >= one_year_before)\
    .all()
    most_active_d = {date: tobs for date, tobs in most_active}
    return jsonify(most_active_d)

@app.route("/api/v1.0/<start>/<end>")
def temp(start,end):
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    temp_q = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start_date).filter(Measurement.date <= end_date)\
        .all()
    temp_l = list(np.ravel(temp_q))
    return jsonify(temp_l)

if __name__ == '__main__':
    app.run(debug=True)
