from colorama import Fore, Style

def color(level):
    return {
        "CRITICAL": Fore.RED,
        "HIGH": Fore.MAGENTA,
        "MEDIUM": Fore.YELLOW,
        "LOW": Fore.GREEN
    }.get(level, Fore.WHITE)

def print_vuln(url, v):
    c = color(v["severity"])
    print(c + f"""
[!] BUG DITEMUKAN
 Website : {url}
 Tipe    : {v['type']}
 Level   : {v['severity']}
 Param   : {v['param']}
 Payload : {v['payload']}
""" + Style.RESET_ALL)

def print_summary(stats):
    print("\n[ RINGKASAN ]")
    for k,v in stats.items():
        print(f"{k} : {v}")
