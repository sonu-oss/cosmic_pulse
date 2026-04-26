import datetime
from skyfield.api import load, wgs84

def get_iss_prediction(minutes_ahead=60):
    stations_url = 'http://celestrak.org/NORAD/elements/stations.txt'
    satellites = load.tle_file(stations_url)
    iss = {sat.name: sat for sat in satellites}['ISS (ZARYA)']

    ts = load.timescale()
    now = datetime.datetime.now(datetime.timezone.utc)
    predictions = []

    for i in range(minutes_ahead):
        future_time = now + datetime.timedelta(minutes=i)
        t = ts.from_datetime(future_time)
        geocentric = iss.at(t)
        subpoint = wgs84.subpoint(geocentric)
        predictions.append({
            "time": future_time.strftime("%H:%M"),
            "lat": subpoint.latitude.degrees,
            "lon": subpoint.longitude.degrees
        })
    return predictions