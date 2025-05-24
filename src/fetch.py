
import requests
import pandas as pd
from datetime import datetime, timedelta
import json

#             <GT name="AdvertisedTimeAtLocation" value="{now_str}"/>


API_KEY = "cc099cfca8464b55b73357eec92da761"

def fetch_departures(station_code="Cst"):
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%dT%H:%M:%S")
    one_hour_later = (now + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")



    query = f"""
    <REQUEST>
      <LOGIN authenticationkey='{API_KEY}' />
      <QUERY objecttype='TrainAnnouncement' orderby='AdvertisedTimeAtLocation' schemaversion="1.9" limit="50" >
        <FILTER>
          <AND>
            <EQ name='LocationSignature' value='{station_code}' />
            <LT name="AdvertisedTimeAtLocation" value="{one_hour_later}"/>
            <EQ name='ActivityType' value='Avgang' />
          </AND>
        </FILTER>
        <INCLUDE>AdvertisedTrainIdent</INCLUDE>
        <INCLUDE>AdvertisedTimeAtLocation</INCLUDE>
        <INCLUDE>FromLocation</INCLUDE>
        <INCLUDE>ActivityType</INCLUDE>
        <INCLUDE>TimeAtLocation</INCLUDE>
        <INCLUDE>TrackAtLocation</INCLUDE>
        <INCLUDE>ToLocation</INCLUDE>
      </QUERY>
    </REQUEST>
    """


 
    response = requests.post(
        url="https://api.trafikinfo.trafikverket.se/v2/data.json",
        data=query.encode("utf-8"),
        headers={"Content-Type": "text/xml"},
    )

    data = response.json()
    print(44445545)




    data = response.json()["RESPONSE"]["RESULT"][0]["TrainAnnouncement"]
    df = pd.json_normalize(data)


    return df

