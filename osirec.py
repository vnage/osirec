import socket
import urllib.request
import hashlib
import base64
import re
import string
import random
import json
import codecs
from urllib.parse import quote, unquote

# Импортируем баннер из отдельного файла
from banner import print_banner

# code by feeraSe telegram: feeracode.t.me
# code by Yarik528 github: github.com/Yarik528

TLD_COUNTRY_MAP = {
    ".ru": "Russia", ".su": "Soviet Union", ".us": "United States",
    ".uk": "United Kingdom", ".de": "Germany", ".fr": "France",
    ".it": "Italy", ".es": "Spain", ".cn": "China", ".jp": "Japan",
    ".kr": "South Korea", ".in": "India", ".br": "Brazil",
    ".ca": "Canada", ".au": "Australia", ".nl": "Netherlands",
    ".pl": "Poland", ".ua": "Ukraine", ".by": "Belarus",
    ".kz": "Kazakhstan", ".com": "Commercial (Global)",
    ".org": "Organization (Global)", ".net": "Network (Global)",
    ".io": "British Indian Ocean Territory", ".ai": "Anguilla",
    ".me": "Montenegro", ".gov": "Government (US)", ".edu": "Education (US)"
}


def get_tld(domain):
    try:
        parts = domain.lower().split(".")
        if len(parts) >= 2:
            return "." + parts[-1]
        return None
    except Exception:
        return None


def get_country_by_domain(domain):
    tld = get_tld(domain)
    if tld and tld in TLD_COUNTRY_MAP:
        return TLD_COUNTRY_MAP[tld]
    return "Unknown / Generic TLD"


def get_server_headers(url):
    if not url.startswith("http"):
        url = "http://" + url
    try:
        req = urllib.request.Request(url, method='HEAD')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        with urllib.request.urlopen(req, timeout=5) as response:
            headers = dict(response.headers)
            server = headers.get('Server', 'Hidden / Unknown')
            powered_by = headers.get('X-Powered-By', 'Hidden / Unknown')
            content_type = headers.get('Content-Type', 'Unknown')
            return {
                "Server": server,
                "X-Powered-By": powered_by,
                "Content-Type": content_type
            }
    except Exception as e:
        return {"Error": f"Could not fetch headers: {str(e)}"}


def get_ip_info(domain):
    try:
        ip = socket.gethostbyname(domain)
        return {"Domain": domain, "IP Address": ip}
    except socket.gaierror:
        return {"Error": "Could not resolve domain"}


def get_full_web_info(domain):
    result = {}
    result.update(get_ip_info(domain))
    result["Country (TLD)"] = get_country_by_domain(domain)
    result.update(get_server_headers(domain))
    return result


def check_username(username):
    if not username or len(username.strip()) == 0:
        return {"Error": "Username cannot be empty"}

    sites = [
        ("GitHub", "https://github.com/{}"),
        ("Twitter/X", "https://twitter.com/{}"),
        ("Instagram", "https://instagram.com/{}"),
        ("Reddit", "https://www.reddit.com/user/{}"),
        ("Pinterest", "https://pinterest.com/{}"),
        ("TikTok", "https://www.tiktok.com/@{}"),
        ("Telegram", "https://t.me/{}"),
        ("VKontakte", "https://vk.com/{}"),
        ("Odnoklassniki", "https://ok.ru/{}"),
        ("LinkedIn", "https://www.linkedin.com/in/{}"),
        ("YouTube", "https://www.youtube.com/@{}"),
        ("Twitch", "https://www.twitch.tv/{}"),
        ("Steam", "https://steamcommunity.com/id/{}"),
        ("Medium", "https://medium.com/@{}"),
        ("GitLab", "https://gitlab.com/{}")
    ]

    results = {}
    for name, url_template in sites:
        url = url_template.format(username)
        try:
            req = urllib.request.Request(url, method='HEAD')
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            code = urllib.request.urlopen(req, timeout=5).getcode()

            if code == 200:
                results[name] = f"Found - {url}"
            else:
                results[name] = "Not Found"
        except Exception:
            results[name] = "Error / Not Found"

    return results


