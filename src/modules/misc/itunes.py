from datetime import datetime

import itunespy


def milliseconds_to_minutes_and_seconds(milliseconds):
    total_seconds = milliseconds // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60

    if minutes == 0:
        return f"{seconds}s"
    else:
        return f"{minutes}m {seconds}s"


def extract_date(datetime_str):
    dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")
    # Extracting only the date part
    return dt.date()


def search(query):
    tracks = itunespy.search_track(query)

    # Extracting data for the first track in the first album
    track = tracks[0]

    length_formatted = milliseconds_to_minutes_and_seconds(track.trackTimeMillis)
    return {
        "url": track.trackViewUrl,
        "name": track.trackName,
        "artist": track.artistName,
        "album": track.collectionName,
        "release_date": extract_date(track.releaseDate),
        "price": f"${track.trackPrice}",
        "length": length_formatted,
        "genre": track.primaryGenreName,
        "thumbnail": track.artworkUrl100,
    }
