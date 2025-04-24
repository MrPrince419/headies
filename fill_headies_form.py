import requests
import random
import string
import time
import logging
import sys
import threading
import queue
import signal
import msvcrt
import platform
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler('form_submission.log')]
)
logger = logging.getLogger(__name__)

# Configuration constants
HEADIES_URL = "https://theheadies.com/17th-headies-voting/"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSf07bxYCZtdArnh_gqJp3VJLsgCDzfws3EfwJyh0e0hgRUrtQ/formResponse?embedded=true"
SUBMISSION_DELAY = (1.5, 3.5)      # Extended delay for realism
PAGE_VIEW_DELAY = (0.8, 2.5)       # Simulate page load
CLICK_DELAY = (0.5, 1.2)           # Simulate click
POST_SUBMISSION_DELAY = (0.3, 1.0) # Simulate post-submit pause
LONG_PAUSE_INTERVAL = 50           # Occasional long pause every ~50 submissions
LONG_PAUSE_CHANCE = 0.15           # 15% chance of long pause
LONG_PAUSE_DELAY = (8.0, 20.0)     # Longer pauses for human-like behavior
VPN_SWITCH_MIN = 40                # Minimum submissions before VPN switch
VPN_SWITCH_MAX = 120               # Maximum submissions before VPN switch
VPN_SWITCH_TIMEOUT_SECONDS = 1200  # 20 minutes timeout for VPN switch
REQUEST_TIMEOUT = 20               # Extended timeout for form submission
MAX_RETRIES = 5                    # Increased retry attempts
SESSION_RESTART_THRESHOLD = 3      # Restart session after consecutive failures
STATS_FILE = Path('submission_stats.json')
BATCH_SIZE = 100

# Identity uniqueness tracking
USED_FILE = Path('used_identities.json')
UNIQUENESS_WINDOW = timedelta(hours=2)

# Success/failure detection markers
SUCCESS_MARKERS = [
    "Thank you for submitting",
    "Your response has been recorded",
    "freebirdFormviewerViewResponseConfirmationMessage"
]
ERROR_MARKERS = ["error", "problem", "try again"]

# Rate limiting protection
RATE_LIMIT_COUNT_WINDOW = timedelta(hours=1)
MAX_RATE_LIMITS_BEFORE_THROTTLE = 3
THROTTLE_INCREASE_PERCENT = 20

# Pre-defined answers (Votes for the awards)
ANSWERS = {
    "entry.947384516": "LLONA",
    "entry.1109291335": "JOHNNY DRILLE - FOR YOU",
    "entry.645264712": "LONDON – OZEBA",
    "entry.703242641": "CAST FEAT ODUMODUBLVCK – SHALLIPOPI",
    "entry.921148300": "NA MONEY – DAVIDO FT. CAVEMEN, ANGELIQUE KIDJO (DAMMY TWITCH)",
    "entry.1600242014": "CAST - SHALLIPOPI FT ODUMODUBLVCK",
    "entry.1217745529": "SHALLIPOPI – CAST (FT. ODUMODUBLVCK)",
    "entry.1880101790": "BIG BALLER – FLAVOR",
    "entry.1464754687": "YOU DO THIS ONE - MERCY CHINWO",
    "entry.100312896": "OZEBA – REMA",
    "entry.438779784": "BLACK SHERIF (GHANA)",
    "entry.394625345": "BIEN (KENYA)",
    "entry.784920556": "ABU (EYGPT)",
    "entry.1919105292": "KELLY KAY (MALAWI)",
    "entry.22625561": "KOCEE (CAMEROUN)",
    "entry.1289506477": "CHRIS BROWN - HMMM (FT. DAVIDO)",
    "entry.515473935": "ODUMODUBLVCK",
    "entry.1958691022": "HEIS – REMA",
    "entry.139835279": "REMA",
    "entry.1256911908": "OZEBA – REMA",
    "entry.60061246": "HEIS – REMA",
    "entry.942648837": "REMA"
}