def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return {"Email": email, "Valid Format": True}
    else:
        return {"Email": email, "Valid Format": False}


def reverse_ip_lookup(ip):
    try:
        host = socket.gethostbyaddr(ip)
        return {"IP": ip, "Hostname": host[0]}
    except Exception:
        return {"IP": ip, "Hostname": "No PTR record found"}


def get_ip_geolocation(ip_address):
    """Определяет примерное местоположение по IP через бесплатный API ip-api.com."""
    # Валидация формата IP
    ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    if not re.match(ip_pattern, ip_address):
        return {"Error": "Invalid IP format. Use: xxx.xxx.xxx.xxx"}

    # Проверка диапазона октетов
    octets = ip_address.split(".")
    for octet in octets:
        if int(octet) > 255:
            return {"Error": "Invalid IP: octets must be 0-255"}

    url = f"http://ip-api.com/json/{ip_address}?fields=status,message,country,regionName,city,lat,lon,isp,as,query"

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Osirec'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())

        if data.get("status") == "success":
            return {
                "IP": data["query"],
                "Country": data["country"],
                "Region": data["regionName"],
                "City": data["city"],
                "Latitude": data["lat"],
                "Longitude": data["lon"],
                "ISP": data["isp"],
                "AS": data["as"]
            }
        else:
            return {"Error": data.get("message", "Invalid IP or reserved range")}

    except urllib.error.URLError as e:
        return {"Error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"Error": f"Geolocation failed: {str(e)}"}


def check_password_strength(password):
    score = 0
    feedback = []
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Too short")
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("No uppercase")
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("No digits")
    if any(c in "!@#$%^&*" for c in password):
        score += 1
    else:
        feedback.append("No special chars")

    strength = f"{score}/4"
    if not feedback:
        feedback.append("Strong")
    return {"Strength": strength, "Details": ", ".join(feedback)}


def generate_password(length=16):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))


def generate_advanced_password():
    print("\n--- Advanced Password Generator ---")
    
    length_input = input("Length (default 16): ").strip() or "16"
    try:
        length = int(length_input)
        if length < 4:
            print("[!] Minimum length is 4")
            return
    except ValueError:
        print("[!] Invalid number")
        return

    use_upper = input("Uppercase A-Z? (y/n, default y): ").lower() != 'n'
    use_lower = input("Lowercase a-z? (y/n, default y): ").lower() != 'n'
    use_digits = input("Digits 0-9? (y/n, default y): ").lower() != 'n'
    use_special = input("Special chars !@#$%^&*? (y/n, default y): ").lower() != 'n'
    use_cyrillic = input("Cyrillic А-Яа-я? (y/n, default n): ").lower() == 'y'

    charset = ""
    if use_upper: charset += string.ascii_uppercase
    if use_lower: charset += string.ascii_lowercase
    if use_digits: charset += string.digits
    if use_special: charset += "!@#$%^&*"
    if use_cyrillic: charset += "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"

    if not charset:
        print("[!] Select at least one character set!")
        return

    password = ''.join(random.choice(charset) for _ in range(length))
    print(f"\n[+] Generated ({length} chars):\n{password}")


def generate_hash(text, algorithm="sha256"):
    try:
        if algorithm == "md5":
            h = hashlib.md5(text.encode()).hexdigest()
        elif algorithm == "sha1":
            h = hashlib.sha1(text.encode()).hexdigest()
        elif algorithm == "sha512":
            h = hashlib.sha512(text.encode()).hexdigest()
        else:
            h = hashlib.sha256(text.encode()).hexdigest()
        return {"Algorithm": algorithm, "Hash": h}
    except Exception as e:
        return {"Error": str(e)}


def format_json(text):
    try:
        parsed = json.loads(text)
        return json.dumps(parsed, indent=4)
    except Exception:
        return "Invalid JSON"


