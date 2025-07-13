import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog, ttk
import requests
import os
import datetime
import threading
import time
import json
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, FIRST_COMPLETED


# setts
MAX_THREADS = 100  
TIMEOUT = 10 
MAX_WORKERS = 10
TEST_URL = 'https://httpbin.org/ip'
PROXY_TYPES = {
    "HTTP/HTTPS": "http",
    "SOCKS4": "socks4",
    "SOCKS5": "socks5"
}
today = datetime.datetime.now().strftime('%Y-%m-%d')
result_dir = os.path.join('results', today)
os.makedirs(result_dir, exist_ok=True)

# cfg
CONFIG_FILE = "config.json"
SOURCES_FILE = "sources.json"

# colors
DARK_BG = "#2e2e2e"
DARK_FG = "#eaeaea"
DARK_BTN_BG = "#444444"
DARK_BTN_FG = "#ffffff"
DARK_ENTRY_BG = "#3c3f41"
DARK_TEXT_BG = "#1e1e1e"
DARK_HIGHLIGHT = "#5a9bd5"
DARK_PROGRESS = "#4a708b"
GOOD_COLOR = "#4CAF50"
BAD_COLOR = "#F44336"
WARNING_COLOR = "#FFC107"
INFO_COLOR = "#2196F3"

# countries etc
COUNTRY_CONTINENT = {
    'AF': 'Africa', 'AX': 'Europe', 'AL': 'Europe', 'DZ': 'Africa', 'AS': 'Oceania',
    'AD': 'Europe', 'AO': 'Africa', 'AI': 'Americas', 'AQ': 'Antarctica', 'AG': 'Americas',
    'AR': 'Americas', 'AM': 'Asia', 'AW': 'Americas', 'AU': 'Oceania', 'AT': 'Europe',
    'AZ': 'Asia', 'BS': 'Americas', 'BH': 'Asia', 'BD': 'Asia', 'BB': 'Americas',
    'BY': 'Europe', 'BE': 'Europe', 'BZ': 'Americas', 'BJ': 'Africa', 'BM': 'Americas',
    'BT': 'Asia', 'BO': 'Americas', 'BQ': 'Americas', 'BA': 'Europe', 'BW': 'Africa',
    'BV': 'Antarctica', 'BR': 'Americas', 'IO': 'Asia', 'BN': 'Asia', 'BG': 'Europe',
    'BF': 'Africa', 'BI': 'Africa', 'KH': 'Asia', 'CM': 'Africa', 'CA': 'Americas',
    'CV': 'Africa', 'KY': 'Americas', 'CF': 'Africa', 'TD': 'Africa', 'CL': 'Americas',
    'CN': 'Asia', 'CX': 'Asia', 'CC': 'Asia', 'CO': 'Americas', 'KM': 'Africa',
    'CG': 'Africa', 'CD': 'Africa', 'CK': 'Oceania', 'CR': 'Americas', 'CI': 'Africa',
    'HR': 'Europe', 'CU': 'Americas', 'CW': 'Americas', 'CY': 'Asia', 'CZ': 'Europe',
    'DK': 'Europe', 'DJ': 'Africa', 'DM': 'Americas', 'DO': 'Americas', 'EC': 'Americas',
    'EG': 'Africa', 'SV': 'Americas', 'GQ': 'Africa', 'ER': 'Africa', 'EE': 'Europe',
    'SZ': 'Africa', 'ET': 'Africa', 'FK': 'Americas', 'FO': 'Europe', 'FJ': 'Oceania',
    'FI': 'Europe', 'FR': 'Europe', 'GF': 'Americas', 'PF': 'Oceania', 'TF': 'Antarctica',
    'GA': 'Africa', 'GM': 'Africa', 'GE': 'Asia', 'DE': 'Europe', 'GH': 'Africa',
    'GI': 'Europe', 'GR': 'Europe', 'GL': 'Americas', 'GD': 'Americas', 'GP': 'Americas',
    'GU': 'Oceania', 'GT': 'Americas', 'GG': 'Europe', 'GN': 'Africa', 'GW': 'Africa',
    'GY': 'Americas', 'HT': 'Americas', 'HM': 'Antarctica', 'VA': 'Europe', 'HN': 'Americas',
    'HK': 'Asia', 'HU': 'Europe', 'IS': 'Europe', 'IN': 'Asia', 'ID': 'Asia',
    'IR': 'Asia', 'IQ': 'Asia', 'IE': 'Europe', 'IM': 'Europe', 'IL': 'Asia',
    'IT': 'Europe', 'JM': 'Americas', 'JP': 'Asia', 'JE': 'Europe', 'JO': 'Asia',
    'KZ': 'Asia', 'KE': 'Africa', 'KI': 'Oceania', 'KP': 'Asia', 'KR': 'Asia',
    'KW': 'Asia', 'KG': 'Asia', 'LA': 'Asia', 'LV': 'Europe', 'LB': 'Asia',
    'LS': 'Africa', 'LR': 'Africa', 'LY': 'Africa', 'LI': 'Europe', 'LT': 'Europe',
    'LU': 'Europe', 'MO': 'Asia', 'MG': 'Africa', 'MW': 'Africa', 'MY': 'Asia',
    'MV': 'Asia', 'ML': 'Africa', 'MT': 'Europe', 'MH': 'Oceania', 'MQ': 'Americas',
    'MR': 'Africa', 'MU': 'Africa', 'YT': 'Africa', 'MX': 'Americas', 'FM': 'Oceania',
    'MD': 'Europe', 'MC': 'Europe', 'MN': 'Asia', 'ME': 'Europe', 'MS': 'Americas',
    'MA': 'Africa', 'MZ': 'Africa', 'MM': 'Asia', 'NA': 'Africa', 'NR': 'Oceania',
    'NP': 'Asia', 'NL': 'Europe', 'NC': 'Oceania', 'NZ': 'Oceania', 'NI': 'Americas',
    'NE': 'Africa', 'NG': 'Africa', 'NU': 'Oceania', 'NF': 'Oceania', 'MK': 'Europe',
    'MP': 'Oceania', 'NO': 'Europe', 'OM': 'Asia', 'PK': 'Asia', 'PW': 'Oceania',
    'PS': 'Asia', 'PA': 'Americas', 'PG': 'Oceania', 'PY': 'Americas', 'PE': 'Americas',
    'PH': 'Asia', 'PN': 'Oceania', 'PL': 'Europe', 'PT': 'Europe', 'PR': 'Americas',
    'QA': 'Asia', 'RE': 'Africa', 'RO': 'Europe', 'RU': 'Europe', 'RW': 'Africa',
    'BL': 'Americas', 'SH': 'Africa', 'KN': 'Americas', 'LC': 'Americas', 'MF': 'Americas',
    'PM': 'Americas', 'VC': 'Americas', 'WS': 'Oceania', 'SM': 'Europe', 'ST': 'Africa',
    'SA': 'Asia', 'SN': 'Africa', 'RS': 'Europe', 'SC': 'Africa', 'SL': 'Africa',
    'SG': 'Asia', 'SX': 'Americas', 'SK': 'Europe', 'SI': 'Europe', 'SB': 'Oceania',
    'SO': 'Africa', 'ZA': 'Africa', 'GS': 'Antarctica', 'SS': 'Africa', 'ES': 'Europe',
    'LK': 'Asia', 'SD': 'Africa', 'SR': 'Americas', 'SJ': 'Europe', 'SE': 'Europe',
    'CH': 'Europe', 'SY': 'Asia', 'TW': 'Asia', 'TJ': 'Asia', 'TZ': 'Africa',
    'TH': 'Asia', 'TL': 'Asia', 'TG': 'Africa', 'TK': 'Oceania', 'TO': 'Oceania',
    'TT': 'Americas', 'TN': 'Africa', 'TR': 'Asia', 'TM': 'Asia', 'TC': 'Americas',
    'TV': 'Oceania', 'UG': 'Africa', 'UA': 'Europe', 'AE': 'Asia', 'GB': 'Europe',
    'US': 'Americas', 'UM': 'Oceania', 'UY': 'Americas', 'UZ': 'Asia', 'VU': 'Oceania',
    'VE': 'Americas', 'VN': 'Asia', 'VG': 'Americas', 'VI': 'Americas', 'WF': 'Oceania',
    'EH': 'Africa', 'YE': 'Asia', 'ZM': 'Africa', 'ZW': 'Africa'
}

