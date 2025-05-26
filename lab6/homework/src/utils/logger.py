from colorama import Fore, Style


class Logger:
    @staticmethod
    def admin(message: str):
        print(f"{Fore.LIGHTRED_EX}[ADMIN]: {message}{Style.RESET_ALL}")

    @staticmethod
    def order(message: str):
        print(f"{Fore.GREEN}[ORDER]: {message}{Style.RESET_ALL}")

    @staticmethod
    def confirm(message: str):
        print(f"{Fore.BLUE}[CONFIRM]: {message}{Style.RESET_ALL}")

    @staticmethod
    def sent(message: str):
        print(f"{Fore.CYAN}[SENT]: {message}{Style.RESET_ALL}")

    @staticmethod
    def info(message: str):
        print(f"{Fore.WHITE}[INFO]: {message}{Style.RESET_ALL}")

    @staticmethod
    def receive(message: str):
        print(f"{Fore.MAGENTA}[RECEIVED]: {message}{Style.RESET_ALL}")

    @staticmethod
    def warning(message: str):
        print(f"{Fore.YELLOW}[WARNING]: {message}{Style.RESET_ALL}")

    @staticmethod
    def error(message: str):
        print(f"{Fore.RED}[ERROR]: {message}{Style.RESET_ALL}")

    @staticmethod
    def fflush(message: str):
        print(f"{Fore.WHITE}{message}", end="", flush=True)
