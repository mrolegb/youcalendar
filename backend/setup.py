import os
from src import tools

channels_table = """ CREATE TABLE IF NOT EXISTS channels (
                                        title text NOT NULL,
                                        channel_id text NOT NULL
                                    ); """


def setup(path: str) -> None:
    c = tools.create_connection(path)
    tools.execute(c, channels_table)
    c.commit()
    c.close()


setup("src/database")
