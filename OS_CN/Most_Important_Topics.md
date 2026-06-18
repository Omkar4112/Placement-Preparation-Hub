# OS & CN: Most Important Topics (Study First)
## High-Priority Placement Study Guide (5-15 LPA Target)

This document aggregates the absolute most critical, high-frequency topics asked in software engineering and full-stack developer technical interviews. Master these topics first before diving into the complete handbooks.

---

# PART 1: OPERATING SYSTEMS (OS)

---

## 1. Process vs Thread
* **What Interviewers Expect:** Deep understanding of memory layout, virtual address spaces, switching cost, and thread safety.

### 1. Precise Definition
A **Process** is an isolated execution instance of a program in memory with its own dedicated address space, while a **Thread** is the smallest schedulable execution unit inside a process that shares resources with other sibling threads of the same parent process.

### 2. Why it exists
Processes prevent applications from corrupting each other's memory (fault isolation). Threads allow cooperative concurrency within the same program, reducing resource and switching overhead.

### 3. Internal Working
* **Process:** The OS allocates a Process Control Block (PCB) and a unique page table. Address space contains distinct Code, Data, Heap, and Stack sections.
* **Thread:** Shared memory includes Heap, Code, and static Data. Private memory is limited to a Stack, Registers, and Program Counter (PC), tracked by a Thread Control Block (TCB).

