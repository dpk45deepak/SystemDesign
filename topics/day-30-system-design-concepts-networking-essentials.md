# System Design Concepts: Networking Essentials

> Video Reference: [System Design Concepts: Networking Essentials](https://www.youtube.com/watch?v=RMu6VAfew88)

## 1. Asli Problem Kya Hai? (The Core Why)

Soch lo ek swiggy order place karne ki situation. Har din lakhon orders aate hain. Agar network layer weak ho, toh:

- **Latency** badh jati hai – user ko order confirm hone mein seconds lagte hain, aur competitive market mein time ka matlab paisa hota hai.
- **Throughput** kam ho jata hai – ek samay mein sirf thode hi requests process ho pate hain, jis se server overload ho jata hai.
- **Reliability** issue hoti hai – packets drop ho sakte hain, connection drop ho sakta hai, aur customers ko error dikhai de sakta hai.

Agar yeh problem solve na ki jaye, toh customer churn, brand damage aur revenue loss hota hai. Isi liye networking fundamentals pe dhyan dena zaroori hai.

## 2. Core Architecture & Mechanisms

### 1️⃣ DNS (Domain Name System)
- **Role:** Domain name ko IP address me convert karta hai. Jaise IRCTC ki website ka URL `www.irctc.co.in` ko `172.31.45.23` me translate karta hai.
- **Caching:** Local DNS cache se repeated lookups se latency reduce hoti hai.

### 2️⃣ Load Balancer
- **Round‑Robin, Least‑Connection, IP‑Hash** – traffic ko multiple backend servers me distribute karta hai.
- **Health Checks:** Regularly backend health check karta hai; agar server down ho jaye toh traffic ko automatically redirect karta hai.
- **Example:** Swiggy ke frontend servers load balancer ke peeche hote hain, jo orders ko equally distribute karte hain.

### 3️⃣ CDN (Content Delivery Network)
- **Edge Servers:** Static assets (images, CSS, JS) globally distributed edge locations par store hote hain.
- **Latency Reduction:** User ke nearest edge se content serve hota hai, jaise Paytm app ke static files India ke regionally distributed servers se load hoti hain.

### 4️⃣ TCP vs UDP
- **TCP (Transmission Control Protocol):** Reliable, ordered delivery. Use hota hai payment gateway communication (e.g., Zerodha’s trade order) ke liye.
- **UDP (User Datagram Protocol):** Fast, no guarantee of delivery. Real‑time services like gaming or VoIP (e.g., Ola’s live driver‑passenger chat) use UDP.

### 5️⃣ NAT (Network Address Translation)
- **Private vs Public IPs:** Internal servers ke private IPs ko public IP se translate karta hai. AWS VPC ke NAT gateway ka example.

### 6️⃣ Consistency & Availability
- **CAP Theorem:** Network partitions (p) ke time pe system ya consistency ya availability sacrifice karega. Example: IRCTC seat booking system must prioritize consistency (no double booking), so it may sacrifice availability temporarily during a partition.

### 7️⃣ Gossip Protocol
- **Purpose:** Distributed systems me state spread karna. Example: Cassandra’s gossip for node health status.

## 3. Architecture Flow

```mermaid
graph TD
    A[Client (Browser/App)] -->|DNS| B[Recursive DNS Resolver]
    B --> C[Authoritative DNS Server]
    C --> D[Load Balancer (AWS ELB)]
    D --> E[Web Server 1]
    D --> F[Web Server 2]
    E --> G[Database Cluster]
    F --> G
    G --> H[Read Replica 1]
    G --> I[Read Replica 2]
    subgraph Edge
        J[CDN Edge Node] -->|Cache| G
    end
```

## 4. Production Case Study

### Uber’s Real‑Time Ride Matching

- **Problem:** Real‑time matching of millions of riders and drivers across India.
- **Solution:**  
  - **UDP** over **QUIC** for low‑latency location updates.  
  - **Load Balancer** (Google Cloud LB) distributes traffic to stateless microservices.  
  - **Redis** as an in‑memory store for quick geospatial queries.  
  - **Consistent Hashing** to map users to specific nodes, reducing cache miss.  
- **Result:** Latency < 200 ms for 99.9 % of requests, even during peak festivals.

### WhatsApp’s End‑to‑End Encryption

- **Problem:** Securely deliver messages globally with minimal delay.
- **Solution:**  
  - **TCP** for reliable message delivery, with **TLS** for encryption.  
  - **CDN** to cache media files for faster delivery.  
  - **Gossip Protocol** within servers to sync metadata.  
- **Result:** 0.5 s average delivery time for text messages, 1 s for media, while maintaining 99.99 % uptime.

## 5. Trade-offs (Pros vs Cons)

| Pros | Cons |
|------|------|
| **Load Balancer** ensures high availability and fault tolerance. | Extra hop may increase latency slightly. |
| **CDN** reduces round‑trip time for static assets. | Additional cost and complexity in cache invalidation. |
| **TCP** guarantees reliable delivery. | Higher overhead, slower compared to UDP. |
| **UDP** provides low latency for real‑time data. | No delivery guarantee, may need application‑level ACKs. |
| **Gossip Protocol** scales well for state dissemination. | Eventual consistency may lead to stale reads. |
| **Consistent Hashing** balances load with minimal re‑hashing. | Requires careful key distribution to avoid hotspots. |

## 6. System Design Interview Cheat Sheet

- **DNS, Load Balancer, CDN**: Always ask about caching, failure handling, and geographic distribution.
- **TCP vs UDP**: Clarify use‑case (reliable vs low‑latency) and trade‑offs.
- **Latency vs Throughput**: Explain how to measure and optimize both.
- **CAP Theorem**: Discuss consistency vs availability during network partitions.
- **Gossip Protocol**: Mention its role in distributed systems for state sync and fault detection.
