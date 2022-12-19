import os
from typing import Dict, List
from src import tools


def get_channel(channel_id: str) -> Dict[str, str] | None:
    sql = """SELECT title, channel_id FROM channels WHERE channel_id='%s';""" % (
        channel_id
    )
    c = tools.create_connection("src/database")
    rows = tools.execute(c, sql)
    c.commit()
    c.close()
    if rows:
        return {"title": rows[0][0], "channel_id": rows[0][1]}
    return None


def get_channels() -> List[Dict[str, str]]:
    sql = """SELECT title, channel_id FROM channels;"""
    c = tools.create_connection("src/database")
    rows = tools.execute(c, sql)
    c.commit()
    c.close()
    return [{"title": r[0], "channel_id": r[1]} for r in rows]


def add_channel(title: str, channel_id: str) -> None:
    sql = """INSERT INTO channels (title, channel_id) VALUES ('%s', '%s');""" % (
        title,
        channel_id,
    )
    c = tools.create_connection("src/database")
    tools.execute(c, sql)
    c.commit()
    c.close()


def delete_channel(channel_id: str) -> None:
    sql = """DELETE FROM channels where channel_id='%s';""" % (channel_id)
    c = tools.create_connection("src/database")
    tools.execute(c, sql)
    c.commit()
    c.close()
