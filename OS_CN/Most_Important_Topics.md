# OS & CN: Most Important Topics (Study First)
## High-Priority Placement Study Guide (5-15 LPA Target)

This document aggregates the absolute most critical, high-frequency topics asked in software engineering and full-stack developer technical interviews. Master these topics first before diving into the complete handbooks.

---

# PART 1: OPERATING SYSTEMS (OS)

---

## 1. Process vs Thread

=========================================
1. EASY UNDERSTANDING
=========================================
* **What is it?** 
  A process is an active running application (like Spotify or Chrome) with its own private memory space. A thread is a lightweight worker inside a process (like a spell-checker inside VS Code) that shares memory with other sibling threads.
* **Why was it created?** 
  To balance stability and speed. Processes provide isolation so that if one crashes, it doesn't affect others. Threads allow fast multitasking and direct communication within a single application without OS overhead.
* **Real-Life Example** 
  Google Chrome launches a new process for each browser tab so that a crashed webpage doesn't freeze the whole browser. However, a multi-threaded web server like Spring Boot runs as a single process spawning a new thread for each user request to handle them quickly.

=========================================
2. BUILD INTUITION
=========================================
* **How does it work internally?** 
  ```
  +-------------------------------------------------------------+
  |                      PROCESS (e.g., Chrome)                 |
  |  +-------------------------------------------------------+  |
  |  | SHARED MEMORY SECTION                                 |  |
  |  | [ Code Segment ]  [ Static/Global Data ]  [ Heap ]    |  |
  |  | [ File Descriptors ]  [ Network Sockets ]             |  |
  |  +-------------------------------------------------------+  |
  |                                                             |
  |  +-----------------------+       +-----------------------+  |
  |  | THREAD 1              |       | THREAD 2              |  |
  |  | - Stack (Local Vars)  |       | - Stack (Local Vars)  |  |
  |  | - CPU Registers       |       | - CPU Registers       |  |
  |  | - Program Counter     |       | - Program Counter     |  |
  |  +-----------------------+       +-----------------------+  |
  +-------------------------------------------------------------+
  ```
  Process context-switching requires changing virtual address maps, which flushes the fast hardware Translation Lookaside Buffer (TLB) cache. Thread context-switching only swaps CPU registers and stack pointers, leaving the page table and TLB cache intact, saving CPU cycles.
* **Why should a software engineer care?** 
  If you are designing a system that requires high isolation (where a crash in one task must not bring down other tasks), use processes. If you need high performance and fast shared state access, use threads.
* **How is it used in real systems?** 
  PostgreSQL uses a process-based model (each connection is a separate process), whereas MySQL uses a thread-based model (each connection is a thread).

=========================================
3. INTERVIEW PREPARATION
=========================================
* **Technical Definition** 
  A Process is the primary unit of OS resource allocation and memory isolation, consisting of its own virtual address space. A Thread is the basic unit of CPU scheduling and execution context that operates within a parent process's memory space.
* **30-Second Interview Answer** 
  "The core difference is memory isolation. A process is an independent program in execution with its own virtual address space, making process switches expensive because they flush the TLB cache. A thread is a lightweight execution unit inside a process that shares its parent's heap, code, and global data, keeping only its own stack, registers, and program counter. Thread context-switching is much faster, but a thread crash can terminate the entire parent process."
* **Common Follow-up Questions** 
  * Why do threads share the heap but not the stack?
  * What is the difference between a virtual memory context switch and a thread context switch?
* **Important Points Interviewers Expect** 
  * Comparison of memory layout (Heap vs. Stack sharing).
  * Explaining the **TLB cache flush** during process switches.
  * Mentioning crash safety trade-offs.
* **Common Mistakes Students Make** 
  * Stating that threads communicate via IPC. (They communicate directly via shared variables; processes use IPC).

=========================================
4. QUICK REVISION
=========================================
* **Key Comparison Table**

| Feature | Process | Thread |
| :--- | :--- | :--- |
| **Memory** | Isolated address space | Shares heap, code, data |
| **Switching Overhead** | High (flushes TLB cache) | Low (retains page tables) |
| **Crash Safety** | High (crash isolated) | Low (can crash parent process) |
| **Communication** | Via IPC (Pipes, Sockets) | Directly via shared memory |

* **One-Line Revision** 
  Processes are isolated containers representing resource allocation; threads are concurrent execution paths inside them.
* **Memory Trick** 
  **P**rocess = **P**rotected. **T**hread = **T**hroughput.

=========================================
5. PROJECT CONNECTION
=========================================
* **React Applications:** JavaScript is single-threaded, running in the browser's renderer process.
* **Spring Boot Applications:** Spawns a Tomcat thread pool inside the JVM process to handle concurrent client requests.
* **REST APIs:** Requests are processed concurrently on separate worker threads.
* **PostgreSQL:** Spawns a dedicated database process for each client connection.
* **JWT Authentication:** Request threads validate stateless JWT signatures concurrently in memory.
* **WebSocket Systems:** Persistent connections are managed by socket-handling threads.
* **Docker Deployments:** Isolates containerized processes using cgroups and namespaces.

---

## 2. Context Switching

=========================================
1. EASY UNDERSTANDING
=========================================
* **What is it?** 
  Context switching is the OS mechanism that pauses a running process or thread, saves its exact register states, swaps in another task, and resumes it.
* **Why was it created?** 
  To support multitasking. By switching between applications thousands of times a second, a single CPU core can run Spotify, Chrome, and VS Code concurrently.
* **Real-Life Example** 
  An office worker reading a report. If they get an email, they place a bookmark (Save Context), reply to the email (Switch Task), look at the bookmark, and resume reading (Restore Context).

=========================================
2. BUILD INTUITION
=========================================
* **How does it work internally?** 
  ```
  [Process A: Running]                       [Process B: Ready]
           |
   (Timer Interrupt / Syscall)
           v
  [1. Transition to Kernel Mode]
  [2. Save Registers to A's PCB] 
           |
           v
  [3. Run Scheduler Algorithm] -------------> [Selects Process B]
                                                      |
  [4. Swap Page Table Base Registers] <---------------+ (TLB Invalidated!)
  [5. Load Registers from B's PCB]
           |
           v
  [6. Transition to User Mode]
           |
           v
                                             [Process B: Running]
  ```
  1. A timer interrupt triggers a mode switch to Kernel Mode.
  2. Current CPU registers are saved to the active task's PCB or TCB.
  3. The OS Scheduler selects the next task.
  4. For process switches, page tables are updated, which **invalidates the TLB cache**.
  5. The CPU loads the registers from the new task's PCB/TCB and resumes execution.
* **Why should a software engineer care?** 
  Context switching is pure overhead. If you configure too many active threads, the CPU wastes all its energy switching tasks instead of executing code.
* **How is it used in real systems?** 
  Asynchronous frameworks (like Node.js) eliminate thread context-switching by running a single-threaded event loop.

=========================================
3. INTERVIEW PREPARATION
=========================================
* **Technical Definition** 
  Context Switching is the operating system mechanism that suspends a running process or thread by saving its CPU register state into its PCB or TCB, allocates the CPU to a new task, and restores its saved state to resume execution.
* **30-Second Interview Answer** 
  "Context switching is the OS swapping execution between tasks. When an interrupt occurs, the CPU switches to kernel mode, saves the current register states, stack pointer, and program counter to the active PCB/TCB. It then schedules another task. For process switches, the kernel swaps virtual memory mappings, which flushes the TLB cache. Finally, the target states are loaded to resume execution."
* **Common Follow-up Questions** 
  * Why is thread context switching cheaper than process context switching?
  * What is the role of the TLB during a context switch?
* **Important Points Interviewers Expect** 
  * Explaining the **TLB cache flush** penalty.
  * Step-by-step state saving sequence.
* **Common Mistakes Students Make** 
  * Forgetting that the CPU must enter Kernel Mode to execute the context switch.

=========================================
4. QUICK REVISION
=========================================
* **Key Points** 
  * Saves/restores registers to PCB/TCB.
  * Process switch flushes TLB; thread switch does not.
  * Frequent switching degrades performance.
* **One-Line Revision** 
  The OS mechanism of saving the CPU execution state of one task and loading the state of another.
* **Memory Trick** 
  **Context** = CPU snapshot. **Switching** = Swapping snapshots.

=========================================
5. PROJECT CONNECTION
=========================================
* **React Applications:** JavaScript event loops avoid context switching.
* **Spring Boot Applications:** Configuring too many Tomcat threads (e.g., 5000) degrades performance due to excessive context switching.
* **REST APIs:** API thread pool sizes should match CPU core counts.
* **PostgreSQL:** High concurrent connections trigger process context-switching bottlenecks.
* **JWT Authentication:** Fast token verification avoids thread blocking and context switches.
* **WebSocket Systems:** Event-driven models keep sockets open without blocking thread context.
* **Docker Deployments:** Container processes share host kernels, avoiding VM context-switching overhead.

---

## 3. Multithreading

=========================================
1. EASY UNDERSTANDING
=========================================
* **What is it?** 
  Multithreading is a design pattern where a single process runs multiple execution paths (threads) concurrently to execute tasks in parallel.
* **Why was it created?** 
  To exploit modern multi-core CPU architectures, allowing background I/O operations to run without blocking the primary user interface thread.
* **Real-Life Example** 
  An IDE editor rendering your typing on one thread, compiling code on a second thread, and downloading dependencies on a third thread in the background.

