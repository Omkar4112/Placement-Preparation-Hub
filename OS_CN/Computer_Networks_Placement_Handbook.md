# Computer Networks Placement Handbook
## Ultimate Interview Preparation Guide (5-15 LPA Target)

---

# SECTION 1: CORE TOPICS & 7-POINT BREAKDOWNS

---

## 1. Computer Networks
* **Connection to Full-Stack Web Development:** Standardizes communication between React frontends and Spring Boot backends across public and private infrastructure.

### 1. Precise Definition
A computer network is a system of interconnected computing nodes (computers, servers, routers, switches) that communicate with each other using standardized protocols over physical or wireless transmission media to share resources and data.

### 2. Why it exists
Networks enable distributed computing. Instead of running monolithic systems on single machines, networks allow services to be modularized, resources to be shared (databases, storage), and clients (browsers) to communicate with servers globally.

### 3. Internal Working
Computing devices encode data into binary electrical, optical, or radio signals. Data is split into smaller units called **packets** (which contain headers for routing and payloads for data). Intermediate devices, such as switches (Layer 2) and routers (Layer 3), read packet headers and use routing tables (via protocols like OSPF or BGP) to forward packets hop-by-hop to their destination IP. The destination reassembles these packets back into the original data stream.

### 4. Advantages / Limitations
* **Advantages:** Facilitates resource sharing, simplifies scale-out architectures, and allows real-time remote communication.
* **Limitations:** Introduces latency and packet loss. Requires security controls (like firewalls and encryption) to protect against eavesdropping and attacks.

### 5. Interview Answer (30-60 seconds)
> "A computer network is an interconnection of computing devices that communicate using standardized protocol suites like TCP/IP. It allows distributed systems to share resources and data. Internally, networks split data into packets, route them across intermediate switches and routers using physical or wireless media, and reassemble them at the destination. While networking enables modern distributed applications, it introduces challenges like latency, packet loss, and security risks, which require protocols like TLS to resolve."

### 6. Common Follow-up Questions
* What is the difference between physical topology and logical topology?
* What is packet switching, and how does it differ from circuit switching?

### 7. Connection to Real Software Systems
When a user visits a React frontend, the browser initiates a network connection to a cloud provider's load balancer, which routes the request to a Spring Boot backend server, which then queries a PostgreSQL database over a private database network.

---

## 2. OSI Model
* **Connection to Full-Stack Web Development:** Organizes network architecture from physical cables up to HTTP/WebSocket protocols in modern applications.

### 1. Precise Definition
The Open Systems Interconnection (OSI) model is a conceptual framework developed by the ISO that defines network communication in seven layers, separating the physical transmission of bits from high-level application logic.

### 2. Why it exists
To standardize network communication and ensure interoperability between different hardware and software vendors. It allows developers to modify a protocol at one layer (e.g., swapping HTTP for WebSockets at Layer 7) without changing the underlying routing layer (Layer 3).

### 3. Internal Working
Data flows down the OSI stack at the sending node (Encapsulation) and up the stack at the receiving node (Decapsulation).
* **Layer 7 (Application):** UI interaction protocols (HTTP, FTP, DNS, WebSocket).
* **Layer 6 (Presentation):** Data formatting, encryption, and compression (SSL/TLS).
* **Layer 5 (Session):** Establishes, manages, and terminates session connections (RPC, NetBIOS).
* **Layer 4 (Transport):** End-to-end reliability and flow control (TCP, UDP). Data units are called **Segments**.
* **Layer 3 (Network):** Routing and logical addressing (IP, ICMP). Data units are called **Packets**.
* **Layer 2 (Data Link):** Node-to-node framing and physical addressing (Ethernet, MAC, ARP). Data units are called **Frames**.
* **Layer 1 (Physical):** Bitstream transmission over hardware media (cables, hubs, electrical voltages).

```
[Sending Host]                                      [Receiving Host]
  Layer 7: Application    --- Encapsulates --->       Layer 7: Application    (Data)
  Layer 6: Presentation                               Layer 6: Presentation   (Data)
  Layer 5: Session                                    Layer 5: Session        (Data)
  Layer 4: Transport      --- Segments --------->     Layer 4: Transport      (Segment)
  Layer 3: Network        --- Packets ----------->    Layer 3: Network        (Packet)
  Layer 2: Data Link      --- Frames ------------>    Layer 2: Data Link      (Frame)
  Layer 1: Physical       --- Bits ------------->     Layer 1: Physical       (Bits)
```

### 4. Advantages / Limitations
* **Advantages:** Clean separation of concerns makes debugging and hardware design modular.
* **Limitations:** The 7-layer division is conceptual. Real-world implementations (like the TCP/IP stack) combine or skip layers to improve performance.

### 5. Interview Answer (30-60 seconds)
> "The OSI model is a conceptual 7-layer framework that standardizes networking protocol design. It divides network communication into seven layers: Physical, Data Link, Network, Transport, Session, Presentation, and Application. During transmission, data flows down the layers on the sending host, with each layer adding header metadata (Encapsulation), and flows up the layers on the receiving host (Decapsulation). It helps developers isolate network issues and design modular protocols, though in practice, the industry uses the simpler TCP/IP model."

### 6. Common Follow-up Questions
* At which OSI layer do routers, switches, and hubs operate? (Answer: Routers at Layer 3; Switches at Layer 2; Hubs at Layer 1).
* What is encapsulation and decapsulation?

### 7. Connection to Real Software Systems
When a React application makes an API request to a Spring Boot backend, the browser handles Layer 7 (HTTP formatting), Layer 6 (encrypting the payload via HTTPS/TLS), Layer 4 (establishing a TCP segment stream), and hands it off to the OS kernel to route the packets (Layer 3) over physical cables (Layer 1).

---

## 3. TCP/IP Model
* **Connection to Full-Stack Web Development:** The concrete protocol stack that powers the internet, handling HTTP, WebSocket, TCP, and IP operations.

### 1. Precise Definition
The TCP/IP model is a concrete, implementation-oriented network model that defines communication using four layers: Network Access, Internet, Transport, and Application.

### 2. Why it exists
While the OSI model is a theoretical guide, the TCP/IP model is the actual architecture of the internet. It was designed to support resource sharing across networks, with an emphasis on routing packets even if some intermediate nodes fail.

### 3. Internal Working
The model consolidates OSI layers into four layers:
1. **Application Layer:** Combines OSI Layers 5, 6, and 7. Houses application protocols (HTTP, HTTPS, DNS, SMTP, WebSockets).
2. **Transport Layer:** Maps to OSI Layer 4. Manages end-to-end host communication via TCP (connection-oriented, reliable) or UDP (connectionless, fast).
3. **Internet Layer:** Maps to OSI Layer 3. Handles packet routing and logical addressing using IPv4 or IPv6.
4. **Network Access Layer:** Combines OSI Layers 1 and 2. Defines how data is physically framed and transmitted over a local link (Ethernet, Wi-Fi, MAC addresses).

### 4. Advantages / Limitations
* **Advantages:** Simpler and more practical than the OSI model. The foundation of the global internet.
* **Limitations:** Protocols are closely tied to the model, making it difficult to introduce new layer-level abstractions.

### 5. Interview Answer (30-60 seconds)
> "The TCP/IP model is the practical four-layer protocol stack that powers the internet. It consists of the Application, Transport, Internet, and Network Access layers. It simplifies the OSI model by combining the application, presentation, and session layers into a single Application layer, and combining the physical and data link layers into the Network Access layer. This model is the foundation of modern web systems, defining how HTTP payloads are encapsulated into TCP segments, routed as IP packets, and transmitted over physical networks."

### 6. Common Follow-up Questions
* How does the TCP/IP model simplify the OSI model?
* What is the role of the Internet layer in the TCP/IP model?

### 7. Connection to Real Software Systems
Spring Boot applications run on top of the TCP/IP stack. The embedded Tomcat server binds to a TCP port (Transport Layer) on an IP address (Internet Layer) to listen for incoming HTTP request packets (Application Layer).

---

## 4. OSI vs TCP/IP Model
* **Connection to Full-Stack Web Development:** Standardizes developer terminology (e.g., using "Layer 4 Load Balancer" for TCP and "Layer 7 Load Balancer" for HTTP routing).

### 1. Precise Definition
The OSI model is a 7-layer theoretical framework used for conceptualizing network architectures, while the TCP/IP model is a 4-layer functional framework that describes the protocols used on the internet.

### 2. Why it exists
Understanding the relationship between the two models allows developers to map conceptual standards to actual protocol implementations.

### 3. Internal Working
* **OSI** has 7 layers; **TCP/IP** has 4.
* **OSI** defines clear boundaries between services, interfaces, and protocols. **TCP/IP** is more loosely structured, designed around the protocols themselves.
* **OSI** was developed by committee (ISO) after the protocols were proposed; **TCP/IP** was built first (by DARPA) to fit working code.

```
OSI Model Layers                     TCP/IP Model Layers
+----------------------+             +----------------------+
| 7. Application       | ----------> |                      |
| 6. Presentation      | ----------> | 4. Application       |
| 5. Session           | ----------> |                      |
+----------------------+             +----------------------+
| 4. Transport         | ----------> | 3. Transport         |
+----------------------+             +----------------------+
| 3. Network           | ----------> | 2. Internet          |
+----------------------+             +----------------------+
| 2. Data Link         | ----------> | 1. Network Access    |
| 1. Physical          | ----------> |                      |
+----------------------+             +----------------------+
```

### 4. Advantages / Limitations
* **OSI:** Great for training and conceptual design, but inefficient for direct software implementation.
* **TCP/IP:** Efficient and widely implemented, but leaves some layer transitions (like encryption vs application formatting) less clearly separated.

### 5. Interview Answer (30-60 seconds)
> "The key difference is that the OSI model is a theoretical 7-layer model used to design network architectures, whereas the TCP/IP model is a practical 4-layer model that defines the protocols used on the internet. OSI separates the application, presentation, and session layers, and the data link and physical layers. TCP/IP groups these into the Application and Network Access layers, respectively. When we talk about Layer 4 load balancing, we refer to OSI Transport layer routing; when we talk about Layer 7 load balancing, we refer to Application layer routing."

### 6. Common Follow-up Questions
* Why did the TCP/IP model succeed over the OSI model in commercial implementation?
* What is a Layer 7 Load Balancer vs a Layer 4 Load Balancer?

