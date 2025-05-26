import aio_pika
from utils.exchange_enum import ExchangeEnum
from utils.logger import Logger
from utils.setup_exchange import setup_exchange


class TeamClient:
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
        self.admin_queue = await self.channel.declare_queue(exclusive=True)
        self.confirmation_queue = await self.channel.declare_queue(exclusive=True)
        admin_exchange = await self.channel.get_exchange(ExchangeEnum.ADMIN.value)
        confirm_exchange = await self.channel.get_exchange(ExchangeEnum.CONFIRM.value)

        await self.admin_queue.bind(admin_exchange, routing_key="admin.teams")
        await self.admin_queue.bind(admin_exchange, routing_key="admin.broadcast")
        await self.confirmation_queue.bind(
            confirm_exchange, routing_key=f"confirm.{self.user_name}.*"
        )

    async def start_consuming(self):
        async def admin_callback(message: aio_pika.IncomingMessage):
            async with message.process():
                Logger.admin(f"{message.body.decode()} (route: {message.routing_key})")

        async def confirmation_callback(message: aio_pika.IncomingMessage):
            async with message.process():
                Logger.confirm(
                    f"{message.body.decode()} (route: {message.routing_key})"
                )

        await self.admin_queue.consume(admin_callback)
        await self.confirmation_queue.consume(confirmation_callback)

    async def send_order(self, message: str):
        await self._publish(
            ExchangeEnum.ORDERS_FANOUT.value,
            f"orders.{message}",
            f"Order from {self.user_name}: {message}",
        )

    async def _publish(self, exchange_name, routing_key, message):
        try:
            exchange = await self.channel.get_exchange(exchange_name)
            msg = aio_pika.Message(body=message.encode(), reply_to=self.user_name)
            await exchange.publish(msg, routing_key=routing_key)
            Logger.order(f"Order sent: {message} (route: {routing_key})")
        except Exception as e:
            Logger.error(
                f"[{self.user_name}] Failed to send message: {e} (route: {routing_key})"
            )

    async def close(self):
        await self.channel.close()
        await self.connection.close()