=========================================
2. BUILD INTUITION
=========================================
* **How does it work internally?** 
  Developer APIs create user-space threads, which the runtime maps to OS kernel-space threads:
  * **One-to-One (1:1):** Every user thread maps directly to an OS thread. (Standard in Linux/Windows/Java). It allows true hardware parallel execution across multiple CPU cores.
  * **Many-to-One (M:1):** Multiple user threads run on one kernel thread. Fast switching, but a blocking call blocks all.
  * **Many-to-Many (M:N):** Multiplexes threads dynamically.
* **Why should a software engineer care?** 
  Multithreading introduces data concurrency conflicts. You must use synchronization locks (Mutex) to protect shared data from race conditions.
* **How is it used in real systems?** 
  Java's Thread Pools pre-allocate threads, avoiding the overhead of creating and destroying threads repeatedly.

=========================================
3. INTERVIEW PREPARATION
=========================================
* **Technical Definition** 
  Multithreading is an execution model allowing multiple threads to run concurrently within a single process address space, utilizing hardware multi-cores to achieve parallel task processing.
* **30-Second Interview Answer** 
  "Multithreading splits a program's execution into multiple concurrent threads inside one process. In modern systems, this uses a 1:1 mapping model where each user thread maps to an OS kernel thread. This allows a process to run CPU-bound tasks in parallel across multiple CPU cores, and execute I/O tasks in the background without blocking the UI thread."
* **Common Follow-up Questions** 
  * Difference between concurrency and parallelism?
  * What are green threads?
* **Important Points Interviewers Expect** 
  * Explaining the **1:1 mapping model**.
  * Distinguishing concurrency from parallelism.
* **Common Mistakes Students Make** 
  * Thinking multithreading always improves performance. (It slows down single-core systems due to switching overhead).

=========================================
4. QUICK REVISION
=========================================
* **Key Points** 
  * Concurrent execution inside a process.
  * Shares heap and code segments.
  * Prone to race conditions (requires synchronization).
* **One-Line Revision** 
  Splitting execution paths within a single process to process tasks concurrently.
* **Memory Trick** 
  **Multithreading** = Multiple workers sharing one desk.

=========================================
5. PROJECT CONNECTION
=========================================
* **React Applications:** JavaScript Web Workers run heavy CPU code on background threads.
* **Spring Boot Applications:** Tomcat delegates requests to a pool of concurrent threads.
* **REST APIs:** API controllers run requests in parallel request threads.
* **PostgreSQL:** Uses parallel worker threads for query index scans.
* **JWT Authentication:** Multiple request threads validate tokens concurrently.
* **WebSocket Systems:** Event listener threads push data to connected client sessions.
* **Docker Deployments:** Docker container resources limit host thread capacity allocations.

---

## 4. Deadlock

=========================================
1. EASY UNDERSTANDING
=========================================
* **What is it?** 
  A deadlock is a lockup state where a set of threads are permanently frozen because each thread holds a lock on a resource the other thread needs, and neither will release their lock.
* **Why was it created?** 
  It is a critical system bug that occurs when threads acquire locks in different orders.
* **Real-Life Example** 
  Two people sitting at a table. Person A holds the fork and waits for the knife. Person B holds the knife and waits for the fork. Neither will let go, freezing dinner.

=========================================
2. BUILD INTUITION
=========================================
* **How does it work internally?** 
  ```
  Process A (Holds Lock 1) ------ Waits For ------> Lock 2 (Held by Process B)
        ^                                                  |
        |------------------ Waits For ---------------------v
  ```
  A deadlock occurs only if the **Four Coffman Conditions** hold simultaneously:
  1. **Mutual Exclusion:** Resources must be non-shareable.
  2. **Hold and Wait:** A thread holding a resource can wait for new ones.
  3. **No Preemption:** Resources cannot be taken away forcefully.
  4. **Circular Wait:** A closed loop of threads exists where each waits for a resource held by the next.
  * **Handling:**
    * **Prevention:** Enforce a strict lock ordering to break the **Circular Wait** condition.
    * **Avoidance:** Check requests at runtime using the **Banker's Algorithm** to ensure safety.
    * **Detection:** Detect loops in lock graphs and abort transactions.
* **Why should a software engineer care?** 
  Deadlocks freeze applications, causing them to time out. Recovering from deadlocks usually requires restarting the server process.
* **How is it used in real systems?** 
  PostgreSQL automatically detects deadlock cycles and aborts one of the blocking transactions.

=========================================
3. INTERVIEW PREPARATION
=========================================
* **Technical Definition** 
  A Deadlock is an execution state where a set of processes are permanently blocked because each process holds a resource and waits for another resource held by another process in the set, forming a circular dependency graph.
* **30-Second Interview Answer** 
  "A deadlock is a freeze state caused by circular resource dependencies among threads. It requires four simultaneous conditions: Mutual Exclusion, Hold and Wait, No Preemption, and Circular Wait. We resolve deadlocks by Prevention, such as ordering lock acquisitions strictly to break Circular Wait, or Avoidance, using the Banker's Algorithm to check resource safety at runtime."
* **Common Follow-up Questions** 
  * Difference between deadlock prevention and avoidance?
  * What is the Ostrich Algorithm?
* **Important Points Interviewers Expect** 
  * Naming all **4 Coffman Conditions**.
  * Showing how Lock Ordering prevents Circular Wait.
* **Common Mistakes Students Make** 
  * Thinking deadlocks only occur in CPU schedulers.

=========================================
4. QUICK REVISION
=========================================
* **Key Points** 
  * Permanent system freeze.
  * Requires 4 Coffman conditions.
  * Break Circular Wait by ordering lock acquisitions.
  * Avoidance uses Banker's Algorithm.
* **One-Line Revision** 
  A system freeze where a loop of threads wait indefinitely for each other's resources.
* **Memory Trick** 
  **M**any **H**ungry **N**injas **C**heat: **M**utual Exclusion, **H**old & Wait, **N**o Preemption, **C**ircular Wait.

=========================================
5. PROJECT CONNECTION
=========================================
* **React Applications:** Freezes occur if two state hooks trigger circular update loops.
* **Spring Boot Applications:** Occurs if Thread A locks Object 1 and waits for Object 2, while Thread B does the opposite.
* **REST APIs:** Reverse-ordered database queries in parallel API calls trigger transaction deadlocks.
* **PostgreSQL:** Background threads check lock graphs, aborting deadlocked queries.
* **JWT Authentication:** Not related.
* **WebSocket Systems:** Session closing threads can deadlock with concurrent message push channels.
* **Docker Deployments:** Microservices can deadlock across network APIs (Service A waits for Service B, which waits for Service A).

---

## 5. Semaphore vs Mutex

=========================================
1. EASY UNDERSTANDING
=========================================
* **What is it?** 
  A Mutex is a lock with a key (only the thread that locked it can unlock it). A Semaphore is a signaling flag (any thread can signal it) that uses an integer counter to manage a pool of multiple resources.
* **Why was it created?** 
  A Mutex protects a single critical section. A Semaphore was created to coordinate access to a pool of multiple identical resources (e.g., a connection pool).
* **Real-Life Example** 
  * **Mutex:** A bathroom key in a coffee shop. Only the person who takes the key can use and unlock the bathroom.
  * **Semaphore:** A restaurant with 5 tables. The host tracks tables using a counter. When tables are full, customers wait in a queue until someone finishes and signals the host.

=========================================
2. BUILD INTUITION
=========================================
* **How does it work internally?** 
  * **Mutex:** Contains a state (Locked/Unlocked) and an **Owner Thread ID**. Only the owner can call `unlock()`. It supports **Priority Inheritance** to prevent priority inversion.
  * **Semaphore:** Contains a counter ($S$) and a wait queue. Has no owner. Any thread can call `signal()` to wake up a thread waiting on `wait()`.
    * `wait()` decrements counter; if negative, the thread is blocked.
    * `signal()` increments counter; if negative, it wakes up a waiter.
* **Why should a software engineer care?** 
  Use a Mutex to serialize access to a shared variable. Use a Semaphore to manage resource limits (like rate limiting API calls).
* **How is it used in real systems?** 
  Connection pools use counting semaphores to block application request threads when all database connections are in use.

=========================================
3. INTERVIEW PREPARATION
=========================================
* **Technical Definition** 
  A Mutex is an ownership-based locking mechanism that enforces mutual exclusion on a critical section. A Semaphore is an integer-based signaling primitive used to manage resource pools or coordinate thread execution order.
* **30-Second Interview Answer** 
  "The core difference is ownership. A Mutex is an ownership-based lock; only the thread that locks it can unlock it. It supports priority inheritance to prevent priority inversion. A Semaphore is a signaling mechanism using an integer counter to manage access to a resource pool. It has no owner; any thread can signal a semaphore to release it."
* **Common Follow-up Questions** 
  * What is Priority Inversion, and how does a Mutex prevent it?
  * Can a binary semaphore be used exactly like a Mutex?
* **Important Points Interviewers Expect** 
  * Emphasizing **Ownership** differences.
  * Explaining how `wait()` and `signal()` modify the counter.
* **Common Mistakes Students Make** 
  * Thinking that semaphores verify thread ownership.

=========================================
4. QUICK REVISION
=========================================
* **Key Comparison Table**

| Feature | Mutex | Semaphore |
| :--- | :--- | :--- |
| **Ownership** | Strict thread ownership | No owner (any thread can signal) |
| **Usage** | Protecting a critical section | Managing resource pools / task signaling |
| **Operations** | `lock()` / `unlock()` | `wait()` / `signal()` |
| **Priority** | Supports Priority Inheritance | Does not prevent priority inversion |

* **One-Line Revision** 
  A Mutex is a lock with a strict owner; a Semaphore is a counter-based signaling tool.
* **Memory Trick** 
  **M**utex = **M**ine (Ownership). **S**emaphore = **S**ignal (Public).

