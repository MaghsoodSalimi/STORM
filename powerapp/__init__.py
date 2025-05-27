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
DATABASE = 'myportfolio'
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
        if row and row[0]:
            return row[0].strftime("%Y-%m-%dT%H:%M:%S")  # format as string
        else:
            # default fallback (24h ago)
            return (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")

def update_last_advertised_time(new_time):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE settings SET last_advertised_time = ?",
                       new_time)
        conn.commit()

def save_train_departures(df):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO train_departures (
                    ActivityId, ActivityType, Advertised, AdvertisedTimeAtLocation, AdvertisedTrainIdent,
                    Canceled, Deleted, DepartureDateOTN, Deviation, EstimatedTimeIsPreliminary,
                    FromLocation, InformationOwner, LocationDateTimeOTN, LocationSignature, ModifiedTime,
                    NewEquipment, Operator, OperationalTrainNumber, PlannedEstimatedTimeAtLocationIsValid,
                    ScheduledDepartureDateTime, TimeAtLocation, ToLocation, TrackAtLocation, TrainOwner,
                    Booking, EstimatedTimeAtLocation, Service, TrainComposition, PlannedEstimatedTimeAtLocation,
                    ViaFromLocation, Hour, DelayMinutes
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            row.get('ActivityId'),
            row.get('ActivityType'),
            row.get('Advertised'),
            row.get('AdvertisedTimeAtLocation').to_pydatetime() if pd.notnull(row.get('AdvertisedTimeAtLocation')) else None,
            row.get('AdvertisedTrainIdent'),
            row.get('Canceled'),
            row.get('Deleted'),
            row.get('DepartureDateOTN'),
            row.get('Deviation'),
            row.get('EstimatedTimeIsPreliminary'),
            row.get('FromLocation'),
            row.get('InformationOwner'),
            row.get('LocationDateTimeOTN'),
            row.get('LocationSignature'),
            row.get('ModifiedTime'),
            row.get('NewEquipment'),
            row.get('Operator'),
            row.get('OperationalTrainNumber'),
            row.get('PlannedEstimatedTimeAtLocationIsValid'),
            row.get('ScheduledDepartureDateTime'),
            row.get('TimeAtLocation').to_pydatetime() if pd.notnull(row.get('TimeAtLocation')) else None,
            row.get('ToLocation'),
            row.get('TrackAtLocation'),
            row.get('TrainOwner'),
            row.get('Booking'),
            row.get('EstimatedTimeAtLocation'),
            row.get('Service'),
            row.get('TrainComposition'),
            row.get('PlannedEstimatedTimeAtLocation'),
            row.get('ViaFromLocation'),
            int(row.get('Hour')),
            int(row.get('DelayMinutes'))
            )
        conn.commit()

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
      <QUERY objecttype='TrainAnnouncement' schemaversion="1.9" limit='10000'>  
        <FILTER>
          <AND>
            <EQ name='Advertised' value='true'  />
            <GTE name='AdvertisedTimeAtLocation' value='{last_AdvertisedTimeAtLocation}' />
            <EQ name='ActivityType' value='Avgang' />
          </AND>
        </FILTER>
        <EXCLUDE>WebLink</EXCLUDE>
        <EXCLUDE>WebLinkName</EXCLUDE>
        <EXCLUDE>OperationalTransportIdentifiers</EXCLUDE>
        <EXCLUDE>OtherInformation</EXCLUDE>
        <EXCLUDE>ViaToLocation</EXCLUDE>
        <EXCLUDE>MobileWebLink</EXCLUDE>
        <EXCLUDE>TimeAtLocationWithSeconds</EXCLUDE>
        <EXCLUDE>TypeOfTraffic</EXCLUDE>
        <EXCLUDE>ProductInformation</EXCLUDE>
      </QUERY>
    </REQUEST>
    """
    response = run_query(query)
    data = response.json()
    train_announcements = data["RESPONSE"]["RESULT"][0].get("TrainAnnouncement", [])
    df = pd.json_normalize(train_announcements)
    return df

def main(mytimer: func.TimerRequest) -> None:
    logging.info('Python timer trigger function started.')
    print("Timer trigger function started at")


    try:
        last_time = get_last_advertised_time()
        logging.info(f"Last AdvertisedTimeAtLocation from DB: {last_time}")

        df = fetch_departures(last_time)

        if not df.empty:
            df['AdvertisedTimeAtLocation'] = pd.to_datetime(df['AdvertisedTimeAtLocation'])
            df['TimeAtLocation'] = pd.to_datetime(df['TimeAtLocation'])
            df['Hour'] = df['AdvertisedTimeAtLocation'].dt.floor('h').dt.hour
            df['DelayMinutes'] = ((df['TimeAtLocation'] - df['AdvertisedTimeAtLocation']).dt.total_seconds() / 60).fillna(0).round().astype(int)

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
