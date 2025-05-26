from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from utils.logger import Logger


class AsyncCLI:
    prompt = "> "

    def __init__(self, user_name):
        self.user_name = user_name
        self.running = True
        self.prompt = f"({user_name}) "
        self.history = InMemoryHistory()
        self.session = PromptSession(history=self.history)

    async def do_exit(self, arg=None):
        """Exit the CLI."""
        Logger.info(f"[{self.user_name}] Exiting CLI.")
        self.running = False

    async def do_clear(self, arg=None):
        """Clear the console."""
        import os

        os.system("cls" if os.name == "nt" else "clear")

    async def do_help(self, arg=None):
        """Show available commands."""
        print("Available commands:\n")
        for attr in dir(self):
            if attr.startswith("do_"):
                name = attr[3:]
                doc = getattr(self, attr).__doc__
                print(
                    f"{name:<15} - {doc.strip().splitlines()[0] if doc else '(no description)'}"
                )

    async def cmdloop(self):
        await self.do_help()
        while self.running:
            try:
                command_line = await self.session.prompt_async(self.prompt)
                if not command_line.strip():
                    continue

                command, *args = command_line.strip().split()
                method = getattr(self, f"do_{command}", None)

                if method and callable(method):
                    await method(" ".join(args))
                else:
                    print(f"Unknown command: {command}")

            except (EOFError, KeyboardInterrupt):
                print("\nExiting...")
                await self.do_exit()
