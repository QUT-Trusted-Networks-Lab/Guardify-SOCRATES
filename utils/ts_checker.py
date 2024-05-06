import Levenshtein

def read_packages_from_file(filename):
    """
    Reads package names from a file and returns them as a list.
    """
    with open(filename, "r") as file:
        return [line.strip() for line in file if line.strip()]

def is_potential_typosquatting(your_package, package_list, threshold=0.8):
    """
    Determines if 'your_package' is potentially a victim of typosquatting.

    Returns 'True' if there is a package in the list with a high similarity score.
    """
    for package in package_list:
        if package != your_package and Levenshtein.ratio(your_package, package) >= threshold:
            return True
    return False

# Read packages from the file
filename = "python_packages.txt"
packages = read_packages_from_file(filename)

# Ask the user to enter a package name
your_package = input("Enter the package name to check for typosquatting: ")

# Check for potential typosquatting
if is_potential_typosquatting(your_package, packages):
    print("Potential typosquatting detected.")
else:
    print("No typosquatting detected.")
