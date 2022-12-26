from flask import Flask, request
import geoip2.database
import re

app = Flask(__name__)


@app.route('/')
def getip():

    if (str(request.args.get('ip')) == "") or (request.args.get('ip') is None):
        result = request.environ['REMOTE_ADDR']
    else:
        result = str(request.args.get('ip'))

    if (re.match(
            r"^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,"
            r"4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,"
            r"4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|["
            r"1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2["
            r"0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:["
            r"0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2["
            r"0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,"
            r"4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|((["
            r"0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|["
            r"1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,"
            r"4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$",
            result)) or (re.match("(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])(\.(?!$)|$)){4}", result)):

        with geoip2.database.Reader('GeoIP2-City_20220610/GeoIP2-City.mmdb') as reader:
            try:
                response = reader.city(result)
                try:
                    subdivisions_iso_code = response.subdivisions.most_specific.iso_code
                except Exception:
                    subdivisions_iso_code = None
                try:
                    subdivisions_name = response.subdivisions.most_specific.name
                except Exception:
                    subdivisions_name = None
                try:
                    city = response.city.names['en']
                except Exception:
                    city = None
                try:
                    longitude = response.location.longitude
                except Exception:
                    longitude = None
                try:
                    latitude = response.location.latitude
                except Exception:
                    latitude = None
            except Exception:
                return {
                    "statusCode": "ERROR",
                    "ipAddress": "",
                    "countryCode": "",
                    "countryName": "",
                    "continentCode": "",
                    "continentName": "",
                    "city": "",
                    "longitude": "",
                    "latitude": "",
                    "zipCode": "",
                    "subdivisions_name": "",
                    "subdivisions_iso_code": ""

                }

        with geoip2.database.Reader('GeoIP2-Country_20220610/GeoIP2-Country.mmdb') as reader:
            try:
                response = reader.country(result)
                try:
                    iso_code = response.country.iso_code
                except Exception:
                    iso_code = None
                try:
                    country_name = response.country.names['en']
                except Exception:
                    country_name = None

                try:
                    continent_code = response.continent.code
                except Exception:
                    continent_code = None
                try:
                    continent_name = response.continent.names['en']
                except Exception:
                    continent_name = None

            except Exception:
                return {
                    "statusCode": "ERROR",
                    "ipAddress": "",
                    "countryCode": "",
                    "countryName": "",
                    "continentCode": "",
                    "continentName": "",
                    "city": "",
                    "longitude": "",
                    "latitude": "",
                    "zipCode": "",
                    "subdivisions_name": "",
                    "subdivisions_iso_code": ""

                }

        return {
            "statusCode": "OK",
            "ipAddress": result,
            "countryCode": iso_code,
            "countryName": country_name,
            "continentCode": continent_code,
            "continentName": continent_name,
            "city": city,
            "longitude": longitude,
            "latitude": latitude,
            "subdivisions_name": subdivisions_name,
            "subdivisions_iso_code": subdivisions_iso_code,
            "zipCode": None

        }
    else:
        return {
            "statusCode": "ERROR",
            "ipAddress": "",
            "countryCode": "",
            "countryName": "",
            "continentCode": "",
            "continentName": "",
            "city": "",
            "longitude": "",
            "latitude": "",
            "zipCode": "",
            "subdivisions_name": "",
            "subdivisions_iso_code": ""

        }


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