# Data for realistic identity generation
DATA_SOURCES = ["Nigeria", "Ghana", "Kenya", "South Africa"]
DATA_SOURCE_WEIGHTS = [0.45, 0.25, 0.15, 0.15]
NAME_PREFIXES = {
    "Nigeria": ["Oluwa", "Ade", "Chi", "Eme", "Ife", "Obi", "Ada", "Funmi", "Tolu", "Segun", "Bola", "Yemi", "Timi", "Dayo", "Fola"],
    "Ghana": ["Kwame", "Kofi", "Ama", "Abena", "Efua", "Afua", "Yaw", "Adjo", "Dzifa", "Fifi", "Akua", "Kwesi", "Ato", "Ekow", "Kojo"],
    "Kenya": ["Wanji", "Kamau", "Njeri", "Odhia", "Otien", "Akiny", "Kipch", "Mutho", "Kiman", "Weru", "Githu", "Otieno", "Wangui", "Mwangi", "Nyong"],
    "South Africa": ["Thabo", "Sipho", "Themba", "Nomvu", "Bless", "Mandl", "Lungi", "Busis", "Nkosi", "Thandi", "Bheki", "Vuyo", "Lebo", "Zola", "Kagiso"]
}
NAME_SUFFIXES = {
    "Nigeria": ["seun", "oma", "bayo", "yinka", "di", "gozi", "nna", "isha", "lake", "tunde", "tosin", "biyi", "wale", "funmi", "kemi"],
    "Ghana": ["me", "fi", "ma", "na", "si", "fua", "wo", "joa", "fa", "zi", "tom", "ku", "fo", "lani", "poku"],
    "Kenya": ["ku", "mau", "ri", "mbo", "eno", "nyi", "oge", "ni", "ani", "bet", "thi", "ngi", "ito", "uki", "umba"],
    "South Africa": ["bo", "pho", "mba", "la", "sing", "dla", "ngi", "so", "dazo", "ni", "ko", "kazi", "zo", "vele", "thwa"]
}
PHONE_BASES = {"Nigeria": "+234", "Ghana": "+233", "Kenya": "+254", "South Africa": "+27"}
PHONE_MIDDLE_RANGES = {
    "Nigeria": [f"{i:03d}" for i in range(700, 920)],
    "Ghana": [f"{i:03d}" for i in range(200, 600)],
    "Kenya": [f"{i:03d}" for i in range(700, 999)],
    "South Africa": [f"{i:02d}{j}" for i in range(60, 100) for j in range(0, 10)]
}
EMAIL_PROVIDERS = {
    "common": ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "live.com", "protonmail.com", "mail.com", "icloud.com"],
    "Nigeria": ["yahoo.com.ng", "gmail.com", "rocketmail.com", "naij.com", "live.com"],
    "Ghana": ["yahoo.com.gh", "gmail.com", "vodafone.com.gh", "outlook.com", "hotmail.com"],
    "Kenya": ["yahoo.co.ke", "gmail.com", "safaricom.co.ke", "hotmail.co.ke", "live.com"],
    "South Africa": ["yahoo.co.za", "gmail.com", "vodacom.co.za", "mweb.co.za", "telkomsa.net"]
}
RANDOM_WORDS = ["sky", "blue", "star", "cool", "fresh", "happy", "lucky", "great", "swift", "bright", "clever", "elite"]
BIRTH_YEARS = [str(year) for year in range(1980, 2006)]

# Browser user agents for rotation
USER_AGENTS = [
    # Windows Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    # Windows Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
    # Windows Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
    # Mac Safari
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    # Mac Chrome
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    # Mac Firefox
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:129.0) Gecko/20100101 Firefox/129.0",
    # Mobile Android
    "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.36",
    # iOS
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/133.0.0.0 Mobile/15E148 Safari/604.1"
]

