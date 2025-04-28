import random
from datetime import datetime, timedelta
from gen import run_pb2

from typing import Any


def generate_event(event_id: int, CONFIG: Any) -> run_pb2.RunningEvent:
    CITIES = CONFIG["cities"]
    DISTANCES = CONFIG["distances"]
    WEATHERS = CONFIG["weathers"]
    TAGS = CONFIG["tags"]

    city = random.choice(CITIES)
    weather = WEATHERS[random.choice(list(WEATHERS.keys()))]
    distance = DISTANCES[random.choice(list(DISTANCES.keys()))]
    start_time = (
        datetime.now() + timedelta(minutes=random.randint(5, 120))
    ).isoformat() + "Z"  # na normalny jakis string
    tags = random.sample(TAGS, k=random.randint(1, len(TAGS)))

    return run_pb2.RunningEvent(
        id=event_id,
        city=city,
        weather=weather,
        distance=distance,
        start_time=start_time,
        tags=tags,
    )
