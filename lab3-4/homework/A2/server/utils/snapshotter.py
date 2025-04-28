import json
import os
import asyncio
from utils.Logger import Logger
from config.ClientData import ClientData

STATE_FILE = "server_state.json"


async def snapshot_state(clients, subscription_counter, interval_seconds=10):
    while True:
        await save_state(clients, subscription_counter)
        Logger.info("Periodic state snapshot saved.")
        await asyncio.sleep(interval_seconds)


def serialize_event(event):
    return {
        "id": event.id,
        "city": event.city,
        "weather": event.weather,
        "distance": event.distance,
        "start_time": event.start_time,
        "tags": list(event.tags),
    }


def deserialize_event(event_data, run_pb2):
    return run_pb2.RunningEvent(
        id=event_data["id"],
        city=event_data["city"],
        weather=event_data["weather"],
        distance=event_data["distance"],
        start_time=event_data["start_time"],
        tags=event_data["tags"],
    )


async def save_state(clients, subscription_counter):
    state = {"subscription_counter": subscription_counter, "clients": {}}

    for client_id, client_data in clients.items():
        client_info = {
            "subscriptions": {},
            "buffer": [serialize_event(event) for event in client_data.buffer],
        }
        for sub_id, sub_data in client_data.subscriptions.items():
            client_info["subscriptions"][str(sub_id)] = {
                "cities": list(sub_data["cities"]),
                "distances": list(sub_data["distances"]),
                "weather_conditions": list(sub_data["weather_conditions"]),
                "tags": list(sub_data["tags"]),
            }
        state["clients"][client_id] = client_info

    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)
    Logger.info("Server state saved to disk.")


def load_state(run_pb2):
    if not os.path.exists(STATE_FILE):
        Logger.info("No previous state found. Starting fresh.")
        return {}, 1

    with open(STATE_FILE, "r") as f:
        state = json.load(f)

    clients = {}
    subscription_counter = state["subscription_counter"]

    for client_id, client_info in state["clients"].items():
        client_data = ClientData()

        for sub_id, sub_data in client_info["subscriptions"].items():
            client_data.subscriptions[int(sub_id)] = {
                "cities": set(sub_data["cities"]),
                "distances": set(sub_data["distances"]),
                "weather_conditions": set(sub_data["weather_conditions"]),
                "tags": set(sub_data["tags"]),
            }

        client_data.buffer = [
            deserialize_event(event, run_pb2) for event in client_info["buffer"]
        ]

        clients[client_id] = client_data

    Logger.info("Server state loaded from disk.")
    return clients, subscription_counter
