# System Design Interview: Mastering Databases

> Video Reference: [System Design Interview: Mastering Databases](https://www.youtube.com/watch?v=P-IY5BEl6Y4)

## 1. Asli Problem Kya Hai? (The Core Why)

Socha karo ek **Swiggy** order ka flow: user place karega order, kitchen ko notification milega, delivery boy ko location update milega, payment gateway se confirmation aayega – sabhi steps ek hi database se data lete hain. Agar database slow ho jaye toh user ko 2-3 minutes ka wait karna padega, aur *order cancellations* ka rate badh jayega.  
High traffic Indian services jaise **IRCTC** (train booking) or **Zerodha** (stock trading) mein, *latency* aur *throughput* critical hai. Agar database design sahi na ho, toh:

- **Availability** drop ho sakti hai (server down, no orders processed)
- **Consistency** issue ho sakta hai (duplicate booking, wrong stock price)
- **Scalability** limit ho jayegi (traffic spike pe crash)

Isliye interviewers ye question puchte hain: *"How would you design the database layer for a high‑traffic service?"*

## 2. Core Architecture & Mechanisms

### 2.1 Data Modeling & Schema Design  
- **Normalize** data for transactional consistency (orders, users, payments).  
- Use **hybrid** approach: relational tables for ACID ops + NoSQL for high‑read, semi‑structured data (e.g., order history in JSON).

### 2.2 Replication & Read Replica  
- **Primary–Replica** pattern: write to primary, read from replicas.  
- *Read Replica* reduces load on primary, improves read latency.  
- *Gossip Protocol* helps replicas sync state efficiently.

### 2.3 Partitioning & Sharding  
- **Horizontal sharding**: split rows across nodes by key (userID, orderID).  
- **Range sharding**: useful for time‑series data (order logs).  
- Sharding reduces contention and spreads storage.

### 2.4 Consistency Models  
- **Strong Consistency**: ACID, good for payments.  
- **Eventual Consistency**: acceptable for order history, cart items.  
- Choose *CAP trade‑off* based on feature importance.

### 2.5 Caching & CDN  
- **Redis/Memcached** for hot data (user session, cart).  
- **CDN** for static assets (menu images).  
- Cache‑invalidation strategy (time‑to‑live + write‑through).

## 3. Architecture Flow

```mermaid
graph TD
    A[User Request] --> B{API Gateway}
    B --> C[Auth Service]
    C --> D[Order Service]
    D --> E[Order DB (Primary)]
    E -->|Read| F[Read Replica 1]
    E -->|Read| G[Read Replica 2]
    D --> H[Cache (Redis)]
    D --> I[Payment Gateway]
    I --> J[Payment DB]
    D --> K[Notification Service]
    K --> L[Delivery Boy App]
```

## 4. Production Case Study

**Zerodha’s Kite Platform**  
- Uses **PostgreSQL** for transactional data (orders, positions).  
- **Cassandra** for real‑time market feeds (high write throughput).  
- **Redis** for session and leaderboard caching.  
- **Read Replicas** spread across Mumbai, Delhi, and Bangalore to keep latency < 50 ms.  
- **Kafka** as an event bus to sync between services, ensuring eventual consistency.

Result: 30‑fold increase in order processing speed, 99.99% uptime during peak trading hours.

## 5. Trade‑offs (Pros vs Cons)

| Pros | Cons |
|------|------|
| **Scalability** – sharding + replicas handle millions of requests. | **Complexity** – managing partitions, failover, and consistency is hard. |
| **High Availability** – replicas keep service alive during node failure. | **Cost** – extra nodes + replication overhead. |
| **Low Latency** – caching and read replicas reduce response time. | **Stale Reads** – eventual consistency can show outdated data. |
| **Flexibility** – mix of SQL & NoSQL for different workloads. | **Operational Overhead** – monitoring, backup, and disaster recovery. |

## 6. System Design Interview Cheat Sheet

- **Start with the problem**: traffic, latency, consistency, scalability.  
- **Choose the right database**: relational for ACID, NoSQL for high‑write/scale.  
- **Apply replication**: primary‑replica for reads, use read replicas strategically.  
- **Shard wisely**: key‑based sharding for even distribution, range sharding for time‑series.  
- **Cache critical data**: Redis/Memcached + CDN for static content, remember cache invalidation.

---
