import json
import os
from typing import List
from threading import current_thread

import concurrent.futures
import requests
import src.log as log
from src.cache import Cache

logger = log.setup_custom_logger("cache")


def get_video_list(
    channel_id: List[str],
    date_from: str,
    date_to: str,
    cache: Cache,
) -> List[dict]:
    r"""Gets a raw list of videos in range for a channel based on channel id"""

    results = []
    for c in channel_id:
        params = {
            "channel_id": c,
            "date_from": date_from,
            "date_to": date_to,
            "part": os.environ["LIST_PART"],
            "type": os.environ["TYPE"],
            "max_results": int(os.environ["MAX_RESULTS"]),
            "order": os.environ["ORDER"],
            "key": os.environ["API_KEY"],
        }

        cache_data = cache.read(params)
        if cache_data:
            logger.info("Reading ids from cache")
            results.append(json.loads(cache_data))
            continue

        headers = {"accept": "application/json"}
        response = requests.get(
            os.environ["VIDEOS_URL"], params=params, headers=headers
        )

        if not cache_data:
            logger.info("Writing ids to cache")
            cache.write(params, json.dumps(response.json()))

        results.append(response.json())

    logger.info(f"Fetching videos from {date_from} to {date_to}")
    return results


def get_video_ids(list: List[dict]) -> str:
    r"""Processes raw data and pulls out video ids"""
    results = ""

    for item in list:
        data = item.get("items", None)
        if data:
            for d in data:
                results += d.get("id").get("videoId") + ","

    return results[:-1]


def get_chunk_video_details(videos_chunk: str, cache: Cache) -> dict:
    r"""Fetch video details by id"""
    params = {
        "id": videos_chunk,
        "part": os.environ["DETAILS_PART"],
        "key": os.environ["API_KEY"],
    }

    cache_data = cache.read(params)
    if cache_data:
        logger.info("Reading video details from cache")
        return json.loads(cache_data)

    headers = {"accept": "application/json"}
    response = requests.get(
        os.environ["VIDEO_DETAILS_URL"], params=params, headers=headers
    )

    if not cache_data:
        logger.info("Writing video details to cache")
        cache.write(params, json.dumps(response.json()))

    return response.json()


def get_chunks(videos: str) -> List[dict]:
    r"""Split a list of video ids into chunks"""
    videos_list = videos.split(",")
    videos_split_list = [
        videos_list[i : i + int(os.environ["CHUNK_SIZE"])]
        for i in range(0, len(videos_list), int(os.environ["CHUNK_SIZE"]))
    ]
    chunks = []
    for vl in videos_split_list:
        chunks.append(",".join(vl))

    logger.info("Split videos into chunks")
    logger.info(chunks)
    return chunks


def get_video_details(videos: str, cache: Cache) -> List[dict]:
    r"""Get video details in chunks and return all data"""
    chunks = get_chunks(videos)
    results = []

    with concurrent.futures.ThreadPoolExecutor(int(os.environ["THREADS"])) as executor:
        future_to_result = (
            executor.submit(get_chunk_video_details, str(c), cache) for c in chunks
        )
        for future in concurrent.futures.as_completed(future_to_result):
            try:
                data = future.result()
                results.append(data)
                thread = current_thread()
                logger.info(f"Video details stashed for worker {thread.name}")
            except Exception as e:
                logger.warn(e)

    return results


def get_video_params(list: List[dict]) -> List[dict]:
    r"""Get video params from the downloaded data"""
    results = []
    for chunk in list:
        chunk_items = chunk.get("items")
        if chunk_items:
            for c in chunk_items:
                results.append(
                    {
                        "id": c.get("id"),
                        "title": c.get("snippet").get("title"),
                        "channelId": c.get("snippet").get("channelId"),
                        "publishedAt": c.get("snippet").get("publishedAt"),
                        "duration": c.get("contentDetails").get("duration"),
                    }
                )

    return results


def get_data(
    channel_id: List[str],
    date_from: str,
    date_to: str,
    cache: Cache,
) -> List[dict]:
    r"""Collect all video info required"""
    logger.info(
        "Getting video list for channels %s from %s to %s"
        % (channel_id, date_from, date_to)
    )
    video_list = get_video_list(channel_id, date_from, date_to, cache)
    logger.info("Getting a list of ids")
    video_ids = get_video_ids(video_list)
    logger.info("Getting video details for set of ids")
    logger.info("Ids: %s" % (video_ids))
    video_details = get_video_details(video_ids, cache)
    return get_video_params(video_details)