=========================================
5. PROJECT CONNECTION
=========================================
* **React Applications:** V8 engine locks protect internal JS call stack scopes.
* **Spring Boot Applications:** Mutexes secure cached variables; semaphores rate-limit outgoing API calls.
* **REST APIs:** Restricts concurrent request thresholds.
* **PostgreSQL:** Uses low-level spinlocks and semaphores internally to manage shared buffers.
* **JWT Authentication:** Signing keys are protected using read-write mutex locks.
* **WebSocket Systems:** Semaphores limit the maximum number of concurrent active chat connections.
* **Docker Deployments:** Consul distributed locks act as cross-container mutexes.

---

## 6. Virtual Memory

=========================================
1. EASY UNDERSTANDING
=========================================
* **What is it?** 
  Virtual Memory is a memory abstraction technique that makes each process believe it has access to a huge, contiguous block of main memory, even if physical RAM is small, by using hard disk space (swap space) as temporary RAM.
* **Why was it created?** 
  To allow execution of applications larger than physical RAM and ensure absolute memory isolation between processes.
* **Real-Life Example** 
  A student's desk (Physical RAM) holding 3 active notebooks. A large backpack (Swap Disk) holds 10 other books. If the student needs a book not on the desk, they swap a book from the desk to the backpack.

=========================================
2. BUILD INTUITION
=========================================
* **How does it work internally?** 
  ```
  Virtual Address Space                       Physical RAM
  +------------------+                    +------------------+
  | Page 0           | ------ Maps -----> | Frame 2          |
  | Page 1           | ------ Maps -----> | Frame 0          |
  | Page 2 (Invalid) | -- Page Fault!     | Frame 1          |
  +------------------+        |           +------------------+
                              v
                        +-----------+
                        | Swap Disk |
                        +-----------+
  ```
  The OS divides memory into Pages (virtual) and Frames (physical RAM).
  1. The CPU sends a virtual address request to the MMU.
  2. The MMU checks the **Page Table**.
  3. If present, it resolves the address.
  4. If absent (invalid bit set), the CPU triggers a **Page Fault** interrupt.
  5. The OS kernel retrieves the page from the swap disk, copies it into a RAM frame, updates the Page Table, and resumes the instruction.
* **Why should a software engineer care?** 
  If your system runs out of physical RAM and starts swapping heavily, the application will freeze because disk access is thousands of times slower than RAM.
* **How is it used in real systems?** 
  Linux uses a swap partition to keep active database caches in physical RAM while moving idle background scripts to the disk.

=========================================
3. INTERVIEW PREPARATION
=========================================
* **Technical Definition** 
  Virtual Memory is a memory management abstraction that separates a program's logical address space from physical RAM, allowing execution of processes whose memory footprint exceeds physical memory capacity by utilizing swap disk space.
* **30-Second Interview Answer** 
  "Virtual memory abstracts physical RAM, giving each process an isolated logical address space. The OS maps virtual pages to physical frames using page tables. When a process accesses a page not loaded in RAM, the MMU triggers a page fault. The OS then swaps that page from the hard disk swap partition into physical RAM, updates the page table, and resumes execution. This allows large applications to run while ensuring process memory isolation."
* **Common Follow-up Questions** 
  * What is a page fault, and how is it resolved?
  * What is thrashing, and how do we prevent it?
* **Important Points Interviewers Expect** 
  * Naming **Pages**, **Frames**, and **Page Tables**.
  * Step-by-step description of page fault handling.
* **Common Mistakes Students Make** 
  * Believing page faults are application crash errors. (They are hardware interrupts handled silently).

=========================================
4. QUICK REVISION
=========================================
* **Key Points** 
  * Separates logical and physical memory.
  * Uses swap disk space to expand RAM.
  * Accessing missing pages triggers a **Page Fault**.
  * Enforces process isolation.
* **One-Line Revision** 
  An abstraction that maps logical pages to physical RAM frames, using the disk to expand memory limits.
* **Memory Trick** 
  **Virtual** Memory = **Invisible** backpack for books.

=========================================
5. PROJECT CONNECTION
=========================================
* **React Applications:** Browser processes allocate virtual memory to render web pages.
* **Spring Boot Applications:** JVM heap configurations reserve virtual address space on the host OS.
* **REST APIs:** Dynamic buffers allocate virtual pages to parse JSON.
* **PostgreSQL:** Uses virtual memory mappings (`mmap`) to cache database pages.
* **JWT Authentication:** Cryptographic signature functions execute inside protected virtual pages.
* **WebSocket Systems:** Managing thousands of active connections relies on virtual memory manager frame allocations.
* **Docker Deployments:** Setting container memory limits stops containers from thrashing host virtual memory.

---

## 7. Paging

=========================================
1. EASY UNDERSTANDING
=========================================
* **What is it?** 
  Paging is the mechanism used to implement virtual memory. It divides logical memory into fixed-size blocks called **Pages** (typically 4KB) and physical RAM into matching blocks called **Frames**.
* **Why was it created?** 
  To eliminate **External Fragmentation**. Because pages are fixed-size, the OS can allocate any free frame in RAM to any process page, meaning we never have to run expensive memory compaction algorithms.
* **Real-Life Example** 
  Breaking a long scroll of text (contiguous memory) into a book with fixed-size pages. You can print and bind pages in any physical order, and use an index table to read them sequentially.

=========================================
2. BUILD INTUITION
=========================================
* **How does it work internally?** 
  ```
  Virtual Address: [ Page Number (p) | Offset (d) ]
                           |
                   +-------v-------+
                   |  TLB (Cache)  | --- Hit ---> Frame (f) + d ---> RAM
                   +-------+-------+
                           | Miss
                   +-------v-------+
                   |  Page Table   | -----------> Frame (f) + d ---> RAM
                   +---------------+
  ```
  1. The CPU generates a virtual address with a **Page Number ($p$)** and an **Offset ($d$)**.
  2. The MMU checks the **Translation Lookaside Buffer (TLB)** cache.
  3. **TLB Hit:** Physical frame ($f$) is resolved immediately.
  4. **TLB Miss:** The MMU reads the process's **Page Table** in RAM. It fetches the frame address, updates the TLB, and combines it with the offset ($f + d$) to access RAM.
  * **PTE Flags:** Valid/Invalid (in RAM or disk), Dirty (modified).
* **Why should a software engineer care?** 
  A TLB miss requires two memory reads (once for the page table, once for the data), slowing down execution. Sequentially accessing arrays maximizes TLB hits.
* **How is it used in real systems?** 
  Database servers like PostgreSQL configure Linux **HugePages** (2MB or 1GB pages) to minimize page table size and maximize TLB hits.

=========================================
3. INTERVIEW PREPARATION
=========================================
* **Technical Definition** 
  Paging is a non-contiguous memory management scheme that partitions logical address space into fixed-size pages and physical memory into identical frames, translating addresses via page tables and optimizing lookups using a Translation Lookaside Buffer.
* **30-Second Interview Answer** 
  "Paging divides logical memory into fixed-size pages and physical memory into matching frames. The MMU indexes the process's page table to translate virtual addresses. To optimize speed, the CPU uses the TLB cache. A TLB hit resolves translations instantly, while a TLB miss requires reading the page table in RAM. Paging prevents external fragmentation but can cause internal fragmentation on the last page."
* **Common Follow-up Questions** 
  * What is a TLB miss?
  * What is Multi-Level Paging?
* **Important Points Interviewers Expect** 
  * Drawing the address translation diagram (Page/Offset to Frame/Offset).
  * Explaining **TLB hits** vs. **TLB misses**.
* **Common Mistakes Students Make** 
  * Stating that pages and frames have different sizes.

=========================================
4. QUICK REVISION
=========================================
* **Key Points** 
  * Fixed-size blocks (Pages and Frames).
  * Eliminates external fragmentation.
  * Mapped via process **Page Tables**.
  * Accelerated by the **TLB** hardware cache.
* **One-Line Revision** 
  A non-contiguous memory allocation technique dividing logical memory into fixed-size pages mapped to physical frames.
* **Memory Trick** 
  **P**age = **P**rogram block. **F**rame = **F**hysical block.

=========================================
5. PROJECT CONNECTION
=========================================
* **React Applications:** Sequential array operations run faster by maximizing CPU caching.
* **Spring Boot Applications:** Large JVM heaps map across thousands of OS memory pages.
* **REST APIs:** API payload serialization maps buffers across multiple virtual pages.
* **PostgreSQL:** Configuring Linux **HugePages** increases database performance under high load.
* **JWT Authentication:** Cryptographic validation code resides in read-only text segment pages.
* **WebSocket Systems:** Persistent session tracking allocations are distributed across physical frames.
* **Docker Deployments:** The host OS kernel manages paging tables for all container namespaces.

---

## 8. System Calls

=========================================
1. EASY UNDERSTANDING
=========================================
* **What is it?** 
  A System Call is a secure gateway that allows a user program to ask the OS kernel to perform privileged hardware operations on its behalf, like reading a file or sending network packets.
* **Why was it created?** 
  To enforce security. If applications could write directly to hardware, a buggy app could overwrite another program's disk files. System calls force programs to request the OS to perform these tasks safely.
* **Real-Life Example** 
  Ordering food at a counter. You tell the cashier (System Call) what you want, and they get it from the kitchen (Kernel Space) and hand it to you. You are not allowed to walk into the kitchen.

