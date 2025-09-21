from enum import Enum
from settings import Settings

class Colors(str, Enum):
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'


def color_text(color: Enum, text: str) -> str:
    return f'{color.value}{text}{Colors.RESET.value}'
