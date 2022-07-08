
from Database_operations import db_operations
from flask import Flask, jsonify, request, render_template


app = Flask(__name__)

data = db_operations()

@app.route('/', methods = ["GET", "POST"])
def my_form():
    vehicalNumber = request.form.get('VehicalName') or None

    if request.form.get('button') == "Nonetype":
        return 

    if request.form.get('button') == "Empty":
        try:
            empty_spots = data.get_empty_parking_spot()
            available_spots = []
            for spots in empty_spots:
                available_spots.append(spots[0])
            result = '''List Of Empty Parking Spot : ''', available_spots
            return render_template('index.html', data = result)
        except:
            result = "No Empty Parking Spot available"
            return render_template('index.html', data = result)


    if request.form.get('button') == "Occupied" :
        try:
            occupied_spots = data.get_Occupied_parking_spot()
            reserved_spots = []

            for spots in occupied_spots:
                reserved_spots.append(spots[0])
            result = '''List Of Occupied Parking Spot : ''', reserved_spots
            return render_template('index.html', data = result)
        except:
            result = "No Parking Spot  is Occupied"
            return render_template('index.html', data = result)


    if request.form.get('button') == "Park" :
            try:
                    
                    result = data.park_vehical(vehicalNumber)
                    return render_template('index.html', data = result)
            except:
                result = "No Parking Spots available"
                return render_template('index.html', data = result)


    if request.form.get('button') == "Depart":
        try:
            result = data.Departing_vehical(vehicalNumber)
            return render_template('index.html', data = result)
        except:
            result = "This Vehical is not Parked in Parking Lot"
            return render_template('index.html', data = result)


    if request.form.get('button') == "Search":
        try:
            result = data.search_vehical(vehicalNumber)
            return render_template('index.html', data = result)
        except:
            result = "This Vehical is not Parked in Parking Lot"
            return render_template('index.html', data = result)





    result = ""

    return render_template('index.html', data = result)




if __name__ == "__main__":
    app.run(debug = True)