=========================================
2. BUILD INTUITION
=========================================
* **How does it work internally?** 
  ```
  User Application                Wrapper Library                 OS Kernel
  +------------------+            +------------------+            +------------------+
  | calls read()     | ---------> | loads syscall id |            | executes syscall |
  |                  |            | triggers trap    | ---------> | (Kernel Mode)    |
  | resumes execution| <--------- | returns status   | <--------- | returns result   |
  +------------------+            +------------------+            +------------------+
  ```
  1. An application calls a library wrapper (like `read()`).
  2. The library loads the system call number and parameters into CPU registers.
  3. The library executes a software interrupt or trap instruction (`syscall`).
  4. The CPU switches from User Mode (Ring 3) to Kernel Mode (Ring 0) and jumps to the kernel's **System Call Handler** table.
  5. The kernel validates inputs, runs the operation, writes the result to registers, and runs a return instruction (`sysret`) to switch back to User Mode.
* **Why should a software engineer care?** 
  System calls introduce execution overhead due to mode-switching. Batching file writes or using buffered streams minimizes system calls and speeds up your applications.
* **How is it used in real systems?** 
  Node.js's `fs.readFile()` executes a `read` system call internally, shifting execution to the kernel to read blocks from the disk.

=========================================
3. INTERVIEW PREPARATION
=========================================
* **Technical Definition** 
  A System Call is the programmatic interface provided by the operating system kernel that allows user-space applications to request privileged operations and hardware services.
* **30-Second Interview Answer** 
  "A system call is a secure gateway between user applications and the kernel. Since applications run in restricted User Mode, they cannot access hardware directly. When a system call is made, the library loads parameters into registers and triggers a hardware trap. The CPU switches to privileged Kernel Mode, validates the inputs, performs the task, and returns to user space. This ensures security, though it introduces state-switching overhead."
* **Common Follow-up Questions** 
  * Difference between a system call and a library call?
  * Difference between an interrupt and a trap?
* **Important Points Interviewers Expect** 
  * Detailed description of the mode switch (Trap -> Kernel Mode -> ISR -> Return -> User Mode).
  * Parameter passing using registers.
* **Common Mistakes Students Make** 
  * Believing that every function call in your code is a system call.

=========================================
4. QUICK REVISION
=========================================
* **Key Points** 
  * Interface between user apps and the kernel.
  * Triggered via software interrupts (traps).
  * Switches CPU from Ring 3 (User) to Ring 0 (Kernel).
  * Parameter passing via registers.
* **One-Line Revision** 
  A secure programmatic interface used by user-space applications to request privileged operations from the kernel.
* **Memory Trick** 
  **Syscall** = **System** room **call** service.

=========================================
5. PROJECT CONNECTION
=========================================
* **React Applications:** React uses the browser's APIs, which perform system calls under the hood to render pixels.
* **Spring Boot Applications:** Database query requests use socket system calls to communicate with the database.
* **REST APIs:** Every parsed API request executes network socket read and write system calls.
* **PostgreSQL:** Uses file system calls (`fsync`) to flush data buffers to physical storage.
* **JWT Authentication:** Accessing system time to verify token expiration executes time-related system calls.
* **WebSocket Systems:** Persistent socket connections rely on the kernel to monitor active network file descriptors.
* **Docker Deployments:** Containers execute system calls directly on the shared host Linux kernel.

---

# PART 1 SUMMARY & PLACEMENT PRACTICE

### Beginner Understanding
Operating Systems manage hardware and run applications inside isolated boxes called **Processes**. To multitask efficiently, processes spawn lightweight workers called **Threads** that share memory. If threads modify the same variable concurrently, a **Race Condition** occurs, corrupting data. To prevent this, we lock the code section (**Critical Section**) using locks like **Mutexes** (exclusive owner) or **Semaphores** (resource counter). If locks are acquired in different sequences, threads can block each other permanently, causing a **Deadlock**.

### Interview Understanding
Interviewers expect candidate fluency in **Process vs. Thread** memory layouts (shared heap vs. private stack), the mechanism of **Context Switching** (PCB register saving and TLB cache flushes), the **Four Coffman Conditions** of deadlock, and the design requirements for critical section safety (Mutual Exclusion, Progress, Bounded Waiting).

### Real Software Engineering Understanding
In real systems, threads are rarely created manually; they are managed inside **Thread Pools** (like Spring Boot's Tomcat pool or HikariCP connection pool). Performance bottlenecks are often caused by resource contention in **Critical Sections** or CPU cycles wasted on **Context Switching** under high load.

---

## Placement Practice & Sheets

### Top 5 Interview Questions
1. Compare a process and a thread across memory layout, creation cost, and switching overhead.
2. Why is process context switching more expensive than thread context switching? Explain the TLB's role.
3. What are the 4 Coffman conditions required for a deadlock to occur? How do you prevent deadlocks?
4. What is the difference between a Mutex and a Binary Semaphore?
5. What is a race condition? Write a simple code example showing a race condition.

### Frequently Asked Follow-up Questions
* *What is Belady's Anomaly, and what algorithms does it affect?* (Answer: Belady's anomaly occurs when adding more memory page frames leads to more page faults. It affects FIFO page replacement, but not stack-based algorithms like LRU).
* *What is Priority Inversion, and how does a Mutex resolve it?* (Answer: Priority inversion is when a low-priority thread holding a lock blocks a high-priority thread because a medium-priority thread preempts the low-priority one. Mutexes solve this by using Priority Inheritance).

### 5-Minute Revision Sheet (Cheat Sheet)
* **Process vs. Thread:** Process has isolated address space (needs IPC). Thread shares heap/code/data but has private stack/registers.
* **Context Switch:** User -> Kernel mode -> Save CPU registers to active PCB/TCB -> Schedule -> Swap memory tables (flushes TLB for processes) -> Load target state -> User mode.
* **Race Condition:** Unsynchronized write access to shared data. Fixed via Mutex/Semaphore.
* **Deadlock Conditions:** Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait. Enforce lock ordering to prevent.
* **Critical Section Criteria:** Mutual Exclusion, Progress, Bounded Waiting.

### 30-Minute Revision Sheet
* **Thread Scheduling:** 1:1 model maps each user thread to a kernel thread for parallel processing. Round Robin schedules threads using a Time Quantum. Too small = excessive context-switching overhead; too large = behaves like FCFS.
* **Synchronization Primitives:**
  * **Mutex:** Locked/Unlocked. Strict thread ownership. Supports Priority Inheritance.
  * **Semaphore:** Integer counter. Signaling mechanism. No owner. `wait()` decrements; `signal()` increments.
  * **Spinlock:** Busy-waiting lock. Used for low-latency, short operations.

### Most Important Placement Questions
* *How does Tomcat handle concurrent HTTP requests in Spring Boot?* 
  Tomcat maintains a Thread Pool. When an HTTP request arrives, the connector maps it to a worker thread from the pool. This thread executes the code in your controller, service, and database repository. Once the response is returned, the thread is returned to the pool. If the database connection pool is empty, the thread blocks using a Semaphore until a connection is freed.

---
---

# PART 2: COMPUTER NETWORKS (CN)

---

## 1. OSI Model

=========================================
1. EASY UNDERSTANDING
=========================================
* **What is it?** 
  The OSI Model is a 7-layer theoretical blueprint explaining how data moves from a user program (like Chrome) down through physical wires, and back up to another program.
* **Why was it created?** 
  To standardize networking. By dividing network tasks into 7 distinct layers, developers can replace protocols at one layer (like swapping HTTP for WebSockets) without rewriting the lower layers.
* **Real-Life Example** 
  Mailing a letter: you write the message (Application), translate it to English (Presentation), write the address on the envelope (Network), hand it to the postman (Data Link), and a truck drives it on the road (Physical).

=========================================
2. BUILD INTUITION
=========================================
* **How does it work internally?** 
  Data is wrapped in headers at each layer on the sender (**Encapsulation**) and unwrapped on the receiver (**Decapsulation**).
  * **L7 Application:** Protocols the user interacts with (HTTP, DNS, WebSocket).
  * **L6 Presentation:** Formats, encrypts, and compresses data (TLS).
  * **L5 Session:** Manages connections.
  * **L4 Transport:** End-to-end reliability (TCP - Segments, UDP - Datagrams).
  * **L3 Network:** Routing and IP addressing (IP - Packets).
  * **L2 Data Link:** Local link addressing (MAC - Frames).
  * **L1 Physical:** Raw physical bits (Cables, Hubs).
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
* **Why should a software engineer care?** 
  Knowing the layers helps you isolate network bugs. A routing error is a Layer 3 issue; an expired SSL certificate is a Layer 6 issue; a bad API route is a Layer 7 issue.
* **How is it used in real systems?** 
  Load balancers can be Layer 4 (routing connections based on port/IP) or Layer 7 (routing traffic based on HTTP cookies or paths).

=========================================
3. INTERVIEW PREPARATION
=========================================
* **Technical Definition** 
  The Open Systems Interconnection (OSI) model is a conceptual 7-layer framework developed by the ISO that standardizes network communication protocols, separating physical transmission from application logic.
* **30-Second Interview Answer** 
  "The OSI model is a 7-layer conceptual framework. It consists of the Physical, Data Link, Network, Transport, Session, Presentation, and Application layers. During transmission, data is encapsulated with headers at each layer on the sender, and decapsulated on the receiver. While it is theoretical, it helps engineers modularize and troubleshoot network systems by separating physical signals from application protocols."
* **Common Follow-up Questions** 
  * At which layers do switches and routers operate?
  * What is encapsulation?
* **Important Points Interviewers Expect** 
  * Listing all 7 layers in the correct order.
  * Naming the data unit at each layer.
* **Common Mistakes Students Make** 
  * Confusing the OSI model (theoretical) with the TCP/IP model (practical).

=========================================
4. QUICK REVISION
=========================================
* **Key Points** 
  * 7-layer theoretical reference model.
  * Encapsulates headers moving down; decapsulates moving up.
  * Modular architecture simplifies protocol replacement.
