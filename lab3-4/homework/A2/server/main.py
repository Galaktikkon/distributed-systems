import asyncio
import json
import grpc
import sys
import random

sys.path.append("./gen")

from gen import run_pb2, run_pb2_grpc
from config.generator import generate_event
from config.ClientData import ClientData
from utils.Logger import Logger
from utils.snapshotter import snapshot_state, load_state
from utils.validation import is_valid_enum_value

clients, subscription_counter = load_state(run_pb2)

lock = asyncio.Lock()

with open("config/config.json", "r") as f:
    CONFIG = json.load(f)


async def event_generator():
    event_id = 1
    while True:
        event = generate_event(event_id, CONFIG)
        event_id += 1

        distance_name = next(
            (
                name
                for name, val in CONFIG["distances"].items()
                if val == event.distance
            ),
            str(event.distance),
        )
        weather_name = next(
            (name for name, val in CONFIG["weathers"].items() if val == event.weather),
            str(event.weather),
        )

        Logger.event(
            f"Generated event {event.id}: city={event.city}, distance={distance_name}, weather={weather_name}, tags={list(event.tags)}"
        )

        await broadcast_event(event)
        await asyncio.sleep(random.randint(1, 5))


async def broadcast_event(event):
    async with lock:
        for client_id, client_data in clients.items():
            matching_subs = [
                sub
                for sub in client_data.subscriptions.values()
                if (not sub["cities"] or event.city in sub["cities"])
                and (not sub["distances"] or event.distance in sub["distances"])
                and (not sub["tags"] or bool(set(event.tags) & sub["tags"]))
                and (
                    not sub["weather_conditions"]
                    or event.weather in sub["weather_conditions"]
                )
            ]

            if matching_subs:
                if client_data.listening and client_data.active_stream:
                    try:
                        await client_data.active_stream.write(
                            run_pb2.StreamResponse(event=event)
                        )
                        Logger.info(f"Sent event {event.id} to client {client_id}")
                    except grpc.aio.AioRpcError as e:
                        Logger.warning(
                            f"Client {client_id} disconnected during event sending: {e}"
                        )
                        client_data.listening = False
                        client_data.buffer.append(event)
                else:
                    client_data.buffer.append(event)
                    Logger.info(f"Buffered event {event.id} for client {client_id}")


