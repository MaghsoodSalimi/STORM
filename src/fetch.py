
import requests
import pandas as pd
from datetime import datetime

API_KEY = "cc099cfca8464b55b73357eec92da761"

def fetch_departures(station_code="Cst"):
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

    query = f"""
    <REQUEST>
      <LOGIN authenticationkey='{API_KEY}' />
      <QUERY objecttype='TrainAnnouncement' orderby='AdvertisedTimeAtLocation'>
        <FILTER>
          <AND>
            <GT name='AdvertisedTimeAtLocation' value='{now}' />
            <EQ name='LocationSignature' value='{station_code}' />
            <EQ name='ActivityType' value='Departure' />
          </AND>
        </FILTER>
        <INCLUDE>AdvertisedTrainIdent</INCLUDE>
        <INCLUDE>AdvertisedTimeAtLocation</INCLUDE>
        <INCLUDE>EstimatedTimeAtLocation</INCLUDE>
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

    data = response.json()["RESPONSE"]["RESULT"][0]["TrainAnnouncement"]
    df = pd.json_normalize(data)
    return df

df = fetch_departures("Cst")
df.to_csv("departures_stockholm.csv", index=False)
print(df[["AdvertisedTrainIdent", "AdvertisedTimeAtLocation", "EstimatedTimeAtLocation"]].head())
