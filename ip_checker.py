import ipaddress
import re
import os

# Fastly IPv4 ranges
fastly_ipv4_ranges = [
    ipaddress.ip_network("23.235.32.0/20"),
    ipaddress.ip_network("43.249.72.0/22"),
    ipaddress.ip_network("103.244.50.0/24"),
    ipaddress.ip_network("103.245.222.0/23"),
    ipaddress.ip_network("103.245.224.0/24"),
    ipaddress.ip_network("104.156.80.0/20"),
    ipaddress.ip_network("140.248.64.0/18"),
    ipaddress.ip_network("140.248.128.0/17"),
    ipaddress.ip_network("146.75.0.0/17"),
    ipaddress.ip_network("151.101.0.0/16"),
    ipaddress.ip_network("157.52.64.0/18"),
    ipaddress.ip_network("167.82.0.0/17"),
    ipaddress.ip_network("167.82.128.0/20"),
    ipaddress.ip_network("167.82.160.0/20"),
    ipaddress.ip_network("167.82.224.0/20"),
    ipaddress.ip_network("172.111.64.0/18"),
    ipaddress.ip_network("185.31.16.0/22"),
    ipaddress.ip_network("199.27.72.0/21"),
    ipaddress.ip_network("199.232.0.0/16")
]

# Fastly IPv6 ranges
fastly_ipv6_ranges = [
    ipaddress.ip_network("2a04:4e40::/32"),
    ipaddress.ip_network("2a04:4e42::/32")
]

# Fastly IPv6 ranges
fastly_ipv6_ranges = [
    ipaddress.ip_network("2a04:4e40::/32"),
    ipaddress.ip_network("2a04:4e42::/32")
]

def is_fastly_ip(ip_str):
    try:
        ip_addr = ipaddress.ip_address(ip_str)
    except ValueError:
        return False

    # Check if the IP address is private
    if ip_addr.is_private:
        return None

    # Check against Fastly ranges (only for IPv4)
    if ip_addr.version == 4:
        for network in fastly_ipv4_ranges:
            if ip_addr in network:
                return True

    return False

def extract_ips_from_log(log_file_path, pattern):
    with open(log_file_path, 'r') as file:
        log_content = file.read()
    return re.findall(pattern, log_content)

def main():
    log_file_path = 'output.log'
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'    
    extracted_ips = extract_ips_from_log(log_file_path, ip_pattern)

    # Ensure the logging directory exists
    log_dir = 'logs/network_activity_logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Log file for the results
    result_log_path = os.path.join(log_dir, 'network_activity_results.log')
    
    with open(result_log_path, 'w') as result_file:
        for ip in extracted_ips:
            fastly_check = is_fastly_ip(ip)
            if fastly_check is None:
                # Ignore private IP addresses
                continue
            elif fastly_check:
                result_file.write(f"{ip} belongs to Fastly\n")
            else:
                result_file.write(f"WARNING: {ip} does not belong to Fastly\n")

if __name__ == '__main__':
    main()