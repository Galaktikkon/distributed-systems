from enum import Enum


class ExchangeEnum(Enum):
    ORDERS_DIRECT = "orders_direct"
    ORDERS_FANOUT = "orders_fanout"
    CONFIRM = "confirm"
    ADMIN = "admin"
