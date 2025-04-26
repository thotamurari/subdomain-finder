# 🔍 Advanced Subdomain Finder Tool

A powerful Python tool to discover subdomains using multiple enumeration techniques.

![Banner](https://img.shields.io/badge/Subdomain-Finder-brightgreen)
![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![License](https://img.shields.io/badge/License-MIT-orange)

---
# 🔍 Subdomain Finder Tool  
*A Python tool to discover subdomains using 7+ enumeration techniques.*  

---

## 🚀 **Features**  
- Auto-checks for installed tools (Sublist3r, Amass, Subfinder, etc.)  
- Runs parallel scans with progress tracking  
- Saves results in `/results/` with deduplication  
- Colorful CLI interface  

---

## ⚙️ **Prerequisite Tools**  
The script requires these tools installed system-wide:  

| Tool | Install Command |
|------|----------------|
| Sublist3r | `git clone https://github.com/aboul3la/Sublist3r.git && cd Sublist3r && pip install -r requirements.txt` |
| Amass | `go install -v github.com/owasp/amass/v3/...@master` |
| Subfinder | `go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest` |
| AssetFinder | `go install -v github.com/tomnomnom/assetfinder@latest` |
| Findomain | `curl -LO https://github.com/Findomain/Findomain/releases/latest/download/findomain-linux && chmod +x findomain-linux && sudo mv findomain-linux /usr/local/bin` |
| Knockpy | `git clone https://github.com/guelfoweb/knock.git && cd knock && pip install -r requirements.txt` |
| MassDNS | `git clone https://github.com/blechschmidt/massdns.git && cd massdns && make && sudo cp bin/massdns /usr/local/bin` |

**Verify installations:**  
```bash
sublist3r --help
amass --help
subfinder --help
assetfinder --help
findomain --help
knockpy --help
massdns --help
