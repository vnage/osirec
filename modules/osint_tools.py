import socket
import urllib.request
import json as py_json

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