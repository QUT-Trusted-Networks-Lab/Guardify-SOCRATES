import requests

def download_all_packages():
    """
    Fetches the list of all packages from PyPI and returns them as a list.
    """
    url = "https://pypi.org/simple/"

    try:
        response = requests.get(url)
        response.raise_for_status()

        # Extract package names from the HTML
        packages = [line.split('>')[1].split('<')[0] for line in response.text.split('\n') if '<a href' in line]
        return packages

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def write_packages_to_file(packages, filename):
    """
    Writes the list of packages to a specified file, each on a new line.
    """
    with open(filename, "w") as file:
        for package in packages:
            file.write(f"{package}\n")

# Fetch the list of packages
packages = download_all_packages()

# Write the list to a file
filename = "python_packages.txt"
write_packages_to_file(packages, filename)

print(f"Total number of packages: {len(packages)}")
print(f"List of packages written to {filename}")