* **One-Line Revision** 
  A 7-layer theoretical blueprint standardizing communication from physical wires up to user software.
* **Memory Trick** 
  **P**lease **D**o **N**ot **T**hrow **S**ausage **P**izza **A**way (Physical, Data Link, Network, Transport, Session, Presentation, Application).

=========================================
5. PROJECT CONNECTION
=========================================
* **React Applications:** React communicates at the Application Layer (Layer 7) using HTTP APIs.
* **Spring Boot Applications:** Embedded servers handle Layer 7 (HTTP) and negotiate Layer 6 encryption (TLS).
* **REST APIs:** REST operates at Layer 7 using HTTP methods to serialize JSON payloads.
* **PostgreSQL:** Queries travel as data payloads encapsulated in Layer 4 TCP segments.
* **JWT Authentication:** JWT claims are processed in the Application Layer.
* **WebSocket Systems:** Upgrades connections from HTTP (L7) to keep a bi-directional channel open.
* **Docker Deployments:** Containers route traffic through Layer 2 virtual switches.

---

## 2. TCP vs UDP

=========================================
1. EASY UNDERSTANDING
=========================================
* **What is it?** 
  TCP is a reliable transport protocol (ensures every byte arrives in order). UDP is a lightweight connectionless transport protocol (sends packets immediately without checking if they arrive).
* **Why was it created?** 
  TCP ensures complete accuracy for services like file transfers. UDP maximizes speed for real-time services like streaming.
* **Real-Life Example** 
  * **TCP:** Mailing a book one page at a time, keeping track of page numbers, and resending lost pages.
  * **UDP:** Shouting a greeting to someone across a street. If they miss a word, they infer it; you don't repeat yourself.

=========================================
2. BUILD INTUITION
=========================================
* **How does it work internally?** 
  * **TCP:** Establishes connections via a **Three-Way Handshake**. Tracks packets using sequence numbers and ACKs. Adjusts speed using Sliding Windows (Flow Control) and Slow Start (Congestion Control). Has a large 20-60 byte header.
  * **UDP:** Simple 8-byte header. Sends datagrams immediately without handshake or state tracking.
* **Why should a software engineer care?** 
  TCP's reliability checks add latency. Under packet loss, TCP experiences **Head-of-Line Blocking**: a lost packet halts all other packets in the buffer, causing lag.
* **How is it used in real systems?** 
  HTTP/2 runs on TCP, while HTTP/3 runs on UDP (using the QUIC protocol) to solve Head-of-Line blocking.

=========================================
3. INTERVIEW PREPARATION
=========================================
* **Technical Definition** 
  TCP is a connection-oriented, reliable transport protocol implementing flow and congestion control, while UDP is a connectionless, best-effort transport protocol optimizing speed and latency.
* **30-Second Interview Answer** 
  "The core difference is reliability vs. speed. TCP is connection-oriented and uses sequence numbers, ACKs, and timers to guarantee in-order, complete packet delivery. It also manages traffic using flow and congestion control. UDP is connectionless and sends packets immediately with an 8-byte header and no delivery checks, maximizing speed. We use TCP for APIs and databases, and UDP for DNS, WebRTC, and real-time streaming."
* **Common Follow-up Questions** 
  * Can you implement reliability on top of UDP?
  * What is TCP Head-of-Line blocking?
* **Important Points Interviewers Expect** 
  * Drawing a comparison table covering connection state, reliability, header sizes, and flow control.
  * Naming correct protocol use cases.
* **Common Mistakes Students Make** 
  * Saying UDP is insecure compared to TCP. (Both are unencrypted; security is added at the presentation layer using SSL/TLS).

=========================================
4. QUICK REVISION
=========================================
* **Key Comparison Table**

| Feature | TCP | UDP |
| :--- | :--- | :--- |
| **Connection** | Connection-oriented (3-way handshake) | Connectionless |
| **Reliability** | Guaranteed in-order, complete | Unreliable (best-effort) |
| **Header Size** | 20 to 60 bytes | 8 bytes |
| **Flow Control** | Yes (Sliding Window) | None |
| **Congestion** | Yes (Slow Start, Avoidance) | None |
| **Use Cases** | HTTP, Database, File Transfer | DNS, VoIP, Video Streaming, WebRTC |

* **One-Line Revision** 
  TCP guarantees reliable, in-order delivery; UDP maximizes speed and minimizes latency.
* **Memory Trick** 
  **TCP** = **T**rustworthy. **UDP** = **U**nchecked.

=========================================
5. PROJECT CONNECTION
=========================================
* **React Applications:** Interacts with HTTP APIs (TCP) and media streams (UDP).
* **Spring Boot Applications:** Tomcat handles incoming REST calls (TCP), while custom syslog integrations send metrics over UDP.
* **REST APIs:** REST architecture mandates TCP-based HTTP reliability.
* **PostgreSQL:** Operates strictly over TCP connection pools.
* **JWT Authentication:** Token exchanges run over TCP.
* **WebSocket Systems:** Upgrades TCP connections to support full-duplex traffic.
* **Docker Deployments:** Exposes container ports for TCP and UDP traffic.

---

## 3. HTTP vs HTTPS

=========================================
1. EASY UNDERSTANDING
=========================================
* **What is it?** 
  HTTP is the unencrypted plaintext protocol of the web. HTTPS is the secure version of HTTP that encrypts all traffic using SSL/TLS, protecting passwords and API tokens.
* **Why was it created?** 
  Standard HTTP transmits data in plain text, making it vulnerable to packet sniffing on public Wi-Fi. HTTPS prevents eavesdropping and data tampering.
* **Real-Life Example** 
  * **HTTP:** Writing a postcard. Anyone along the postal route can read the message.
  * **HTTPS:** Placing the message inside a locked box before mailing it. Only the recipient has the key.

=========================================
2. BUILD INTUITION
=========================================
* **How does it work internally?** 
  HTTPS runs HTTP over the SSL/TLS protocol on port 443.
  1. The server presents its **Digital Certificate** containing its public key.
  2. The client verifies the certificate against trusted **Certificate Authorities (CAs)**.
  3. The client and server run a cryptographic handshake to exchange a **Symmetric Session Key** using asymmetric encryption.
  4. Subsequent HTTP headers and payloads are encrypted using this symmetric key.
* **Why should a software engineer care?** 
  Browsers block or label non-HTTPS sites as "Not Secure," which damages search engine rankings (SEO).
* **How is it used in real systems?** 
  Nginx or AWS Application Load Balancers terminate SSL certificates, decrypting HTTPS requests before forwarding plain HTTP to backend application servers.

=========================================
3. INTERVIEW PREPARATION
=========================================
* **Technical Definition** 
  HTTPS is an encrypted extension of the Hypertext Transfer Protocol that runs over SSL/TLS on port 443, ensuring confidentiality, data integrity, and server authentication.
* **30-Second Interview Answer** 
  "HTTPS secures web traffic by running HTTP over SSL/TLS on port 443. During the handshake, the server presents a CA-signed certificate. The client verifies the certificate, and both sides negotiate a symmetric session key. Once established, all HTTP headers and payloads are encrypted, ensuring confidentiality, data integrity, and server authentication."
* **Common Follow-up Questions** 
  * How does asymmetric encryption differ from symmetric encryption in HTTPS?
  * What is the role of a Certificate Authority (CA)?
* **Important Points Interviewers Expect** 
  * Pointing out that HTTPS operates on port 443.
  * Explaining **Certificate Validation**.
  * Describing why asymmetric encryption is used for key exchange, and symmetric is used for data transfer.
* **Common Mistakes Students Make** 
  * Thinking that HTTPS encrypts only the body of the request. (It encrypts the entire HTTP packet, including headers, paths, cookies, and body; only the target IP address is visible).

=========================================
4. QUICK REVISION
=========================================
* **Key Points** 
  * Secure version of HTTP operating on port 443.
  * Encrypts headers and payloads.
  * Relies on CA-signed digital certificates for validation.
  * Combines asymmetric (key exchange) and symmetric (data transfer) encryption.
* **One-Line Revision** 
  An encrypted version of HTTP that secures web data using SSL/TLS protocols and CA certificates.
* **Memory Trick** 
  **HTTPS** = **HTTP** + **S**ecure lock.

=========================================
5. PROJECT CONNECTION
=========================================
* **React Applications:** Connects to HTTPS API endpoints to protect credentials in transit.
* **Spring Boot Applications:** SSL keys can be configured directly inside `application.properties` to serve HTTPS traffic.
* **REST APIs:** Production REST APIs should mandate HTTPS connections.
* **PostgreSQL:** Client connections can be secured over SSL.
* **JWT Authentication:** Indispensable for protecting JWTs from interception.
* **WebSocket Systems:** Secure WebSockets (`wss://`) run over HTTPS channels.
* **Docker Deployments:** Uses Let's Encrypt containers to automate SSL updates for application servers.

---

## 4. DNS (Domain Name System)

=========================================
1. EASY UNDERSTANDING
=========================================
* **What is it?** 
  DNS is the Domain Name System. It acts as the phonebook of the internet, translating domain names (like `google.com`) into routable IP addresses (like `142.250.190.46`).
* **Why was it created?** 
  Humans remember names easily, but computer networks require numerical IP addresses to route packets. DNS bridges this gap.
* **Real-Life Example** 
  Searching "Alice" in your phone's contact list (DNS) to resolve her name to her actual phone number (`+1-555...`) to start a call.

