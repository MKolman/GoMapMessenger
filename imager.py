import staticmap


def make_image(raid):
    team_colors = ["#e5e5e5", "#0576ee", "#f2160a", "#fad107"]
    lon, lat = raid["gym"]["longitude"], raid["gym"]["latitude"]
    m = staticmap.StaticMap(800, 300)
    pokemon = staticmap.IconMarker((lon, lat), "./img/pkmn/{}.png".format(
                                   raid["pokemon"]["id"]), 60, 60)
    m.add_marker(pokemon)
    marker = staticmap.CircleMarker((lon, lat), team_colors[raid["team"]], 10)
    m.add_marker(marker)
    img = m.render(zoom=16)
    img.save("img/tmp_raid.png")


if __name__ == "__main__":
    make_image(14.454331, 46.048264, 150)