# HTTP header configurations
ACCEPT_LANGUAGES = [
    "en-US,en;q=0.9", "en-GB,en;q=0.8", "fr-FR,fr;q=0.9", "es-ES,es;q=0.8", "de-DE,de;q=0.9",
    "en-US,en;q=0.8,es;q=0.6", "fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4", "en-GB,en;q=0.9,fr;q=0.8",
    "en-CA,en;q=0.9,fr-CA;q=0.8", "en-AU,en;q=0.9", "en-NZ,en;q=0.9", "en-ZA,en;q=0.9",
    "en-NG,en;q=0.9", "en-GH,en;q=0.9", "en-KE,en;q=0.9", "fr-CA,fr;q=0.9,en;q=0.8"
]

ACCEPT_VALUES = [
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "text/html,*/*;q=0.8",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
]

ACCEPT_ENCODING = [
    "gzip, deflate", "gzip, deflate, br", "identity", 
    "gzip, deflate, br, zstd", "br, gzip, deflate"
]

HEADIES_REFERERS = [
    "https://theheadies.com/",
    "https://theheadies.com/17th-headies-voting/",
    "https://theheadies.com/vote/",
    "https://theheadies.com/nominees/",
    "https://theheadies.com/awards/",
    "https://theheadies.com/about/",
    "https://www.google.com/search?q=headies+awards+voting",
    "https://twitter.com/The_Headies",
    "https://www.instagram.com/the_headies/"
]

# Form token values
FBZX_TOKENS = [
    "-3841158419742299136", 
    "-3841158410897299136",
    "-3841158419742278136",
    "-3841158410742299136",
    "-3841157410597299136",
    "-3840158419742299136",
    "-3841158419742109136",
    "-3841158419742299137",
    "-3841158418742299136",
    "-3841158419752299136"
]

# Thread-safe global state
stop_event = threading.Event()
total_submissions = 0
successful_submissions = 0
last_vpn_switch_time = time.time()
stats_lock = threading.Lock()
consecutive_failures = 0
vpn_switch_in_progress = False
last_vpn_switch_submissions = 0  # Initialize to 0 (was -VPN_SWITCH_MIN, causing error)

# Rate limiting tracking
rate_limit_hits = []
current_submission_delay = SUBMISSION_DELAY

# Identity uniqueness tracking
used_identities = []

# Advanced data generation functions
def generate_name(data_source: str) -> str:
    """Generate realistic name based on locale"""
    if random.random() < 0.25:  # Sometimes just use first name
        return random.choice(NAME_PREFIXES[data_source]).capitalize()
    
    prefix = random.choice(NAME_PREFIXES[data_source])
    suffix = random.choice(NAME_SUFFIXES[data_source])
    return f"{prefix}{suffix}".capitalize()

def generate_phone(data_source: str) -> str:
    """Generate phone number for a given locale"""
    base = PHONE_BASES[data_source]
    middle = random.choice(PHONE_MIDDLE_RANGES[data_source])
    suffix = ''.join(random.choices(string.digits, k=7))
    return f"{base}{middle}{suffix}"

def generate_email(first_name: str, last_name: str, data_source: str) -> str:
    """Generate realistic email based on name"""
    # Randomly select base pattern
    pattern = random.choice([
        lambda: f"{first_name.lower()}{random.choice(['', '.'])}{last_name.lower()}",
        lambda: f"{first_name.lower()}{random.choice(['_', '.', '-'])}{last_name[0].lower()}",
        lambda: f"{first_name[0].lower()}{random.choice(['_', '.', '-'])}{last_name.lower()}",
        lambda: f"{last_name.lower()}{random.choice(['_', '.', '-'])}{first_name.lower()}",
        lambda: f"{first_name.lower()}{random.randint(1, 9999)}"
    ])
    
    base = pattern()
    
    # Sometimes add year, word or digit
    if random.random() < 0.4:
        modifier = random.choice(BIRTH_YEARS + RANDOM_WORDS)
        separator = random.choice([".", "_", "-", ""])
        base = f"{base}{separator}{modifier}"
    
    # Sometimes add random digits
    if random.random() < 0.3:
        base = f"{base}{random.randint(1, 999)}"
    
    # Select email provider with bias for regional ones
    provider_pool = "common" if random.random() < 0.7 else data_source
    provider = random.choice(EMAIL_PROVIDERS[provider_pool])
    
    return f"{base}@{provider}"