=========================================
2. BUILD INTUITION
=========================================
* **How does it work internally?** 
  ```
  [Browser] --1. Query api.site.com --> [DNS Resolver (ISP)] --8. Returns IP --> [Browser]
                                                  |
                                        +---------+---------+
                                        | 2. Query          | 3. Point to TLD
                                        v                   v
                                   [Root Server]       [TLD Server (.com)]
                                                            ^
                                                  4. Query  | 5. Point to Auth
                                                            |
                                                            v
                                                   [Authoritative Server]
                                                      (Returns IP)
  ```
  DNS uses a hierarchical recursive lookup process:
  1. The client checks its local cache. If it misses, it queries a **DNS Resolver**.
  2. The Resolver queries the **Root Server (`.`)**, which points to the TLD server (e.g., `.com`).
  3. The Resolver queries the **TLD Server**, which points to the domain's **Authoritative Server**.
  4. The Authoritative Server returns the matching IP address.
  5. The Resolver caches the IP based on its **TTL (Time to Live)** and returns it to the browser.
  * **Record Types:** `A` (IPv4), `AAAA` (IPv6), `CNAME` (Alias), `MX` (Mail).
* **Why should a software engineer care?** 
  Knowing how DNS caching and TTL work helps you avoid downtime during server migrations.
* **How is it used in real systems?** 
  Cloud providers (like AWS Route 53) use DNS to route domain calls to regional load balancers based on user location.

=========================================
3. INTERVIEW PREPARATION
=========================================
* **Technical Definition** 
  The Domain Name System (DNS) is a distributed, hierarchical database that translates domain names into logical IP addresses, operating primarily over UDP port 53.
* **30-Second Interview Answer** 
  "DNS is a distributed hierarchical lookup system. When a domain is requested, a recursive resolver queries the Root, TLD, and Authoritative servers in sequence to find the IP address record. DNS uses UDP port 53 for speed, falling back to TCP for large payloads. TTL values manage caching lifetimes. As developers, we configure A records to map domains to IPs and CNAME records to alias domains."
* **Common Follow-up Questions** 
  * Why does DNS run over UDP?
  * What is a CNAME record?
* **Important Points Interviewers Expect** 
  * Drawing the hierarchical lookup diagram.
  * Naming record types (`A`, `AAAA`, `CNAME`).
  * Defining **TTL**.
* **Common Mistakes Students Make** 
  * Thinking DNS is resolved for every API request. (It is cached by the OS).

=========================================
4. QUICK REVISION
=========================================
* **Key Points** 
  * Translates domain names to IP addresses.
  * Hierarchical: Root (`.`), TLD (`.com`), Authoritative.
  * Runs over UDP port 53.
  * Record types: `A` (IPv4), `AAAA` (IPv6), `CNAME` (Alias).
* **One-Line Revision** 
  A distributed phonebook that translates domain names to machine-routable IP addresses.
* **Memory Trick** 
  **DNS** = **D**omain **N**umber **S**earch.

=========================================
5. PROJECT CONNECTION
=========================================
* **React Applications:** React builds initiate DNS resolutions when making Axios calls.
* **Spring Boot Applications:** Resolves connection string hostnames (like `db.yoursite.com`) to database IPs.
* **REST APIs:** API calls map endpoints using DNS records.
* **PostgreSQL:** Listens on host names resolved by the local OS.
* **JWT Authentication:** Not related.
* **WebSocket Systems:** Clients connect to WebSocket endpoints using hostnames resolved by DNS.
* **Docker Deployments:** Docker runs an internal DNS server to map container names to virtual IPs.

---

## 5. TCP Three-Way Handshake

=========================================
1. EASY UNDERSTANDING
=========================================
* **What is it?** 
  The Three-Way Handshake is the process used by TCP to establish a reliable connection between a client and a server before sending any application data.
* **Why was it created?** 
  Since networks are unreliable, both hosts must verify that their upload and download channels are active, and agree on initial sequence numbers (ISNs).
* **Real-Life Example** 
  A telephone check:
  1. Client: "Hello, can you hear me?" (SYN)
  2. Server: "Yes, I can. Can you hear me?" (SYN-ACK)
  3. Client: "Yes, I can hear you too." (ACK)
  Connection established.

=========================================
2. BUILD INTUITION
=========================================
* **How does it work internally?** 
  ```
  Client                                                  Server
    | ---------- SYN (Seq = x) -------------------------> | (SYN-RECEIVED)
    | <--------- SYN-ACK (Seq = y, Ack = x + 1) --------- |
    | ---------- ACK (Ack = y + 1) ---------------------> | (ESTABLISHED)
  (ESTABLISHED)
  ```
  1. **SYN:** Client sends a packet with `SYN` flag set and a random Initial Sequence Number ($x$). (State: `SYN-SENT`).
  2. **SYN-ACK:** Server acknowledges the SYN ($x + 1$) and sends its own sequence number ($y$). (State: `SYN-RECEIVED`).
  3. **ACK:** Client sends an `ACK` packet ($y + 1$). Both enter `ESTABLISHED` state.
  * **SYN Flood:** Attackers send many SYNs but ignore SYN-ACKs, filling the server's buffer. Prevented using **SYN Cookies**, which encode connection info in the sequence number.
* **Why should a software engineer care?** 
  The handshake adds **1 RTT** of latency. Reusing established connections (using Keep-Alive) improves API speed.
* **How is it used in real systems?** 
  Web browsers use persistent connections (HTTP Keep-Alive) to reuse established TCP sockets.

=========================================
3. INTERVIEW PREPARATION
=========================================
* **Technical Definition** 
  The TCP Three-Way Handshake is the connection establishment protocol that synchronizes initial sequence numbers (ISNs) and allocates buffer resources on both client and server nodes prior to data transmission.
* **30-Second Interview Answer** 
  "The three-way handshake establishes a reliable TCP connection. First, the client sends a SYN packet with a random initial sequence number to the server. Second, the server responds with a SYN-ACK packet, acknowledging the client's sequence number and sending its own. Third, the client sends an ACK packet back to confirm. Once complete, both hosts enter the established state, ready to send data."
* **Common Follow-up Questions** 
  * What is a SYN Flood attack?
  * Why is the initial sequence number randomized?
* **Important Points Interviewers Expect** 
  * Packet sequence (**SYN -> SYN-ACK -> ACK**).
  * Explaining sequence synchronization ($x \to x+1$).
* **Common Mistakes Students Make** 
  * Thinking that application data is sent during the first two steps.

=========================================
4. QUICK REVISION
=========================================
* **Key Points** 
  * Establishes reliable TCP connections.
  * Synchronizes sequence numbers ($x$ and $y$).
  * Sequence: SYN -> SYN-ACK -> ACK.
  * Mitigated against SYN Floods via SYN Cookies.
* **One-Line Revision** 
  The three-step synchronization process used to establish a reliable TCP socket connection before data transfer.
* **Memory Trick** 
  **S**ay **S**ay-**A**ck **A**cknowledge (SYN, SYN-ACK, ACK).

=========================================
5. PROJECT CONNECTION
=========================================
* **React Applications:** Browser runs the handshake before sending HTTP requests.
* **Spring Boot Applications:** Tomcat handles incoming handshakes inside the OS socket queue.
* **REST APIs:** Standard API calls require completing the handshake first.
* **PostgreSQL:** HikariCP keeps database connections open to avoid handshake latency.
* **JWT Authentication:** Validation filters operate on requests sent over established channels.
* **WebSocket Systems:** WebSockets establish connections on top of an active TCP handshake.
* **Docker Deployments:** Exposes ports that receive and forward TCP handshake packets.

---

## 6. REST API

=========================================
1. EASY UNDERSTANDING
=========================================
* **What is it?** 
  A REST API is an architectural style for designing APIs. It organizes database records into **Resources** identified by URLs (e.g., `/api/products`), which you view or modify using standard HTTP methods.
* **Why was it created?** 
  To standardize web service communication. REST uses standard HTTP features, making APIs easy to integrate, scale, and cache.
* **Real-Life Example** 
  A library system: `GET /books` retrieves books, `POST /books` adds a book, and `DELETE /books/5` removes book number 5.

=========================================
2. BUILD INTUITION
=========================================
* **How does it work internally?** 
  REST relies on six design constraints:
  1. **Statelessness:** The server stores no client session context. Each request must carry all the data needed to process it.
  2. **Uniform Interface:** Resources are identified by URIs and manipulated using standard HTTP verbs:
     * `GET`: Safe & Idempotent (retrieve data).
     * `POST`: Unsafe & Non-idempotent (create resource).
     * `PUT`: Unsafe & Idempotent (replace/create resource).
     * `PATCH`: Unsafe & Non-idempotent (partial update).
     * `DELETE`: Unsafe & Idempotent (remove resource).
  3. **Client-Server Separation.**
  4. **Cacheability.**
  5. **Layered System.**
  6. **Code on Demand (Optional).**
* **Why should a software engineer care?** 
  Understanding **Idempotency** (executing an operation multiple times produces the same system state as executing it once) prevents duplicate transactions during network retries.
* **How is it used in real systems?** 
  React frontend uses Axios to fetch product JSON lists from a Spring Boot `@RestController` endpoint.

=========================================
3. INTERVIEW PREPARATION
=========================================
* **Technical Definition** 
  Representational State Transfer (REST) is a stateless, client-server web architectural style that exposes resources via URIs and manipulates them using standard HTTP methods.
* **30-Second Interview Answer** 
  "REST is an architectural style for web APIs centered around resources identified by URIs. Its core constraint is statelessness, meaning the server does not store client session data, allowing it to scale horizontal easily. It uses standard HTTP methods: GET to retrieve, POST to create, PUT to replace, and DELETE to remove. GET, PUT, and DELETE are idempotent, ensuring safety during request retries."
* **Common Follow-up Questions** 
  * Difference between PUT and PATCH?
  * What is idempotency?
