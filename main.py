from auth import register, login
from modules.osint_tools import get_ip_info, check_username, get_whois_info, get_dns_records
from modules.security_tools import check_password_strength, generate_hash
from modules.coding_tools import format_code_snippet, base64_encode, base64_decode

def main():
    print("welcome to the local toolkit!")
    while True:
        choice = input("\nselect action:\n1. register\n2. login\n3. exit\n> ")
        
        if choice == "1":
            l = input("login: ")
            p = input("password: ")
            success, msg = register(l, p)
            print(msg)
            
        elif choice == "2":
            l = input("login: ")
            p = input("password: ")
            success, msg = login(l, p)
            if success:
                print(msg)
                logged_in_menu()
            else:
                print(msg)
                
        elif choice == "3":
            break

def logged_in_menu():
    while True:
        print("\ntools menu:")
        print("1. osint tools")
        print("2. security tools")
        print("3. coding tools")
        print("4. back")
        
        ch = input("> ")
        if ch == "1":
            osint_menu()
        elif ch == "2":
            security_menu()
        elif ch == "3":
            coding_menu()
        elif ch == "4":
            break

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

if __name__ == "__main__":
    main()