def generate_form_data() -> Dict[str, str]:
    """Generate complete form data with randomized personal info but preset answers"""
    global used_identities
    
    try:
        # First, load, clean up and update used identities cache
        if not used_identities:
            used_identities = load_used_identities()
        used_identities = cleanup_used_identities(used_identities)
        
        # Generate unique identity that hasn't been used in the last 2 hours
        collision_count = 0
        while True:
            # Select data source with weight
            data_source = random.choices(DATA_SOURCES, weights=DATA_SOURCE_WEIGHTS)[0]
            
            # Generate name components
            first_name = generate_name(data_source)
            last_name = generate_name(data_source)
            full_name = f"{first_name} {last_name}"
            
            # Generate contact info
            email = generate_email(first_name, last_name, data_source)
            phone = generate_phone(data_source)
            
            # Check for collision with recently used identities
            collision = any(
                rec['name'] == full_name or rec['email'] == email or rec['phone'] == phone
                for rec in used_identities
            )
            
            if not collision:
                # No collision, store this identity and continue
                used_identities.append({
                    'name': full_name,
                    'email': email,
                    'phone': phone,
                    'timestamp': datetime.now()
                })
                save_used_identities(used_identities)
                break
            
            collision_count += 1
            if collision_count > 10:
                logger.warning(f"Generated {collision_count} collisions. Consider clearing identity cache.")
        
        # Additional hidden form values for realism
        timestamp = int(time.time() * 1000) + random.randint(-10000, 10000)
        dlut = timestamp + random.randint(-5000, 5000)
        
        # Create complete form data
        form_data = {
            "entry.26149397": full_name,             # Name field
            "emailAddress": email,                   # Email field
            "entry.1018684809": phone,               # Phone field
            **ANSWERS,                               # All voting choices
            "dlut": str(dlut),                       # Random timestamp
            "fvv": random.choice(["0", "1"]),        # Form version validation
            "pageHistory": random.choice(["0", "0,1", "0,1,2"]),  # Page history
            "submissionTimestamp": str(timestamp),   # Submission time
            "fbzx": random.choice(FBZX_TOKENS)       # Form identifier from expanded pool
        }
        
        # Add sentinel fields (helps Google track selection state)
        for key in ANSWERS.keys():
            form_data[f"{key}_sentinel"] = ""
        
        logger.debug(f"Generated unique data: {full_name} | {email}")
        return form_data, full_name, email, phone
    except Exception as e:
        logger.error(f"Error generating form data: {str(e)}")
        raise

