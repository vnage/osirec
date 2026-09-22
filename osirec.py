import socket
import urllib.request
import hashlib
import base64

def get_ip_info(domain):
    try:
        ip = socket.gethostbyname(domain)
        return {"domain": domain, "ip": ip}
    except socket.gaierror:
        return {"error": "could not resolve domain"}

def check_username(username):
    sites = [
        "https://github.com/{}",
        "https://twitter.com/{}",
        "https://instagram.com/{}",
        "https://www.reddit.com/user/{}"
    ]
    results = {}
    for site in sites:
        url = site.format(username)
        try:
            code = urllib.request.urlopen(url).getcode()
            if code == 200:
                results[site.split('/')[2]] = "found"
            else:
                results[site.split('/')[2]] = "not found"
        except Exception:
            results[site.split('/')[2]] = "error or not found"
    return results

def get_whois_info(domain):
    try:
        import whois
        w = whois.whois(domain)
        return {
            "registrar": w.registrar,
            "creation_date": str(w.creation_date),
            "country": w.country
        }
    except ImportError:
        return {"error": "python-whois library not installed"}
    except Exception as e:
        return {"error": str(e)}

def get_dns_records(domain):
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT']
    results = {}
    try:
        import dns.resolver
        for rtype in record_types:
            try:
                answers = dns.resolver.resolve(domain, rtype)
                results[rtype] = [str(rdata) for rdata in answers]
            except Exception:
                results[rtype] = []
        return results
    except ImportError:
        return {"error": "dnspython library not installed"}

def check_password_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*" for c in password):
        score += 1
    return f"password strength: {score}/4"

def generate_hash(text, algorithm="sha256"):
    if algorithm == "md5":
        return hashlib.md5(text.encode()).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(text.encode()).hexdigest()
    else:
        return hashlib.sha256(text.encode()).hexdigest()

def format_code_snippet(code, language="python"):
    return f"```{language}\n{code.strip()}\n```"

def base64_encode(text):
    return base64.b64encode(text.encode()).decode()

def base64_decode(text):
    try:
        return base64.b64decode(text.encode()).decode()
    except Exception:
        return "invalid base64 string"

def osint_menu():
    while True:
        print("\nosint submenu:")
        print("1. domain ip info")
        print("2. username check (sherlock-like)")
        print("3. whois lookup")
        print("4. dns records")
        print("5. back")
        
        ch = input("> ")
        if ch == "1":
            domain = input("enter domain: ")
            print(get_ip_info(domain))
        elif ch == "2":
            username = input("enter username: ")
            print(check_username(username))
        elif ch == "3":
            domain = input("enter domain: ")
            print(get_whois_info(domain))
        elif ch == "4":
            domain = input("enter domain: ")
            print(get_dns_records(domain))
        elif ch == "5":
            break

def security_menu():
    while True:
        print("\nsecurity submenu:")
        print("1. check password strength")
        print("2. generate hash")
        print("3. back")
        
        ch = input("> ")
        if ch == "1":
            pwd = input("enter password: ")
            print(check_password_strength(pwd))
        elif ch == "2":
            text = input("enter text: ")
            algo = input("algorithm (md5/sha1/sha256): ") or "sha256"
            print(generate_hash(text, algo))
        elif ch == "3":
            break

def coding_menu():
    while True:
        print("\ncoding submenu:")
        print("1. format code snippet")
        print("2. base64 encode")
        print("3. base64 decode")
        print("4. back")
        
        ch = input("> ")
        if ch == "1":
            code = input("paste code:\n")
            lang = input("language (default python): ") or "python"
            print(format_code_snippet(code, lang))
        elif ch == "2":
            text = input("enter text: ")
            print(base64_encode(text))
        elif ch == "3":
            text = input("enter base64 string: ")
            print(base64_decode(text))
        elif ch == "4":
            break

def tools_menu():
    while True:
        print("\ntools menu:")
        print("1. osint tools")
        print("2. security tools")
        print("3. coding tools")
        print("4. exit")
        
        ch = input("> ")
        if ch == "1":
            osint_menu()
        elif ch == "2":
            security_menu()
        elif ch == "3":
            coding_menu()
        elif ch == "4":
            break

if __name__ == "__main__":
    print("welcome to osirec toolkit!")
    tools_menu()