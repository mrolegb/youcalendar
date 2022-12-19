import os
from flask import Flask, request
from flask_cors import CORS
from waitress import serve
from src import builder, channels, tools
from src.cache import Cache
from debug import mock

app = Flask(__name__)
CORS(app, send_wildcard=True)
cache = Cache(os.environ["CACHE_URL"], int(os.environ["CACHE_PORT"]))


@app.route("/cache")
def qa_cache_flush():
    if not request.headers.get("Authorize") == os.environ.get("AUTH_KEY"):
        return tools.get_response("error", "Request unauthorized"), 401
    if cache.cache:
        cache.cache.flushdb()
    return tools.get_response("success", "QA - Cache flushed"), 200


@app.route("/videos", methods=["POST"])
def get_video_data():
    if not request.content_type.startswith("application/json"):
        return tools.get_response("error", "Invalid content, expecting json"), 400

    if not os.environ["API_KEY"]:
        return tools.get_response("error", ' "Missing API key'), 500

    channel_list = [c["channel_id"] for c in channels.get_channels()]
    if not channel_list:
        return tools.get_response("error", "No channels added"), 500

    request_data = request.get_json()

    if request_data:
        if request.headers.get("Debug") == "1":
            return tools.get_response("success", mock.get_mock()), 200

        if request_data.get("date_from") and request_data.get("date_to"):
            data = builder.get_data(
                channel_list,
                request_data.get("date_from"),
                request_data.get("date_to"),
                cache,
            )
            return tools.get_response("success", data), 200
    return tools.get_response("error", "Invalid request parameters"), 400


@app.route("/channels")
def get_channels():
    c = channels.get_channels()
    if c:
        return tools.get_response("success", c), 200
    return tools.get_response("error", "No channels recorded"), 400


@app.route("/channels", methods=["POST"])
def add_channel():
    if not request.headers.get("Authorize") == os.environ.get("AUTH_KEY"):
        return tools.get_response("error", "Request unauthorized"), 401

    if not request.content_type.startswith("application/json"):
        return tools.get_response("error", "Invalid content, expecting json"), 400

    data = request.get_json()
    if data:
        if data.get("title") and data.get("channel_id"):
            channels.add_channel(data.get("title"), data.get("channel_id"))
            return (
                tools.get_response("success", "Added channel %s" % data["title"]),
                200,
            )
    return tools.get_response("error", "Channel details missing"), 400


@app.route("/channels", methods=["DELETE"])
def delete_channel():
    if not request.headers.get("Authorize") == os.environ.get("AUTH_KEY"):
        return tools.get_response("error", "Request unauthorized"), 401

    if not request.content_type.startswith("application/json"):
        return tools.get_response("error", "Invalid content, expecting json"), 400

    data = request.get_json()
    if data:
        if data.get("channel_id"):
            if not channels.get_channel(data.get("channel_id")):
                return (
                    tools.get_response(
                        "error", "No channel with id %s" % data.get("channel_id")
                    ),
                    400,
                )
            channels.delete_channel(data.get("channel_id"))
            return (
                tools.get_response(
                    "success", "Channel with id %s was deleted" % data["channel_id"]
                ),
                200,
            )
        else:
            return tools.get_response("error", "No channel data"), 400
    return tools.get_response("error", "No channel data"), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3080))
    serve(app, threads=10, host="0.0.0.0", port=port)
