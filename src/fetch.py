
import requests
import pandas as pd
from datetime import datetime, timedelta
import json

#             <GT name="AdvertisedTimeAtLocation" value="{now_str}"/>
# limit="100" 

# <GT name="AdvertisedTimeAtLocation" value="{from_time}"/>
#            <LT name="AdvertisedTimeAtLocation" value="{to_time}"/>
# <GT name="AdvertisedTimeAtLocation" value="{from_time}"/>
# <EQ name='LocationSignature' value='{station_code}' />
# <NE name='FromLocation' value=''  />
'''       
        <INCLUDE>AdvertisedTrainIdent</INCLUDE>
        <INCLUDE>AdvertisedTimeAtLocation</INCLUDE>
        <INCLUDE>FromLocation</INCLUDE>
        <INCLUDE>ActivityType</INCLUDE>
        <INCLUDE>TimeAtLocation</INCLUDE>
        <INCLUDE>TrackAtLocation</INCLUDE>
        <INCLUDE>ToLocation</INCLUDE>
         

'''


API_KEY = "cc099cfca8464b55b73357eec92da761"

def fetch_departures(station_code="Cst"):
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%dT%H:%M:%S")
    one_hour_later = (now + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")

    print (now_str)

    from_time = '2025-04-01T00:00:00'
                  
    to_time = '2025-05-01T00:00:00'

    query = f"""
    <REQUEST>
      <LOGIN authenticationkey='{API_KEY}' />
      <QUERY objecttype='TrainAnnouncement' orderby='AdvertisedTimeAtLocation' schemaversion="1.9" >  
        <FILTER>
          <AND>
            <EQ name='Advertised' value='true'  />

            
            
            
            <EQ name='ActivityType' value='Avgang' />
          </AND>
        </FILTER>
        <EXCLUDE>ActivityId</EXCLUDE>
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

    print(query)

    try:
        response = requests.post(
            url="https://api.trafikinfo.trafikverket.se/v2/data.json",
            data=query.encode("utf-8"),
            headers={"Content-Type": "text/xml"},
        )

        # Check for HTTP errors
        response.raise_for_status()

        # Try parsing JSON
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            print("❌ Failed to parse JSON response:")
            print(response.text)
            raise e

        # Check for API-level errors in the response
        if "RESPONSE" in data and "RESULT" in data["RESPONSE"]:
            result = data["RESPONSE"]["RESULT"][0]
            if "ERROR" in result:
                print("⚠️ API Error:")
                print(json.dumps(result["ERROR"], indent=2))
            else:
                print("✅ Success")
        else:
            print("⚠️ Unexpected response format:")
            print(json.dumps(data, indent=2))

    except requests.exceptions.RequestException as e:
        print("🚨 HTTP Request failed:")
        print(e)
        
  


    data = response.json()
 




    data = response.json()["RESPONSE"]["RESULT"][0]["TrainAnnouncement"]
    df = pd.json_normalize(data)


    return df