### 7. Connection to Real Software Systems
Nginx acts as a Layer 7 Load Balancer when it routes requests based on HTTP URL paths (e.g., `/api/v1/users` to Spring Boot, `/` to React CDN), and acts as a Layer 4 Load Balancer when it routes connections based only on TCP ports and IP addresses.

---

## 5. IP Address
* **Connection to Full-Stack Web Development:** Identifies backend servers, database nodes, and API endpoints across the internet or within virtual private clouds.

### 1. Precise Definition
An Internet Protocol (IP) address is a numerical label assigned to each device connected to a computer network that uses the Internet Protocol for communication, serving as a logical identifier for routing.

### 2. Why it exists
Devices must be addressable to send and receive data. An IP address provides a logical location identifier that routers can use to find the best path for sending packets across networks.

### 3. Internal Working
An IP address belongs to the Internet Layer (Layer 3). When a packet is sent:
* The sender includes the Source IP and Destination IP in the IP header.
* Routers read the Destination IP and apply a **subnet mask** (using bitwise AND operations) to determine the network portion of the address vs the host portion.
* The router checks its routing table to forward the packet to the next hop.
* IP addresses can be:
  * *Static:* Manually configured and permanent.
  * *Dynamic:* Assigned automatically by a **DHCP (Dynamic Host Configuration Protocol)** server.
  * *Private:* Non-routable on the public internet, used inside local networks (defined by RFC 1918, e.g., `10.0.0.0/8`, `192.168.0.0/16`).
  * *Public:* Internationally coordinated and routable on the public internet.

### 4. Advantages / Limitations
* **Advantages:** Allows logical grouping of networks (subnetting), simplifying global routing tables.
* **Limitations:** IP addresses can change (DHCP lease expiration), requiring a translation layer like DNS to maintain reliable connections.

### 5. Interview Answer (30-60 seconds)
> "An IP address is a logical identifier assigned to devices on a TCP/IP network. Operating at Layer 3, it allows routers to forward packets across different subnets. IP addresses consist of a network ID and a host ID, which routers identify using a subnet mask. They can be public and routable across the internet, or private and restricted to local networks. Because IP addresses are dynamic, software applications rely on DNS to translate domain names to IP addresses."

### 6. Common Follow-up Questions
* What is CIDR notation (e.g., `/24`)? (Answer: Classless Inter-Domain Routing; `/24` means the first 24 bits represent the network prefix, leaving 8 bits for host addresses).
* What is the purpose of NAT (Network Address Translation)?

### 7. Connection to Real Software Systems
When deploying a database like PostgreSQL on AWS RDS, it is assigned a private IP address within a private subnet, preventing public internet access while allowing Spring Boot backend instances in the same VPC to connect securely.

---

## 6. IPv4 vs IPv6
* **Connection to Full-Stack Web Development:** Ensures web APIs are accessible to clients on both legacy IPv4 networks and modern IPv6 cellular and consumer networks.

### 1. Precise Definition
IPv4 is a 32-bit logical addressing scheme that supports up to $4.3 \times 10^9$ addresses, whereas IPv6 is a 128-bit logical addressing scheme designed to resolve IPv4 address exhaustion.

### 2. Why it exists
The internet grew faster than expected, and the $4.3$ billion addresses available under IPv4 have been depleted. IPv6 exists to provide a larger address space ($3.4 \times 10^{38}$ addresses) and simplify routing configurations.

### 3. Internal Working
* **Address Size:** IPv4 uses 32-bit addresses written in dot-decimal format (e.g., `192.0.2.1`). IPv6 uses 128-bit addresses written in hexadecimal format (e.g., `2001:db8::1`).
* **Header Structure:** IPv6 has a simplified, fixed-size 40-byte header, which speeds up processing in routers compared to the variable-sized IPv4 header.
* **Security:** IPsec (security encryption protocol) is built directly into IPv6, whereas it is optional in IPv4.
* **No Broadcast:** IPv6 replaces broadcast traffic with multicast and anycast, reducing network noise.
* **Autoconfiguration:** IPv6 supports SLAAC (Stateless Address Autoconfiguration), allowing devices to generate their own IP address without a DHCP server.

| Parameter | IPv4 | IPv6 |
| :--- | :--- | :--- |
| **Address Space** | 32-bit (4.3 Billion addresses) | 128-bit ($3.4 \times 10^{38}$ addresses) |
| **Notation** | Dot-Decimal (e.g., `192.168.1.1`) | Hexadecimal (e.g., `2001:0db8::0001`) |
| **Header Size** | Variable (20 to 60 bytes) | Fixed (40 bytes) |
| **ARP Support** | Uses ARP to map IP to MAC | Uses Neighbor Discovery Protocol (NDP) |
| **NAT Required** | Yes (due to address limits) | No (every device can have a public IP) |

### 4. Advantages / Limitations
* **IPv6:**
  * *Advantages:* Unlimited address space, no NAT required, cleaner routing headers, built-in security.
  * *Limitations:* Not backward compatible with IPv4, requiring transition strategies like dual-stack routing or tunneling.

### 5. Interview Answer (30-60 seconds)
> "The primary difference between IPv4 and IPv6 is address space. IPv4 uses a 32-bit address space, providing roughly 4.3 billion addresses, which has now been exhausted. IPv6 uses a 128-bit address space, offering a virtually unlimited number of addresses. Beyond address size, IPv6 improves on IPv4 by using a simplified, fixed-size header to speed up routing, removing the need for NAT through end-to-end direct addressing, and replacing broadcast traffic with multicast. However, they are not backward-compatible, so systems must use dual-stack routing to support both."

### 6. Common Follow-up Questions
* What is a Dual-Stack network implementation?
* Why does IPv6 omit check-summing at the IP layer? (Answer: Because check-summing is handled at Layer 2 and Layer 4; removing it from Layer 3 speeds up packet processing in routers).

### 7. Connection to Real Software Systems
DNS servers host both `A` records (translating domain names to IPv4 addresses) and `AAAA` records (translating domain names to IPv6 addresses). Modern React applications use dual-stack configurations to ensure clients can connect regardless of their network type.

---

## 7. MAC Address
* **Connection to Full-Stack Web Development:** Used at the local network level to direct packet delivery to specific virtual machines or physical server network cards.

### 1. Precise Definition
A Media Access Control (MAC) address is a unique, 48-bit physical identifier burned into a device's Network Interface Card (NIC) during manufacturing, serving as a permanent address within a local network segment (Layer 2).

### 2. Why it exists
IP addresses are logical and can change depending on where a device connects. A MAC address is a permanent physical identifier that allows devices on the same local network segment to send frames directly to one another.

### 3. Internal Working
A MAC address is a 48-bit hex identifier, split into two parts:
* **Organizational Unique Identifier (OUI):** The first 24 bits, which identify the manufacturer (e.g., Intel, Apple).
* **Network Interface Controller Database:** The last 24 bits, assigned by the manufacturer.

At the Data Link Layer (Layer 2), Ethernet frames encapsulate packets and include the source and destination MAC addresses. When a frame travels over Ethernet:
1. The NIC reads the destination MAC address.
2. If the address matches its own MAC or is a broadcast address (`FF:FF:FF:FF:FF:FF`), it processes the frame.
3. If it does not match, the NIC discards the frame.

```
Ethernet Frame:
+---------------------+---------------------+-----------------+---------+
| Destination MAC     | Source MAC          | EtherType (0x80)| Payload |
| (6 Bytes)           | (6 Bytes)           | (2 Bytes)       | (Data)  |
+---------------------+---------------------+-----------------+---------+
```

### 4. Advantages / Limitations
* **Advantages:** Guaranteed uniqueness prevents hardware addressing conflicts on local links.
* **Limitations:** MAC addresses cannot be used for routing across networks because they do not contain subnet information.

### 5. Interview Answer (30-60 seconds)
> "A MAC address is a 48-bit physical identifier assigned to a network interface card at the factory. It operates at Layer 2 of the OSI model and is used to deliver data frames between devices on the same local network segment. Unlike logical IP addresses, MAC addresses are permanent and do not contain routing information. When sending data across different subnets, routers rewrite the Layer 2 headers with the MAC address of the next-hop interface while keeping the Layer 3 IP addresses intact."

### 6. Common Follow-up Questions
* How does a switch build its MAC address table? (Answer: By inspecting the source MAC address of incoming frames on each physical port).
* What is MAC spoofing?

### 7. Connection to Real Software Systems
Cloud virtual machines (like AWS EC2 instances) are assigned virtual MAC addresses by the hypervisor. This allows host servers to route internal network traffic to the correct virtual machine container.

---

## 8. DNS (Domain Name System)
* **Connection to Full-Stack Web Development:** Resolves domain names (e.g., `api.yoursite.com`) to the IP address of your load balancer or Spring Boot backend server.

### 1. Precise Definition
The Domain Name System (DNS) is a distributed database that translates human-readable domain names (e.g., `example.com`) into machine-routable IP addresses (e.g., `192.0.2.1`).

### 2. Why it exists
Humans memorize names easily, but computer networks require numerical IP addresses to route packets. DNS provides a global, scalable directory service to bridge this gap.

### 3. Internal Working
DNS resolution uses a hierarchical, recursive process:
1. The client checks its local cache. If there is a miss, it queries a **DNS Resolver** (usually managed by the ISP).
2. The Resolver queries a **Root Name Server** (`.`), which redirects the resolver to the **Top-Level Domain (TLD) Name Server** (e.g., `.com`).
3. The TLD Name Server redirects the resolver to the **Authoritative Name Server** for the target domain.
4. The Authoritative Name Server returns the IP address to the resolver.
5. The resolver caches the IP address for the duration of its **TTL (Time to Live)** and returns it to the client's browser.

```
Browser ----> DNS Resolver ----> Root Server (.)
                     | --------> TLD Server (.com)
                     | --------> Authoritative Server (example.com) -> Returns IP
```

* **Common DNS Record Types:**
  * `A`: Maps a domain to an IPv4 address.
  * `AAAA`: Maps a domain to an IPv6 address.
  * `CNAME`: Maps a domain to another domain (alias).
  * `MX`: Directs mail traffic to mail servers.
  * `TXT`: Stores text metadata, often used for security validations (like SPF or DKIM).

### 4. Advantages / Limitations
* **Advantages:** Scale-invariant lookup system using caching; allows servers to be swapped or scaled out behind a single domain name.
* **Limitations:** DNS updates take time to propagate globally due to TTL caching. Unencrypted DNS queries are vulnerable to intercept attacks (resolved using DNS over HTTPS/TLS).

