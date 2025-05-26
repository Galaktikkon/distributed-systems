import aio_pika
from utils.exchange_enum import ExchangeEnum
from utils.logger import Logger
from utils.setup_exchange import setup_exchange


class AdminClient:
    def __init__(self, user_name):
        self.user_name = user_name
        self.connection = None
        self.channel = None
        self.queue = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
        self.channel = await self.connection.channel()
        await self.setup()

    async def setup(self):
        await setup_exchange(self.channel)
        self.queue = await self.channel.declare_queue(exclusive=True)
        confirm_exchange = await self.channel.get_exchange(ExchangeEnum.CONFIRM.value)
        orders_copy_exchange = await self.channel.get_exchange(
            ExchangeEnum.ORDERS_FANOUT.value
        )

        await self.queue.bind(confirm_exchange, routing_key="#")
        await self.queue.bind(
            orders_copy_exchange,
            routing_key="#",
        )

    async def start_consuming(self):
        async def callback(message: aio_pika.IncomingMessage):
            async with message.process():
                Logger.info(f"{message.body.decode()} ({message.routing_key})")

        await self.queue.consume(callback)

    async def send_teams(self, message: str):
        await self._publish("admin.teams", message)

    async def send_suppliers(self, message: str):
        await self._publish("admin.suppliers", message)

    async def send_broadcast(self, message: str):
        await self._publish("admin.broadcast", message)

    async def _publish(self, routing_key, message):
        try:
            exchange = await self.channel.get_exchange(ExchangeEnum.ADMIN.value)

            await exchange.publish(
                aio_pika.Message(body=message.encode()),
                routing_key=routing_key,
            )
            Logger.sent(f"Message sent: {message} (route: {routing_key})")
        except Exception as e:
            Logger.error(f"Failed to send message: {e}")

    async def close(self):
        await self.channel.close()
        await self.connection.close()
