# 🔥 Ultimate Proxy Checker 

```
"""
▓█████▄  ██▀███   ▒█████    ▄████  ██▓███   ██▓ ▄████▄  
▒██▀ ██▌▓██ ▒ ██▒▒██▒  ██▒ ██▒ ▀█▒▓██░  ██▒▓██▒▒██▀ ▀█  
░██   █▌▓██ ░▄█ ▒▒██░  ██▒▒██░▄▄▄░▓██░ ██▓▒▒██▒▒▓█    ▄ 
░▓█▄   ▌▒██▀▀█▄  ▒██   ██░░▓█  ██▓▒██▄█▓▒ ▒░██░▒▓▓▄ ▄██▒
░▒████▓ ░██▓ ▒██▒░ ████▓▒░░▒▓███▀▒▒██▒ ░  ░░██░▒ ▓███▀ ░
 ▒▒▓  ▒ ░ ▒▓ ░▒▓░░ ▒░▒░▒░  ░▒   ▒ ▒▓▒░ ░  ░░▓  ░ ░▒ ▒  ░
 ░ ▒  ▒   ░▒ ░ ▒░  ░ ▒ ▒░   ░   ░ ░▒ ░      ▒ ░  ░  ▒   
 ░ ░  ░   ░░   ░ ░ ░ ░ ▒  ░ ░   ░ ░░        ▒ ░░        
   ░       ░         ░ ░        ░            ░  ░ ░      
 ░                                           ░░          
"""
🚀 Core Features
# PROTOCOL SUPPORT
- [✓] HTTP/HTTPS 
- [✓] SOCKS4
- [✓] SOCKS5

# VERIFICATION
- [✓] Live Connection Testing
- [✓] Speed Benchmarking (ms)
- [✓] Country Detection (GeoIP)
- [✓] Continent Sorting

# PERFORMANCE
- [✓] 100-Thread Parallel Processing 
- [✓] Smart Timeout Handling
- [✓] Auto-Bad Proxy Filtering
💻 Installation
# Clone & Run (One-Liner)
git clone https://github.com/yourusername/proxy-checker.git && cd proxy-checker && pip install -r requirements.txt && python checker_gui.py
🛠 How It Works
"""
1. INPUT -> Load proxies from:
   - File (IP:PORT format)
   - Auto-download (15+ sources)

2. PROCESS -> Checks each proxy for:
   - Connectivity (can establish connection)
   - Speed (response time in ms)
   - Location (country/continent via GeoIP)

3. OUTPUT -> Saves working proxies:
   /results/YYYY-MM-DD/
   ├── GoodProxies_HTTP_ALL.txt
   ├── GoodProxy_SOCKS5_US_85ms.txt
   └── BadProxies.txt
"""
🌐 Auto-Source URLs

# HTTP/S
https://api.proxyscrape.com/v2/?request=getproxies&protocol=http
https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt

# SOCKS5
https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt
https://t.me/s/proxysocks5list [Telegram Channel]
⚙️ Config Settings (config.json)
{
  "max_threads": 100,
  "timeout_sec": 8,
  "test_url": "https://httpbin.org/ip",
  "auto_update_sources": true,
  "anonymize_checks": false
}

📸 Screenshot Preview
![Proxy Checker Interface](Preview.png)