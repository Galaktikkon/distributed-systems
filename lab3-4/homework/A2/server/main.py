import asyncio
import json
import grpc
import sys

sys.path.append("./gen")

from gen import run_pb2, run_pb2_grpc
from config.generator import generate_event

subscriptions = {}
subscription_counter = 1
lock = asyncio.Lock()

with open("config/config.json", "r") as f:
    CONFIG = json.load(f)


class RunningService(run_pb2_grpc.RunningServiceServicer):
    async def Subscribe(self, request, context):
        global subscription_counter
        client_id = request.client_id
        cities = set(request.cities)
        distances = set(request.distances)
        tags = set(request.tags)

        async with lock:
            subscription_id = subscription_counter
            subscription_counter += 1
            if client_id not in subscriptions:
                subscriptions[client_id] = {}
            subscriptions[client_id][subscription_id] = {
                "cities": cities,
                "distances": distances,
                "tags": tags,
                "context": context,
            }
            print(
                f"[INFO] New subscription: client_id={client_id}, subscription_id={subscription_id}"
            )

        event_id = 1
        try:
            while True:
                event = generate_event(event_id, CONFIG)
                event_id += 1

                if (
                    (not cities or event.city in cities)
                    and (not distances or event.distance in distances)
                    and (not tags or bool(set(event.tags) & tags))
                ):
                    print(
                        f"[INFO] Sending event {event.id} to client {client_id} (sub_id {subscription_id})"
                    )
                    await context.write(event)

                await asyncio.sleep(1)
        except grpc.aio.AioRpcError as e:
            print(
                f"[WARNING] Client {client_id} (sub_id {subscription_id}) disconnected: {e}"
            )
        finally:
            async with lock:
                if (
                    client_id in subscriptions
                    and subscription_id in subscriptions[client_id]
                ):
                    del subscriptions[client_id][subscription_id]
                    if not subscriptions[client_id]:
                        del subscriptions[client_id]
                print(
                    f"[INFO] Subscription {subscription_id} for client {client_id} removed."
                )

    async def Unsubscribe(self, request, context):
        client_id = request.client_id
        subscription_id = request.subscription_id
        async with lock:
            if (
                client_id in subscriptions
                and subscription_id in subscriptions[client_id]
            ):
                del subscriptions[client_id][subscription_id]
                if not subscriptions[client_id]:
                    del subscriptions[client_id]
                print(
                    f"[INFO] Unsubscribed client {client_id} from subscription {subscription_id}"
                )
                return run_pb2.UnsubscribeResponse(
                    success=True, message="Unsubscribed successfully."
                )
            else:
                print(
                    f"[WARNING] Unsubscribe failed: client {client_id}, subscription {subscription_id} not found."
                )
                return run_pb2.UnsubscribeResponse(
                    success=False, message="Subscription not found."
                )


async def main():
    server = grpc.aio.server()
    run_pb2_grpc.add_RunningServiceServicer_to_server(RunningService(), server)
    server.add_insecure_port("[::]:50051")
    print("[INFO] AsyncIO Running server started on port 50051")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(main())
