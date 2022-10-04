import sys
import socket
import json
import urllib

from flask import Flask, request, jsonify
import youtube_dl


app = Flask(__name__)

def grab_title_url(id):
    id = id[32:]
    try:
        params = {"format": "json", "url": "https://www.youtube.com/watch?v={}".format(id)}
        url = "https://www.youtube.com/oembed"
        query_string = urllib.parse.urlencode(params)
        url = url + "?" + query_string
        with urllib.request.urlopen(url) as response:
            response_text = response.read()
            data = json.loads(response_text.decode())
            return(data['title'])
    except:
        return('channel')

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'forceurl': True
}


@app.route("/")
def hello_world():
    version = sys.version_info
    return f"<p>Hello, World!</p></br>Running Python: {version.major}.{version.minor}.{version.micro}<br>Hostname: {socket.gethostname()}"


@app.route("/video", methods=['POST', 'GET'])
def get_video():
    # uri = request.form["uri"]
    # options = {
    #     'format': request.form["format"].strip('\"')
    # }
    if request.is_json:
        data = request.get_json()

        if not data["url"]:
            content = {"success": False, "error": "/q called without a 'uri' query param"}
            return jsonify(content)

        url = data["url"].strip('\"')
        # title = grab_title_url(url)

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:

            result = ydl.extract_info(
                data["url"],
                download=False # We just want to extract the info
            )
            # ydl.download([data["url"]])

        return jsonify(
            success = True,
            data = url,
            result = result,
            # download = result['url'],
            # options = options['format'],
            # title = title
        )
    return {"error": "Request must be JSON"}, 415