### 5. Interview Answer (30-60 seconds)
> "DNS is the Domain Name System, a distributed directory that translates domain names into routative IP addresses. When a user requests a domain, the browser queries a recursive DNS resolver. If not cached, the resolver queries the Root server, the TLD server, and finally the domain's Authoritative Name Server to retrieve the IP record. DNS relies primarily on UDP port 53 for fast resolution and uses TTL values to manage cache lifetimes. Understanding DNS is key for configuring web routing records like A, AAAA, and CNAME."

### 6. Common Follow-up Questions
* Why does DNS use UDP instead of TCP? (Answer: Speed. UDP has no connection establishment handshake, minimizing lookup latency. DNS falls back to TCP port 53 if the response packet exceeds 512 bytes).
* What is DNS poisoning, and how does DNSSEC prevent it?

### 7. Connection to Real Software Systems
When deploying a full-stack application, you configure an `A` record mapping `yoursite.com` to your load balancer's public IP, and a `CNAME` record mapping `www.yoursite.com` to `yoursite.com`.

---

## 9. ARP (Address Resolution Protocol)
* **Connection to Full-Stack Web Development:** Translates the IP address of your Spring Boot app server to its physical MAC address on the local server rack switch.

### 1. Precise Definition
The Address Resolution Protocol (ARP) is a Layer 2 protocol used to map a known IP address (Layer 3) to a physical MAC address (Layer 2) on a local area network segment.

### 2. Why it exists
IP packets are routed across networks using logical IP addresses, but final frame delivery on a local network segment requires a physical MAC address. ARP bridges the gap between Layer 3 and Layer 2.

### 3. Internal Working
When a host wants to send an IP packet to a target on the same local network:
1. The host checks its local **ARP Cache** for the target's MAC address.
2. **ARP Cache Miss:** The host broadcasts an **ARP Request** frame to the local network: *"Who has IP `192.168.1.5`? Tell `192.168.1.2`."* (Targeted to MAC `FF:FF:FF:FF:FF:FF`).
3. Every device on the local network processes the request, but only the device with IP `192.168.1.5` responds.
4. The target sends an **ARP Reply** directly to the requester: *"I have `192.168.1.5`. My MAC is `00:1A:2B:3C:4D:5E`."*
5. The requester stores this mapping in its ARP Cache and begins sending data frames directly to the target MAC.

```
Sender (192.168.1.2) -------- ARP Request (Broadcast) -------> Broadcast Domain
Target (192.168.1.5) <------- ARP Reply (Unicast) ------------ Sender
```

### 4. Advantages / Limitations
* **Advantages:** Dynamic mapping removes the need to manually configure MAC tables on every device.
* **Limitations:** ARP has no built-in verification, making it vulnerable to **ARP Spoofing/Poisoning** attacks where an attacker sends fake ARP replies to intercept network traffic.

### 5. Interview Answer (30-60 seconds)
> "ARP, or Address Resolution Protocol, maps a logical IP address to a physical MAC address within a local network segment. When a device wants to send data to an IP address on its local subnet, it checks its ARP cache. On a cache miss, it broadcasts an ARP request containing the target IP. The device with that IP sends back a unicast ARP reply containing its MAC address. The sender caches this mapping and uses it to construct the Layer 2 frames. ARP is critical for final frame delivery, but is vulnerable to ARP spoofing due to a lack of authentication."

