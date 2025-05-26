import asyncio
import sys

sys.path.append("src")

from cli.base import AsyncCLI
from supplier.client import SupplierClient


class SupplierCLI(AsyncCLI):
    def __init__(self, user_name, products):
        super().__init__(user_name)
        self.client = SupplierClient(user_name, products)

    async def do_exit(self, arg=None):
        """Exit the CLI."""
        await super().do_exit(arg)
        await self.client.close()


async def main():
    if len(sys.argv) > 2:
        user_name = sys.argv[1]
        products = sys.argv[2].split(",")
    else:
        user_name = input("Enter your supplier name: ").strip()
        products = input("Enter products separated by commas: ").strip().split(",")

    cli = SupplierCLI(user_name, products)
    await cli.client.connect()
    asyncio.create_task(cli.client.start_consuming())
    await cli.cmdloop()


if __name__ == "__main__":
    asyncio.run(main())
