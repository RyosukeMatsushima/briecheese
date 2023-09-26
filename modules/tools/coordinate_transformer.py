import math

# this class is used to transform latitude and longitude to x and y coordinates

class CoordinateTransformer:
    def __init__(self, ref_lat, ref_lon):
        self.ref_lat = ref_lat
        self.ref_lon = ref_lon

        earth_radius = 6378137.0
        self.m_per_deg_lat = math.pi * earth_radius / 180.0
        self.m_per_deg_lon = math.pi * earth_radius * math.cos(math.radians(self.ref_lat)) / 180.0

    def transform_to_x_y(self, lat, lon):
        x = (lon - self.ref_lon) * self.m_per_deg_lon
        y = (lat - self.ref_lat) * self.m_per_deg_lat

        return x, y

    def transform_to_lat_lon(self, x, y):
        lat = y / self.m_per_deg_lat + self.ref_lat
        lon = x / self.m_per_deg_lon + self.ref_lon

        return lat, lon