* **Important Points Interviewers Expect** 
  * Naming constraints like **Statelessness** and **Uniform Interface**.
  * Explaining **Idempotency** for GET, PUT, and DELETE vs. POST.
* **Common Mistakes Students Make** 
  * Thinking that POST is idempotent.

=========================================
4. QUICK REVISION
=========================================
* **Key Points** 
  * Stateless architectural style.
  * Resources identified by URIs.
  * Standard HTTP methods enforce operations.
  * Idempotence prevents duplicate side effects.
* **One-Line Revision** 
  An API architectural style exposing resources via URIs and manipulating them using stateless HTTP methods.
* **Memory Trick** 
  **REST** = **R**esources **E**xposed as **S**tateless **T**ransactions.

=========================================
5. PROJECT CONNECTION
=========================================
* **React Applications:** Calls REST endpoints to fetch data payloads.
* **Spring Boot Applications:** Maps controllers to REST routes using annotations like `@RestController`.
* **REST APIs:** The central communication contract.
* **PostgreSQL:** Provides tables mapped to REST resources via JPA.
* **JWT Authentication:** Stateless JWTs authorize client requests to REST controllers.
* **WebSocket Systems:** REST calls authorize users before upgrading to WebSockets.
* **Docker Deployments:** Deploys API servers in containers exposing REST ports.

---

## 7. JWT Authentication Flow

=========================================
1. EASY UNDERSTANDING
=========================================
* **What is it?** 
  JWT is JSON Web Token. It is a stateless authentication mechanism. Instead of the server storing user session records, the server encodes the user's ID and permissions directly into a signed cryptographic token and hands it to the client.
* **Why was it created?** 
  To support microservices scaling. JWT allows servers to authenticate users statelessly without checking a central session database for every API request.
* **Real-Life Example** 
  A theme park wristband. Once you buy a ticket, the host gives you a signed wristband (JWT) listing your access. Ride operators verify the signature on the wristband; they don't check a central database.

=========================================
2. BUILD INTUITION
=========================================
* **How does it work internally?** 
  * **JWT Structure:** Composed of three parts separated by dots (`.`):
    * **Header:** Hashing algorithm (e.g., `{"alg":"HS256"}`).
    * **Payload:** Contains claims (e.g., user ID, roles, expiration).
    * **Signature:** Cryptographic verification hash: `HMACSHA256(base64(Header) + "." + base64(Payload), SecretKey)`.
  * **Authentication Flow:**
    ```
    React Client                                            Spring Boot Backend
      | ----- POST /login (Credentials) ------------------> |
      |                                                     | [Validates, Generates Signed JWT]
      | <---- Response (JWT Token) ------------------------ |
      | ----- GET /api/data (Header: Bearer JWT) ---------> |
      |                                                     | [Verifies Signature, Extracts Claims]
      | <---- Response (Data) ----------------------------- |
    ```
    1. Client logs in.
    2. Server signs a JWT with its private key and returns it.
    3. Client appends it to subsequent request headers: `Authorization: Bearer <token>`.
    4. Server verifies the signature using its secret key.
  * **Revocation:** Because verification is stateless, a compromised JWT cannot be easily revoked before expiration. Resolved using short token lifetimes and **Refresh Token Rotation**.
* **Why should a software engineer care?** 
  Base64 payloads are readable by anyone. Never store passwords or private details inside a JWT payload.
* **How is it used in real systems?** 
  Spring Security filters parse Bearer tokens and populate security contexts statelessly.

=========================================
3. INTERVIEW PREPARATION
=========================================
* **Technical Definition** 
  A JSON Web Token (JWT) is a compact, URL-safe standard (RFC 7519) that encodes claims as a JSON object signed cryptographically using a secret key or public/private key pair to enable stateless authentication.
* **30-Second Interview Answer** 
  "JWT is a stateless token-based authentication standard. A token is composed of a Base64-encoded Header, Payload, and cryptographic Signature. After login, the server generates and signs the token, returning it to the client. The client includes it in the Authorization header of subsequent API requests. The server validates the signature using its key, authenticating the user without checking a session database, making it highly scalable."
* **Common Follow-up Questions** 
  * LocalStorage vs. HttpOnly Cookie storage?
  * How do you revoke a JWT?
* **Important Points Interviewers Expect** 
  * Naming all three components: **Header, Payload, and Signature**.
  * Emphasizing that JWTs are signed, not encrypted.
* **Common Mistakes Students Make** 
  * Storing passwords or sensitive data in the payload.

=========================================
4. QUICK REVISION
=========================================
* **Key Points** 
  * Stateless authentication standard.
  * Split into Header, Payload, and Signature.
  * Base64-encoded, not encrypted.
  * Signature verified using the server's secret key.
* **One-Line Revision** 
  A self-contained signed token encoding user details to enable stateless client-server authentication.
* **Memory Trick** 
  **JWT** = **J**son **W**rist **T**icket.

=========================================
5. PROJECT CONNECTION
=========================================
* **React Applications:** Stores JWTs, injecting them into Axios headers.
* **Spring Boot Applications:** Implements authentication filters using libraries like `jjwt`.
* **REST APIs:** The primary authorization payload format for microservice APIs.
* **PostgreSQL:** Unburdened by user session database lookups.
* **JWT Authentication:** The core protocol.
* **WebSocket Systems:** Validates token strings during connection upgrades.
* **Docker Deployments:** Configures containers with shared secret keys.

---

## 8. WebSocket

=========================================
1. EASY UNDERSTANDING
=========================================
* **What is it?** 
  WebSocket is a protocol that provides a persistent, two-way (full-duplex) communication channel over a single TCP connection. It allows the server to push real-time updates to the browser instantly.
* **Why was it created?** 
  HTTP is pull-only. While polling works, it adds high header overhead. WebSockets allow low-latency, real-time bi-directional streaming.
* **Real-Life Example** 
  A phone call. Once connected, both you and your friend can speak and listen at the same time, without hanging up and redialing for each sentence.

=========================================
2. BUILD INTUITION
=========================================
* **How does it work internally?** 
  ```
  React Client                                            Spring Boot Backend
    | ----- GET (Upgrade to WebSocket) -----------------> |
    | <---- 101 Switching Protocols ---------------------- |
    |<====== WebSocket Connection (TCP) =================>|
  ```
  1. **Handshake:** Client sends an HTTP request with upgrade headers: `Connection: Upgrade` and `Upgrade: websocket`.
  2. **Upgrade:** Server responds with status code `101 Switching Protocols`.
  3. **Data Transfer:** The connection remains open over TCP, transferring lightweight frames (minimal 2-10 byte headers).
* **Why should a software engineer care?** 
  Because WebSockets are stateful, scaling requires sticky sessions or a shared message broker (like Redis) to route messages across multiple servers.
* **How is it used in real systems?** 
  Real-time stock trading dashboards or chat applications use WebSockets to push price updates or messages instantly.

=========================================
3. INTERVIEW PREPARATION
=========================================
* **Technical Definition** 
  WebSocket is a TCP-based application protocol that provides full-duplex, bi-directional communication channels initiated via an HTTP handshake and upgraded via status code 101.
* **30-Second Interview Answer** 
  "WebSocket is a protocol enabling full-duplex, bi-directional communication over a single TCP connection. It begins with an HTTP upgrade request. The server returns a 101 Switching Protocols response, upgrading the socket. The TCP connection is kept open, allowing both sides to push lightweight frames at any time, avoiding the overhead of HTTP request-response headers."
* **Common Follow-up Questions** 
  * Difference between WebSocket and Server-Sent Events (SSE)?
  * How do you scale WebSockets?
* **Important Points Interviewers Expect** 
  * Explaining the **HTTP Upgrade (101 status code)**.
  * Contrasting **Full-Duplex** vs. HTTP.
  * Explaining scaling challenges.
* **Common Mistakes Students Make** 
  * Thinking WebSockets run on UDP. (They run on TCP).

=========================================
4. QUICK REVISION
=========================================
* **Key Points** 
  * Full-duplex bi-directional communication.
  * Upgrades via HTTP 101 status code.
  * Minimal header overhead (2-10 bytes frames).
  * Stateful TCP connection.
* **One-Line Revision** 
  A protocol providing persistent, low-overhead bi-directional communication over a single TCP connection.
* **Memory Trick** 
  **WebSocket** = Web socket kept open.

=========================================
5. PROJECT CONNECTION
=========================================
* **React Applications:** Uses browser `new WebSocket('ws://...')` APIs.
* **Spring Boot Applications:** Implements `WebSocketConfigurer` to register message brokers.
* **REST APIs:** Works alongside REST; REST handles authorization before upgrade.
* **PostgreSQL:** Uses Listen/Notify commands to push updates to a WebSocket handler.
* **JWT Authentication:** Tokens are validated during the connection handshake.
* **WebSocket Systems:** The core protocol.
* **Docker Deployments:** Configures proxies to support connection upgrade headers.

---

## 9. Cookies vs Sessions

=========================================
1. EASY UNDERSTANDING
=========================================
* **What is it?** 
  Cookies are client-side text files stored in the browser. Sessions are server-side data stores that track user state. They work together: the server creates a session and sends the session ID to the browser in a cookie.
* **Why was it created?** 
  To maintain state across stateless HTTP requests safely.
* **Real-Life Example** 
  A coat check ticket. You hand your coat (Session Data) to the attendant, they give you a ticket (Cookie containing Session ID). When you want your coat back, you present the ticket.