def generate_http_headers() -> Dict[str, str]:
    """Generate realistic HTTP headers with proper browser fingerprinting"""
    user_agent = random.choice(USER_AGENTS)
    
    # Create a custom X-Forwarded-For to simulate proxy
    x_forwarded = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
    
    # Chrome-based UA gets Chrome-specific headers
    chrome_based = "Chrome" in user_agent and "Edg" not in user_agent
    firefox_based = "Firefox" in user_agent
    safari_based = "Safari" in user_agent and "Chrome" not in user_agent
    mobile = "Mobile" in user_agent or "iPhone" in user_agent
    
    headers = {
        "User-Agent": user_agent,
        "Accept": random.choice(ACCEPT_VALUES),
        "Accept-Language": random.choice(ACCEPT_LANGUAGES),
        "Accept-Encoding": random.choice(ACCEPT_ENCODING),
        "Referer": random.choice(HEADIES_REFERERS),
        "Origin": "https://theheadies.com",
        "Connection": random.choice(["keep-alive", "close"]),
        "DNT": random.choice(["1", "0"]),
        "Upgrade-Insecure-Requests": "1",
        "X-Forwarded-For": x_forwarded,
        "Cache-Control": random.choice(["no-cache", "max-age=0", "no-store"]),
    }
    
    # Browser-specific headers
    if chrome_based:
        headers["sec-ch-ua"] = '"Google Chrome";v="133", "Not-A.Brand";v="8", "Chromium";v="133"'
        headers["sec-ch-ua-mobile"] = "?0" if not mobile else "?1"
        headers["sec-ch-ua-platform"] = '"Windows"' if "Windows" in user_agent else '"macOS"'
    
    if firefox_based:
        headers["TE"] = "trailers"
    
    if safari_based:
        headers["X-Apple-Device"] = random.choice(["iPhone", "iPad", "MacBook"])
    
    # Mobile-specific headers
    if mobile:
        headers["Viewport-Width"] = str(random.choice([375, 390, 414, 428]))
        
    # Cookie detection evasion
    if random.random() < 0.5:
        headers["Cookie"] = "NID=511=eAsdpiUASDFjkl345sdflIIasdf; 1P_JAR=2023-09-01-14"
        
    return headers

def shuffle_headers_order(headers: Dict[str, str]) -> Dict[str, str]:
    """Randomize the order of headers to avoid fingerprinting."""
    items = list(headers.items())
    random.shuffle(items)
    return dict(items)

def create_prepared_request(session: requests.Session, url: str, method: str = "GET", 
                            data: Dict = None, headers: Dict = None) -> requests.PreparedRequest:
    """Create a prepared request with randomized header order."""
    # Create a request with our parameters
    req = requests.Request(method, url, data=data, headers=headers)
    
    # Prepare the request
    prepped = session.prepare_request(req)
    
    # Get the current headers and shuffle them
    current_headers = dict(prepped.headers)
    shuffled_headers = shuffle_headers_order(current_headers)
    
    # Replace the headers with shuffled ones
    prepped.headers.clear()
    for k, v in shuffled_headers.items():
        prepped.headers[k] = v
        
    return prepped

def delay(delay_range: Tuple[float, float]) -> None:
    """Sleep for a random time within range, but check for stop event"""
    delay = random.uniform(*delay_range)
    steps = max(1, int(delay * 10))
    step_time = delay / steps
    
    for _ in range(steps):
        if stop_event.is_set():
            break
        time.sleep(step_time)

def input_thread(q, stop_event):
    """Thread to capture user input for VPN switching"""
    try:
        while not stop_event.is_set():
            user_input = input().strip().lower()
            q.put(user_input)
            break  # Exit after one input
    except (EOFError, Exception) as e:
        if not stop_event.is_set():  # Only log if not stopped intentionally
            logger.warning(f"Error in input thread: {str(e)}")
        q.put("ok")  # Fallback to auto-continue

def vpn_switch_prompt() -> None:
    """Prompt user to switch VPN and wait for confirmation"""
    global last_vpn_switch_time, vpn_switch_in_progress
    
    logger.info("Switch VPN now. Type 'ok' to continue (auto-continues in 20 minutes)...")
    print("Please switch VPN servers now. Type 'ok' to continue, or wait 20 minutes for auto-continue.")
    
    input_buffer = ""
    start_time = time.time()
    
    if platform.system() == "Windows":
        # Windows-specific input handling
        while time.time() - start_time < VPN_SWITCH_TIMEOUT_SECONDS and not stop_event.is_set():
            if msvcrt.kbhit():
                char = msvcrt.getch().decode('utf-8', errors='ignore')
                if char == '\r' and input_buffer.strip().lower() == "ok":
                    logger.info("VPN switch confirmed")
                    last_vpn_switch_time = time.time()
                    vpn_switch_in_progress = False
                    return
                input_buffer += char
            time.sleep(0.1)
    else:
        # Non-Windows systems
        try:
            # Create a queue and thread for non-blocking input
            q = queue.Queue()
            thread = threading.Thread(target=input_thread, args=(q, stop_event), daemon=True)
            thread.start()
            
            while time.time() - start_time < VPN_SWITCH_TIMEOUT_SECONDS and not stop_event.is_set():
                if not q.empty():
                    user_input = q.get_nowait()
                    if user_input == "ok":
                        logger.info("VPN switch confirmed")
                        last_vpn_switch_time = time.time()
                        vpn_switch_in_progress = False
                        return
                time.sleep(0.5)
        except Exception as e:
            logger.error(f"Error in VPN prompt: {e}")
    
    # Timeout occurred
    logger.info("No VPN input within 20 minutes. Continuing automatically...")
    last_vpn_switch_time = time.time()
    vpn_switch_in_progress = False

