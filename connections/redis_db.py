import redis
import os
from dotenv import load_dotenv
load_dotenv()

REDIS_CLIENT = redis.Redis(
    host="redis-10522.c293.eu-central-1-1.ec2.cloud.redislabs.com",
    port=10522,
    password=os.getenv("REDIS_KEY"),
    decode_responses=True
)