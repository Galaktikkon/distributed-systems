import aio_pika
from utils.exchange_enum import ExchangeEnum
from utils.logger import Logger
from utils.setup_exchange import setup_exchange


class SupplierClient:
    def __init__(self, user_name: str, products: str | list[str]):
        self.products = [p.strip() for p in products]
        self.connection = None
        self.channel = None
        self.queues: dict[str, aio_pika.Queue] = {}
        self.user_name = user_name

    async def connect(self):
        self.connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
        self.channel = await self.connection.channel()
        await self.setup()

    async def setup(self):
        await setup_exchange(self.channel)
        orders_exchange = await self.channel.get_exchange(
            ExchangeEnum.ORDERS_DIRECT.value
        )
        confirm_exchange = await self.channel.get_exchange(ExchangeEnum.CONFIRM.value)

        self.queue = await self.channel.declare_queue(exclusive=True)
        admin_exchange = await self.channel.get_exchange(ExchangeEnum.ADMIN.value)
        await self.queue.bind(admin_exchange, routing_key="admin.suppliers")
        await self.queue.bind(admin_exchange, routing_key="admin.broadcast")

        for product in self.products:
            queue = await self.channel.declare_queue(
                name=f"orders.{product}", durable=True
            )
            await queue.bind(orders_exchange, routing_key=f"orders.{product}")
            self.queues[product] = queue

        self.confirm_exchange = confirm_exchange

    async def start_consuming(self):
        async def admin_callback(message: aio_pika.IncomingMessage):
            async with message.process():
                Logger.admin(f"{message.body.decode()} (route: {message.routing_key})")

        def order_callback(product):
            async def callback(message: aio_pika.IncomingMessage):
                async with message.process():
                    reply_to = message.reply_to
                    Logger.receive(
                        f"Received order: {message.body.decode()} (route: {message.routing_key})"
                    )
                    Logger.info(f"Processing order: {message.body.decode()}")
                    await self.send_confirmation(product, reply_to)

            return callback

        await self.queue.consume(admin_callback)

        for product, queue in self.queues.items():
            await queue.consume(order_callback(product))

    async def send_confirmation(self, product, reply_to: str | None = None):
        routing_key = f"confirm.{reply_to}.{product}"
        message = f"{self.user_name} confirms order for {product} from {reply_to}"
        try:
            await self.confirm_exchange.publish(
                aio_pika.Message(body=message.encode()), routing_key=routing_key
            )
            Logger.sent(f"Sent confirmation: {message} (route: {routing_key})")
        except Exception as e:
            Logger.error(f"Failed to send confirmation: {e} (route: {routing_key})")

    async def close(self):
        await self.channel.close()
        await self.connection.close()
