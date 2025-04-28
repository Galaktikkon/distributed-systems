from colorama import Fore, Style, init

init(autoreset=True)


class Logger:
    @staticmethod
    def info(message: str):
        print(f"{Fore.WHITE}[INFO] {message}{Style.RESET_ALL}")

    @staticmethod
    def warning(message: str):
        print(f"{Fore.RED}[WARNING] {message}{Style.RESET_ALL}")

    @staticmethod
    def init(message: str):
        print(f"{Fore.YELLOW}[INIT] {message}{Style.RESET_ALL}")

    @staticmethod
    def buffer(message: str):
        print(f"{Fore.BLUE}[BUFFER] {message}{Style.RESET_ALL}")

    @staticmethod
    def event(message: str):
        print(f"{Fore.GREEN}[EVENT GENERATED] {message}{Style.RESET_ALL}")
