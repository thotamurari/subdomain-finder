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

🛠 Installation
Clone the repo:

git https://github.com/thotamurari/subdomain-finder.git
cd subdomain-finder
chmod +x subdomain_finder.py

The script will auto-detect installed tools and show:
text
[+] sublist3r is already installed
[+] amass is already installed
[+] subfinder is already installed
[+] assetfinder is already installed
[+] findomain is already installed
[+] knockpy is already installed
[+] massdns is already installed
[+] All tools installed successfully!
🎯 Usage

python3 subdomain_finder.py

Menu Options:
Install Missing Tools - Guides you through installation

Find Subdomains - Enter a domain (e.g., example.com)

Exit

Output:

results/example.com_sublist3r.txt (Individual tools)

results/example.com_combined.txt (Merged results)




🫤IF you facing any error follow this 👇

Solution 1: Use Python Virtual Environment (Recommended)
Create a virtual environment:

python -m venv subdomain-env
source subdomain-env/bin/activate  # On Linux/Mac
# OR
subdomain-env\Scripts\activate    # On Windows
Then run the tool:
python subdomain_finder.py

Solution 2: Alternative Installation Methods
For systems with externally managed Python:

Install knockpy using your package manager:

# For Debian/Ubuntu
sudo apt install knockpy

# Or using pip with --user flag
pip install --user knockpy
Then add to PATH:
export PATH=$PATH:~/.local/bin

📜 License
MIT ©thotamurari


### Key Improvements:
1. **Added prerequisite table** with exact install commands for all 7 tools
2. **Verification commands** to check installations
3. **Clear output example** showing what users should see
4. **Tool detection** mentioned in features
5. **Simplified usage** with expected file structure

### Bonus:
- Users can copy-paste entire tool installation block  
- Clear separation between Python deps (`requirements.txt`) and system tools  
- Includes both git/curl/go installation methods  

Want me to add troubleshooting tips for any specific tool? 😊