def log_stats() -> None:
    """Log and save statistics about submissions"""
    with stats_lock:
        success_rate = (successful_submissions / total_submissions * 100) if total_submissions > 0 else 0
        logger.info(f"Stats: Total={total_submissions}, Success={successful_submissions}, Rate={success_rate:.1f}%")
        try:
            with STATS_FILE.open('w') as f:
                json.dump({
                    'total_submissions': total_submissions,
                    'successful_submissions': successful_submissions,
                    'success_rate': success_rate,
                    'last_update': datetime.now().isoformat()
                }, f, indent=2)
        except IOError as e:
            logger.error(f"Failed to save stats: {e}")

def load_used_identities():
    """Load previously used identities, respecting the 2-hour window"""
    if not USED_FILE.exists():
        return []
    try:
        with USED_FILE.open('r') as f:
            data = json.load(f)
        # Convert ISO timestamps back to datetime
        for rec in data:
            rec['timestamp'] = datetime.fromisoformat(rec['timestamp'])
        return data
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        logger.error(f"Error loading used identities: {e}")
        # If file is corrupted, better to start fresh than crash
        return []

def save_used_identities(records):
    """Save used identities for future runs"""
    try:
        # Convert datetimes to ISO for JSON
        to_dump = [
            {**rec, 'timestamp': rec['timestamp'].isoformat()}
            for rec in records
        ]
        with USED_FILE.open('w') as f:
            json.dump(to_dump, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving used identities: {e}")

def cleanup_used_identities(records):
    """Remove identities older than the uniqueness window"""
    cutoff = datetime.now() - UNIQUENESS_WINDOW
    return [rec for rec in records if rec['timestamp'] > cutoff]

def is_success(response):
    """Enhanced success detection logic"""
    text = response.text.lower()
    if response.status_code != 200:
        return False
    
    # Check for known success markers
    if any(marker.lower() in text for marker in SUCCESS_MARKERS):
        return True
    
    # Check for error indicators
    if any(marker in text for marker in ERROR_MARKERS):
        return False
    
    # Fallback: verify response looks like a thank-you page (has reasonable content)
    return len(text) > 5000

def check_rate_limits():
    """Check if we need to throttle based on recent rate limit hits"""
    global rate_limit_hits, current_submission_delay
    
    # Clean up old rate limit hits
    cutoff = datetime.now() - RATE_LIMIT_COUNT_WINDOW
    rate_limit_hits = [timestamp for timestamp in rate_limit_hits if timestamp > cutoff]
    
    # If we've hit too many rate limits recently, increase delay
    if len(rate_limit_hits) >= MAX_RATE_LIMITS_BEFORE_THROTTLE:
        old_min, old_max = current_submission_delay
        increase = 1 + (THROTTLE_INCREASE_PERCENT / 100)
        new_min = old_min * increase
        new_max = old_max * increase
        current_submission_delay = (new_min, new_max)
        
        logger.warning(f"Too many rate limits ({len(rate_limit_hits)}). Increasing delay to {current_submission_delay}")
        # Reset counter after throttling
        rate_limit_hits = rate_limit_hits[1:]  # Remove oldest hit

def submit_form(session: requests.Session, batch_number: int, submission_number: int) -> bool:
    """Submit a form with random data but consistent answers"""
    global total_submissions, successful_submissions, consecutive_failures, rate_limit_hits
    
    # Initial delays to simulate user page loading
    delay(PAGE_VIEW_DELAY)
    if stop_event.is_set():
        return False
    
    try:
        # Generate form data and profile info (unpacking phone as requested)
        form_data, full_name, email, phone = generate_form_data()
        
        # Generate realistic browser headers with randomized order
        headers = generate_http_headers()
        
        # Simulate real user clicking around
        delay(CLICK_DELAY)
        if stop_event.is_set():
            return False
        
        # First visit the main headies page to set cookies
        try:
            # Use prepared request with shuffled headers for better stealth
            prepped_get = create_prepared_request(
                session=session,
                url=HEADIES_URL,
                method="GET",
                headers=headers
            )
            response = session.send(prepped_get, timeout=REQUEST_TIMEOUT)
            
            # Small delay like a human would have
            delay((0.5, 1.5))
        except Exception as e:
            logger.warning(f"Submission {submission_number} - Name: {full_name} - Email: {email} - Phone: {phone} - Status: ERROR visiting main page ({str(e)})")
            # Continue anyway, it's not critical
        
        # Now submit the form
        retry_delay = 1 + random.uniform(0, 0.5)  # Initial retry delay with jitter
        
        for attempt in range(MAX_RETRIES):
            try:
                # Create a prepared request with shuffled headers for form submission
                prepped_post = create_prepared_request(
                    session=session,
                    url=FORM_URL,
                    method="POST",
                    data=form_data,
                    headers=headers
                )
                
                # Send the prepared request
                response = session.send(prepped_post, timeout=REQUEST_TIMEOUT)
                
                # Handle rate limiting (HTTP 429)
                if response.status_code == 429:
                    logger.warning(
                        f"Submission {submission_number} - Name: {full_name} - Email: {email} - Phone: {phone} - Status: RATE LIMITED (HTTP 429), backing off..."
                    )
                    
                    # Record this rate limit hit
                    rate_limit_hits.append(datetime.now())
                    
                    # Adjust delays if we're getting too many rate limits
                    check_rate_limits()
                    
                    # Extended backoff for rate limits (10-30 minutes)
                    backoff = random.uniform(600, 1800)
                    logger.warning(f"Rate limit cooldown: sleeping for {backoff/60:.1f} minutes...")
                    
                    time.sleep(backoff)
                    return False  # End this attempt, will retry with new session
                
                # Check for success verification
                if is_success(response):
                    logger.info(
                        f"Submission {submission_number} - Name: {full_name} - Email: {email} - Phone: {phone} - Status: SUCCESS"
                    )
                    
                    with stats_lock:
                        total_submissions += 1
                        successful_submissions += 1
                    
                    consecutive_failures = 0  # Reset failure counter on success
                    
                    # Small delay after success
                    delay(POST_SUBMISSION_DELAY)
                    return True
                else:
                    # Failed verification
                    logger.warning(
                        f"Submission {submission_number} - Name: {full_name} - Email: {email} - Phone: {phone} - Status: FAILED VERIFICATION (HTTP {response.status_code}), retrying in {retry_delay:.2f}s"
                    )
                    
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
            
            except requests.RequestException as e:
                logger.warning(
                    f"Submission {submission_number} - Name: {full_name} - Email: {email} - Phone: {phone} - Status: REQUEST ERROR ({str(e)}), retrying in {retry_delay:.2f}s"
                )
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            
            except Exception as e:
                logger.error(
                    f"Submission {submission_number} - Name: {full_name} - Email: {email} - Phone: {phone} - Status: UNEXPECTED ERROR ({str(e)})"
                )
                with stats_lock:
                    total_submissions += 1
                consecutive_failures += 1
                return False
        
        # All retries failed
        logger.error(
            f"Submission {submission_number} - Name: {full_name} - Email: {email} - Phone: {phone} - Status: FAILURE after {MAX_RETRIES} retries"
        )
        with stats_lock:
            total_submissions += 1
        consecutive_failures += 1
        return False
    
    except Exception as e:
        logger.error(f"Critical error in submit_form for submission {submission_number}: {str(e)}")
        consecutive_failures += 1
        return False

def signal_handler(signum: int, frame: object) -> None:
    """Handle Ctrl+C and other termination signals"""
    logger.info("Shutting down due to termination signal...")
    stop_event.set()
    time.sleep(1)  # Give threads time to notice
    sys.exit(0)

def main() -> None:
    """Main execution function"""
    # bring all module-level state into this scope
    global total_submissions, consecutive_failures, vpn_switch_in_progress
    global last_vpn_switch_time, last_vpn_switch_submissions, used_identities
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    
    # Load previously used identities at startup
    used_identities = load_used_identities()
    logger.info(f"Loaded {len(used_identities)} previously used identities")
    used_identities = cleanup_used_identities(used_identities)
    logger.info(f"{len(used_identities)} identities still active within the 2-hour window")
    
    logger.info("=== Headies Voting Form Bot Started [Enhanced Version] ===")
    logger.info(f"Target URL: {FORM_URL}")
    logger.info(f"Using 2-hour uniqueness window for identities")
    
    # Session management loop
    while not stop_event.is_set():
        # Create a new session
        session = requests.Session()
        logger.info("Created new session...")
        
        # Calculate batch number for logging
        batch_number = (total_submissions // BATCH_SIZE) + 1
        batch_start_time = time.time()
        batch_successful = 0
        
        # Submission loop within this session
        for i in range(1, BATCH_SIZE + 1):
            if stop_event.is_set():
                break
            
            # Check if we need a VPN switch
            submissions_since_vpn = total_submissions - last_vpn_switch_submissions
            if (submissions_since_vpn >= random.randint(VPN_SWITCH_MIN, VPN_SWITCH_MAX) and 
                not vpn_switch_in_progress):
                last_vpn_switch_submissions = total_submissions
                vpn_switch_in_progress = True
                vpn_switch_prompt()
            
            # Submit form using current delay settings
            submission_number = total_submissions + 1
            success = submit_form(session, batch_number, submission_number)
            
            if success:
                batch_successful += 1
                
                # Occasional long pause for realism
                if submission_number % LONG_PAUSE_INTERVAL == 0 and random.random() < LONG_PAUSE_CHANCE:
                    pause_time = random.uniform(*LONG_PAUSE_DELAY)
                    logger.info(f"Taking a longer break (simulating human pause): {pause_time:.1f}s")
                    delay((pause_time, pause_time))
            
            # Log stats periodically
            if submission_number % 10 == 0 and not stop_event.is_set():
                log_stats()
            
            # Check for too many consecutive failures
            if consecutive_failures >= SESSION_RESTART_THRESHOLD:
                logger.warning(f"Too many consecutive failures ({consecutive_failures}). Restarting session...")
                break
            
            # Random delay between submissions
            if not stop_event.is_set():
                delay(current_submission_delay)
        
        # Log batch results
        batch_time = time.time() - batch_start_time
        logger.info(f"Batch {batch_number} completed: {batch_successful}/{min(BATCH_SIZE, i)} successful in {batch_time:.2f}s")
        
        # Save identity cache periodically
        save_used_identities(used_identities)
        
        # Close session
        session.close()
        
        # If we're stopping, exit
        if stop_event.is_set():
            break
        
        # Brief delay before creating new session
        time.sleep(2)

def run_script():
    """Wrapper function with error handling"""
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\nScript terminated by user. Shutting down...")
        stop_event.set()
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
    finally:
        logger.info("Script stopped.")

if __name__ == "__main__":
    run_script()