CONTINENTS = ["Africa", "Americas", "Asia", "Europe", "Oceania", "Antarctica"]
# load/create config
def load_default_config(self):
    self.config = {
        "sources": {
            "http": [
                "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http",
                "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt"
            ],
            "socks4": [
                "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4",
                "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt"
            ],
            "socks5": [
                "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5",
                "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt"
            ]
        },
        "anonymize": False,
        "custom_test_url": "https://httpbin.org/ip"
    }
    # Save it for future runs
    with open('config.json', 'w') as f:
        json.dump(self.config, f, indent=4)

def load_config():
    default_config = {
        "sources": {
            "http": [
                "https://proxyspace.pro/http.txt", 
                "https://proxyspace.pro/https.txt", 
                "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",  
                "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/http.txt",  
                "https://api.proxyscrape.com/?request=displayproxies&proxytype=http",
                "https://www.proxy-list.download/api/v1/get?type=http",
                "https://spys.me/proxy.txt",  
            ],
            "socks4": [
                "https://proxyspace.pro/socks4.txt",  
                "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks4.txt",
                "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
                "https://api.openproxylist.xyz/socks4.txt",
                "https://www.proxy-list.download/api/v1/get?type=socks4",
            ],
            "socks5": [
                "https://proxyspace.pro/socks5.txt", 
                "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
                "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
                "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
                "https://www.proxy-list.download/api/v1/get?type=socks5",
            ]
        },
        "anonymize": False,
        "custom_test_url": "https://httpbin.org/ip",
        "update_frequency": 6, 
        "max_proxies_per_type": 1500,
        "verify_ssl": True,
        "timeout": 10  
    }
    
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            try:
                return json.load(f)
            except:
                return default_config
    return default_config

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