### 4. Advantages / Limitations
* **Process:** Excellent stability (crashed process doesn't affect others); high creation and communication (IPC) overhead.
* **Thread:** Lightweight, fast communication via shared memory; bugs (e.g., memory corruption) can crash the entire parent process.

### 5. Interview Answer (30-60 seconds)
> "A process is a program in execution with an isolated virtual memory space, representing the unit of resource allocation. A thread is a lightweight execution unit inside a process, sharing the parent's code, data, and heap while keeping its own stack, registers, and program counter. Consequently, thread context switching is cheaper because it doesn't swap page tables or flush the TLB cache. However, processes provide better fault isolation, as a thread crash can terminate the entire process."

### 6. Common Follow-up Questions
* Why do threads share the heap but not the stack?
* What is the difference between a virtual memory context switch and a thread context switch?

### 7. Connection to Real Software Systems
Google Chrome spawns a new process for each browser tab (so a crashed tab doesn't freeze the browser), whereas a backend web server like Spring Boot runs as a single process spawning a new thread for each concurrent user request to process queries quickly.

---

## 2. Context Switching
* **What Interviewers Expect:** Detailed step-by-step register save/restore sequence and the concept of CPU cache invalidation.

### 1. Precise Definition
Context Switching is the operating system mechanism that suspends a running process or thread by saving its execution state, allocates the CPU to another task, and restores its saved state to resume execution.

### 2. Why it exists
To enable multitasking and time-sharing on a CPU, allowing multiple applications to make progress concurrently.

### 3. Internal Working
1. CPU transitions from User Mode to Kernel Mode via a timer interrupt or trap.
2. Kernel saves current CPU register states (PC, SP, general registers) into the active task's PCB or TCB.
3. Scheduler selects the next task.
4. For process switches, the kernel loads the new task's page table register, which flushes the hardware Translation Lookaside Buffer (TLB).
5. Kernel loads the registers from the new task's PCB or TCB.
6. CPU switches to User Mode and resumes execution.

### 4. Advantages / Limitations
* **Advantages:** Enables fair time-sharing and responsive user interfaces.
* **Limitations:** Pure system overhead. High frequency of switching degrades overall application throughput.

### 5. Interview Answer (30-60 seconds)
> "Context switching is how the OS swaps execution between threads or processes. When an interrupt occurs, the kernel saves the active CPU register states, stack pointer, and program counter into the task's PCB or TCB. It then selects another task, loads its saved state, and returns to user mode. While essential for concurrency, process context switching is expensive because it requires changing virtual memory mappings, which flushes the TLB cache and causes memory access latency."

### 6. Common Follow-up Questions
* What is the role of the TLB in context switching?
* How does hardware support context switching? (e.g., Register renaming/multiple register sets).

### 7. Connection to Real Software Systems
High-concurrency servers like Node.js use asynchronous, single-threaded architectures specifically to minimize context-switching overhead, whereas multi-threaded Java applications must optimize thread pool sizes to prevent CPU cores from spending all their time switching instead of executing business logic.

---

## 3. Multithreading
* **What Interviewers Expect:** Mapping models (1:1, Many:Many) and CPU-bound vs I/O-bound threading strategies.

### 1. Precise Definition
Multithreading is a programming and execution model that allows multiple threads to run concurrently within a single process to execute independent subtasks in parallel.

### 2. Why it exists
To utilize multi-core CPU architectures and keep applications responsive by executing background tasks (e.g., I/O operations) without blocking the primary user interface.

### 3. Internal Working
The runtime environment maps user-space threads to kernel-space threads:
* **One-to-One (1:1):** Every user thread maps directly to an OS kernel thread. Provides true parallelism across cores. (Used by Linux/Windows/Java).
* **Many-to-One (Many:1):** Multiple user threads mapped to one kernel thread. Fast switching, but one blocking thread blocks all.
* **Many-to-Many (Many:Many):** Multiplexes many user threads to a smaller number of kernel threads.

### 4. Advantages / Limitations
* **Advantages:** High application responsiveness and utilization of multi-core CPUs.
* **Limitations:** Introduces lock contention, race conditions, deadlocks, and complex debugging.

### 5. Interview Answer (30-60 seconds)
> "Multithreading is the execution of multiple threads concurrently within a single process to achieve parallelism on multicore processors. In modern systems like Linux, this is implemented using a 1:1 model where each user thread maps to an OS kernel thread. This allows threads to run in parallel on separate CPU cores. While multithreading dramatically improves performance and responsiveness, it introduces data consistency issues that require synchronization primitives like locks."

### 6. Common Follow-up Questions
* What is the difference between concurrency and parallelism?
* What are Green Threads, and how do they differ from Native OS Threads?

### 7. Connection to Real Software Systems
In Spring Boot, Tomcat maintains a thread pool. When concurrent requests hit the server, Spring Boot delegates each request to an independent thread, allowing the app to query PostgreSQL in parallel across different database connections.

---

## 4. Deadlock
* **What Interviewers Expect:** The 4 Coffman conditions, Banker's algorithm logic, and deadlock prevention vs detection.

### 1. Precise Definition
A Deadlock is a state in which a set of processes are permanently blocked because each process is holding a resource and waiting for another resource held by another process in the same set.

### 2. Why it exists
It occurs as a side effect of locking mechanisms in concurrent systems when resources are requested in different sequences by independent execution threads.

### 3. Internal Working
#### The 4 Necessary Conditions (Must all hold simultaneously):
1. **Mutual Exclusion:** At least one resource must be held in non-shareable mode.
2. **Hold and Wait:** A process holding allocated resources can request and wait for new ones.
3. **No Preemption:** Resources cannot be forcibly taken away.
4. **Circular Wait:** A closed loop of processes must exist where each waits for a resource held by the next.

```
Process A (Holds Lock 1) ------ Waits For ------> Lock 2 (Held by Process B)
      ^                                                  |
      |------------------ Waits For ---------------------v
```

### 4. Advantages / Limitations
* **Advantages:** None. It represents a system execution freeze.
* **Limitations:** Hard to debug; resolving deadlocks requires aborting transactions, terminating processes, or rebooting the server.

### 5. Interview Answer (30-60 seconds)
> "A deadlock is a situation where a set of processes are permanently blocked because they have circular dependencies on resources. It occurs only if four conditions hold simultaneously: Mutual Exclusion, Hold and Wait, No Preemption, and Circular Wait. We handle deadlocks by Prevention, such as enforcing a strict resource locking order to break the Circular Wait condition, or Avoidance, using the Banker's Algorithm to verify if resource allocation will leave the system in a safe state."

### 6. Common Follow-up Questions
* What is the difference between deadlock prevention and deadlock avoidance?
* How does a database engine detect and recover from deadlocks?

### 7. Connection to Real Software Systems
In a database like PostgreSQL, if Transaction A updates Row 1 and attempts to update Row 2, while Transaction B updates Row 2 and attempts to update Row 1, a deadlock occurs. PostgreSQL detects this cycle, aborts one of the transactions, and logs a deadlock error.

---

## 5. Semaphore vs Mutex
* **What Interviewers Expect:** Ownership differences, priority inversion issues, and code-level synchronization scenarios.

### 1. Precise Definition
A **Mutex** is a locking mechanism that enforces mutual exclusion on a critical section with strict thread ownership, whereas a **Semaphore** is an integer-based signaling mechanism used to manage resource pools or coordinate task ordering among multiple threads.

### 2. Why it exists
They exist to coordinate concurrent resource access, protecting critical sections from race conditions and synchronization errors.

### 3. Internal Working
* **Mutex:** Contains a binary state (locked/unlocked) and an owner thread ID. Only the thread that locks the mutex can unlock it. It supports *Priority Inheritance* to prevent priority inversion.
* **Semaphore:** Contains a counter value and a blocked thread queue. `wait()` decrements the counter; if negative, the caller is blocked. `signal()` increments the counter and wakes up a blocked thread. Any thread can signal a semaphore.

### 4. Advantages / Limitations
* **Mutex:** Safer due to ownership validation; limited to protecting single resources.
* **Semaphore:** Can manage multiple identical resources (counting semaphores); prone to errors (e.g., forgetting to signal) leading to deadlocks.

### 5. Interview Answer (30-60 seconds)
> "The key difference is ownership. A Mutex is a locking mechanism designed to protect a single critical section; only the thread that locks the mutex is allowed to unlock it. It supports priority inheritance to prevent priority inversion. A Semaphore is a signaling mechanism that uses an integer counter to manage access to a pool of resources. It has no owner; any thread can signal a semaphore to wake up another thread. Use a mutex to protect shared state, and a semaphore to manage resource limits."

### 6. Common Follow-up Questions
* What is Priority Inversion, and how does a Mutex prevent it?
* What is a Binary Semaphore, and does it function exactly like a Mutex? (Answer: No, because it lacks the concept of ownership).

### 7. Connection to Real Software Systems
In web development, we use a Mutex to ensure that a singleton counter variable is updated by only one request thread at a time. We use a Counting Semaphore to implement API rate limiters, restricting active connections to a third-party payment gateway to 10 concurrent requests.

---

## 6. Virtual Memory
* **What Interviewers Expect:** Physical vs Logical address mapping, Page Tables, and Page Fault resolution flows.

### 1. Precise Definition
Virtual Memory is a memory management abstraction that maps a process's logical address space to physical RAM, allowing programs to run even if their memory footprint exceeds the size of physical memory.

### 2. Why it exists
To isolate processes from one another, simplify address layouts for compilers, and run applications that are larger than physical RAM by utilizing secondary storage.

### 3. Internal Working
The OS divides memory into pages and maps virtual pages to physical RAM frames via a Page Table.
1. When virtual memory is accessed, the CPU's Memory Management Unit (MMU) checks the Page Table.
2. If the page is present in RAM, the physical address is resolved.
3. If the page is absent (invalid bit set), a **Page Fault** interrupt is triggered.
4. The OS kernel handles the interrupt by reading the page from disk swap space into RAM, updating the page table, and restarting the failed instruction.

### 4. Advantages / Limitations
* **Advantages:** Absolute process isolation, runs large applications, and increases multitasking capacity.
* **Limitations:** Disk swapping is slow. Over-reliance on virtual memory swapping causes severe system degradation (Thrashing).

### 5. Interview Answer (30-60 seconds)
> "Virtual Memory is an abstraction that separates a program's logical address space from physical RAM. The OS maps virtual pages to physical frames using a page table. When an address is requested that isn't loaded in RAM, the MMU triggers a page fault. The OS kernel intercepts this, retrieves the page from disk swap space, loads it into RAM, updates the page table, and resumes execution. This allows processes to run larger codebases than physical RAM allows, while ensuring absolute memory isolation."

### 6. Common Follow-up Questions
* What is a page fault, and what are its performance implications?
* How does virtual memory enforce security boundaries between processes?

### 7. Connection to Real Software Systems
On a Linux server running Spring Boot and PostgreSQL, virtual memory allows the OS to cache large database files in physical RAM, while swapping out idle background system processes to the swap disk to maintain high database speed.

---

## 7. Paging
* **What Interviewers Expect:** Structure of the virtual address, role of the TLB, and multi-level page table architecture.

### 1. Precise Definition
Paging is a non-contiguous memory management scheme that divides logical memory into fixed-size blocks called **pages** and physical memory into matching blocks called **frames**, eliminating the need for contiguous allocation.

### 2. Why it exists
To eliminate external fragmentation in physical memory by allowing the OS to place program segments into any available physical frame.

### 3. Internal Working
* **Address Translation:** A virtual address is split into a Page Number ($p$) and an Offset ($d$).
* **TLB Lookup:** The MMU first checks the Translation Lookaside Buffer (TLB), a fast hardware cache.
  * *TLB Hit:* Resolves physical frame ($f$) immediately.
  * *TLB Miss:* Reads the process's Page Table in RAM, fetches the frame number, updates the TLB, and accesses the physical address ($f + d$).

```
Virtual Address: [ Page Number (p) | Offset (d) ]
                         |
                 +-------v-------+
                 |    TLB        | --- Hit ---> Frame (f) + d -> RAM
                 +-------+-------+
                         | Miss
                 +-------v-------+
                 | Page Table    | -----------> Frame (f) + d -> RAM
                 +---------------+
```

### 4. Advantages / Limitations
* **Advantages:** No external fragmentation; simplifies sharing of memory pages between processes.
* **Limitations:** Introduces internal fragmentation in the last page; page table lookups add latency on TLB misses.

### 5. Interview Answer (30-60 seconds)
> "Paging is a memory management scheme that divides logical memory into fixed-size pages and physical memory into matching frames. The MMU translates virtual addresses by checking a page table. To optimize speed, it uses a hardware cache called the Translation Lookaside Buffer (TLB) to store recent translations. On a TLB miss, the MMU reads the page table in RAM. Paging prevents external fragmentation, but it introduces page table memory overhead and latency on TLB misses."

### 6. Common Follow-up Questions
* What is a TLB miss, and how does the OS handle it?
* What is Multi-Level Paging, and why is it used? (Answer: It breaks the page table into a tree structure so the OS does not have to keep a single, massive, contiguous page table in RAM).

### 7. Connection to Real Software Systems
Most modern operating systems use a default page size of 4KB. Large-scale database servers like PostgreSQL can use **HugePages** (e.g., 2MB pages) to minimize page table size, increase TLB hits, and improve query processing speed.

---

## 8. System Calls
* **What Interviewers Expect:** Transition between User and Kernel modes, trap instructions, and input validation security.

### 1. Precise Definition
A System Call is a programmatic interface that allows user-space applications to request privileged operations (like I/O, process creation, or hardware access) from the operating system kernel.

### 2. Why it exists
To act as a secure gatekeeper, preventing user applications from accessing hardware directly or corrupting system resource states.

### 3. Internal Working
1. User application loads parameters into CPU registers and sets the System Call Number.
2. Executing a trap instruction (e.g., `syscall` or `sysenter`) triggers a software interrupt.
3. The CPU switches from User Mode (Ring 3) to Kernel Mode (Ring 0) and jumps to the kernel's trap handler table.
4. The kernel validates the arguments, runs the operation, writes the return value to registers, and runs a return instruction (e.g., `sysret`) to switch the CPU back to User Mode.

### 4. Advantages / Limitations
* **Advantages:** Secures system resources; abstracts complex hardware interactions behind standard APIs (like POSIX).
* **Limitations:** Switch overhead (user-to-kernel state changes) slows down performance.

### 5. Interview Answer (30-60 seconds)
> "A system call is a programmatic interface that allows user-space applications to request privileged services from the kernel. Because applications run in a restricted user mode, they cannot access hardware directly. When a system call is made, the program loads parameters into registers and triggers a hardware trap. The CPU switches to kernel mode, executes the request, and switches back to user mode. This provides security, though the transition introduces performance overhead."

### 6. Common Follow-up Questions
* What is the difference between a system call and a library call (e.g., `printf` vs `write`)?
* What steps occur during user-to-kernel mode transition?

### 7. Connection to Real Software Systems
When a Node.js API receives a request and writes to a log file using `fs.writeFileSync()`, the runtime executes a `write` system call, switching execution to the kernel to write the bytes to the physical storage drive.

---
---

# PART 2: COMPUTER NETWORKS (CN)

---

## 1. OSI Model
* **What Interviewers Expect:** Detailed understanding of all 7 layers, protocols at each layer, and the encapsulation concept.

### 1. Precise Definition
The Open Systems Interconnection (OSI) model is a conceptual 7-layer framework developed by the ISO to standardize network communication protocols and ensure interoperability.

### 2. Why it exists
To modularize networking. By dividing network tasks into distinct layers, engineers can design and replace protocols at one layer (e.g., switching from IPv4 to IPv6) without modifying the other layers.

### 3. Internal Working
Data is wrapped in headers at each layer on the sender (Encapsulation) and unwrapped on the receiver (Decapsulation).
* **7. Application:** HTTP, DNS, WebSockets (User interface interaction).
* **6. Presentation:** Encryption, formatting, TLS (Data representation).
* **5. Session:** Establishing and managing communication channels.
* **4. Transport:** TCP (Segments), UDP (Datagrams) (End-to-end delivery).
* **3. Network:** IP, ICMP (Packets) (Routing across subnets).
* **2. Data Link:** Ethernet, MAC addressing (Frames) (Node-to-node hop).
* **1. Physical:** Copper wires, fiber cables, raw bits.

### 4. Advantages / Limitations
* **Advantages:** Highly structured, modular design simplifies troubleshooting.
* **Limitations:** The 7-layer separation is theoretical. Commercial protocol designs (like TCP/IP) merge layers to improve performance.

### 5. Interview Answer (30-60 seconds)
> "The OSI model is a 7-layer conceptual framework that standardizes networking protocol design. It consists of the Physical, Data Link, Network, Transport, Session, Presentation, and Application layers. During transmission, data is encapsulated with headers at each layer on the sending device, and decapsulated on the receiving device. While useful for modeling and debugging, real-world networks rely on the simplified, 4-layer TCP/IP model."

### 6. Common Follow-up Questions
* How does encapsulation change a data unit as it moves from Layer 4 to Layer 2?
* At which layers do switches and routers operate?

### 7. Connection to Real Software Systems
In full-stack architectures, a React request is formatted at Layer 7 (HTTP), encrypted at Layer 6 (TLS), established as a stream at Layer 4 (TCP), and routed through internet routers at Layer 3 (IP).

---

## 2. TCP vs UDP
* **What Interviewers Expect:** Comparison of reliability, handshakes, header sizes, and usage scenarios.

### 1. Precise Definition
**TCP** is a connection-oriented, reliable transport protocol that guarantees in-order, error-free delivery of byte streams, while **UDP** is a connectionless, lightweight transport protocol that sends datagrams immediately without delivery guarantees.

### 2. Why it exists
To provide options: TCP for applications where reliability is critical, and UDP for real-time services where speed and low latency are prioritized.

### 3. Internal Working
* **TCP:** Performs a 3-way handshake to establish connections. Uses sequence numbers and acknowledgements (ACKs) to track packets, retransmitting lost ones. Employs sliding windows for flow control and slow-start for congestion control.
* **UDP:** Simple 8-byte header (containing Source/Destination Ports, Length, Checksum). Sends packets without checking connection status or delivery success.

### 4. Advantages / Limitations
* **TCP:** Reliable and handles traffic flow control; slower, higher overhead, and susceptible to head-of-line blocking.
* **UDP:** Extremely fast and low overhead; does not guarantee packet delivery or order.

### 5. Interview Answer (30-60 seconds)
> "The core difference is that TCP is connection-oriented and reliable, while UDP is connectionless and unreliable. TCP uses a three-way handshake, sequence numbers, and ACKs to guarantee in-order delivery, and manages traffic flow and network congestion. UDP sends packets immediately with an 8-byte header and no delivery checks, maximizing speed. We use TCP for HTTP APIs and databases, and UDP for DNS, real-time streaming, and WebRTC."

### 6. Common Follow-up Questions
* How does HTTP/3 implement reliability over UDP? (Answer: By using the QUIC protocol at the application layer).
* What is TCP Head-of-Line Blocking?

### 7. Connection to Real Software Systems
React communicates with Spring Boot over TCP (via HTTP) to ensure API payloads arrive complete. However, real-time gaming or video applications use UDP to keep latency low, choosing to drop late frames instead of pausing execution to wait for retransmissions.

---

## 3. HTTP vs HTTPS
* **What Interviewers Expect:** TLS handshake details, CA verification, asymmetric/symmetric key exchange, and default ports.

### 1. Precise Definition
**HTTP** is an unencrypted, plaintext application-layer protocol used for transferring web resources, while **HTTPS** is an encrypted, secure extension of HTTP that uses the SSL/TLS protocol to encrypt communication.

### 2. Why it exists
To prevent eavesdropping, data tampering, and man-in-the-middle attacks on public networks.

### 3. Internal Working
* **HTTP:** Communicates in plaintext over TCP port 80.
* **HTTPS:** Communicates over TCP port 443. The connection flow is:
  1. Server sends its SSL/TLS certificate containing its public key.
  2. Client verifies the certificate using trusted Certificate Authorities.
  3. Client and server use asymmetric encryption to exchange a symmetric session key.
  4. Subsequent HTTP requests and responses are encrypted using this symmetric key.

### 4. Advantages / Limitations
* **Advantages:** Secures user credentials and API data; builds user trust and improves SEO ranking.
* **Limitations:** The cryptographic handshake adds network round-trip time and CPU load (mitigated by TLS 1.3).

### 5. Interview Answer (30-60 seconds)
> "HTTPS is the secure version of HTTP. It encrypts communication by running HTTP over the SSL/TLS protocol on port 443. During connection, the server presents a CA-signed digital certificate. The client verifies the certificate, and both sides run a handshake to exchange a symmetric session key. Once established, all HTTP data is encrypted, guaranteeing confidentiality, integrity, and server authentication."

### 6. Common Follow-up Questions
* What is the role of a Certificate Authority?
* How does symmetric encryption differ from asymmetric encryption in HTTPS?

### 7. Connection to Real Software Systems
When deploying a full-stack system, developers install an SSL certificate on Nginx or AWS Load Balancer (HTTPS). This handles decryption before forwarding plain HTTP traffic to Spring Boot inside a secure private VPC network.

---

## 4. DNS (Domain Name System)
* **What Interviewers Expect:** Hierarchical lookup flow (Root, TLD, Authoritative), UDP vs TCP ports, and record types.

### 1. Precise Definition
The Domain Name System (DNS) is a distributed database that translates human-readable domain names (e.g., `google.com`) into routable IP addresses (e.g., `142.250.190.46`).

### 2. Why it exists
Computers route packets using numerical IP addresses, but domain names are much easier for humans to remember.

### 3. Internal Working
DNS uses a hierarchical recursive process:
1. Client checks local cache. If it misses, it queries a **DNS Resolver**.
2. Resolver queries the **Root Server (`.`)**, which points to the TLD server (e.g., `.com`).
3. Resolver queries the **TLD Server**, which points to the domain's **Authoritative Server**.
4. The Authoritative Server returns the IP address.
5. Resolver returns the IP to the browser, caching it according to its **TTL (Time to Live)**.

* **Record Types:** `A` (IPv4), `AAAA` (IPv6), `CNAME` (Alias), `MX` (Mail).

### 4. Advantages / Limitations
* **Advantages:** Highly scalable; allows backend IPs to change without updating client code.
* **Limitations:** Unencrypted queries are vulnerable to sniffing (mitigated by DNS over HTTPS); updates take time to propagate due to TTL caching.

### 5. Interview Answer (30-60 seconds)
> "DNS is the Domain Name System, a distributed directory that translates domain names into IP addresses. When a domain is requested, the resolver queries the Root, TLD, and Authoritative Name Servers to retrieve the IP record. DNS runs primarily over UDP port 53 for speed and uses Time to Live (TTL) values to manage cache lifetimes. Common records include A records for IPv4, AAAA for IPv6, and CNAME for domain mapping."

### 6. Common Follow-up Questions
* Why does DNS run on UDP instead of TCP?
* What is DNS poisoning?

### 7. Connection to Real Software Systems
When deploying a React frontend on Vercel and Spring Boot on AWS, you configure an `A` record mapping `api.yoursite.com` to your load balancer's IP, and a `CNAME` record mapping `www.yoursite.com` to your frontend domain.

---

## 5. TCP Three-Way Handshake
* **What Interviewers Expect:** Packet sequence (SYN, SYN-ACK, ACK), transition states, and SYN flood attacks.

### 1. Precise Definition
The TCP Three-Way Handshake is the process used to establish a reliable, connection-oriented session between a client and a server, synchronizing sequence numbers and allocating buffers before data transmission begins.

### 2. Why it exists
To ensure both the client and server are capable of sending and receiving data, and to agree on initial sequence numbers (ISNs) to track packets.

### 3. Internal Working
1. **SYN:** Client sends a `SYN` packet containing an initial sequence number ($x$) to the server. (Client state: `SYN-SENT`).
2. **SYN-ACK:** Server responds with a `SYN-ACK` packet. It sets the ACK number to $x + 1$ and includes its own sequence number ($y$). (Server state: `SYN-RECEIVED`).
3. **ACK:** Client sends an `ACK` packet with the ACK number set to $y + 1$. Once received, both hosts enter the `ESTABLISHED` state.

```
Client                                                  Server
  | ---------- SYN (Seq = x) -------------------------> |
  | <--------- SYN-ACK (Seq = y, Ack = x + 1) --------- |
  | ---------- ACK (Ack = y + 1) ---------------------> | (ESTABLISHED)
(ESTABLISHED)
```

### 4. Advantages / Limitations
* **Advantages:** Prevents stale connections and establishes sequence tracking.
* **Limitations:** Adds a full round-trip time (1RTT) of latency. Prone to **SYN Flood** DoS attacks (mitigated using **SYN Cookies**).

### 5. Interview Answer (30-60 seconds)
> "The TCP Three-Way Handshake establishes a reliable connection. First, the client sends a SYN packet with a random initial sequence number to the server. Second, the server responds with a SYN-ACK packet, acknowledging the client's sequence number and sending its own. Third, the client sends an ACK packet back to confirm. Once complete, both hosts allocate buffers and enter the established state, ready to send data."

### 6. Common Follow-up Questions
* What is a SYN Flood attack, and how do SYN Cookies prevent it?
* Why is the initial sequence number randomized?

### 7. Connection to Real Software Systems
Before your React client can send an HTTP POST request to Spring Boot, the browser's network stack must complete a three-way handshake with the server's open port.

---

## 6. REST API
* **What Interviewers Expect:** Constraints of REST, HTTP methods, idempotency, and status code groups.

### 1. Precise Definition
Representational State Transfer (REST) is an architectural style for designing stateless, client-server web APIs that manipulate resources using standard HTTP methods and URIs.

### 2. Why it exists
To standardize web services, simplifying client-server communication using standard HTTP features rather than custom protocols.

### 3. Internal Working
REST relies on six design constraints:
* **Statelessness:** Each request must contain all the data needed to process it. The server does not store client session state.
* **Uniform Interface:** Resources are identified by URIs and manipulated using standard methods:
  * `GET` (Safe, Idempotent): Retrieve data.
  * `POST` (Unsafe, Non-idempotent): Create resources.
  * `PUT`/`PATCH` (Unsafe, Idempotent/Non-idempotent): Update resources.
  * `DELETE` (Unsafe, Idempotent): Remove resources.
* **Client-Server Separation, Cacheability, Layered System, and Code on Demand.**

### 4. Advantages / Limitations
* **Advantages:** Highly scalable; easy to cache; clean decoupling of client and server.
* **Limitations:** Prone to over-fetching or under-fetching data; lacks a strict contract schema.

### 5. Interview Answer (30-60 seconds)
> "REST is an architectural style for building APIs centered around resources identified by URIs. Its core constraint is statelessness, meaning the server does not store client session data, allowing it to scale easily. REST uses standard HTTP methods—GET to retrieve, POST to create, PUT to replace, and DELETE to remove. It also enforces a uniform interface and cacheable responses, making it the standard for web APIs."

### 6. Common Follow-up Questions
* What is the difference between PUT and PATCH?
* What is idempotency? Which HTTP methods are idempotent?

### 7. Connection to Real Software Systems
A React client uses Axios to send a `GET /api/products` request to a Spring Boot `@RestController`, which queries PostgreSQL, serializes the result to JSON, and returns a `200 OK` response.

---

## 7. JWT Authentication Flow
* **What Interviewers Expect:** Composite parts of a JWT, token storage choices (local storage vs cookies), and token revocation strategies.

### 1. Precise Definition
JSON Web Token (JWT) is a compact, URL-safe standard (RFC 7519) that securely transmits user claims as a JSON object, cryptographically signed using a secret key or public/private key pair.

### 2. Why it exists
To enable stateless authentication, removing the need for servers to store session state in memory, which simplifies horizontal scaling.

### 3. Internal Working
* **Structure:** Consists of three parts separated by dots:
  * **Header:** Hashing algorithm (e.g., HS256).
  * **Payload:** Claims (user ID, roles, expiration time).
  * **Signature:** Hash of (Header + Payload) signed with the server's secret key.
* **Authentication Flow:**
  1. Client sends credentials to Spring Boot.
  2. Spring Boot validates them, signs a JWT, and returns it.
  3. React client stores the token and appends it to subsequent request headers:
     * `Authorization: Bearer <token>`
  4. Spring Boot verifies the signature using its secret key, authenticating the user immediately.

### 4. Advantages / Limitations
* **Advantages:** Stateless and scalable; works across domains; self-contained payload reduces database queries.
* **Limitations:** Hard to revoke once issued (requires a Redis blocklist); larger token size increases request payloads.

### 5. Interview Answer (30-60 seconds)
Stateless JWT flow structure:
> "JWT is a stateless authentication mechanism. A JWT consists of a Header, Payload, and Signature. After login validation, the server generates and signs the token, returning it to the client. The client stores it and appends it to the Authorization header of subsequent API requests. The server validates the signature using its secret key, authenticating the user without checking a session database, which makes it highly scalable."

### 6. Common Follow-up Questions
* Where should you store a JWT on the client side (LocalStorage vs HttpOnly Cookie)?
* How do you handle JWT revocation before expiration?

### 7. Connection to Real Software Systems
A custom Spring Security filter intercepts requests to protected endpoints, reads the JWT from the request header, validates it using a secret key, and populates the Security Context before delegating to the controller.

---

## 8. WebSocket
* **What Interviewers Expect:** Comparison with polling/SSE, HTTP upgrade flow (101 status code), and connection scaling strategies.

### 1. Precise Definition
WebSocket is an application-layer protocol that provides full-duplex, bi-directional communication channels over a single, long-lived TCP connection, initiated via an HTTP handshake.

### 2. Why it exists
Standard HTTP is pull-only, preventing servers from pushing real-time updates. WebSocket allows real-time, low-latency updates without the overhead of HTTP request-response cycles.

### 3. Internal Working
1. **Handshake:** Client sends an HTTP request containing:
   * `Connection: Upgrade`
   * `Upgrade: websocket`
2. **Upgrade:** Server responds with `101 Switching Protocols`, upgrading the socket.
3. **Data Transfer:** The connection remains open over TCP, transferring lightweight text or binary frames with minimal headers (2-10 bytes).

```
React Client                                            Spring Boot Backend
  | ----- GET (Upgrade to WebSocket) -----------------> |
  | <---- 101 Switching Protocols ---------------------- |
  |<====== WebSocket Connection (TCP) =================>|
```

### 4. Advantages / Limitations
* **Advantages:** Full-duplex real-time communication; minimal overhead compared to HTTP polling.
* **Limitations:** Stateful connections are harder to load balance; requires sticky sessions or a message broker (like Redis) to scale across multiple servers.

### 5. Interview Answer (30-60 seconds)
> "WebSocket is a protocol that enables full-duplex, bi-directional communication over a single, long-lived TCP connection. It starts with an HTTP request containing upgrade headers. The server returns a 101 Switching Protocols response, upgrading the connection. The TCP socket is kept open, allowing both client and server to push light-weight data frames at any time, avoiding HTTP header overhead."

### 6. Common Follow-up Questions
* How does WebSocket compare to Server-Sent Events (SSE)?
* How do you load balance and scale WebSocket connections?

### 7. Connection to Real Software Systems
A React trading dashboard connects to a Spring Boot server via WebSockets, allowing the server to push live stock price ticks directly to the UI without requiring the client to refresh.

---

## 9. Cookies vs Sessions
* **What Interviewers Expect:** Comparison of client-side vs server-side storage, session lifecycle, and security flags.

### 1. Precise Definition
A **Cookie** is a client-side storage mechanism where a web server saves small text files in the browser, while a **Session** is a server-side storage mechanism that tracks user state in memory or a database, associated with a unique session ID.

### 2. Why it exists
To maintain state across stateless HTTP requests.

### 3. Internal Working
* **Cookie:** Server sends a `Set-Cookie` header. The browser automatically stores this data and appends it to subsequent request headers.
* **Session:** Server generates a Session ID, stores the session data on the server, and returns the Session ID to the client as a cookie. The browser sends the Session ID cookie, and the server reads it to load the user's state.

### 4. Advantages / Limitations
* **Cookie:** Lightweight and managed by the browser; limited to 4KB and vulnerable to XSS/CSRF.
* **Session:** Secure (data remains on the server) and supports larger storage; limits horizontal scaling unless synced using a database or cache.

| Parameter | Cookie | Session |
| :--- | :--- | :--- |
| **Storage Location** | Client Browser | Server (RAM, Database, Cache) |
| **Data Size** | Limited (4KB) | Virtually unlimited |
| **Scalability** | High (Client-side) | Low (Requires server sync/sticky sessions) |
| **Security** | Vulnerable if unencrypted | Highly secure |

### 5. Interview Answer (30-60 seconds)
> "Cookies are client-side text files stored in the browser, which are automatically sent with every request to the domain. Sessions are server-side data stores that track user state. They work together: the server creates a session in its memory or database, and sends the session ID to the client in a cookie. On subsequent requests, the server uses the session ID cookie to load the user's data. Cookies are lightweight but limited to 4KB, while sessions are secure but require server resource synchronization to scale."

### 6. Common Follow-up Questions
* What are the HttpOnly and SameSite flags in cookies?
* How does session storage work in a distributed microservice architecture?

### 7. Connection to Real Software Systems
When a user logs into a web app, Spring Boot creates an HTTPSession, stores it in a Redis cache, and sets a cookie with the session ID in the browser, ensuring any server instance in the cluster can handle subsequent requests.

---

## 10. Client-Server Architecture
* **What Interviewers Expect:** Client-server separation of concerns, request-response lifecycles, and N-tier architecture structures.

### 1. Precise Definition
Client-Server Architecture is a distributed application model that separates tasks between resource providers (servers) and service requesters (clients).

### 2. Why it exists
To centralize security controls, business logic, and data storage on dedicated, managed servers, while offloading user interface rendering to user devices.

### 3. Internal Working
* **Client:** Runs the frontend (React), handles user inputs, and initiates connections by sending requests.
* **Server:** Listens on a port, processes business logic, and queries database systems (PostgreSQL).
* **Communication:** Standardized protocols like HTTP/TCP are used to route requests and responses across the network.

### 4. Advantages / Limitations
* **Advantages:** Centralized security and business logic; easy to maintain and scale; lightweight clients.
* **Limitations:** The server is a potential single point of failure and a performance bottleneck if not scaled behind a load balancer.

### 5. Interview Answer (30-60 seconds)
> "Client-Server Architecture is a distributed model where responsibilities are split between clients, which request services, and servers, which process requests and manage data. The client initiates communication over the network to the server's IP address and port. The server processes the request, queries databases, and returns a response. This design centralizes data and business logic, though it requires load balancers and scaling strategies to handle high traffic and avoid single points of failure."

### 6. Common Follow-up Questions
* What is the difference between a monolithic and a microservices server architecture?
* What is a Three-Tier Architecture? (Answer: Client tier, Application server tier, and Database storage tier).

### 7. Connection to Real Software Systems
In web applications, the browser rendering React acts as the client, Spring Boot acts as the application server, and PostgreSQL acts as the database server, communicating over TCP-based network connections.