class RunningService(run_pb2_grpc.RunningServiceServicer):
    async def Register(self, request, context):
        client_id = request.client_id
        async with lock:
            if client_id in clients:
                Logger.info(f"Client {client_id} reconnected (existing session)")
                return run_pb2.RegisterResponse(
                    success=True, message="Reconnected to existing session."
                )
            else:
                clients[client_id] = ClientData()
                Logger.info(f"Client {client_id} registered successfully")
                return run_pb2.RegisterResponse(
                    success=True, message="New client registered."
                )

    async def Unregister(self, request, context):
        client_id = request.client_id
        async with lock:
            if client_id in clients:
                del clients[client_id]
                Logger.info(f"Client {client_id} unregistered and data cleared.")
                return run_pb2.UnregisterResponse(
                    success=True, message="Unregistered successfully."
                )
            else:
                Logger.warning(f"Unregister failed: client {client_id} not found.")
                return run_pb2.UnregisterResponse(
                    success=False, message="Client not found."
                )

    async def Subscribe(self, request, context):
        global subscription_counter
        client_id = request.client_id

        invalid_weathers = [
            w
            for w in request.weather_conditions
            if not is_valid_enum_value(run_pb2.WeatherCondition, w)
        ]
        invalid_distances = [
            d
            for d in request.distances
            if not is_valid_enum_value(run_pb2.DistanceType, d)
        ]

        if invalid_weathers or invalid_distances:
            error_msg = ""
            if invalid_weathers:
                error_msg += f"Invalid weather condition(s): {invalid_weathers}. "
            if invalid_distances:
                error_msg += f"Invalid distance type(s): {invalid_distances}. "
            return run_pb2.SubscriptionResponse(
                success=False, subscription_id=0, message=error_msg.strip()
            )

        async with lock:
            if client_id not in clients:
                return run_pb2.SubscriptionResponse(
                    success=False, subscription_id=0, message="Client not registered"
                )

            subscription_id = subscription_counter
            subscription_counter += 1
            clients[client_id].subscriptions[subscription_id] = {
                "cities": set(request.cities),
                "weather_conditions": set(request.weather_conditions),
                "distances": set(request.distances),
                "tags": set(request.tags),
            }
            Logger.info(
                f"Client {client_id} subscribed with subscription_id {subscription_id}"
            )

            return run_pb2.SubscriptionResponse(
                success=True,
                subscription_id=subscription_id,
                message="Subscribed successfully.",
            )

    async def Unsubscribe(self, request, context):
        client_id = request.client_id
        subscription_id = request.subscription_id

        async with lock:
            if (
                client_id in clients
                and subscription_id in clients[client_id].subscriptions
            ):
                del clients[client_id].subscriptions[subscription_id]
                Logger.info(f"Client {client_id} unsubscribed from {subscription_id}")
                return run_pb2.UnsubscribeResponse(
                    success=True, message="Unsubscribed successfully"
                )
            else:
                Logger.warning(
                    f"Unsubscribe failed: client {client_id}, subscription {subscription_id} not found"
                )
                return run_pb2.UnsubscribeResponse(
                    success=False, message="Subscription not found"
                )

    async def EventStream(self, request, context):
        client_id = request.client_id
        async with lock:
            if client_id not in clients:
                Logger.warning(
                    f"Unregistered client {client_id} tried to connect EventStream"
                )
                return

            clients[client_id].active_stream = context
            clients[client_id].listening = True
            Logger.info(f"Client {client_id} started listening")

            # buffer handler
            buffer_size = len(clients[client_id].buffer)
            if buffer_size > 0:
                await context.write(
                    run_pb2.StreamResponse(
                        buffered_info=run_pb2.BufferedEventInfo(
                            buffered_count=buffer_size
                        )
                    )
                )
                Logger.info(
                    f"Client {client_id} has {buffer_size} buffered events, sending them now..."
                )
                for event in clients[client_id].buffer:
                    await context.write(run_pb2.StreamResponse(event=event))
                    await asyncio.sleep(1)
                clients[client_id].buffer.clear()

        try:
            while True:
                await asyncio.sleep(1)
        except grpc.aio.AioRpcError as e:
            Logger.warning(f"Client {client_id} disconnected: {e}")
        finally:
            async with lock:
                if client_id in clients:
                    clients[client_id].listening = False
                    clients[client_id].active_stream = None
                    Logger.info(f"Client {client_id} stopped listening")


async def main():
    server = grpc.aio.server(
        options=[
            ("grpc.keepalive_time_ms", 10000),
            ("grpc.keepalive_timeout_ms", 5000),
            ("grpc.keepalive_permit_without_calls", True),
        ]
    )

    run_pb2_grpc.add_RunningServiceServicer_to_server(RunningService(), server)
    server.add_insecure_port("[::]:50051")
    Logger.init("AsyncIO Running server started on port 50051")

    saver_coro = asyncio.create_task(snapshot_state(clients, subscription_counter, 10))
    event_coro = asyncio.create_task(event_generator())

    await server.start()

    await server.start()

    try:
        await server.wait_for_termination()
    except (asyncio.CancelledError, KeyboardInterrupt):
        Logger.warning("Shutdown requested. Stopping server gracefully...")
        await server.stop(5)
        event_coro.cancel()
        saver_coro.cancel()
        await asyncio.gather(event_coro, saver_coro, return_exceptions=True)
        Logger.info("Server shutdown complete.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        Logger.warning("KeyboardInterrupt caught, exiting...")
