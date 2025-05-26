import asyncio
import sys

sys.path.append("src")

from cli.base import AsyncCLI
from team.client import TeamClient


class TeamCLI(AsyncCLI):
    def __init__(self, user_name):
        super().__init__(user_name)
        self.client = TeamClient(user_name)

    async def do_order(self, arg):
        """Send order message."""

        product = arg.strip()
        if not product:
            print("Order cannot be empty.")
            return

        await self.client.send_order(product)

    async def do_exit(self, arg=None):
        """Exit the CLI."""
        await super().do_exit(arg)
        await self.client.close()


async def main():
    if len(sys.argv) > 1:
        user_name = sys.argv[1]
    else:
        user_name = input("Enter your team name: ").strip()

    cli = TeamCLI(user_name)
    await cli.client.connect()
    asyncio.create_task(cli.client.start_consuming())
    await cli.cmdloop()


if __name__ == "__main__":
    asyncio.run(main())
