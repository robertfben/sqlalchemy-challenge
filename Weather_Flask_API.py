# import flask and other dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#############################################
# Database Setup
#############################################

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
# Declaring base
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#############################################
# Flask Setup
#############################################

# create app, pass in __name__
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Define what to do when user hits the index route
@app.route("/")
def home():
    # home route
    print("Server received request for 'Home' page...")
    return "Welcome to the Climate API 'Home' Page!<br><br> \
        Here are the possible routes you can access:<br> \
            /api/v1.0/precipitation<br> \
            /api/v1.0/stations<br> \
            /api/v1.0/tobs<br> \
            /api/v1.0/(start_date) OR<br> \
            /api/v1.0/(start_date)/(end_date)"

############ Next Route ##################

# Define what to do when user hits the /about route
@app.route("/about")
def about():
    #about route
    print("Server received request for 'About' page ...")
    return "Welcome to the Climate API 'About' page!"

############ Next Route ##################

# Define when user hits precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # create Session link from Python to DB
    session = Session(engine)

    # Perform a query to retrieve the data and precipitation scores
    dataPrecipitationScores = session.execute("SELECT date, prcp FROM measurement\
                                          WHERE date between '2016-08-23' AND '2017-08-23'\
                                          ORDER BY date DESC;").all()

    session.close()

    # Create dictionary from the row data and append to a list 
    all_precipitation = []
    for date, prcp in dataPrecipitationScores:
        precip_dict = {}
        # date as key and precipitation as value
        precip_dict[date] = prcp
        all_precipitation.append(precip_dict)

    # return jsonified list
    return jsonify(all_precipitation)

############ Next Route ##################

# Define when user hits precipitation route
@app.route("/api/v1.0/stations")
def stations():
    # create Session link from Python to DB
    session = Session(engine)

    # Perform a query to retrieve the data and precipitation scores
    Stations_List = session.execute("SELECT id, station, name FROM station;").all()

    session.close()

    # Create dictionary from the row data and append to a list 
    all_stations = []
    for id, station, name in Stations_List:
        station_dict = {}
        station_dict["id"] = id
        station_dict["station"] = station
        station_dict["name"] = name
        all_stations.append(station_dict)

    # return jsonified list
    return jsonify(all_stations)

############ Next Route ##################

# Define when user hits temperature route
@app.route("/api/v1.0/tobs")
def tobs():
    # create Session link from Python to DB
    session = Session(engine)

    # Perform a query to retrieve the dates and temperature observations of the most active station for the previous year of data
    tobs_obs = session.execute("SELECT Measurement.date, Measurement.tobs FROM Measurement \
                                        JOIN Station \
                                        ON Measurement.station = Station.station \
                                        WHERE Station.id = 7 \
                                        AND Measurement.date between '2016-08-23' AND '2017-08-23';").all()
    
    session.close()

    # create dictionary from the row data and append to a list
    all_temps = []
    for date, tobs in tobs_obs:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_temps.append(tobs_dict)
    
    # return jsonified list
    return jsonify(all_temps)

############ Next Route ##################

# Define when user hits inputted start date route only
@app.route("/api/v1.0/<start_date>")
def Starting_Date_Temps(start_date):
    """Fetch min, max, and avg temps. for all dates on and after given start date"""
    # creating session link
    session = Session(engine)

    starting_date_minmaxAvg = session.execute(f"SELECT MIN(tobs), MAX(tobs), AVG(tobs) \
                                                FROM Measurement \
                                                WHERE date >= '{start_date}';").all()

    session.close()

    # create dictionary from the row data and append to list
    minMaxAvg_List = []
    for min, max, avg in starting_date_minmaxAvg:
        minMaxAvg_Dict = {}
        minMaxAvg_Dict["Minimum Temperature"] = min
        minMaxAvg_Dict["Maximum Temperature"] = max
        minMaxAvg_Dict["Average Temperature"] = avg
        minMaxAvg_List.append(minMaxAvg_Dict)

    # return jsonified list
    return jsonify(minMaxAvg_List)

############## Next Route ##################

# Define when user hits inputted start date route only
@app.route("/api/v1.0/<start_date>/<end_date>")
def Starting_Ending_Date_Temps(start_date,end_date):
    """Fetch min, max, and avg temps. for all dates between given start date and end date"""
    # creating session link
    session = Session(engine)

    starting_ending_date_minmaxAvg = session.execute(f"SELECT MIN(tobs), MAX(tobs), AVG(tobs) \
                                                FROM Measurement \
                                                WHERE date BETWEEN '{start_date}' AND '{end_date}';").all()

    session.close()

    # create dictionary from the row data and append to list
    minMaxAvg_Between_List = []
    for min, max, avg in starting_ending_date_minmaxAvg:
        minMaxAvg_Between_Dict = {}
        minMaxAvg_Between_Dict["Minimum Temperature"] = min
        minMaxAvg_Between_Dict["Maximum Temperature"] = max
        minMaxAvg_Between_Dict["Average Temperature"] = avg
        minMaxAvg_Between_List.append(minMaxAvg_Between_Dict)

    # return jsonified list
    return jsonify(minMaxAvg_Between_List)


####################################################
if __name__ == "__main__":
    app.run(debug=True)
