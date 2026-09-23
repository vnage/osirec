# banner.py

RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'

OSIREC_BANNER = rf"""{RED}{BOLD}
  ___  ____  _____ 
 / _ \/ ___||  ___|
| | | \___ \| |_   
| |_| |___) |  _|  
 \___/|____/|_|    
                   
{RESET}"""

AUTHORS_LINE = f"{RED}Authors: feeraSe & Yarik528{RESET}"
SEPARATOR = "-" * 40


def print_banner():
    """Выводит приветственный баннер при запуске."""
    print(OSIREC_BANNER)
    print(AUTHORS_LINE)
    print(SEPARATOR)
