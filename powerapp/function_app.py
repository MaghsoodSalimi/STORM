import logging
import azure.functions as func






import logging
import requests
import pandas as pd
from datetime import datetime, timedelta
import json
import azure.functions as func
import pyodbc
import os

API_KEY = "cc099cfca8464b55b73357eec92da761"



SERVER = 'myportfolioserver.database.windows.net'
DATABASE = 'portfolio'
USERNAME = 'max'
PASSWORD = '1356ML56ml456!!'
DRIVER = '{ODBC Driver 18 for SQL Server}'

def get_db_connection():
    conn_str = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
    return pyodbc.connect(conn_str)

def get_last_advertised_time():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT last_advertised_time FROM settings")
        row = cursor.fetchone()
        logging.info(f"3-last date retrieved from database.{row[0]}")
        return row[0]


def update_last_advertised_time(new_time):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE settings SET last_advertised_time = ?",
                       new_time)
        conn.commit()

import json

def convert_complex_field(field_value, field_name):
    
    
    return field_value[0][field_name]

        
    
def check_for_na_fields(fieldvalue):
    
    if pd.isna(fieldvalue):
        return None
    else:
        return fieldvalue    



def save_train_departures(df):
    logging.info(f"9x9x9x- Preparing to insert {len(df)} rows")
    if df.empty:
        return
    


 
    insert_query = """
            
            IF NOT EXISTS (
    SELECT 1 FROM train_departures WHERE ActivityId = ?)

            INSERT INTO train_departures (
                ActivityId, ActivityType, Advertised, AdvertisedTimeAtLocation, AdvertisedTrainIdent,
                Canceled, Deleted, DepartureDateOTN,  EstimatedTimeIsPreliminary,
                FromLocation, InformationOwner, LocationDateTimeOTN, LocationSignature, ModifiedTime,
                NewEquipment, Operator, OperationalTrainNumber, 
                ScheduledDepartureDateTime, TimeAtLocation, ToLocation, TrackAtLocation, TrainOwner,
                EstimatedTimeAtLocation,   
                Hour, DelayMinutes




            ) VALUES (?,?,?, ?,?,?,?,?,?,?,?,?,?,?,?,?, ?,?,?,?,?,?,?,?,?)

        """

    rows_to_insert = []
    for _, row in df.iterrows():
        
        row_tuple = (
            row.get('ActivityId'), # 1
            row.get('ActivityId'), # 2 
            row.get('ActivityType'), # 3 
            row.get('Advertised'), # 4
            row.get('AdvertisedTimeAtLocation'), # 5
            row.get('AdvertisedTrainIdent'), # 6
            row.get('Canceled'), # 7
            row.get('Deleted'), #
            row.get('DepartureDateOTN'), # 9
            row.get('EstimatedTimeIsPreliminary'), #10
            convert_complex_field(row.get('FromLocation'), "LocationName"), # 18 
            
            check_for_na_fields(row.get('InformationOwner')), # 17
            check_for_na_fields(row.get('LocationDateTimeOTN')), #16 
            check_for_na_fields(row.get('LocationSignature')), # 15 
            check_for_na_fields(row.get('ModifiedTime')), # 14 

            check_for_na_fields(row.get('NewEquipment')), # 13 
            check_for_na_fields(row.get('Operator')), # 12
            0 if pd.isna(row.get('OperationalTrainNumber')) else row.get('OperationalTrainNumber'), # 11 
            row.get('ScheduledDepartureDateTime'), # 9 
            row.get('TimeAtLocation'), # 8 
            
            convert_complex_field(row.get('ToLocation'), "LocationName"), # 7 
            check_for_na_fields(row.get('TrackAtLocation')), # 6 
            check_for_na_fields(row.get('TrainOwner')), # 5
            check_for_na_fields(row.get('EstimatedTimeAtLocation')), # 4
            
            
            
            int(row['Hour']) if pd.notnull(row['Hour']) else 0, # 2
            int(row['DelayMinutes']) if pd.notnull(row['DelayMinutes']) else 0  # 1



            
        )
        
        rows_to_insert.append(row_tuple)
        
    
    logging.info(f"Preparing to insert {len(rows_to_insert)} rows")

    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Disable fast_executemany to avoid TVP issues
        cursor.fast_executemany = False
        
        try:
            cursor.executemany(insert_query, rows_to_insert)
            conn.commit()
            logging.info(f"Successfully inserted {len(rows_to_insert)} rows")
        except Exception as e:
            logging.error(f"Batch insert failed: {e}")
            logging.error(f"First row data: {rows_to_insert[0] if rows_to_insert else 'No data'}")
            raise



