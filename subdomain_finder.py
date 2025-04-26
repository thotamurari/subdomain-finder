import os
import sys
import subprocess
import time
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import platform
from colorama import Fore, Style, init
import shutil

# Initialize colorama
init(autoreset=True)

# Global variables
REQUIRED_TOOLS = {
    'sublist3r': {
        'install': 'git clone https://github.com/aboul3la/Sublist3r.git && cd Sublist3r && python3 -m pip install --user -r requirements.txt',
        'test': 'sublist3r --help',
        'is_python': True
    },
    'amass': {
        'install': 'go install -v github.com/owasp/amass/v3/...@master',
        'test': 'amass --help',
        'is_python': False
    },
    'subfinder': {
        'install': 'go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest',
        'test': 'subfinder --help',
        'is_python': False
    },
    'assetfinder': {
        'install': 'go install -v github.com/tomnomnom/assetfinder@latest',
        'test': 'assetfinder --help',
        'is_python': False
    },
    'findomain': {
        'install': 'curl -LO https://github.com/Findomain/Findomain/releases/latest/download/findomain-linux && chmod +x findomain-linux && sudo mv findomain-linux /usr/local/bin/findomain',
        'test': 'findomain --help',
        'is_python': False
    },
    'knockpy': {
        'install': 'git clone https://github.com/guelfoweb/knock.git && cd knock && python3 -m pip install --user -r requirements.txt',
        'test': 'knockpy --help',
        'is_python': True
    },
    'massdns': {
        'install': 'git clone https://github.com/blechschmidt/massdns.git && cd massdns && make && sudo cp bin/massdns /usr/local/bin',
        'test': 'massdns --help',
        'is_python': False
    }
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""
{Fore.GREEN}╔═╗┬ ┬┌─┐┌─┐┌─┐┌┐┌┬┌─┐┌─┐┬─┐{Style.RESET_ALL}
{Fore.GREEN}╚═╗├─┤├─┤│  ├─┤││││┌─┘├┤ ├┬┘{Style.RESET_ALL}
{Fore.GREEN}╚═╝┴ ┴┴ ┴└─┘┴ ┴┘└┘┴└─┘└─┘┴└─{Style.RESET_ALL}
{Fore.CYAN}Advanced Subdomain Enumeration Tool{Style.RESET_ALL}
{Fore.YELLOW}By Security Engineer{Style.RESET_ALL}
    """
    print(banner)

def check_tool_installed(tool):
    try:
        # Special check for Python tools
        if REQUIRED_TOOLS[tool].get('is_python', False):
            # Check if in PATH or Python modules
            try:
                subprocess.run(REQUIRED_TOOLS[tool]['test'], shell=True, check=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return True
            except:
                # Check if installed as Python module
                result = subprocess.run(f"python3 -m {tool} --help", shell=True,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return result.returncode == 0
        else:
            # Check binary in PATH
            return shutil.which(tool) is not None
    except:
        return False

def install_tool(tool):
    print(f"{Fore.BLUE}[*] Installing {tool}...{Style.RESET_ALL}")
    
    try:
        # Add user binaries to PATH for Python tools
        if REQUIRED_TOOLS[tool].get('is_python', False):
            home = os.path.expanduser("~")
            os.environ["PATH"] += f":{home}/.local/bin"
        
        # Run the installation command
        process = subprocess.run(
            REQUIRED_TOOLS[tool]['install'],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if process.returncode != 0:
            print(f"{Fore.RED}[-] Installation failed for {tool}{Style.RESET_ALL}")
            print(f"Error output:\n{process.stderr}")
            return False
        
        # Verify installation
        if not check_tool_installed(tool):
            print(f"{Fore.RED}[-] Installation verification failed for {tool}{Style.RESET_ALL}")
            return False
            
        print(f"{Fore.GREEN}[+] {tool} installed successfully!{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}[-] Exception during {tool} installation: {str(e)}{Style.RESET_ALL}")
        return False

def install_all_tools():
    print(f"{Fore.YELLOW}[!] This will install all required tools. Continue? (y/n){Style.RESET_ALL}")
    if input().lower() != 'y':
        return
    
    # Check for prerequisites
    print(f"{Fore.BLUE}[*] Checking system prerequisites...{Style.RESET_ALL}")
    
    # Check for Go
    if not shutil.which('go'):
        print(f"{Fore.RED}[-] Go (golang) is required but not installed. Please install it first.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Installation instructions: https://golang.org/doc/install{Style.RESET_ALL}")
        return
    
    # Check for Git
    if not shutil.which('git'):
        print(f"{Fore.RED}[-] Git is required but not installed. Please install it first.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] On Ubuntu/Debian: sudo apt install git{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] On CentOS/RHEL: sudo yum install git{Style.RESET_ALL}")
        return
    
    # Install tools
    failed_installs = []
    for tool in REQUIRED_TOOLS:
        if not check_tool_installed(tool):
            if not install_tool(tool):
                failed_installs.append(tool)
        else:
            print(f"{Fore.GREEN}[+] {tool} is already installed{Style.RESET_ALL}")
    
    if failed_installs:
        print(f"{Fore.RED}[-] Failed to install: {', '.join(failed_installs)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Some tools may require manual installation{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}[+] All tools installed successfully!{Style.RESET_ALL}")

def run_sublist3r(domain):
    output_file = f"results/{domain}_sublist3r.txt"
    try:
        command = f"sublist3r -d {domain} -o {output_file}"
        subprocess.run(command, shell=True, check=True)
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}[-] Sublist3r failed: {e}{Style.RESET_ALL}")
        return None

def run_amass(domain):
    output_file = f"results/{domain}_amass.txt"
    try:
        command = f"amass enum -passive -d {domain} -o {output_file}"
        subprocess.run(command, shell=True, check=True)
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}[-] Amass failed: {e}{Style.RESET_ALL}")
        return None

def run_subfinder(domain):
    output_file = f"results/{domain}_subfinder.txt"
    try:
        command = f"subfinder -d {domain} -o {output_file}"
        subprocess.run(command, shell=True, check=True)
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}[-] Subfinder failed: {e}{Style.RESET_ALL}")
        return None

def run_assetfinder(domain):
    output_file = f"results/{domain}_assetfinder.txt"
    try:
        command = f"assetfinder --subs-only {domain} > {output_file}"
        subprocess.run(command, shell=True, check=True)
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}[-] Assetfinder failed: {e}{Style.RESET_ALL}")
        return None

def run_findomain(domain):
    output_file = f"results/{domain}_findomain.txt"
    try:
        command = f"findomain -t {domain} -u {output_file}"
        subprocess.run(command, shell=True, check=True)
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}[-] Findomain failed: {e}{Style.RESET_ALL}")
        return None

def run_dnsdumpster(domain):
    output_file = f"results/{domain}_dnsdumpster.txt"
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        session = requests.Session()
        response = session.get('https://dnsdumpster.com/', headers=headers)
        
        csrf_token = response.text.split('name="csrfmiddlewaretoken" value="')[1].split('"')[0]
        cookies = {'csrftoken': csrf_token}
        
        data = {
            'csrfmiddlewaretoken': csrf_token,
            'targetip': domain,
            'user': 'free'
        }
        
        response = session.post('https://dnsdumpster.com/', headers=headers, 
                              cookies=cookies, data=data, timeout=30)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table', class_='table')
        
        subdomains = set()
        for table in tables:
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) > 0:
                    subdomain = cells[0].text.strip()
                    if domain in subdomain:
                        subdomains.add(subdomain)
        
        with open(output_file, 'w') as f:
            f.write('\n'.join(subdomains))
        
        return output_file
    except Exception as e:
        print(f"{Fore.RED}[-] DNSDumpster failed: {e}{Style.RESET_ALL}")
        return None

def run_ctfr(domain):
    output_file = f"results/{domain}_ctfr.txt"
    try:
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        subdomains = set()
        for entry in data:
            name = entry['name_value']
            if '\n' in name:
                for sub in name.split('\n'):
                    if domain in sub:
                        subdomains.add(sub)
            elif domain in name:
                subdomains.add(name)
        
        with open(output_file, 'w') as f:
            f.write('\n'.join(subdomains))
        
        return output_file
    except Exception as e:
        print(f"{Fore.RED}[-] CTFR failed: {e}{Style.RESET_ALL}")
        return None

def run_enumeration(domain):
    if not os.path.exists('results'):
        os.makedirs('results')
    
    tools = {
        'Sublist3r': run_sublist3r,
        'Amass': run_amass,
        'Subfinder': run_subfinder,
        'AssetFinder': run_assetfinder,
        'Findomain': run_findomain,
        'DNSDumpster': run_dnsdumpster,
        'CTFR': run_ctfr
    }
    
    results = {}
    
    print(f"\n{Fore.CYAN}[*] Starting subdomain enumeration for {domain}{Style.RESET_ALL}")
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(func, domain): name for name, func in tools.items()}
        
        for future in futures:
            tool_name = futures[future]
            try:
                output_file = future.result()
                if output_file and os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                    results[tool_name] = output_file
                    with open(output_file, 'r') as f:
                        count = len(f.readlines())
                    print(f"{Fore.GREEN}[+] {tool_name} found {count} subdomains ({output_file}){Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}[-] {tool_name} returned no results{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[-] {tool_name} failed: {str(e)}{Style.RESET_ALL}")
    
    # Combine all results
    combined_file = f"results/{domain}_combined.txt"
    unique_subdomains = set()
    
    for tool, file in results.items():
        try:
            with open(file, 'r') as f:
                for line in f:
                    subdomain = line.strip()
                    if subdomain and domain in subdomain:
                        unique_subdomains.add(subdomain)
        except Exception as e:
            print(f"{Fore.RED}[-] Error reading {tool} results: {e}{Style.RESET_ALL}")
            continue
    
    with open(combined_file, 'w') as f:
        f.write('\n'.join(sorted(unique_subdomains)))
    
    print(f"\n{Fore.CYAN}[*] Found {len(unique_subdomains)} unique subdomains{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[*] Combined results saved to {combined_file}{Style.RESET_ALL}")

def main_menu():
    clear_screen()
    print_banner()
    
    while True:
        print(f"\n{Fore.YELLOW}Main Menu:{Style.RESET_ALL}")
        print(f"1. {Fore.GREEN}Install Required Tools{Style.RESET_ALL}")
        print(f"2. {Fore.CYAN}Run Subdomain Enumeration{Style.RESET_ALL}")
        print(f"3. {Fore.RED}Exit{Style.RESET_ALL}")
        
        try:
            choice = input(f"\n{Fore.BLUE}Select an option (1-3): {Style.RESET_ALL}").strip()
            
            if choice == '1':
                install_all_tools()
            elif choice == '2':
                domain = input(f"\n{Fore.BLUE}Enter target domain (e.g., example.com): {Style.RESET_ALL}").strip()
                if domain:
                    if not domain.startswith(('http://', 'https://')):
                        domain = domain.replace('www.', '')  # Remove www if present
                    run_enumeration(domain)
                else:
                    print(f"{Fore.RED}[-] Please enter a valid domain{Style.RESET_ALL}")
            elif choice == '3':
                print(f"{Fore.YELLOW}[!] Exiting...{Style.RESET_ALL}")
                sys.exit(0)
            else:
                print(f"{Fore.RED}[-] Invalid choice{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Operation cancelled by user{Style.RESET_ALL}")
            continue
        except Exception as e:
            print(f"{Fore.RED}[-] Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    # Check if running in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print(f"{Fore.YELLOW}[!] Warning: Not running in a virtual environment{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Recommended to create one with: python3 -m venv env && source env/bin/activate{Style.RESET_ALL}")
    
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[-] Program terminated by user{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}[-] Fatal error: {e}{Style.RESET_ALL}")
        sys.exit(1)
