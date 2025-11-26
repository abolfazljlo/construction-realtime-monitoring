# Simple ANSI color utilities for styled prints
class Log:
    RESET = "\033[0m"
    BOLD = "\033[1m"

    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"

    @staticmethod
    def info(msg: str):
        print(f"{Log.CYAN}{Log.BOLD}ℹ [NotificationService] {msg}{Log.RESET}")

    @staticmethod
    def success(msg: str):
        print(f"{Log.GREEN}{Log.BOLD}✔ [NotificationService] {msg}{Log.RESET}")

    @staticmethod
    def warn(msg: str):
        print(f"{Log.YELLOW}{Log.BOLD}⚠ [NotificationService] {msg}{Log.RESET}")

    @staticmethod
    def error(msg: str):
        print(f"{Log.RED}{Log.BOLD}✘ [NotificationService] {msg}{Log.RESET}")
