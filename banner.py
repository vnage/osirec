
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

OSIREC_BANNER = f"""{CYAN}{BOLD}
     ___       ____  _____ 
    / _ \ _ __/ ___||  ___|
   | | | | '_ \___ \| |_   
   | |_| | |_) |__) |  _|  
    \___/| .__/____/|_|    
         |_|               
{RESET}"""

AUTHORS_LINE = f"{CYAN}Authors: feeraSe & Yarik528{RESET}"
SEPARATOR = "-" * 40


def print_banner():
    print(OSIREC_BANNER)
    print(AUTHORS_LINE)
    print(SEPARATOR)
