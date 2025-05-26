import aio_pika
from utils.exchange_enum import ExchangeEnum


async def setup_exchange(channel: aio_pika.abc.AbstractChannel):
    orders_direct = await channel.declare_exchange(
        ExchangeEnum.ORDERS_DIRECT.value, type=aio_pika.ExchangeType.DIRECT
    )
    orders_fanout = await channel.declare_exchange(
        ExchangeEnum.ORDERS_FANOUT.value, type=aio_pika.ExchangeType.FANOUT
    )

    await orders_direct.bind(orders_fanout)

    await channel.declare_exchange(
        ExchangeEnum.CONFIRM.value, type=aio_pika.ExchangeType.TOPIC
    )
    await channel.declare_exchange(
        ExchangeEnum.ADMIN.value, type=aio_pika.ExchangeType.TOPIC
    )