### 6. Common Follow-up Questions
* What is Gratuitous ARP? (Answer: An unsolicited ARP reply sent by a device to announce its IP-to-MAC mapping, used to detect duplicate IP addresses or update switch tables when a network card is swapped).
* How does an ARP request cross a router boundary? (Answer: It doesn't. ARP broadcasts are limited to the local subnet; the router processes the packet and uses its own ARP table to forward the packet on the next link).

### 7. Connection to Real Software Systems
When your Spring Boot backend communicates with a PostgreSQL database on the same local network subnet, the backend OS runs ARP to resolve the database's IP address into a MAC address to send data frames over the local network switch.

---

## 10. HTTP (Hypertext Transfer Protocol)
* **Connection to Full-Stack Web Development:** The foundation of web APIs. React frontends send HTTP requests to Spring Boot backends to fetch or modify data.

### 1. Precise Definition
The Hypertext Transfer Protocol (HTTP) is an application-layer, stateless protocol used to transmit hypermedia documents and structured data across the web.

### 2. Why it exists
HTTP provides a standardized, text-based request-response protocol for client-server communication, allowing web browsers to request resources and APIs to exchange data.

### 3. Internal Working
HTTP uses a request-response model over a TCP connection (typically port 80).
* **Statelessness:** Each request is independent and contains no history of previous interactions.
* **Structure:**
  * *Request:* Method (GET, POST, PUT, DELETE), Path, Headers (metadata, Content-Type), and Body.
  * *Response:* Status Code (e.g., 200 OK, 404 Not Found, 500 Internal Server Error), Headers, and Body.
* **Protocol Evolutions:**
  * **HTTP/1.1:** Introduced persistent TCP connections (Keep-Alive) and pipelining.
  * **HTTP/2:** Introduced binary framing, multiplexing (sending multiple requests over a single TCP connection without head-of-line blocking at the application level), header compression (HPACK), and server push.
  * **HTTP/3:** Replaces TCP with **QUIC** (a UDP-based transport protocol), resolving TCP head-of-line blocking during packet loss and speeding up connection handshakes.

### 4. Advantages / Limitations
* **Advantages:** Simple, human-readable text design; widely supported and easily cached.
* **Limitations:** High header overhead; stateless design requires extra mechanisms (like cookies or JWTs) to manage user state; unencrypted data is vulnerable to packet sniffing (resolved by HTTPS).

### 5. Interview Answer (30-60 seconds)
> "HTTP is the Hypertext Transfer Protocol, a stateless application-layer protocol used for client-server communication. It runs on a request-response model, where the client sends an HTTP request (defining a method, path, headers, and payload), and the server returns a response code and data. While HTTP/1.1 introduced persistent connections, HTTP/2 improved performance through multiplexing over a single TCP connection, and HTTP/3 transition to QUIC over UDP to eliminate head-of-line blocking."

### 6. Common Follow-up Questions
* What is the difference between HTTP/1.1 and HTTP/2?
* How does HTTP manage state if the protocol itself is stateless? (Answer: Using Cookies, Sessions, or Authorization Headers).

### 7. Connection to Real Software Systems
A React application uses `fetch()` or `Axios` to send HTTP requests to a Spring Boot `@RestController` endpoint, which returns JSON data serialized from database query results.

---

## 11. HTTPS (Hypertext Transfer Protocol Secure)
* **Connection to Full-Stack Web Development:** Encrypts user credentials, API keys, and session data sent between React clients and Spring Boot backends.

### 1. Precise Definition
HTTPS is an extension of HTTP that encrypts communications using the SSL/TLS protocol to guarantee data confidentiality, integrity, and authentication.

### 2. Why it exists
Standard HTTP sends data in plain text, leaving it vulnerable to packet sniffing, tampering, and man-in-the-middle (MITM) attacks. HTTPS encrypts the connection to protect sensitive user data like passwords, credit card numbers, and API tokens.

### 3. Internal Working
HTTPS runs HTTP over an encrypted SSL/TLS session (typically port 443).
1. The client initiates a connection to the server.
2. The server responds with its **SSL/TLS Certificate** containing the server's public key.
3. The client verifies the certificate against built-in trusted **Certificate Authorities (CAs)**.
4. Once verified, the client and server perform a TLS handshake to generate a shared **symmetric session key** using asymmetric encryption.
5. All subsequent HTTP requests and responses are encrypted using this symmetric key before being sent over TCP.

```
HTTP  -----> [Plain Text] ----------> TCP Segment
HTTPS ----> [SSL/TLS Layer (Encryption)] ---> [Ciphertext] ---> TCP Segment
```

### 4. Advantages / Limitations
* **Advantages:** Prevents eavesdropping and tampering; authenticates the server's identity to prevent spoofing.
* **Limitations:** The initial encryption handshake adds a small amount of latency and CPU overhead (mitigated by TLS Session Resumption).

### 5. Interview Answer (30-60 seconds)
> "HTTPS is the secure version of HTTP. It encrypts communication by running HTTP over the SSL/TLS protocol on port 443. During connection, the server presents a digital certificate verified by a trusted Certificate Authority. The client and server run a cryptographic handshake to authenticate the server and negotiate a symmetric session key. Once established, all HTTP data is encrypted before transmission, preventing eavesdropping, tampering, and man-in-the-middle attacks."

### 6. Common Follow-up Questions
* How does HTTPS verify that a certificate is untampered? (Answer: By verifying the digital signature of the Certificate Authority using the CA's public key stored in the browser's root trust store).
* What is a Man-in-the-Middle (MITM) attack?

### 7. Connection to Real Software Systems
When deploying a full-stack system, developers install an SSL certificate (often from Let's Encrypt) on an Nginx reverse proxy or AWS Load Balancer. This handles HTTPS decryption before forwarding the plain HTTP traffic to the Spring Boot backend inside a secure private network.

---

## 12. SSL/TLS (Secure Sockets Layer / Transport Layer Security)
* **Connection to Full-Stack Web Development:** Underpins secure database connections (PostgreSQL over SSL) and API endpoints (HTTPS).

### 1. Precise Definition
Transport Layer Security (TLS)—the successor to Secure Sockets Layer (SSL)—is a cryptographic protocol that provides secure communication over a computer network, enforcing confidentiality, data integrity, and authentication.

### 2. Why it exists
To secure transport protocols (like TCP) so that upper-layer application traffic (like HTTP or SMTP) can be transmitted over public networks without risk of interception or modification.

### 3. Internal Working
TLS uses two phases of cryptography:
1. **Asymmetric Cryptography (The TLS Handshake):** Used to authenticate the server (and optionally the client) and securely exchange a symmetric key.
   * *Server Authentication:* The server shares its public key signed by a CA. The client verifies it using the CA's public key.
   * *Key Exchange:* Algorithms like Diffie-Hellman Ephemeral (ECDHE) allow both sides to agree on a shared secret key without sending the key itself over the network.
2. **Symmetric Cryptography (Data Transfer):** Once the session key is agreed on, all application data is encrypted and decrypted using fast symmetric algorithms like AES or ChaCha20.
3. **Data Integrity:** A Message Authentication Code (MAC or HMAC) is appended to each packet to ensure the data is not modified in transit.

```
Client                                                  Server
  | ----- ClientHello (Supported Cipher Suites) ----->    |
  | <---- ServerHello, Certificate, Key Exchange -----    |
  | ----- [Verify Cert], Key Exchange, Finished ----->    |
  | <---- Session Key Confirmed, Finished ------------    |
  |<============== Encrypted Session Data ============>|
```

### 4. Advantages / Limitations
* **Advantages:** High security, data integrity, and server authentication.
* **Limitations:** TLS 1.2 requires two network round-trips (2RTT) for the handshake (improved to 1RTT in TLS 1.3).

### 5. Interview Answer (30-60 seconds)
> "TLS is a cryptographic protocol operating between the Transport and Application layers that secures network communication. It uses asymmetric encryption during the handshake phase to authenticate the server's certificate and agree on a symmetric key using algorithms like Diffie-Hellman. Once the handshake is complete, it switches to symmetric encryption using the agreed key for fast data transfer, and appends message authentication codes to ensure data integrity."

### 6. Common Follow-up Questions
* What is the difference between SSL and TLS? (Answer: SSL is the older, deprecated version; TLS is the modern, secure version, though the term 'SSL' is still commonly used to refer to both).
* What is a cipher suite?
* Explain the handshake differences between TLS 1.2 and TLS 1.3. (Answer: TLS 1.3 reduces the handshake from 2 round-trips to 1 round-trip and drops obsolete, insecure cipher suites).

### 7. Connection to Real Software Systems
When Spring Boot connects to a PostgreSQL database, you configure the connection pool to use TLS (`ssl=true`) to ensure that queries and credentials sent over the cloud network are encrypted.

---

## 13. TCP (Transmission Control Protocol)
* **Connection to Full-Stack Web Development:** Ensures that HTTP request and response packets between React and Spring Boot arrive complete and in order.

### 1. Precise Definition
The Transmission Control Protocol (TCP) is a connection-oriented, reliable, byte-stream transport-layer protocol that guarantees in-order, error-free delivery of data packets across a network.

### 2. Why it exists
IP networks are inherently unreliable; packets can be lost, corrupted, duplicated, or arrive out of order. TCP exists to manage these network limits, providing application developers with a reliable communication channel.

### 3. Internal Working
* **Connection-Oriented:** Establishes a virtual connection using a **Three-Way Handshake** before sending data.
* **Reliability (ARQ):** Every transmitted segment contains a sequence number. The receiver sends **ACKs (Acknowledgements)** to confirm receipt. If the sender's retransmission timer expires before it receives an ACK, it resends the packet.
* **Flow Control (Sliding Window):** The receiver advertises its buffer capacity (window size) in each ACK. The sender adjusts the amount of data it sends to avoid overwhelming the receiver's buffer.
* **Congestion Control:** The sender maintains a congestion window ($cwnd$) to avoid overloading the network, adjusting speed using algorithms like Slow Start and Congestion Avoidance (e.g., TCP Reno or BBR).

```
TCP Segment Header:
+------------------------------+------------------------------+
| Source Port (16 bits)        | Destination Port (16 bits)   |
+------------------------------+------------------------------+
| Sequence Number (32 bits)                                   |
+------------------------------+------------------------------+
| Acknowledgment Number (32 bits)                             |
+------------------------------+------------------------------+
| Window Size (16 bits)        | Flags (SYN, ACK, FIN, RST...) |
+------------------------------+------------------------------+
```

### 4. Advantages / Limitations
* **Advantages:** Guaranteed packet delivery and ordering simplifies application logic.
* **Limitations:** The connection handshake, acknowledgements, and congestion controls introduce latency. Prone to **Head-of-Line Blocking**: if a single packet is lost, all subsequent packets must wait in the buffer until the lost packet is retransmitted.

### 5. Interview Answer (30-60 seconds)
> "TCP is a connection-oriented, reliable transport-layer protocol. It guarantees error-free, in-order packet delivery using sequence numbers and acknowledgements. It manages network traffic through flow control, which uses a sliding window to keep the sender from overwhelming the receiver's buffer, and congestion control, which adjusts transmission speeds based on network load. While TCP is highly reliable, its connection overhead and susceptibility to head-of-line blocking make it slower than UDP."

### 6. Common Follow-up Questions
* How does the Sliding Window algorithm work?
* What is TCP Head-of-Line (HoL) blocking?

### 7. Connection to Real Software Systems
When a backend server queries a PostgreSQL database, it uses a TCP connection to ensure that the SQL query and the database results arrive complete and error-free.

---

## 14. UDP (User Datagram Protocol)
* **Connection to Full-Stack Web Development:** Powers fast, real-time services like DNS lookups, video streaming, and voice communication.

### 1. Precise Definition
The User Datagram Protocol (UDP) is a lightweight, connectionless, unreliable transport-layer protocol that sends independent packets (datagrams) without establishing a connection or guaranteeing delivery.

### 2. Why it exists
TCP's connection handshake, acknowledgements, and retransmissions introduce latency. UDP exists to provide a fast, minimal-overhead alternative for applications that prioritize low latency over guaranteed delivery.

### 3. Internal Working
* **Connectionless:** UDP sends datagrams immediately without a handshake.
* **Unreliable:** It does not use sequence numbers, ACKs, or retransmissions. Packets are sent and forgotten.
* **Header Simplicity:** UDP has a minimal 8-byte header (containing only Source Port, Destination Port, Length, and Checksum), compared to TCP's 20-byte header.
* **No Congestion/Flow Control:** UDP sends packets at the rate requested by the application, regardless of network congestion.

```
UDP Segment Header:
+------------------------------+------------------------------+
| Source Port (16 bits)        | Destination Port (16 bits)   |
+------------------------------+------------------------------+
| Length (16 bits)             | Checksum (16 bits)           |
+------------------------------+------------------------------+
```

### 4. Advantages / Limitations
* **Advantages:** Minimal overhead; fast packet transmission with zero connection latency; supports broadcast and multicast.
* **Limitations:** Packets can be lost, duplicated, or arrive out of order. The application layer must handle any sorting or recovery logic if needed.

### 5. Interview Answer (30-60 seconds)
> "UDP is a connectionless, lightweight transport-layer protocol that provides fast, low-overhead transmission. It does not establish a connection, send acknowledgements, or manage flow control, meaning it does not guarantee packet delivery or order. With a simple 8-byte header, it minimizes latency, making it ideal for real-time applications like DNS, VoIP, and video streaming, where occasional packet loss is acceptable."

### 6. Common Follow-up Questions
* Why does UDP have a checksum if it is an unreliable protocol? (Answer: To detect packet corruption; if the checksum check fails, the receiver discards the corrupted packet, though it does not request a retransmission).
* How does HTTP/3 utilize UDP?

### 7. Connection to Real Software Systems
Real-time web applications (like video conferencing or online multiplayer games) use UDP (via WebRTC) to stream audio and video packets, allowing the system to drop late frames rather than freezing to wait for retransmissions.

---

## 15. TCP vs UDP
* **Connection to Full-Stack Web Development:** Helps developers choose the right protocol: TCP for reliable APIs and database connections, and UDP for real-time streaming and fast lookups.

### 1. Precise Definition
TCP is a connection-oriented, reliable transport protocol that guarantees ordered packet delivery, whereas UDP is a connectionless, lightweight transport protocol that prioritizes speed and low latency without delivery guarantees.

### 2. Why it exists
This distinction provides developers with a choice between reliability (TCP) and speed (UDP) depending on the needs of the application.

### 3. Internal Working
Refer to the comparative table below:

| Feature | TCP | UDP |
| :--- | :--- | :--- |
| **Connection State** | Connection-oriented (Requires 3-way handshake) | Connectionless (Sends immediately) |
| **Reliability** | Guaranteed delivery (Uses ACKs and Retransmissions) | Best-effort delivery (Packets can be lost) |
| **Packet Ordering** | Guaranteed in-order delivery | No order guarantee (Packets can arrive out of sequence) |
| **Header Size** | 20 to 60 bytes | 8 bytes |
| **Flow & Congestion Control**| Yes (Sliding window, Slow Start) | None |
| **Transmission Type** | Byte stream (continuous) | Datagrams (independent packets) |

### 4. Advantages / Limitations
See individual sections for TCP and UDP.

### 5. Interview Answer (30-60 seconds)
> "The key difference is that TCP is a connection-oriented, reliable protocol, while UDP is a connectionless, best-effort protocol. TCP uses a three-way handshake to establish a connection, uses sequence numbers and ACKs to guarantee in-order delivery, and manages traffic flow and network congestion. This introduces latency, but guarantees completeness. UDP sends packets immediately with an 8-byte header and no delivery checks, maximizing speed. We use TCP for HTTP APIs and database connections, and UDP for DNS, streaming, and real-time WebRTC channels."

### 6. Common Follow-up Questions
* Can you implement reliability on top of UDP? (Answer: Yes, by writing sequencing and ACK logic in the application layer, which is how HTTP/3's QUIC protocol works).
* Which protocol is preferred for file transfers, and why?

### 7. Connection to Real Software Systems
A web browser uses TCP to request your React app's static HTML files, ensuring the code arrives intact, but uses UDP for a WebRTC video call to keep latency low.

---

## 16. Three-Way Handshake
* **Connection to Full-Stack Web Development:** The sequence of packets sent when a browser connects to a Spring Boot API server over a secure TCP channel.

### 1. Precise Definition
The TCP Three-Way Handshake is the process used to establish a reliable, connection-oriented session between a client and a server, synchronizing sequence numbers and allocating buffers before data transmission begins.

### 2. Why it exists
Since network links are unreliable, both hosts must verify that they can send and receive data before transmitting application payloads. The handshake also allows both sides to agree on initial sequence numbers (ISNs) to track packets.

### 3. Internal Working
The handshake uses three steps:
1. **SYN (Synchronize):** The client sends a packet with the `SYN` flag set, along with a random initial sequence number ($x$), to the server. (Client state: `SYN-SENT`).
2. **SYN-ACK (Synchronize-Acknowledge):** The server receives the SYN, allocates TCP buffers, and sends a reply with the `SYN` and `ACK` flags set. It acknowledges the client's packet by setting the ACK number to $x + 1$, and sends its own random initial sequence number ($y$). (Server state: `SYN-RECEIVED`).
3. **ACK (Acknowledge):** The client receives the SYN-ACK and sends an acknowledgement packet with the `ACK` flag set, setting the ACK number to $y + 1$. (Client state: `ESTABLISHED`, Server state: `ESTABLISHED` once received).

```
Client                                                  Server
  | ---------- SYN (Seq = x) -------------------------> | (SYN-RECEIVED)
  | <--------- SYN-ACK (Seq = y, Ack = x + 1) --------- |
  | ---------- ACK (Ack = y + 1) ---------------------> | (ESTABLISHED)
(ESTABLISHED)
```

### 4. Advantages / Limitations
* **Advantages:** Ensures both channels (upload and download) are active before data transfer.
* **Limitations:** Adds a full network round-trip time (1RTT) of latency. Vulnerable to **SYN Flood** DoS attacks, where an attacker sends many SYNs and ignores the server's SYN-ACKs, filling the server's connection buffer (mitigated using **SYN Cookies**).

### 5. Interview Answer (30-60 seconds)
> "The TCP Three-Way Handshake establishes a reliable connection between a client and a server. First, the client sends a SYN packet containing a random initial sequence number to the server. Second, the server responds with a SYN-ACK packet, acknowledging the client's sequence number and sending its own initial sequence number. Third, the client sends an ACK packet back to the server to confirm receipt. Once complete, both hosts enter the established state, and data transmission can begin."

### 6. Common Follow-up Questions
* What is a SYN Flood attack, and how do SYN Cookies prevent it? (Answer: SYN Cookies allow the server to avoid allocating buffer memory when receiving a SYN packet; instead, the server encodes connection information in the sequence number of the SYN-ACK packet, allocating resources only after receiving a valid ACK).
* Why is the initial sequence number randomized? (Answer: To prevent attackers from predicting sequence numbers and injecting malicious packets into an active connection).

### 7. Connection to Real Software Systems
When a React frontend initiates an API request, the browser's network stack runs the 3-way handshake with the Spring Boot server's port before sending the actual HTTP request payload.

---

## 17. Four-Way Connection Termination
* **What Interviewers Commonly Ask:** "Why does TCP connection termination require four steps, and what is the purpose of the TIME-WAIT state?"
* **Most Important Points to Remember:** FIN/ACK sequence; half-closed connection; TIME-WAIT duration ($2 \times \text{MSL}$).

### 1. Precise Definition
The Four-Way Connection Termination is the process used to gracefully close an active TCP connection, ensuring both hosts have finished sending their remaining data before freeing resource buffers.

### 2. Why it exists
TCP is full-duplex, meaning both channels (client-to-server and server-to-client) run independently. One host closing its sending channel does not mean the other host is done sending data, so each direction must be closed independently.

### 3. Internal Working
1. **FIN (Client to Server):** When the client is done sending data, it sends a packet with the `FIN` flag set. (Client state: `FIN-WAIT-1`).
2. **ACK (Server to Client):** The server receives the FIN and sends an `ACK`. (Server state: `CLOSE-WAIT`, Client state: `FIN-WAIT-2`). At this point, the client can no longer send data but can still receive it (half-closed connection).
3. **FIN (Server to Client):** Once the server finishes sending its remaining data, it sends its own `FIN` packet to the client. (Server state: `LAST-ACK`).
4. **ACK (Client to Server):** The client receives the FIN and sends a final `ACK`. (Client state: `TIME-WAIT`, Server state: `CLOSED` once received).
5. **TIME-WAIT State:** The client remains in the `TIME-WAIT` state for a duration of $2 \times \text{MSL}$ (Maximum Segment Lifetime, typically 4 minutes) before closing. This ensures any delayed packets still in transit are discarded rather than corrupting a new connection on the same port, and guarantees the server received the final ACK.

```
Client                                                  Server
  | ---------- FIN -----------------------------------> |
  | <--------- ACK ------------------------------------ | (CLOSE-WAIT)
  |                                                     | (Sends remaining data)
  | <--------- FIN ------------------------------------ |
  | ---------- ACK -----------------------------------> | (CLOSED)
(TIME-WAIT) -> (CLOSED after 2MSL)
```

### 4. Advantages / Limitations
* **Advantages:** Prevents data loss during shutdown by allowing both sides to finish their operations.
* **Limitations:** The TIME-WAIT state keeps socket resources open in the OS kernel for a few minutes. High-traffic servers can run out of available ports if connections close too quickly (resolved using TCP socket reuse configurations).

### 5. Interview Answer (30-60 seconds)
> "TCP uses a four-way handshake to close a connection because the protocol is full-duplex, requiring each direction of the connection to be terminated independently. First, the client sends a FIN packet, which the server acknowledges with an ACK, putting the connection into a half-closed state. Once the server finishes sending its data, it sends its own FIN packet. The client responds with a final ACK and enters the TIME-WAIT state for two times the Maximum Segment Lifetime. This ensures any delayed packets are discarded and the server received the final ACK before the port is reused."

### 6. Common Follow-up Questions
* What is the TIME-WAIT state, and why is it necessary?
* What is a half-closed TCP connection?

### 7. Connection to Real Software Systems
When a Spring Boot server closes a connection to a PostgreSQL database, the OS socket transition through these four states. If the connection is closed abruptly (e.g., due to a crash), the OS may send a `RST` (Reset) packet to immediately terminate the socket.

---

## 18. Client-Server Architecture
* **Connection to Full-Stack Web Development:** The basic design of web systems, where React applications act as clients that request resources from Spring Boot servers.

### 1. Precise Definition
Client-Server Architecture is a distributed application structure that partition tasks or workloads between resource providers (servers) and service requesters (clients).

### 2. Why it exists
To centralize business logic, data access, and security controls on dedicated servers, while offloading presentation rendering and user interactions to client devices.

### 3. Internal Working
* **The Client:** Initiates communication by sending requests. It is responsible for rendering the user interface and handling user interactions.
* **The Server:** Listens on a dedicated port for incoming connections, processes requests, runs business logic, and interacts with storage systems (like databases). It then returns a response to the client.
* **State Management:** Can be *Stateless* (the server treats each request as independent, as seen in REST APIs) or *Stateful* (the server maintains client session state in memory).

### 4. Advantages / Limitations
* **Advantages:** Centralizes data security, access control, and business logic. Clients can be lightweight (browsers).
* **Limitations:** The server can represent a single point of failure and a performance bottleneck if it is not scaled out behind a load balancer.

### 5. Interview Answer (30-60 seconds)
> "Client-Server Architecture is a distributed design that separates responsibilities between clients, which request services, and servers, which process requests and manage data. The client initiates a connection to the server's IP address and port. The server processes the request, queries databases if needed, and returns a response. This design centralizes data and business logic, though it requires load balancers and scaling strategies to handle high traffic and avoid single points of failure."

### 6. Common Follow-up Questions
* What is the difference between 2-tier, 3-tier, and N-tier architectures?
* How does client-server architecture differ from peer-to-peer (P2P) architecture?

### 7. Connection to Real Software Systems
In a modern full-stack web application, a React frontend running in the user's browser is the client, a Spring Boot backend is the application server, and PostgreSQL is the data storage server.

---

## 19. REST API (Representational State Transfer)
* **Connection to Full-Stack Web Development:** The standard communication protocol for web APIs, using HTTP methods to exchange JSON data between React and Spring Boot.

### 1. Precise Definition
REST is an architectural style for designing networked applications that relies on a stateless, client-server, cacheable communications protocol (typically HTTP) to manipulate resources using standard operations.

### 2. Why it exists
REST simplifies web service design by using standard HTTP features instead of complex, custom protocols (like SOAP). This standardization makes APIs easy to integrate, scale, and cache.

### 3. Internal Working
REST is defined by six design constraints:
1. **Uniform Interface:** Resources are identified by URIs (e.g., `/api/v1/users`). Resources are manipulated using standard HTTP methods:
   * `GET`: Retrieve a resource (Safe and Idempotent).
   * `POST`: Create a resource (Neither Safe nor Idempotent).
   * `PUT`: Replace an existing resource or create if missing (Idempotent).
   * `PATCH`: Partially update a resource (Not Idempotent).
   * `DELETE`: Remove a resource (Idempotent).
2. **Statelessness:** Each request from a client must contain all the information needed to understand and process it. The server does not store client session context.
3. **Client-Server Separation:** Clients and servers run and scale independently.
4. **Cacheability:** Responses must define themselves as cacheable or non-cacheable to improve network performance.
5. **Layered System:** Clients cannot tell if they are connected directly to the end server or an intermediate proxy or load balancer.
6. **Code on Demand (Optional):** Servers can transfer executable code (like JavaScript) to the client.

### 4. Advantages / Limitations
* **Advantages:** Scalable due to statelessness; easy to cache; highly compatible with web browsers.
* **Limitations:** Over-fetching or under-fetching data (requests return all resource properties; solved by technologies like GraphQL). Lacks a strict contract, which can lead to API versioning drift.

### 5. Interview Answer (30-60 seconds)
> "REST is an architectural style for designing APIs based on resources identified by URIs and manipulated using standard HTTP methods like GET, POST, PUT, and DELETE. Its core constraint is statelessness, meaning each request must contain all the data needed to process it, allowing the server to scale easily without storing session data. REST also enforces a uniform interface and cacheable responses, making it the standard for web application APIs."

### 6. Common Follow-up Questions
* What is the difference between PUT and PATCH?
* What does it mean for an API operation to be Idempotent? (Answer: An operation is idempotent if running it multiple times produces the same system state as running it once; e.g., GET, PUT, and DELETE are idempotent, while POST is not).

### 7. Connection to Real Software Systems
A React client sends a `GET /api/v1/products` request to a Spring Boot `@RestController` endpoint, which queries PostgreSQL, serializes the product list to JSON, and returns a `200 OK` response.

---

## 20. WebSocket
* **Connection to Full-Stack Web Development:** Enables real-time, bi-directional communication (such as chat notifications or live dashboards) between React clients and Spring Boot backends.

### 1. Precise Definition
WebSocket is an application-layer protocol that provides full-duplex, bi-directional communication channels over a single, long-lived TCP connection, initiated via an HTTP handshake.

### 2. Why it exists
HTTP's request-response model is pull-only; the client must request data, meaning the server cannot push updates dynamically. While techniques like polling or Server-Sent Events (SSE) exist, WebSocket provides a low-overhead, bi-directional alternative for real-time web applications.

### 3. Internal Working
1. **Handshake:** The client initiates a standard HTTP request to the server with connection upgrade headers:
   * `Connection: Upgrade`
   * `Upgrade: websocket`
   * `Sec-WebSocket-Key: <base64-key>`
2. **Upgrade:** If the server supports the protocol, it responds with status code `101 Switching Protocols`.
3. **Persistent Connection:** The underlying TCP connection remains open, and the communication switches to the WebSocket protocol.
4. **Framing:** Data is sent in lightweight binary or text frames (with a minimal 2 to 10-byte header, compared to HTTP's large headers), allowing both sides to push messages at any time.

```
Client                                                  Server
  | ----- HTTP GET (Upgrade to WebSocket) ------------> |
  | <---- HTTP 101 Switching Protocols ---------------- |
  |<====== WebSocket Full-Duplex Connection (TCP) =====>|
  | ----- [Frame: Hello] -----------------------------> |
  | <---- [Frame: Live Update] ------------------------ |
```

### 5. Interview Answer (30-60 seconds)
> "WebSocket is a protocol that enables full-duplex, bi-directional communication over a single, long-lived TCP connection. It starts with an HTTP request containing upgrade headers. If the server supports WebSockets, it returns a 101 Switching Protocols response, upgrading the socket. The TCP connection is kept open, allowing both client and server to send light-weight data frames at any time. This avoids the overhead of HTTP headers and polling, making it ideal for real-time applications like chat rooms and live dashboards."

### 6. Common Follow-up Questions
* How does WebSocket compare to Server-Sent Events (SSE)? (Answer: SSE is a one-way protocol where only the server can push updates to the client over standard HTTP; WebSockets is bi-directional).
* How does a WebSocket connection scale across multiple backend servers? (Answer: Since WebSockets are stateful and tied to a single server, you must use sticky sessions on your load balancer or a message broker like Redis Pub/Sub to sync messages across backend instances).

### 7. Connection to Real Software Systems
A React chat application connects to a Spring Boot server using a WebSocket connection managed by STOMP or SockJS, allowing users to send and receive messages instantly without reloading the page.

---

## 21. Cookies
* **Connection to Full-Stack Web Development:** Stored in the browser (React) and automatically sent with HTTP requests to Spring Boot servers to track sessions and user preferences.

### 1. Precise Definition
A cookie is a small piece of text data sent by a web server and stored by the user's browser, which is automatically included in the headers of subsequent requests to the same server.

### 2. Why it exists
Because HTTP is stateless, the server cannot naturally recognize requests coming from the same user. Cookies allow servers to store state information (like a session ID) on the client, which is automatically returned with every request.

### 3. Internal Working
1. When a client authenticates, the server includes a cookie in the response headers:
   * `Set-Cookie: session_id=xyz123; Secure; HttpOnly; SameSite=Strict`
2. The browser stores this data in its local cookie store, mapped to the domain.
3. For every subsequent request to that domain, the browser automatically appends the cookie to the request headers:
   * `Cookie: session_id=xyz123`
4. **Security Flags:**
   * `HttpOnly`: Prevents client-side scripts (like JavaScript) from reading the cookie, protecting it from Cross-Site Scripting (XSS) attacks.
   * `Secure`: Forces the browser to send the cookie only over encrypted HTTPS connections.
   * `SameSite`: Controls whether cookies are sent with cross-site requests, protecting against Cross-Site Request Forgery (CSRF) attacks (options: `Strict`, `Lax`, or `None`).

### 4. Advantages / Limitations
* **Advantages:** Managed automatically by the browser; supports security flags to protect sensitive session tokens.
* **Limitations:** Limited capacity (4KB per cookie); can increase HTTP request payload size; vulnerable to CSRF if not configured correctly with `SameSite`.

### 5. Interview Answer (30-60 seconds)
> "A cookie is a small text file sent by a web server and stored by the client's browser. Once set, the browser automatically appends the cookie to the headers of all subsequent requests to that domain, allowing the server to maintain state. To secure cookies, we use flags like HttpOnly to block JavaScript access and prevent XSS leaks, Secure to restrict transmission to HTTPS, and SameSite to prevent CSRF attacks."

### 6. Common Follow-up Questions
* What is the difference between session cookies and persistent cookies? (Answer: Session cookies are stored in volatile memory and deleted when the browser closes; persistent cookies contain an Expiration or Max-Age date and are saved to disk).
* Explain how SameSite protects against CSRF.

### 7. Connection to Real Software Systems
When a user logs into a web app, the Spring Boot backend creates a session, writes the session ID to an `HttpOnly` cookie, and sends it to the browser. The browser automatically includes this cookie in subsequent API requests.

---

## 22. Sessions
* **Connection to Full-Stack Web Development:** Tracks logged-in user state in the Spring Boot backend, utilizing a session ID cookie sent by the React client.

### 1. Precise Definition
A session is a server-side state-management mechanism that stores user interaction data across multiple requests, associating it with a unique Session ID shared with the client.

### 2. Why it exists
Storing all user data (such as shopping cart contents or user permissions) on the client is insecure and increases payload sizes. Sessions allow the server to store this data securely in memory or a database, requiring the client to hold only a reference key (the Session ID).

### 3. Internal Working
1. The client sends login credentials to the server.
2. **Session Creation:** The server validates the credentials, generates a unique Session ID, and creates a data record in its session store (RAM or database).
3. **Token Handback:** The server returns the Session ID to the client, usually in a cookie named `JSESSIONID` (Java) or `PHPSESSID`.
4. **State Lookup:** The client's browser sends this cookie with subsequent requests. The server reads the Session ID, retrieves the associated data record from its store, and loads the user's state.
5. **Session Expiration:** The session is deleted if it is idle for a configured period (e.g., 30 minutes) or when the user logs out.

```
Client                                                  Server
  | ----- POST /login (Credentials) ------------------> |
  |                                                     | [Creates Session #XYZ]
  | <---- Response + Set-Cookie (JSESSIONID=XYZ) ------- |
  | ----- GET /cart (Cookie: JSESSIONID=XYZ) ---------> |
  |                                                     | [Look up Session #XYZ]
  | <---- Response (Cart Data) ------------------------ |
```

### 4. Advantages / Limitations
* **Advantages:** Highly secure because the actual data remains on the server; allows storing larger amounts of state data.
* **Limitations:** Stateful servers do not scale easily. If sessions are stored in memory, requests must go to the same server (sticky sessions), or the servers must sync session state using a shared cache like Redis.

### 5. Interview Answer (30-60 seconds)
> "A session is a server-side state management mechanism that tracks user data across requests. When a user logs in, the server generates a unique session ID and stores the user's data in memory or a database. The session ID is sent to the browser, typically as a cookie. On subsequent requests, the server reads the session ID cookie to look up the user's data. Sessions are highly secure but can limit scalability, requiring a shared cache like Redis to sync session data across multiple server instances."

### 6. Common Follow-up Questions
* How do you scale session storage across a cluster of backend servers?
* What is the difference between session state and cookie state?

### 7. Connection to Real Software Systems
In Spring Boot, Spring Session handles session management. It can be configured to store session data in a shared PostgreSQL table or a Redis cache, ensuring that if one Spring Boot instance crashes, other instances in the cluster can still read the user's session.

---

## 23. JWT (JSON Web Token) Authentication Flow
* **Connection to Full-Stack Web Development:** A standard stateless authentication pattern where React stores a signed token and includes it in the Authorization headers of API requests to Spring Boot.

### 1. Precise Definition
JSON Web Token (JWT) is an open standard (RFC 7519) that defines a compact, self-contained way to securely transmit information between parties as a JSON object, signed using a secret key (HMAC) or a public/private key pair (RSA).

### 2. Why it exists
Traditional session authentication requires servers to store user session states, which limits scalability. JWT enables stateless authentication: all user metadata and permissions are encoded directly inside the token, allowing any backend server to verify the user without looking up session records in a database.

### 3. Internal Working
* **Token Structure:** A JWT consists of three parts separated by dots (`.`):
  * **Header:** Defines the token type and the hashing algorithm used (e.g., HS256).
  * **Payload:** Contains the claims (user metadata, permissions, expiration date).
  * **Signature:** The hash of the encoded header and payload, signed using a secret key known only to the server.
  * Formatted as: `base64Url(Header).base64Url(Payload).Signature`
* **Authentication Flow:**
  1. The client POSTs login credentials to the Spring Boot server.
  2. The server validates the credentials and generates a JWT signed with its private key.
  3. The server returns the JWT to the React client.
  4. The React application stores the token in memory or a cookie, and appends it to the headers of subsequent requests:
     * `Authorization: Bearer <token>`
  5. The Spring Boot server reads the token, verifies the signature using its key, extracts the user metadata and roles from the payload, and processes the request. No database session lookup is required.

```
React Client                                            Spring Boot Backend
  | ----- POST /login (Credentials) ------------------> |
  |                                                     | [Validates, Generates Signed JWT]
  | <---- Response (JWT Token) ------------------------ |
  | ----- GET /api/data (Header: Bearer JWT) ---------> |
  |                                                     | [Verifies Signature, Extracts Claims]
  | <---- Response (Data) ----------------------------- |
```

### 4. Advantages / Limitations
* **Advantages:** Completely stateless, simplifying horizontal scaling; works well across different domains (CORS-friendly); self-contained payload reduces database queries.
* **Limitations:** Cannot be easily revoked once issued (it remains valid until it expires, unless you implement a token blocklist in Redis). Token size is larger than a session ID cookie, increasing request sizes.

### 5. Interview Answer (30-60 seconds)
> "JWT is a stateless authentication mechanism where user identity and permissions are encoded as a signed JSON payload. A JWT has three parts: the Header, the Payload, and the cryptographically signed Signature. When a client logs in, the server generates and signs the JWT, returning it to the client. The client includes this token in the Authorization header of subsequent API requests. The server validates the signature using its key, allowing it to authenticate the user without performing database session lookups, which improves system scalability."

### 6. Common Follow-up Questions
* How do you revoke a JWT token before it expires? (Answer: By maintaining a short token lifetime and using a Redis-backed blocklist to track revoked tokens, or using refresh token rotation).
* Where should you store a JWT on the client side (Local Storage vs HttpOnly Cookie) and what are the security trade-offs? (Answer: Local Storage is vulnerable to XSS attacks; HttpOnly cookies protect against XSS but are vulnerable to CSRF, requiring SameSite protections).

### 7. Connection to Real Software Systems
In a Spring Boot security configuration, a custom filter intercepts incoming requests, reads the JWT from the `Authorization: Bearer` header, verifies the signature using a library like `jjwt`, and populates the Spring Security context with the user's details.

---
---

# SECTION 2: INTERVIEW QUESTIONS & STRUCTURED ANSWERS

This section provides structured, high-impact answers for the most common Computer Networks questions asked in technical interviews.

---

### Explain TCP vs UDP.
**How to Structure Your Answer:**
1. **Core Distinction:** Define connection-oriented vs connectionless.
2. **Reliability Mechanisms:** Explain how TCP ensures delivery while UDP does not.
3. **Header & Performance:** Compare header sizes and latency overhead.
4. **Use Case Examples:** Connect each to real-world applications.

**Interview Answer:**
> "The core difference between TCP and UDP is that TCP is a connection-oriented, reliable protocol, whereas UDP is connectionless and lightweight.
> 
> TCP establishes a connection using a three-way handshake and guarantees that packets arrive in order and error-free by using sequence numbers, acknowledgements, and retransmissions. It also uses sliding windows for flow control and congestion control to manage traffic. This ensures reliability but introduces latency.
> 
> UDP, on the other hand, sends independent packet datagrams immediately without a handshake or delivery guarantees. It has a minimal 8-byte header compared to TCP's 20-byte header, which minimizes latency. We use TCP for applications where reliability is critical, such as HTTP web traffic and database queries. We use UDP for real-time services like DNS, VoIP, and WebRTC streaming where speed is prioritized over occasional packet loss."

---

### Explain HTTP vs HTTPS.
**How to Structure Your Answer:**
1. **Definitions:** Define both protocols and state the core difference (security encryption).
2. **Cryptographic Layer:** Mention that HTTPS runs HTTP over SSL/TLS.
3. **Ports & Verification:** Compare default ports (80 vs 443) and mention CA certificates.
4. **Security Goals:** Mention authentication, integrity, and confidentiality.

**Interview Answer:**
> "HTTP and HTTPS are application-layer protocols used for client-server communication, with the key difference being security encryption.
> 
> HTTP transmits data in plain text, making it vulnerable to interception and tampering. HTTPS secures this connection by running HTTP over the SSL/TLS protocol, typically on port 443. 
> 
> During connection, HTTPS uses digital certificates issued by trusted Certificate Authorities to verify the server's identity. It then performs a cryptographic handshake to negotiate a symmetric key for data encryption. This guarantees three things: confidentiality (e.g., encrypting passwords and tokens), data integrity (preventing transit modifications), and authentication (proving the client is talking to the real server)."

---

### Explain DNS.
**How to Structure Your Answer:**
1. **Core Definition:** Define DNS as a phonebook that translates domains to IPs.
2. **Hierarchy & Resolution Steps:** Explain the step-by-step path from Root to TLD to Authoritative servers.
3. **Transport Protocol:** Mention that it runs over UDP/TCP port 53.
4. **Key Record Types:** List common records (`A`, `AAAA`, `CNAME`).

**Interview Answer:**
> "DNS, or the Domain Name System, is a distributed database that translates human-readable domain names into routable IP addresses.
> 
> When a user requests a domain, the query goes to a recursive resolver. If the address is not in the cache, the resolver queries the Root server (`.`), which points to the TLD server (like `.com`), which in turn points to the domain's Authoritative Name Server. The Authoritative server returns the IP address, which the resolver caches based on its Time to Live (TTL) value before returning it to the browser.
> 
> DNS primarily uses UDP port 53 to keep lookups fast, falling back to TCP if responses exceed 512 bytes. Common records include `A` for IPv4, `AAAA` for IPv6, and `CNAME` for domain aliases."

---

### Explain the OSI Model.
**How to Structure Your Answer:**
1. **Core Definition:** Define it as a conceptual standardization tool.
2. **Layer Order:** List the seven layers from bottom to top (PDNTSPA).
3. **Data Flow:** Briefly explain encapsulation and decapsulation.

**Interview Answer:**
> "The OSI model is a theoretical 7-layer framework developed by the ISO to standardize network communication and ensure compatibility across hardware and software vendors.
> 
> The layers, from bottom to top, are:
> 1. **Physical:** Transmission of raw bits.
> 2. **Data Link:** Framing and physical MAC addressing.
> 3. **Network:** Routing and logical IP addressing.
> 4. **Transport:** End-to-end reliability and flow control.
> 5. **Session:** Managing communication sessions.
> 6. **Presentation:** Data formatting, compression, and encryption.
> 7. **Application:** Interface for user software, such as HTTP.
> 
> As data is sent, it goes down the stack on the sender, with each layer adding header metadata (Encapsulation), and flows back up the stack on the receiver (Decapsulation)."

---

### Explain the Three-Way Handshake.
**How to Structure Your Answer:**
1. **Core Purpose:** Explain that it establishes a reliable TCP connection.
2. **The Three Steps:** Detail the SYN, SYN-ACK, and ACK sequence.
3. **Negotiated Values:** Mention the synchronization of sequence numbers and window sizes.

**Interview Answer:**
> "The TCP Three-Way Handshake is the process used to establish a reliable, connection-oriented session between a client and a server before any application data is sent.
> 
> 1. First, the client sends a **SYN** (Synchronize) packet containing a random initial sequence number ($x$) to the server, indicating it wants to connect.
> 2. Second, the server responds with a **SYN-ACK** packet. It acknowledges the client's request by setting the ACK number to $x + 1$ and includes its own random initial sequence number ($y$).
> 3. Third, the client sends an **ACK** packet back to the server with the ACK number set to $y + 1$.
> 
> Once the server receives this final ACK, the connection is established on both sides, buffers are allocated, and data transmission can begin."

---

### Explain the JWT Authentication Flow.
**How to Structure Your Answer:**
1. **Definition:** Define JWT as a signed, self-contained JSON token.
2. **Flow Sequence:** Explain login, token generation, client storage, and API requests.
3. **Server Verification:** Emphasize the stateless verification of the signature.

**Interview Answer:**
> "The JWT Authentication Flow is a stateless authentication pattern.
> 
> First, the client sends login credentials to the server. After validating them, the server generates a JWT containing user claims (like user ID and roles) in the payload, signs the header and payload using a secret key, and sends the token back to the client.
> 
> The client stores this token in memory or an HttpOnly cookie. For subsequent API requests, the client appends the token to the `Authorization` header as a Bearer token.
> 
> The server intercepts the request, decodes the token, and verifies the signature using its secret key. If valid, the user is authenticated immediately. This makes the flow stateless, removing the need for the server to maintain session stores or perform database lookups to verify the user."

---

### Explain WebSockets.
**How to Structure Your Answer:**
1. **Core Purpose:** Explain that WebSockets provide full-duplex, real-time communication.
2. **Handshake & Upgrade:** Explain how the connection upgrades from HTTP.
3. **Data Framing:** Mention the low overhead of frames compared to HTTP requests.

**Interview Answer:**
> "WebSockets is a protocol that provides full-duplex, bi-directional communication channels over a single, long-lived TCP connection.
> 
> The connection starts with a standard HTTP request from the client containing connection upgrade headers. If the server supports the protocol, it returns a `101 Switching Protocols` status code, upgrading the socket.
> 
> Once upgraded, the HTTP protocol is detached, and the underlying TCP connection remains open. Client and server can then push text or binary frames to each other at any time without the overhead of HTTP request headers. This makes WebSockets far more efficient than HTTP polling for real-time systems like chat and live notifications."

---

### Explain how a browser request reaches a Spring Boot backend and returns data from PostgreSQL.
**How to Structure Your Answer:**
1. **DNS & Connection:** DNS lookup resolves domain to IP, and a TCP/TLS handshake is performed.
2. **Routing & Load Balancing:** The request travels over routers, reaching a reverse proxy (like Nginx) which forwards it to Spring Boot.
3. **Spring Boot Lifecycle:** The request passes filters, matches the controller mapping, and calls the service layer.
4. **Database Access:** The repository layer queries PostgreSQL over a TCP connection pool, returning data.
5. **Response Return:** Spring Boot serializes the entity to JSON, returning the HTTP response to the browser to render in React.

```
React App (Browser) --> DNS Lookup (Resolve Domain) --> TCP/TLS Handshake
  ^                                                             |
  |                                                             v
HTTP Response (JSON) <--- Spring Boot (Tomcat Port) <--- Reverse Proxy (Nginx)
                                |
                        Queries (HikariCP)
                                |
                                v
                        PostgreSQL Database
```

**Interview Answer:**
> "When a user triggers an action in a React application:
> 
> 1. **DNS Resolution:** The browser queries DNS to translate the API domain into an IP address, then performs a TCP and TLS handshake on port 443.
> 2. **Routing & Reverse Proxy:** The HTTP request travels over the network to the cloud router and a reverse proxy (like Nginx) or load balancer, which terminates the TLS session and forwards the HTTP request to the Spring Boot application port.
> 3. **Spring Boot Processing:** Inside Spring Boot, the request passes through security filters (which validate the JWT, if present). Tomcat forwards the request to the `DispatcherServlet`, which routes it to the matching `@RestController` method.
> 4. **Service & Database Query:** The controller calls the service layer. The repository layer (via Spring Data JPA) uses a connection pool (like HikariCP) to send an SQL query over a TCP connection to PostgreSQL.
> 5. **Serialization & Response:** PostgreSQL returns the rows, which JPA maps to Java entities. The controller serializes these objects to JSON and returns an HTTP response back through the proxy to the browser, where React updates the UI state."

---
---

# SECTION 3: REVISION & PLACEMENT PRACTICE

---

## Top 50 CN Interview Questions (Revision Sheet)

1. **What is a Computer Network?** An interconnection of nodes that communicate using standardized protocols to share resources.
2. **What is the difference between physical MAC and logical IP addresses?** A MAC address is a permanent physical identifier (Layer 2); an IP address is a logical address used for routing across subnets (Layer 3).
3. **What is the OSI Model?** A conceptual 7-layer framework that standardizes network communication.
4. **What is the TCP/IP Model?** A practical 4-layer protocol stack (Application, Transport, Internet, Network Access) that powers the internet.
5. **What is a Hub?** A Layer 1 physical device that broadcasts incoming signals to all ports, causing collisions.
6. **What is a Layer 2 Switch?** A Data Link device that forwards frames to specific ports by inspecting destination MAC addresses.
7. **What is a Router?** A Layer 3 network device that routes packets between different subnets based on IP addresses.
8. **What is ARP?** Address Resolution Protocol; it maps a known IP address to a physical MAC address on a local subnet.
9. **Explain how DNS works in one sentence.** It is a hierarchical directory system that resolves domain names to IP addresses.
10. **What is the difference between TCP and UDP?** TCP is connection-oriented and reliable; UDP is connectionless, fast, and does not guarantee delivery.
11. **Explain the TCP Three-Way Handshake.** The process of establishing a connection using SYN, SYN-ACK, and ACK packets.
12. **Why does TCP termination require a Four-Way handshake?** Because TCP is full-duplex, meaning each direction of the connection must be closed independently.
13. **What is the purpose of the TCP TIME-WAIT state?** It keeps the socket open for $2 \times \text{MSL}$ to ensure delayed packets are discarded and the remote host received the final ACK.
14. **What is Flow Control in TCP?** A mechanism using a sliding window to prevent a fast sender from overwhelming a slow receiver's buffer.
15. **What is Congestion Control in TCP?** A mechanism that prevents the sender from overloading the network, using algorithms like Slow Start.
16. **What is a Socket?** An IP address and port number combination that serves as an endpoint for network communication.
17. **What is the difference between IPv4 and IPv6?** IPv4 uses 32-bit addresses; IPv6 uses 128-bit addresses, offering a larger address space and simplified routing headers.
18. **Explain the role of ICMP.** Internet Control Message Protocol; used by network devices to send error messages and operational info (e.g., used by `ping`).
19. **What is DHCP?** Dynamic Host Configuration Protocol; automatically assigns IP addresses and configuration settings to devices on a network.
20. **What is NAT?** Network Address Translation; maps multiple private IP addresses inside a local network to a single public IP to conserve addresses.
21. **What is the difference between symmetric and asymmetric encryption?** Symmetric uses the same key for encryption and decryption; asymmetric uses a public key to encrypt and a private key to decrypt.
22. **What is SSL/TLS?** Cryptographic protocols that secure communication over TCP using certificate authentication and session encryption.
23. **What is a Certificate Authority (CA)?** A trusted third party that issues digital certificates to verify a server's identity.
24. **How does HTTPS protect data?** By running standard HTTP requests over an encrypted TLS connection.
25. **What is HTTP?** A stateless, text-based application-layer request-response protocol.
26. **What is HTTP Multiplexing?** An HTTP/2 feature that allows sending multiple requests and responses concurrently over a single TCP connection.
27. **What is HTTP/3's main improvement?** It runs over the QUIC protocol (using UDP), which eliminates head-of-line blocking during packet loss.
28. **What is a REST API?** An API architectural style based on resources represented by URIs and manipulated using standard HTTP methods.
29. **What does Idempotency mean in APIs?** An operation is idempotent if running it multiple times produces the same system state as running it once (e.g., PUT, DELETE).
30. **What is a WebSocket?** A protocol that provides full-duplex, bi-directional communication channels over a single, long-lived TCP connection.
31. **What is the difference between WebSockets and Long Polling?** WebSockets keeps a single connection open for two-way communication; long polling repeatedly opens new HTTP connections to pull updates.
32. **What is a Cookie?** A small text file sent by a server and stored by the browser, which is automatically included in subsequent requests to that domain.
33. **What is an HttpOnly Cookie?** A security flag that blocks JavaScript from reading the cookie, protecting it against XSS attacks.
34. **What is the SameSite Cookie flag?** A security flag that controls whether cookies are sent with cross-site requests, protecting against CSRF attacks.
35. **What is a Session?** A server-side state mechanism that associates user data with a unique session ID cookie stored in the browser.
36. **Explain the structure of a JWT.** A three-part token containing a Base64-encoded Header, Payload (claims), and a cryptographically signed Signature.
37. **What makes JWT stateless?** The token contains all user claims and is signed by the server, allowing verification without database lookups.
38. **What is the difference between Authorization and Authentication?** Authentication verifies *who* a user is; Authorization verifies *what* permissions they have.
39. **What is CORS?** Cross-Origin Resource Sharing; a browser security mechanism that restricts web pages from making requests to a different domain.
40. **What is the purpose of a Subnet Mask?** A bitmask used by routers to separate the network ID from the host ID in an IP address.
41. **What is CIDR?** Classless Inter-Domain Routing; a method for allocating IP addresses and routing packets using custom prefix lengths.
42. **What is a Gateway?** A node on a network that serves as an entrance to another network, routing local traffic to the internet.
43. **What is the loopback address?** An IP address used by a host to send network traffic to itself (IPv4: `127.0.0.1`, IPv6: `::1`).
44. **What is a Port Number?** A 16-bit number that identifies a specific process or service on a host (e.g., HTTP is port 80).
45. **What is the difference between a broadcast and a multicast address?** Broadcast sends packets to all hosts on a subnet; multicast sends packets to a specific group of subscribed hosts.
46. **What is the purpose of the TTL field in an IP header?** Time to Live; a hop counter decremented by each router. When it reaches 0, the packet is discarded to prevent infinite routing loops.
47. **What is Link Aggregation?** Combining multiple physical network links into a single logical link to increase bandwidth and reliability.
48. **Explain the difference between safe and unsafe HTTP methods.** Safe methods do not modify server state (e.g., GET); unsafe methods can modify state (e.g., POST, DELETE).
49. **What is a reverse proxy?** A server (like Nginx) positioned in front of backend servers that handles load balancing, SSL termination, and routing.
50. **What is a Keep-Alive header?** An HTTP header that requests a persistent TCP connection to reuse the socket for multiple requests.

---

## One-Page CN Revision Sheet (Cheat Sheet)

```
+------------------------------------------------------------------------------------------------+
|                                  COMPUTER NETWORKS CHEAT SHEET                                 |
+------------------------------------------------------------------------------------------------+
| LAYER PROTOCOLS (OSI Model):                                                                   |
| - Layer 7 (Application): HTTP, DNS, FTP, WebSocket, SMTP                                       |
| - Layer 6 (Presentation): SSL/TLS (Data encryption, formatting)                                |
| - Layer 5 (Session): RPC, NetBIOS (Session coordination)                                       |
| - Layer 4 (Transport): TCP (reliable, byte stream), UDP (unreliable, datagrams)                |
| - Layer 3 (Network): IP (IPv4, IPv6 routing), ICMP, ARP (resolves IP to MAC)                   |
| - Layer 2 (Data Link): Ethernet, MAC addresses (node-to-node framing)                          |
| - Layer 1 (Physical): Cables, copper wires, fiber optics, raw bits                             |
|                                                                                                |
| TCP 3-WAY HANDSHAKE:                                                                           |
| Client                     SYN (Seq = x) -----------------------------> Server                 |
| Client <------------------ SYN-ACK (Seq = y, Ack = x + 1) -------------- Server                 |
| Client ------------------- ACK (Ack = y + 1) -------------------------> Server                 |
|                                                                                                |
| TCP CONNECTION CLOSING:                                                                        |
| Client ------------------- FIN ---------------------------------------> Server                 |
| Client <------------------ ACK (Half-closed) -------------------------- Server                 |
| Client <------------------ FIN (Server done sending) ------------------ Server                 |
| Client ------------------- ACK ---------------------------------------> Server (CLOSED)         |
| (TIME-WAIT: 2MSL) -> CLOSED                                                                    |
|                                                                                                |
| JWT COMPOSITE PARTS:                                                                           |
| base64Url(Header) . base64Url(Payload) . HMAC-SHA256(Header.Payload, SecretKey)                |
|                                                                                                |
| WEBSOCKET UPGRADE REQUEST HEADERS:                                                             |
| Connection: Upgrade                                                                            |
| Upgrade: websocket                                                                             |
| Sec-WebSocket-Key: <base64-string>                                                             |
| -> Server Response: 101 Switching Protocols                                                    |
|                                                                                                |
| PRIVATE IP RANGES (RFC 1918):                                                                  |
| - Class A: 10.0.0.0 to 10.255.255.255                                                          |
| - Class B: 172.16.0.0 to 172.31.255.255                                                        |
| - Class C: 192.168.0.0 to 192.168.255.255                                                      |
+------------------------------------------------------------------------------------------------+
```

---

## Most Important Placement Questions & Follow-up Questions

### Question 1: What is the difference between a Layer 4 Load Balancer and a Layer 7 Load Balancer?
* **Answer:** A Layer 4 load balancer operates at the Transport layer (TCP/UDP), routing connections based on IP addresses and port numbers without inspecting the application data payload. A Layer 7 load balancer operates at the Application layer, inspecting HTTP/HTTPS headers, URLs, cookies, and payloads to make routing decisions (e.g., path-based routing).
* **Follow-up:** *Which one is more resource-intensive, and why?* (Answer: Layer 7 load balancing is more resource-intensive because the balancer must perform a full TCP handshake with the client and decrypt the TLS payload to inspect the application data before routing it to the backend).

### Question 2: What is the TCP Head-of-Line (HoL) Blocking problem, and how does HTTP/3 resolve it?
* **Answer:** In HTTP/2, multiple requests are multiplexed over a single TCP connection. However, if a single TCP packet is lost in transit, TCP halts all communication on that connection, blocking all multiplexed streams until the lost packet is retransmitted and acknowledged. HTTP/3 resolves this by running over QUIC (built on UDP), where each stream is managed independently. A packet loss on one stream does not block or impact the other active streams.
* **Follow-up:** *Why was QUIC built on top of UDP instead of creating a new Transport Layer protocol?* (Answer: To bypass middlebox ossification; firewalls, routers, and gateways on the internet are programmed to block or drop unknown protocols, so using UDP ensures compatibility with existing hardware).

### Question 3: How does JWT authentication work stateless, and what is the security implication of a long-lived JWT?
* **Answer:** JWT is stateless because all user session metadata and roles are stored in the token payload itself. The authenticity of this data is guaranteed by a cryptographic signature generated by the server's private key. If a JWT is long-lived, an attacker who intercepts the token (via XSS or interception) can access the system until the token expires, as stateless servers cannot easily revoke individual tokens.
* **Follow-up:** *How do you implement secure token revocation with JWTs?* (Answer: By using short-lived Access Tokens (e.g., 15 minutes) paired with a long-lived Refresh Token stored in an HttpOnly cookie. The server can revoke the Refresh Token in a database, forcing the client to re-authenticate when their access token expires).
