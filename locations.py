import json
from shapely.geometry import Polygon, Point


class Districts(object):
    def __init__(self):
        self.districts = dict()
        with open("districts.geojson") as f:
            data = json.load(f)
            for dist in data["data"]:
                key = dist["name"], dist["id"]
                self.districts[key] = Polygon(dist["coordinates"])

    def get(self, lon, lat):
        result = []
        p = Point([lon, lat])
        for name, poly in self.districts.items():
            if poly.contains(p):
                result.append(name)
        return result


if __name__ == "__main__":
    d = Districts()
    print(d.get(14.489414, 46.047267))