=========================================
2. BUILD INTUITION
=========================================
* **How does it work internally?** 
  * **Cookie:** Server sends a `Set-Cookie` header. The browser automatically stores this text and appends it to subsequent request headers.
    * Flags: `HttpOnly` (blocks JS access/XSS), `Secure` (HTTPS only), `SameSite` (Strict/Lax, blocks CSRF).
  * **Session:** Server generates a Session ID, stores session data in its memory, and returns the ID as a cookie. On subsequent requests, the server uses the ID cookie to load the session data.
* **Why should a software engineer care?** 
  Sessions limit horizontal scaling. If user data is stored in Server A's RAM, requests hitting Server B will fail. You must use a shared cache like Redis to sync session data.
* **How is it used in real systems?** 
  Spring Session coordinates session synchronization across backend clusters using Redis.

=========================================
3. INTERVIEW PREPARATION
=========================================
* **Technical Definition** 
  A Cookie is a client-side key-value storage mechanism managed by the browser. A Session is a server-side state-management system linked to clients via a unique Session ID.
* **30-Second Interview Answer** 
  "Cookies are client-side text files stored in the browser, which are automatically sent with every request to the domain. Sessions are server-side data stores that track user state. They work together: the server creates a session in its memory or database, and sends the session ID to the client in a cookie. On subsequent requests, the server uses the session ID cookie to load the user's data. Cookies are lightweight but limited to 4KB, while sessions are secure but require server resource synchronization to scale."
* **Common Follow-up Questions** 
  * Explain SameSite and HttpOnly flags.
  * How do you scale session storage across server clusters?
* **Important Points Interviewers Expect** 
  * Location of storage (client vs. server).
  * Security flags.
  * Scaling limitations.
* **Common Mistakes Students Make** 
  * Thinking session data is stored in the cookie. (Only the ID is).

=========================================
4. QUICK REVISION
=========================================
* **Key Comparison Table**

| Parameter | Cookie | Session |
| :--- | :--- | :--- |
| **Storage Location** | Client Browser | Server (RAM, Database, Cache) |
| **Data Size** | Limited (4KB) | Virtually unlimited |
| **Scalability** | High (Client-side) | Low (Requires server sync/Redis) |
| **Security** | Vulnerable if unencrypted | Highly secure |

* **One-Line Revision** 
  Cookies are local browser files; sessions are secure server-side records linked by a cookie ID.
* **Memory Trick** 
  **Cookie** = Client. **Session** = Server.

=========================================
5. PROJECT CONNECTION
=========================================
* **React Applications:** Reads non-HttpOnly cookies from `document.cookie`.
* **Spring Boot Applications:** Tomcat creates `HttpSession` states managed by Spring Security.
* **REST APIs:** REST APIs avoid sessions to remain stateless.
* **PostgreSQL:** Stores persistent session tables if configured for database-backed sessions.
* **JWT Authentication:** Storing JWTs in HttpOnly cookies protect them from XSS extraction.
* **WebSocket Systems:** Reads cookies during the connection handshake to authorize users.
* **Docker Deployments:** Deploys Redis container clusters to synchronize session states.

---

## 10. Client-Server Architecture

=========================================
1. EASY UNDERSTANDING
=========================================
* **What is it?** 
  Client-Server Architecture splits tasks between service requesters (Clients like React in your browser) and resource providers (Servers like Spring Boot on a host machine).
* **Why was it created?** 
  To separate concerns, keeping business logic and database access secure on managed servers while offloading user interactions to client devices.
* **Real-Life Example** 
  A restaurant where the customer (Client) reviews the menu and orders, and the kitchen (Server) prepares the food and returns it to the table.

=========================================
2. BUILD INTUITION
=========================================
* **How does it work internally?** 
  * **Client:** Initiates connections by sending requests. Handles user inputs and renders the UI.
  * **Server:** Listens on a port, processes business logic, and queries database systems (PostgreSQL).
  * **N-Tier Architecture:** Splits the server tier into sub-tiers: Presentation Tier (React), Application Tier (Spring Boot), and Data Tier (PostgreSQL).
* **Why should a software engineer care?** 
  Decoupling allows you to update, maintain, and scale the frontend and backend independently.
* **How is it used in real systems?** 
  React is hosted on a CDN (like Vercel) while Spring Boot runs on auto-scaling VM instances behind load balancers.

=========================================
3. INTERVIEW PREPARATION
=========================================
* **Technical Definition** 
  Client-Server Architecture is a distributed application model that splits workloads between service requesters (clients) and centralized resource providers (servers) communicating over network channels.
* **30-Second Interview Answer** 
  "Client-server architecture is a distributed design model. The client initiates requests over a network, and the server processes them, manages database records, and returns responses. This separates concerns, keeping business logic and data secure on the server while keeping the client application lightweight. We scale this architecture using load balancers to distribute client requests across multiple backend instances."
* **Common Follow-up Questions** 
  * Difference between client-server and peer-to-peer (P2P)?
  * What is a Three-Tier Architecture?
* **Important Points Interviewers Expect** 
  * Explaining **Separation of Concerns**.
  * Defining the request-response lifecycle.
* **Common Mistakes Students Make** 
  * Thinking that the client can directly access the database.

=========================================
4. QUICK REVISION
=========================================
* **Key Points** 
  * Distributed workload splitting.
  * Client initiates; Server responds.
  * Separates UI rendering from business logic/data.
  * Scaled using load balancers and CDNs.
* **One-Line Revision** 
  A distributed design model separating user interface requests from centralized server processing.
* **Memory Trick** 
  **Client** = Requesters. **Server** = Providers.

=========================================
5. PROJECT CONNECTION
=========================================
* **React Applications:** Acts as the client application.
* **Spring Boot Applications:** Acts as the application server.
* **REST APIs:** Serves as the communication contract between client and server.
* **PostgreSQL:** Acts as the data storage server.
* **JWT Authentication:** Client sends credentials; server generates tokens.
* **WebSocket Systems:** Establishes bi-directional communication channels.
* **Docker Deployments:** Deploys client Nginx proxies and backend API servers in separate containers.

---

# PART 2 SUMMARY & PLACEMENT PRACTICE

### Beginner Understanding
**HTTP** is the protocol browsers use to request pages, upgraded to **HTTPS** using **SSL/TLS** encryption to protect data. **Client-Server Architecture** separates the browser UI from the server's business logic. **REST APIs** use standard HTTP commands (GET, POST) to update resources. **WebSockets** allow servers to push real-time updates directly to browsers. To manage state, servers use **Cookies** (client-side files), **Sessions** (secure server-side storage linked by session IDs), or **JWTs** (cryptographically signed stateless tokens).

### Interview Understanding
Interviewers check knowledge of HTTP/2 multiplexing, TLS key exchange flows, REST method idempotency, WebSocket upgrades, cookie security flags, session clustering, and the composite parts of a JWT.

### Real Software Engineering Understanding
Production architectures implement SSL termination at gateways, store session cache records in Redis, and manage stateless JWTs with short lifetimes and refresh token rotation.

---

## Placement Practice & Sheets

### Top 5 Interview Questions
1. What is HTTP/2 multiplexing? How does it differ from HTTP/1.1 pipelining?
2. Explain the cryptographic handshake of HTTPS. Detail how symmetric and asymmetric key exchanges are combined.
3. Compare Cookie-based Sessions and stateless JWT Authentication.
4. Draw the structural layout of a JWT token. Explain how the signature is generated and validated.
5. Draw the sequence diagram for a WebSocket connection upgrade.

### Frequently Asked Follow-up Questions
* *What is the difference between GET, PUT, and PATCH?* (Answer: GET retrieves resources safely. PUT replaces a resource completely or creates it if missing, and is idempotent. PATCH performs a partial update, and is non-idempotent).
* *What is Cross-Origin Resource Sharing (CORS)?* (Answer: A browser security mechanism that restricts a web page from making requests to a different domain than the one that served it, managed using CORS response headers).

### 5-Minute Revision Sheet (Cheat Sheet)
* **HTTP/2:** Binary framing, header compression (HPACK), multiplexing.
* **TLS Handshake:** ClientHello -> ServerHello + Cert -> Key Exchange -> Session Key Confirmed.
* **JWT Parts:** Header (alg), Payload (claims), Signature. `Header.Payload.Signature`.
* **Cookie Flags:** HttpOnly (blocks JS), Secure (HTTPS only), SameSite (Strict/Lax, blocks CSRF).
* **WebSocket Upgrade:** Client HTTP Upgrade request -> Server 101 status code -> TCP WebSocket channel.

### 30-Minute Revision Sheet
* **Stateless vs. Stateful Scales:**
  * Stateful sessions require server memory. In server clusters, you must sync sessions using Redis.
  * Stateless JWTs require zero server memory. The server verifies tokens using its secret key, allowing request load balancing across any instance.
* **JWT Storage Security:**
  * Storing in LocalStorage is vulnerable to XSS.
  * Storing in HttpOnly, Secure cookies protects against XSS, but requires SameSite flags to block CSRF.

### Most Important Placement Questions
* *How does a browser request load a profile page securely in a modern React, Spring Boot, and PostgreSQL microservice setup?* 
  1. The React app reads the stored JWT and initiates an Axios `GET /api/v1/profile` request.
  2. The browser executes a DNS lookup, resolves the API gateway IP, and runs a TCP and TLS 1.3 handshake (port 443).
  3. The request, encrypted via TLS, reaches Nginx. Nginx decrypts it (SSL termination) and forwards the plain HTTP request carrying the `Authorization: Bearer <token>` header to the Spring Boot gateway.
  4. Spring Boot's security filter parses the JWT, verifies its signature using a shared key, extracts the user ID, and forwards the request.
  5. The profile service queries PostgreSQL using HikariCP. PostgreSQL returns the rows, which are mapped to a JSON response and returned to React to update the UI.
