NETWORK_KNOWLEDGE = [
    {
        "name": "network",
        "keywords": ["computer network", "network", "কম্পিউটার নেটওয়ার্ক", "নেটওয়ার্ক"],
        "definition": "A computer network is a group of connected devices that communicate and share data or resources.",
        "details": "Networks can use wired or wireless connections and may operate over local or wide geographic areas."
    },
    {
        "name": "ip_address",
        "keywords": ["ip address", "ip", "আইপি অ্যাড্রেস", "আইপি"],
        "definition": "An IP address is a numerical address used to identify a device or network interface on an IP network.",
        "details": "IP addresses are used for network communication and routing."
    },
    {
        "name": "ipv4",
        "keywords": ["ipv4", "ipv4 address"],
        "definition": "IPv4 is the fourth version of the Internet Protocol and uses 32-bit addresses.",
        "details": "An IPv4 address is commonly written as four decimal numbers separated by dots, such as 192.168.1.10."
    },
    {
        "name": "ipv6",
        "keywords": ["ipv6", "ipv6 address"],
        "definition": "IPv6 is the sixth version of the Internet Protocol and uses 128-bit addresses.",
        "details": "IPv6 provides a much larger address space than IPv4."
    },
    {
        "name": "local_ip",
        "keywords": ["local ip", "private ip", "local ip address", "private ip address"],
        "definition": "A local or private IP address identifies a device within a private network.",
        "details": "Private IPv4 ranges include 10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16."
    },
    {
        "name": "public_ip",
        "keywords": ["public ip", "public ip address"],
        "definition": "A public IP address is an address that can identify a network or device on the public Internet.",
        "details": "Internet service providers commonly assign public IP addresses to customer connections."
    },
    {
        "name": "mac_address",
        "keywords": ["mac address", "mac", "ম্যাক অ্যাড্রেস"],
        "definition": "A MAC address is a hardware-level network interface identifier used on local networks.",
        "details": "MAC addresses are commonly represented as hexadecimal values."
    },
    {
        "name": "dns",
        "keywords": ["dns", "domain name system", "ডিএনএস"],
        "definition": "DNS translates domain names into IP addresses and helps locate network services.",
        "details": "For example, a DNS resolver can translate a website hostname into an IP address."
    },
    {
        "name": "dhcp",
        "keywords": ["dhcp", "dynamic host configuration protocol"],
        "definition": "DHCP automatically provides network configuration information to devices.",
        "details": "DHCP can assign IP addresses, subnet information, gateways, and DNS server information."
    },
    {
        "name": "router",
        "keywords": ["network router", "router", "রাউটার"],
        "definition": "A router forwards network traffic between different networks.",
        "details": "Home routers commonly connect a local network to an Internet service provider."
    },
    {
        "name": "gateway",
        "keywords": ["default gateway", "network gateway", "gateway", "গেটওয়ে"],
        "definition": "A default gateway is the network device used to send traffic from a local network toward other networks.",
        "details": "In many home networks, the router acts as the default gateway."
    },
    {
        "name": "wifi",
        "keywords": ["wi-fi", "wifi", "wireless network", "ওয়াইফাই"],
        "definition": "Wi-Fi is a wireless networking technology used to connect devices to a local network.",
        "details": "Wi-Fi commonly operates using IEEE 802.11 standards."
    },
    {
        "name": "ethernet",
        "keywords": ["ethernet", "wired network", "ইথারনেট"],
        "definition": "Ethernet is a family of wired networking technologies commonly used for local area networks.",
        "details": "Ethernet commonly uses network cables and network interface hardware."
    },
    {
        "name": "network_adapter",
        "keywords": ["network adapter", "network interface", "network interface card", "nic", "নেটওয়ার্ক অ্যাডাপ্টার"],
        "definition": "A network adapter is hardware or software that provides network connectivity to a computer.",
        "details": "A computer may have separate Ethernet and Wi-Fi network adapters."
    },
    {
        "name": "port",
        "keywords": ["network port", "port number", "network port number", "পোর্ট"],
        "definition": "A network port is a logical endpoint used to identify a particular service or connection on a host.",
        "details": "TCP and UDP use port numbers from 0 through 65535."
    },
    {
        "name": "tcp",
        "keywords": ["tcp", "transmission control protocol"],
        "definition": "TCP is a connection-oriented transport protocol designed for reliable, ordered data delivery.",
        "details": "TCP is commonly used by applications that require reliable communication."
    },
    {
        "name": "udp",
        "keywords": ["udp", "user datagram protocol"],
        "definition": "UDP is a connectionless transport protocol that sends datagrams without providing TCP-style delivery guarantees.",
        "details": "UDP is often useful when low overhead or low latency is more important than guaranteed delivery."
    },
    {
        "name": "http",
        "keywords": ["http", "hypertext transfer protocol"],
        "definition": "HTTP is an application-layer protocol used for communication between clients and web servers.",
        "details": "HTTP commonly uses TCP transport and is the foundation of traditional web communication."
    },
    {
        "name": "https",
        "keywords": ["https", "http secure", "secure http"],
        "definition": "HTTPS is HTTP protected using TLS encryption.",
        "details": "HTTPS helps protect web traffic against interception and tampering."
    },
    {
        "name": "ping",
        "keywords": ["network ping", "ping command", "ping", "পিং"],
        "definition": "Ping is a network diagnostic mechanism used to test reachability and measure round-trip response time.",
        "details": "Ping commonly uses ICMP echo request and echo reply messages."
    },
    {
        "name": "firewall",
        "keywords": ["network firewall", "firewall", "ফায়ারওয়াল"],
        "definition": "A firewall controls network traffic according to configured security rules.",
        "details": "Firewalls can allow or block traffic based on addresses, ports, protocols, applications, or other conditions."
    },
    {
        "name": "vpn",
        "keywords": ["vpn", "virtual private network", "ভিপিএন"],
        "definition": "A VPN creates an encrypted or otherwise protected network connection across another network.",
        "details": "VPNs are commonly used for privacy, secure remote access, and connecting to private networks."
    }
]
def get_network_knowledge():
    return NETWORK_KNOWLEDGE
def search_network_knowledge(query):
    if not query:
        return []
    text = str(query).strip().lower()
    matches = []
    for item in NETWORK_KNOWLEDGE:
        best_keyword = None
        for keyword in item["keywords"]:
            keyword_lower = keyword.lower().strip()
            if not keyword_lower:
                continue
            keyword_words = keyword_lower.split()
            if len(keyword_words) == 1:
                matched = keyword_lower in text.split()
            else:
                matched = keyword_lower in text
            if matched:
                if (
                    best_keyword is None
                    or len(keyword_lower) > len(best_keyword)
                ):
                    best_keyword = keyword_lower
        if best_keyword is not None:
            matches.append(
                (
                    len(best_keyword),
                    item
                )
            )
    matches.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in matches]
