import asyncio
import sys


sys.path.append("src")

from cli.base import AsyncCLI
from admin.client import AdminClient


class AdminCLI(AsyncCLI):
    def __init__(self, user_name):
        super().__init__(user_name)
        self.client = AdminClient(user_name)

    async def do_teams(self, arg: str):
        """Send message to teams."""

        message = arg.strip()
        if not message:
            print("Message cannot be empty.")
            return

        await self.client.send_teams(message)

    async def do_suppliers(self, arg: str):
        """Send message to suppliers."""

        message = arg.strip()
        if not message:
            print("Message cannot be empty.")
            return

        await self.client.send_suppliers(message)

    async def do_broadcast(self, arg: str):
        """Broadcast message to everyone."""

        message = arg.strip()
        if not message:
            print("Message cannot be empty.")
            return
        await self.client.send_broadcast(message)

    async def do_exit(self, arg=None):
        """Exit the CLI."""
        await super().do_exit()
        await self.client.close()


async def main():
    if len(sys.argv) > 1:
        user_name = sys.argv[1]
    else:
        user_name = "admin"

    cli = AdminCLI(user_name)
    await cli.client.connect()
    asyncio.create_task(cli.client.start_consuming())
    await cli.cmdloop()


if __name__ == "__main__":
    asyncio.run(main())