# ini config
config = load_config()

# proxy test
def check_proxy_speed(proxy, proxy_type, stop_event, test_url=None):
    if stop_event.is_set():
        return proxy, None, None, None
    
    scheme = PROXY_TYPES[proxy_type]
    proxies = {"http": f"{scheme}://{proxy}", "https": f"{scheme}://{proxy}"}
    start_time = time.time()
    try:
        url = test_url if test_url else TEST_URL
        response = requests.get(url, proxies=proxies, timeout=TIMEOUT)
        if response.status_code == 200:
            elapsed = int((time.time() - start_time) * 1000)
            country = get_country(proxy)
            return proxy, elapsed, country, response.text
    except Exception as e:
        pass
    return proxy, None, None, None

def get_country(proxy):
    ip = proxy.split(":")[0]
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=countryCode", timeout=5)
        if r.status_code == 200:
            data = r.json()
            return data.get("countryCode", "Unknown")
    except:
        pass
    return "Unknown"

def save_master_file(good_proxies, proxy_type):
    file_path = os.path.join(result_dir, f'GoodProxies_{proxy_type.replace("/", "_")}_ALL.txt')
    with open(file_path, 'w') as f:
        for proxy, speed, country, _ in good_proxies:
            f.write(f"{proxy} # {country} # {speed}ms\n")

def save_selected_continents_files(good_proxies, proxy_type, selected_continents, output_callback):
    count = 0
    for proxy, speed, country, _ in good_proxies:
        continent = COUNTRY_CONTINENT.get(country, "Unknown")
        if continent in selected_continents:
            filename = f"GoodProxy_{proxy_type.replace('/', '_')}_{country}_{speed}ms.txt"
            file_path = os.path.join(result_dir, filename)
            with open(file_path, 'w') as f:
                f.write(proxy)
            output_callback(f"📄 Saved proxy {proxy} ({country}/{continent}) to: {filename}", INFO_COLOR)
            count += 1
    if count == 0:
        output_callback("⚠️ No proxies matched the selected continents for separate saving.", WARNING_COLOR)

