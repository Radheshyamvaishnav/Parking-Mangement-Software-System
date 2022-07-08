import sqlite3
import datetime

                

class db_creation:

    def vehical_details(self):
        conn = sqlite3.connect('Parking_Management_System.db')

        conn.execute('''CREATE TABLE Vehical_details
                (ID                   INTEGER     PRIMARY KEY   AUTOINCREMENT  NOT NULL,
                VehicalNumber         TEXT                                     NOT NULL,
                ParkingSpaceNumber    INTEGER                                  NOT NULL,
                ParkingStarttime      Text              ,
                ParkingEndtime        Text              
                 );
                ''')
        
        conn.close()



    def ParkingSpot_details(self):
        conn = sqlite3.connect('Parking_Management_System.db')

        conn.execute('''
                CREATE TABLE ParkingSpot_details
                (
                ParkingSpotNumber     INTEGER     PRIMARY KEY   AUTOINCREMENT   NOT NULL,
                Spot                  TEXT        NOT NULL      ,
                VehicalNumber         TEXT
                 );
                ''')


        for i in range(1,51):
            conn.execute(''' INSERT INTO ParkingSpot_details (Spot, VehicalNumber) \
                    VALUES ( "Empty" , Null )''');

            conn.commit()

        
        conn.close()



class db_operations:

    def get_empty_parking_spot(self):
            conn = sqlite3.connect('Parking_Management_System.db')
            cursor = conn.cursor()

            try:
                empty_spot = cursor.execute(''' Select *  
                                            FROM ParkingSpot_details 
                                            Where Spot = "Empty" ;  
                                            ''')
                
                conn.commit()
                return empty_spot
            except:
                empty_spot = "None"
                return empty_spot


            

    def get_Occupied_parking_spot(self):
            conn = sqlite3.connect('Parking_Management_System.db')
            cursor = conn.cursor()
            try:
                Occupied_spot = cursor.execute(''' Select *  
                                            FROM ParkingSpot_details 
                                            Where Spot = "Occupied" ;  
                                            ''')

                conn.commit()
            
                
                return Occupied_spot
            except:
                Occupied_spot = "None"
                return Occupied_spot


    def park_vehical(self,VehicalNumber):
        conn = sqlite3.connect('Parking_Management_System.db')
        cursor = conn.cursor()
        
        empty_spot = self.get_empty_parking_spot()
        empty_spot = empty_spot.fetchone()

        cursor.execute('''
        Update ParkingSpot_details  Set VehicalNumber = ?,
        Spot = "Occupied"   
        Where  ParkingSpotNumber = ? ;
        ''', (VehicalNumber, str(empty_spot[0])))   

        cursor.execute( " INSERT INTO Vehical_details (VehicalNumber, ParkingSpaceNumber, ParkingStarttime) \
                    VALUES ( ? , ?, ? )", (VehicalNumber, str(empty_spot[0]), datetime.datetime.now() ))



        conn.commit()
       

        parking_details = " Please Park Your Vehical " + VehicalNumber + " at Spot Number " + str(empty_spot[0])

        return parking_details




    def Departing_vehical(self, VehicalNumber ):
            conn = sqlite3.connect('Parking_Management_System.db')
            cursor = conn.cursor()

            departing_VehicalNumber = cursor.execute("Select * FROM ParkingSpot_details Where VehicalNumber == ? ;", (VehicalNumber,) )
            departing_Vehical_Number = departing_VehicalNumber.fetchone()

            cursor.execute('''
                            Update ParkingSpot_details  Set VehicalNumber = NULL,
                            Spot = "Empty"   
                            Where  VehicalNumber == ? ;
                            ''', (str(departing_Vehical_Number[2]),))  
            
            cursor.execute('''
                            Update Vehical_details  Set ParkingEndtime = ?
                            Where  VehicalNumber == ? ;
                            ''', ( datetime.datetime.now(),str(departing_Vehical_Number[2])))  
            
            conn.commit()

            result = "Vehical " + VehicalNumber + " is departed from Spot "  + str(departing_Vehical_Number[2] + " and total fare is " + str(self.fare_calculator(VehicalNumber)) + " Rs ")
            return result
            


    def fare_calculator(self, VehicalNumber):
        conn = sqlite3.connect('Parking_Management_System.db')
        cursor = conn.cursor()

        departing_VehicalNumber = cursor.execute("Select ParkingStarttime, ParkingEndtime FROM Vehical_details Where VehicalNumber == ? ;", (VehicalNumber,) )
        departing_Vehical_Number = departing_VehicalNumber.fetchone()

        starttime = datetime.datetime.strptime(departing_Vehical_Number[0], '%Y-%m-%d %H:%M:%S.%f').hour   
        endtime = datetime.datetime.strptime(departing_Vehical_Number[1], '%Y-%m-%d %H:%M:%S.%f').hour
        total_hours = endtime - starttime
        if total_hours <= 0:
            return 10
        else:
            return total_hours*10

    def search_vehical(self, VehicalNumber):
        conn = sqlite3.connect('Parking_Management_System.db')
        cursor = conn.cursor()

        Vehical = cursor.execute("Select VehicalNumber, ParkingSpotNumber  FROM ParkingSpot_details Where VehicalNumber == ? ;", (VehicalNumber,) )

        Vehical = Vehical.fetchone()
        result = "Vehical " + str(Vehical[0]) + " is parked at spot " + str(Vehical[1])

        return result




            

if __name__ == "__main__":
#     # create = db_creation()
#     # create.ParkingSpot_details()
#     # create.vehical_details()

    data =  db_operations()
    # print(data.get_empty_parking_spot())
#     print(data.get_Occupied_parking_spot())
#     print(data.park_vehical("MH23645"))
    print(data.search_vehical("MH652365126"))
#     print(data.fare_calculator("MH23645"))