def run_query(query):
    try:
        response = requests.post(
            url="https://api.trafikinfo.trafikverket.se/v2/data.json",
            data=query.encode("utf-8"),
            headers={"Content-Type": "text/xml"},
        )
        response.raise_for_status()
        data = response.json()
        if "RESPONSE" in data and "RESULT" in data["RESPONSE"]:
            result = data["RESPONSE"]["RESULT"][0]
            if "ERROR" in result:
                logging.error("API Error: %s", json.dumps(result["ERROR"], indent=2))
            else:
                logging.info("API query successful")
        else:
            logging.warning("Unexpected response format: %s", json.dumps(data, indent=2))
    except requests.exceptions.RequestException as e:
        logging.error("HTTP Request failed: %s", e)
        raise e
    return response

def fetch_departures(last_AdvertisedTimeAtLocation):
    query = f"""
    <REQUEST>
      <LOGIN authenticationkey='{API_KEY}' />
      <QUERY objecttype='TrainAnnouncement' schemaversion="1.9" limit='5'>  
        <FILTER>
          <AND>
            <EQ name='Advertised' value='true'  />
            <GTE name='AdvertisedTimeAtLocation' value='{last_AdvertisedTimeAtLocation}' />
            <EQ name='ActivityType' value='Avgang' />
          </AND>
        </FILTER>
        <EXCLUDE>WebLink</EXCLUDE>
        <EXCLUDE>TrainComposition</EXCLUDE>
        <EXCLUDE>WebLinkName</EXCLUDE>
        <EXCLUDE>OperationalTransportIdentifiers</EXCLUDE>
        <EXCLUDE>OtherInformation</EXCLUDE>
        <EXCLUDE>ViaToLocation</EXCLUDE>
        <EXCLUDE>MobileWebLink</EXCLUDE>
        <EXCLUDE>TimeAtLocationWithSeconds</EXCLUDE>
        <EXCLUDE>TypeOfTraffic</EXCLUDE>
        <EXCLUDE>Booking</EXCLUDE>
        <EXCLUDE>Deviation</EXCLUDE>
        <EXCLUDE>Service</EXCLUDE>
        <EXCLUDE>ProductInformation</EXCLUDE>
        <EXCLUDE>ViaFromLocation</EXCLUDE>
      </QUERY>
    </REQUEST>
    """
    # logging.info(query)

    response = run_query(query)
    
    data = response.json()
    
    train_announcements = data["RESPONSE"]["RESULT"][0].get("TrainAnnouncement", [])
    
    df = pd.json_normalize(train_announcements)
    
    return df





app = func.FunctionApp()




@app.function_name(name="load_data_trigger")
@app.route(route="load-data")  # This sets the HTTP endpoint: /api/load-data
def load_data_trigger(req: func.HttpRequest) -> func.HttpResponse:


    logging.info('1- Python timer trigger function executed.')


    
    print("2- Timer trigger function started at")


    try:
        last_time = get_last_advertised_time()

 

        logging.info(f"4- Last AdvertisedTimeAtLocation from DB: {last_time}")

        df = fetch_departures(last_time)

        


        if not df.empty:
            df['AdvertisedTimeAtLocation'] = pd.to_datetime(df['AdvertisedTimeAtLocation'])
            
            if 'TimeAtLocation' not in df.columns:
                df['TimeAtLocation'] = pd.to_datetime(0)
                df['AdvertisedTimeAtLocation'] = pd.to_datetime(0)

            
            df['TimeAtLocation'] = pd.to_datetime(df['TimeAtLocation'] )
            
            df['Hour'] = df['AdvertisedTimeAtLocation'].dt.floor('h').dt.hour
            df['DelayMinutes'] = ((df['TimeAtLocation'] - df['AdvertisedTimeAtLocation']).dt.total_seconds() / 60).fillna(0).round().astype(int)

            logging.info("9- new fields added to DataFrame")

            save_train_departures(df)
            logging.info(f"Saved {len(df)} new train departures.")

            # Update last_advertised_time to max value in new data
            new_last_time = df['AdvertisedTimeAtLocation'].max().strftime("%Y-%m-%dT%H:%M:%S")
            update_last_advertised_time(new_last_time)
            logging.info(f"Updated last_advertised_time to: {new_last_time}")

        else:
            logging.info("No new data fetched.")

    except Exception as e:
        logging.error(f"Exception in function: {e}")

    logging.info('Python timer trigger function completed.')

    return func.HttpResponse("Data loading complete", status_code=200)