# fetch proxies
def fetch_proxies_from_source(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return [p.strip() for p in response.text.splitlines() if p.strip()]
    except Exception as e:
        print(f"Error fetching from {url}: {str(e)}")
    return []

# checking
def start_checking(proxies, proxy_type, output_callback, after_check_callback, 
                  stop_event, progress_callback=None, test_url=None, anonymize=False):
    unique_proxies = list(set([p.strip() for p in proxies if p.strip()]))
    good_proxies = []
    bad_proxies = []
    total = len(unique_proxies)
    checked = 0
    stats = {
        'total': total,
        'checked': 0,
        'good': 0,
        'bad': 0,
        'countries': {},
        'speeds': []
    }

    output_callback(f"🔍 Checking {total} proxies ({proxy_type})...\n", INFO_COLOR)

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        future_to_proxy = {executor.submit(check_proxy_speed, proxy, proxy_type, stop_event, test_url): proxy 
                         for proxy in unique_proxies}
        
        try:
            while future_to_proxy and not stop_event.is_set():
                try:
                    done, not_done = wait(future_to_proxy.keys(), timeout=30, return_when=FIRST_COMPLETED)
                    
                    if not done:
                        output_callback("⚠️ Timeout for some proxies (continuing)...", WARNING_COLOR)
                        continue
                        
                    for future in done:
                        proxy = future_to_proxy.pop(future)
                        try:
                            proxy, speed, country, _ = future.result()
                            checked += 1
                            stats['checked'] = checked
                            
                            if progress_callback:
                                progress_callback(checked, total, stats)
                            
                            if speed is not None and country is not None:
                                output_callback(f"[✓] Good: {proxy} - {speed}ms - {country}", GOOD_COLOR)
                                good_proxies.append((proxy, speed, country, None))
                                stats['good'] += 1
                                stats['countries'][country] = stats['countries'].get(country, 0) + 1
                                stats['speeds'].append(speed)
                            else:
                                output_callback(f"[✗] Bad: {proxy}", BAD_COLOR)
                                bad_proxies.append(proxy)
                                stats['bad'] += 1
                        except Exception as e:
                            output_callback(f"[!] Error checking {proxy}: {str(e)}", WARNING_COLOR)
                            stats['bad'] += 1
                            
                    future_to_proxy = {f: p for f, p in future_to_proxy.items() if f in not_done}
                    
                except Exception as e:
                    output_callback(f"[!] Batch error: {str(e)}", WARNING_COLOR)
                    
        finally:
            if stop_event.is_set():
                executor.shutdown(wait=False, cancel_futures=True)
                output_callback("\n🛑 Checking stopped by user!", WARNING_COLOR)
            else:
                output_callback("\n✅ All proxies processed", INFO_COLOR)

    if stats['good'] > 0:
        stats['avg_speed'] = sum(stats['speeds']) // len(stats['speeds'])
        stats['min_speed'] = min(stats['speeds'])
        stats['max_speed'] = max(stats['speeds'])
    else:
        stats['avg_speed'] = 0
        stats['min_speed'] = 0
        stats['max_speed'] = 0
    
    save_master_file(good_proxies, proxy_type)
    
    bad_file = os.path.join(result_dir, f'BadProxies_{proxy_type.replace("/", "_")}.txt')
    with open(bad_file, 'w') as f:
        f.writelines(f"{proxy}\n" for proxy in bad_proxies)

    after_check_callback(good_proxies, proxy_type, stats)

class ProxyCheckerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Proxy Checker v3.0 [Ready]")
        self.root.configure(bg=DARK_BG)
        self.proxy_type_var = tk.StringVar(value="HTTP/HTTPS")
        self.proxies = []
        self.good_proxies = []
        self.checking_thread = None
        self.stop_event = threading.Event()
        self.running = False
        self.stats = {}
        self.config = load_config()
        
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        
        top_frame = tk.Frame(root, bg=DARK_BG)
        top_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=5)
        
        tk.Label(top_frame, text="Proxy Type:", bg=DARK_BG, fg=DARK_FG).pack(side='left', padx=5)
        self.proxy_type_menu = tk.OptionMenu(top_frame, self.proxy_type_var, *PROXY_TYPES.keys())
        self.proxy_type_menu.config(bg=DARK_BTN_BG, fg=DARK_BTN_FG, highlightthickness=0)
        self.proxy_type_menu.pack(side='left', padx=5)
        
        self.anonymize_var = tk.BooleanVar(value=self.config.get("anonymize", False))
        tk.Checkbutton(top_frame, text="Anonymize", variable=self.anonymize_var, 
                      bg=DARK_BG, fg=DARK_FG, selectcolor=DARK_BTN_BG,
                      command=self.toggle_anonymize).pack(side='left', padx=10)
        
        tk.Label(top_frame, text="Test URL:", bg=DARK_BG, fg=DARK_FG).pack(side='left', padx=5)
        self.test_url_var = tk.StringVar(value=self.config.get("custom_test_url", TEST_URL))
        self.test_url_entry = tk.Entry(top_frame, textvariable=self.test_url_var, 
                                     bg=DARK_ENTRY_BG, fg=DARK_FG, insertbackground=DARK_FG)
        self.test_url_entry.pack(side='left', expand=True, fill='x', padx=5)
        
        btn_frame = tk.Frame(root, bg=DARK_BG)
        btn_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=5)
        
        tk.Button(btn_frame, text="Load Proxies", command=self.load_file, 
                 bg=DARK_BTN_BG, fg=DARK_BTN_FG).pack(side='left', expand=True, fill='x', padx=2)
        tk.Button(btn_frame, text="Fetch Online", command=self.fetch_online, 
                 bg=DARK_BTN_BG, fg=DARK_BTN_FG).pack(side='left', expand=True, fill='x', padx=2)
        self.start_btn = tk.Button(btn_frame, text="Start Checking", command=self.start_check, 
                                 bg=DARK_BTN_BG, fg=DARK_BTN_FG)
        self.start_btn.pack(side='left', expand=True, fill='x', padx=2)
        self.stop_btn = tk.Button(btn_frame, text="Stop", command=self.stop_check, 
                                 bg="#8B0000", fg=DARK_BTN_FG, state=tk.DISABLED)
        self.stop_btn.pack(side='left', expand=True, fill='x', padx=2)
        tk.Button(btn_frame, text="Settings", command=self.open_settings, 
                 bg=DARK_BTN_BG, fg=DARK_BTN_FG).pack(side='left', expand=True, fill='x', padx=2)
        
        progress_frame = tk.Frame(root, bg=DARK_BG)
        progress_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=100, style="dark.Horizontal.TProgressbar")
        self.progress_bar.pack(fill='x', pady=2)
        
        self.progress_label = tk.Label(progress_frame, text="Ready", bg=DARK_BG, fg=DARK_FG)
        self.progress_label.pack(fill='x')
        
        self.stats_label = tk.Label(progress_frame, text="", bg=DARK_BG, fg=INFO_COLOR)
        self.stats_label.pack(fill='x')
        
        self.output = scrolledtext.ScrolledText(root, bg=DARK_TEXT_BG, fg=DARK_FG, 
                                              insertbackground=DARK_FG, wrap=tk.WORD)
        self.output.grid(row=3, column=0, sticky='nsew', padx=10, pady=5)
        
        style = ttk.Style()
        style.theme_use('default')
        style.configure("dark.Horizontal.TProgressbar", 
                        background=DARK_PROGRESS,
                        troughcolor=DARK_ENTRY_BG,
                        bordercolor=DARK_BG,
                        lightcolor=DARK_PROGRESS,
                        darkcolor=DARK_PROGRESS)
        
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, 
                             anchor=tk.W, bg=DARK_BG, fg=DARK_FG)
        status_bar.grid(row=4, column=0, sticky='ew', padx=10, pady=5)

    def log(self, msg, color=None):
        color = color or DARK_FG
        self.output.configure(state='normal')
        self.output.tag_config(color, foreground=color)
        self.output.insert(tk.END, msg + "\n", color)
        self.output.see(tk.END)
        self.output.configure(state='disabled')
        self.status_var.set(msg[:100])  

    def update_progress(self, current, total, stats=None):
        percent = (current / total) * 100
        self.progress_var.set(percent)
        self.progress_label.config(text=f"Progress: {current}/{total} ({percent:.1f}%)")
        
        if stats:
            self.stats = stats
            good = stats.get('good', 0)
            bad = stats.get('bad', 0)
            countries_count = len(stats.get('countries', {}))
            avg_speed = stats.get('avg_speed', 0)
            
            self.stats_label.config(
                text=f"Good: {good} | Bad: {bad} | Countries: {countries_count} | "
                    f"Avg Speed: {avg_speed}ms"
            )
            self.root.title(
                f"Advanced Proxy Checker v3.0 [Checked: {current}/{total} | Good: {good} | Bad: {bad}]"
            )

    def load_file(self):
        if self.running:
            messagebox.showwarning("Warning", "Please stop checking first.")
            return
            
        file_path = filedialog.askopenfilename(title="Select proxy file", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as f:
                self.proxies = [line.strip() for line in f if line.strip()]
            self.log(f"📂 Loaded {len(self.proxies)} proxies from file.", INFO_COLOR)

    def fetch_online(self):
        try:
            # Add this config validation
            if not hasattr(self, 'config') or 'sources' not in self.config:
                self.load_default_config()
                
            proxy_type = self.proxy_type_var.get()
            scheme = PROXY_TYPES[proxy_type]
            sources = self.config['sources'].get(scheme, [])
            
            if not sources:
                self.log("⚠️ No sources configured for this proxy type.", WARNING_COLOR)
                return
                
            self.log("🌐 Fetching proxies online...", INFO_COLOR)
            
            all_proxies = []
            with ThreadPoolExecutor(max_workers=5) as executor:
                future_to_url = {executor.submit(fetch_proxies_from_source, url): url for url in sources}
                
                try:
                    for future in as_completed(future_to_url):
                        url = future_to_url[future]
                        try:
                            proxies = future.result()
                            if proxies:
                                all_proxies.extend(proxies)
                                self.log(f"✓ Fetched {len(proxies)} proxies from {url}", GOOD_COLOR)
                            else:
                                self.log(f"⚠️ No proxies from {url}", WARNING_COLOR)
                        except Exception as e:
                            self.log(f"⚠️ Failed to fetch from {url}: {str(e)}", BAD_COLOR)
                            
                except Exception as e:
                    self.log(f"⚠️ Critical error during fetch: {str(e)}", BAD_COLOR)
                    
        except Exception as e:
            self.log(f"⚠️ Initialization error: {str(e)}", BAD_COLOR)
            return
            
        finally:
            if all_proxies:
                self.proxies = list(set(all_proxies))  # Remove duplicates
                self.log(f"🌐 Total fetched: {len(self.proxies)} proxies", INFO_COLOR)
            else:
                self.log("⚠️ Failed to fetch any proxies online.", WARNING_COLOR)

    def start_check(self):
        if self.running:
            return
            
        if not self.proxies:
            messagebox.showwarning("No Proxies", "Please load or fetch proxies first.")
            return
            
        self.output.configure(state='normal')
        self.output.delete(1.0, tk.END)
        self.output.configure(state='disabled')
        
        self.stop_event.clear()
        self.running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress_var.set(0)
        self.stats_label.config(text="")
        
        proxy_type = self.proxy_type_var.get()
        test_url = self.test_url_var.get() if self.test_url_var.get() else TEST_URL
        anonymize = self.anonymize_var.get()
        
        self.log(f"🚀 Starting proxy check ({proxy_type})...", INFO_COLOR)
        self.log(f"🔗 Test URL: {test_url}", INFO_COLOR)
        self.log(f"🕵️ Anonymize: {'Yes' if anonymize else 'No'}", INFO_COLOR)

        self.checking_thread = threading.Thread(
            target=self.threaded_check, 
            args=(proxy_type, test_url, anonymize),
            daemon=True
        )
        self.checking_thread.start()

    def stop_check(self):
        if self.running:
            self.stop_event.set()
            self.running = False
            self.log("\n🛑 Stopping check... Please wait.", WARNING_COLOR)
            self.stop_btn.config(state=tk.DISABLED)

    def threaded_check(self, proxy_type, test_url, anonymize):
        def safe_log(msg, color=None):
            self.root.after(0, lambda: self.log(msg, color))

        def safe_after_check(good_proxies, proxy_type, stats):
            self.root.after(0, lambda: self.after_check(good_proxies, proxy_type, stats))
            
        def safe_progress(current, total, stats):
            self.root.after(0, lambda: self.update_progress(current, total, stats))

        try:
            start_checking(
                proxies=self.proxies,
                proxy_type=proxy_type,
                output_callback=safe_log,
                after_check_callback=safe_after_check,
                stop_event=self.stop_event,
                progress_callback=safe_progress,
                test_url=test_url,
                anonymize=anonymize
            )
        except Exception as e:
            safe_log(f"⚠️ Error during checking: {str(e)}", WARNING_COLOR)
        finally:
            self.root.after(0, self.reset_ui)

    def after_check(self, good_proxies, proxy_type, stats):
        self.good_proxies = good_proxies
        self.stats = stats
        
        # stats
        self.log("\n📊 Statistics:", INFO_COLOR)
        self.log(f"✅ Good proxies: {stats['good']}", GOOD_COLOR)
        self.log(f"❌ Bad proxies: {stats['bad']}", BAD_COLOR)
        self.log(f"⏱️ Average speed: {stats.get('avg_speed', 0)}ms", INFO_COLOR)
        self.log(f"🚀 Fastest: {stats.get('min_speed', 0)}ms", GOOD_COLOR)
        self.log(f"🐢 Slowest: {stats.get('max_speed', 0)}ms", BAD_COLOR)
        
        if stats['countries']:
            self.log("\n🌍 Countries:", INFO_COLOR)
            for country, count in sorted(stats['countries'].items(), key=lambda x: x[1], reverse=True):
                self.log(f"{country}: {count}", INFO_COLOR)
        
        self.ask_continents(proxy_type)

    def reset_ui(self):
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress_label.config(text="Completed")
        self.root.title("Advanced Proxy Checker v3.0 [Ready]")

    def ask_continents(self, proxy_type):
        popup = tk.Toplevel(self.root)
        popup.title("Save Options")
        popup.configure(bg=DARK_BG)
        
        main_frame = tk.Frame(popup, bg=DARK_BG)
        main_frame.pack(padx=10, pady=10)
        
        tk.Label(main_frame, text="Select continents for individual proxy files:", 
                bg=DARK_BG, fg=DARK_FG).pack(anchor='w', pady=5)

        check_frame = tk.Frame(main_frame, bg=DARK_BG)
        check_frame.pack(fill='x', padx=10)
        
        vars = {}
        for i, cont in enumerate(CONTINENTS):
            var = tk.BooleanVar(value=True)
            cb = tk.Checkbutton(check_frame, text=cont, variable=var, 
                              bg=DARK_BG, fg=DARK_FG, selectcolor=DARK_BTN_BG)
            cb.grid(row=i//3, column=i%3, sticky='w', padx=5, pady=2)
            vars[cont] = var

        btn_frame = tk.Frame(main_frame, bg=DARK_BG)
        btn_frame.pack(fill='x', pady=10)
        
        def on_save():
            selected = [c for c,v in vars.items() if v.get()]
            popup.destroy()
            save_selected_continents_files(self.good_proxies, proxy_type, selected, self.log)
            self.show_stats_popup()
        
        def on_skip():
            popup.destroy()
            self.log("ℹ️ Skipped saving individual proxy files.", INFO_COLOR)
            self.show_stats_popup()
        
        tk.Button(btn_frame, text="Save Selected", command=on_save, 
                 bg=DARK_BTN_BG, fg=DARK_BTN_FG).pack(side='left', expand=True, padx=5)
        tk.Button(btn_frame, text="Skip", command=on_skip, 
                 bg=DARK_BTN_BG, fg=DARK_BTN_FG).pack(side='left', expand=True, padx=5)

        popup.transient(self.root)
        popup.grab_set()
        self.root.wait_window(popup)

    def show_stats_popup(self):
        stats = self.stats
        popup = tk.Toplevel(self.root)
        popup.title("Check Statistics")
        popup.configure(bg=DARK_BG)
        
        main_frame = tk.Frame(popup, bg=DARK_BG)
        main_frame.pack(padx=10, pady=10)
        
        tk.Label(main_frame, text="📊 Proxy Check Statistics", 
                bg=DARK_BG, fg=INFO_COLOR, font=('Arial', 12, 'bold')).pack(pady=5)
        
        stats_frame = tk.Frame(main_frame, bg=DARK_BG)
        stats_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(stats_frame, text=f"✅ Good Proxies: {stats['good']}", 
                bg=DARK_BG, fg=GOOD_COLOR, anchor='w').pack(fill='x')
        tk.Label(stats_frame, text=f"❌ Bad Proxies: {stats['bad']}", 
                bg=DARK_BG, fg=BAD_COLOR, anchor='w').pack(fill='x')
        
        tk.Label(stats_frame, text=f"⏱️ Average Speed: {stats.get('avg_speed', 0)}ms", 
                bg=DARK_BG, fg=INFO_COLOR, anchor='w').pack(fill='x')
        tk.Label(stats_frame, text=f"🚀 Fastest Proxy: {stats.get('min_speed', 0)}ms", 
                bg=DARK_BG, fg=GOOD_COLOR, anchor='w').pack(fill='x')
        tk.Label(stats_frame, text=f"🐢 Slowest Proxy: {stats.get('max_speed', 0)}ms", 
                bg=DARK_BG, fg=BAD_COLOR, anchor='w').pack(fill='x')
        
        if stats['countries']:
            tk.Label(stats_frame, text=f"🌍 Countries: {len(stats['countries'])}", 
                    bg=DARK_BG, fg=INFO_COLOR, anchor='w').pack(fill='x')
            
            countries_frame = tk.Frame(stats_frame, bg=DARK_BG)
            countries_frame.pack(fill='x', pady=5)
            
            for i, (country, count) in enumerate(sorted(stats['countries'].items(), key=lambda x: x[1], reverse=True)):
                if i < 5:
                    tk.Label(countries_frame, text=f"{country}: {count}", 
                            bg=DARK_BG, fg=DARK_FG, anchor='w').pack(fill='x')
        
        tk.Button(main_frame, text="Close", command=popup.destroy, 
                 bg=DARK_BTN_BG, fg=DARK_BTN_FG).pack(pady=10)
        
        popup.transient(self.root)
        popup.grab_set()

    def toggle_anonymize(self):
        self.config['anonymize'] = self.anonymize_var.get()
        save_config(self.config)
        if self.anonymize_var.get():
            self.log("🕵️ Anonymize mode enabled - using TOR for requests", INFO_COLOR)
        else:
            self.log("🕵️ Anonymize mode disabled", INFO_COLOR)

    def open_settings(self):
        popup = tk.Toplevel(self.root)
        popup.title("Settings")
        popup.configure(bg=DARK_BG)
        
        main_frame = tk.Frame(popup, bg=DARK_BG)
        main_frame.pack(padx=10, pady=10)
        
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)
        
        for proxy_type, scheme in PROXY_TYPES.items():
            frame = tk.Frame(notebook, bg=DARK_BG)
            notebook.add(frame, text=proxy_type)
            
            sources = self.config['sources'].get(scheme, [])
            listbox = tk.Listbox(frame, bg=DARK_ENTRY_BG, fg=DARK_FG, selectbackground=DARK_HIGHLIGHT)
            for source in sources:
                listbox.insert(tk.END, source)
            listbox.pack(side='left', fill='both', expand=True, padx=5, pady=5)
            
            scrollbar = tk.Scrollbar(frame, command=listbox.yview)
            scrollbar.pack(side='right', fill='y')
            listbox.config(yscrollcommand=scrollbar.set)
            
            btn_frame = tk.Frame(frame, bg=DARK_BG)
            btn_frame.pack(fill='x', pady=5)
            
            def add_source(scheme=scheme, listbox=listbox):
                url = simpledialog.askstring("Add Source", "Enter proxy source URL:")
                if url and url not in listbox.get(0, tk.END):
                    listbox.insert(tk.END, url)
            
            tk.Button(btn_frame, text="Add", command=add_source, 
                     bg=DARK_BTN_BG, fg=DARK_BTN_FG).pack(side='left', expand=True, padx=2)
            
            def remove_source(scheme=scheme, listbox=listbox):
                selection = listbox.curselection()
                if selection:
                    listbox.delete(selection[0])
            
            tk.Button(btn_frame, text="Remove", command=remove_source, 
                     bg=DARK_BTN_BG, fg=DARK_BTN_FG).pack(side='left', expand=True, padx=2)
        
        def save_sources():
            for i, (proxy_type, scheme) in enumerate(PROXY_TYPES.items()):
                frame = notebook.children[notebook.tabs()[i]]
                listbox = frame.children['!listbox']
                self.config['sources'][scheme] = list(listbox.get(0, tk.END))
            save_config(self.config)
            popup.destroy()
            self.log("⚙️ Settings saved successfully.", INFO_COLOR)
        
        tk.Button(main_frame, text="Save Settings", command=save_sources, 
                 bg=DARK_BTN_BG, fg=DARK_BTN_FG).pack(pady=10)
        
        popup.transient(self.root)
        popup.grab_set()
        self.root.wait_window(popup)

if __name__ == '__main__':
    root = tk.Tk()
    
    config = {}
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except:
        config = {
            "sources": {
                "http": [
                    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http",
                    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt"
                ],
                "socks4": [
                    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4",
                    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt"
                ],
                "socks5": [
                    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5",
                    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt"
                ]
            },
            "anonymize": False,
            "custom_test_url": "https://httpbin.org/ip"
        }
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
    
    try:
        root.iconbitmap('proxy.ico')
    except:
        pass
    
    root.geometry("800x600")
    
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('.', background=DARK_BG, foreground=DARK_FG)
    style.configure('TNotebook', background=DARK_BG, borderwidth=0)
    style.configure('TNotebook.Tab', background=DARK_BTN_BG, foreground=DARK_FG, padding=[10, 5])
    style.map('TNotebook.Tab', background=[('selected', DARK_HIGHLIGHT)])
    
    app = ProxyCheckerGUI(root)
    app.config = config
    
    root.mainloop()
