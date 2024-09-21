import requests

# Function to check if /login or /auth/login exists
def check_login_paths(domain):
    login_paths = ['/login', '/auth/login']
    domain_url = 'https://' + domain.strip()

    for path in login_paths:
        test_url = domain_url + path
        try:
            response = requests.head(test_url, timeout=5)
            if response.status_code == 200:
                print(f'Login page found at: {test_url}')
            else:
                print(f'No login page found at: {test_url}')
        except requests.RequestException as e:
            print(f'Error checking {test_url}: {e}')

# Function to read domains from a text file and check login paths
def check_domains_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            domains = file.readlines()
            for domain in domains:
                print(f"\nChecking domain: {domain.strip()}")
                check_login_paths(domain)
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage: Check domains listed in 'domains.txt'
file_path = 'domains.txt'
check_domains_from_file(file_path)
