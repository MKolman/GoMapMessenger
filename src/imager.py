import staticmap
import requests
from SECRETS import CHAT


class UploadError(Exception):
    def __init__(self, message, extra_data=None):
        super(Exception, self).__init__(message)

        self.extra_data = extra_data


def make_image(raid):
    team_colors = ["#e5e5e5", "#0576ee", "#f2160a", "#fad107"]
    lon, lat = raid["lon"], raid["lat"]
    m = staticmap.StaticMap(800, 300)
    pokemon = staticmap.IconMarker((lon, lat), "./img/pkmn/{}.png".format(
                                   raid["pokemon_id"]), 60, 60)
    m.add_marker(pokemon)
    marker = staticmap.CircleMarker((lon, lat), "black", 12)
    m.add_marker(marker)
    marker = staticmap.CircleMarker((lon, lat), team_colors[raid["team"]], 10)
    m.add_marker(marker)
    img = m.render(zoom=16)
    img.save("img/tmp_raid.png")


def upload_image(img_upload_url):
    """
    Uploads an image hosted in 'img_upload_url' to uploads.im and returns its
    new url.
    """
    url = "http://uploads.im/api?upload=" + img_upload_url
    for i in range(5):
        response = requests.get(url)
        if response.ok:
            break
        print("Upload not successful. Retrying...")
    try:
        return response.json()['data']['img_url']
    except Exception as exc:
        raise UploadError(str(exc), extra_data=response)


if __name__ == "__main__":
    make_image(14.454331, 46.048264, 150)