def url_encode(text):
    return quote(text)


def url_decode(text):
    try:
        return unquote(text)
    except Exception:
        return "Invalid URL encoding"


def rot13_safe(text):
    return codecs.encode(text, 'rot_13')


def web_tools_menu():
    while True:
        print("\n--- Web Tools ---")
        print("1. Full Domain Info (IP, Country, Server)")
        print("2. Get IP Address Only")
        print("3. Check Server Headers")
        print("4. Back")

        ch = input("> ")
        if ch == "1":
            domain = input("Enter Domain: ")
            print(json.dumps(get_full_web_info(domain), indent=2))
        elif ch == "2":
            domain = input("Enter Domain: ")
            print(get_ip_info(domain))
        elif ch == "3":
            url = input("Enter URL: ")
            print(json.dumps(get_server_headers(url), indent=2))
        elif ch == "4":
            break


def osint_tools_menu():
    while True:
        print("\n--- Osint Tools ---")
        print("1. Username Check (Social Media)")
        print("2. Validate Email Format")
        print("3. Reverse IP Lookup")
        print("4. IP Geolocation")
        print("5. Back")

        ch = input("> ")
        if ch == "1":
            username = input("Enter Username: ")
            res = check_username(username)
            for k, v in res.items():
                print(f"{k}: {v}")
        elif ch == "2":
            email = input("Enter Email: ")
            print(validate_email(email))
        elif ch == "3":
            ip = input("Enter IP: ")
            print(reverse_ip_lookup(ip))
        elif ch == "4":
            ip = input("Enter IP Address: ")
            result = get_ip_geolocation(ip)
            for k, v in result.items():
                print(f"{k}: {v}")
        elif ch == "5":
            break


def coding_security_menu():
    while True:
        print("\n--- Coding & Security ---")
        print("1. Check Password Strength")
        print("2. Generate Simple Password (Legacy)")
        print("3. Generate Advanced Password (Custom)")
        print("4. Generate Hash (MD5/SHA)")
        print("5. Base64 Encode/Decode")
        print("6. URL Encode/Decode")
        print("7. Format JSON")
        print("8. ROT13 Cipher")
        print("9. Back")

        ch = input("> ")
        if ch == "1":
            pwd = input("Enter Password: ")
            print(check_password_strength(pwd))
        elif ch == "2":
            length = input("Length (default 16): ") or "16"
            try:
                print(generate_password(int(length)))
            except ValueError:
                print("Invalid number")
        elif ch == "3":
            generate_advanced_password()
        elif ch == "4":
            text = input("Enter Text: ")
            algo = input("Algorithm (md5/sha1/sha256/sha512): ") or "sha256"
            print(generate_hash(text, algo))
        elif ch == "5":
            action = input("Encode (1) or Decode (2)? ")
            text = input("Enter Text: ")
            if action == "1":
                print(base64.b64encode(text.encode()).decode())
            else:
                try:
                    print(base64.b64decode(text.encode()).decode())
                except Exception:
                    print("Invalid Base64")
        elif ch == "6":
            action = input("Encode (1) or Decode (2)? ")
            text = input("Enter Text: ")
            if action == "1":
                print(url_encode(text))
            else:
                print(url_decode(text))
        elif ch == "7":
            print("Paste JSON:")
            text = input("")
            print(format_json(text))
        elif ch == "8":
            text = input("Enter Text: ")
            print(rot13_safe(text))
        elif ch == "9":
            break


def main_menu():
    print_banner()

    while True:
        print("\nWelcome To Osirec Toolkit")
        print("1. Web Tools")
        print("2. Osint Tools")
        print("3. Coding & Security")
        print("4. Exit")

        ch = input("> ")
        if ch == "1":
            web_tools_menu()
        elif ch == "2":
            osint_tools_menu()
        elif ch == "3":
            coding_security_menu()
        elif ch == "4":
            break


if __name__ == "__main__":
    main_menu()
