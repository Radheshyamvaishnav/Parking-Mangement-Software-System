import sqlite3
from Database_operations import db_operations
from flask import Flask, jsonify, request, render_template


app = Flask(__name__)

data = db_operations()

@app.route('/', methods = ["GET", "POST"])
def my_form():
    vehicalNumber = request.form.get('VehicalName') or None

    try:

        if request.form.get('button') == "Empty":
                empty_spots = data.get_empty_parking_spot()
                available_spots = []
                for spots in empty_spots:
                    available_spots.append(spots[0])
                result = '''List Of Empty Parking Spot : ''', available_spots
                return render_template('index.html', data = result)
            

        elif request.form.get('button') == "Occupied" :
                occupied_spots = data.get_Occupied_parking_spot()
                reserved_spots = []

                for spots in occupied_spots:
                    reserved_spots.append(spots[0])
                result = '''List Of Occupied Parking Spot : ''', reserved_spots
                return render_template('index.html', data = result)


        elif request.form.get('button') == "Park" :
                result = data.park_vehical(vehicalNumber)
                return render_template('index.html', data = result)


        elif request.form.get('button') == "Depart":
                result = data.Departing_vehical(vehicalNumber)
                return render_template('index.html', data = result)


        elif request.form.get('button') == "Search":
            result = data.search_vehical(vehicalNumber)
            return render_template('index.html', data = result)


        else:
            
            result = "Run Query & View Your Results Here"

            return render_template('index.html', data = result)

    except sqlite3.IntegrityError as sqlerror:

        return render_template('index.html', data = "Please Enter Valid Vehical Name")




if __name__ == "__main__":
    app.run(debug = True)