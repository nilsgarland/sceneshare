from urllib.parse import urlparse, parse_qs

def get_video_id(url):
    url_data = urlparse(url)
    query = parse_qs(url_data.query)
    try:
        video = query["v"][0]
    except KeyError as e:
        return "none"
    return video

