import os
import pytest
from redis import Redis


@pytest.fixture(scope="class", autouse=True)
def redis_connection():
    redis = Redis(host=os.environ["CACHE_URL"], port=int(os.environ["CACHE_PORT"]))
    return redis


class TestClass:
    def test_redis_connection(self, redis_connection):
        assert redis_connection.set("testKey", "testValue")
        assert redis_connection.get("testKey") == b"testValue"
