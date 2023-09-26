import PIL.Image
from PIL.ExifTags import TAGS, GPSTAGS

GPSINFO = 34853

def read_exif(file_name):
    exif_data = PIL.Image.open(file_name)._getexif()

    gps_info = extract_gps_info(exif_data)

    if not gps_info:
        raise RuntimeError("GPS information not found in EXIF data.")

    lat_lon = get_lat_lon(gps_info)

    if not lat_lon:
        raise RuntimeError("GPS information not found in EXIF data.")

    latitude, longitude, altitude = lat_lon
    print(
        f"Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude}"
    )

    return latitude, longitude, altitude

def extract_gps_info(exif_data):
    gps_info = {}

    if GPSINFO in exif_data:
        for tag, value in exif_data[GPSINFO].items():
            tag_name = GPSTAGS.get(tag, tag)
            gps_info[tag_name] = value

        return gps_info
    else:
        return None

def get_lat_lon(gps_info):
    if gps_info is None:
        return None

    lat = gps_info.get("GPSLatitude")
    lon = gps_info.get("GPSLongitude")
    alt = gps_info.get("GPSAltitude")

    print(lat)

    if lat and lon:
        lat_ref = gps_info.get("GPSLatitudeRef", "N")
        lon_ref = gps_info.get("GPSLongitudeRef", "E")

        lat_deg = lat[0][0] / lat[0][1]
        lat_min = lat[1][0] / lat[1][1]
        lat_sec = lat[2][0] / lat[2][1]

        lon_deg = lon[0][0] / lon[0][1]
        lon_min = lon[1][0] / lon[1][1]
        lon_sec = lon[2][0] / lon[2][1]

        if lat_ref == "S":
            lat_deg = -lat_deg

        if lon_ref == "W":
            lon_deg = -lon_deg

        latitude = lat_deg + lat_min / 60 + lat_sec / 3600
        longitude = lon_deg + lon_min / 60 + lon_sec / 3600
        altitude = alt[0] / alt[1]

        return latitude, longitude, altitude
    else:
        return None
