# Stateful vs Stateless Architectures Explained

> Video Reference: [Stateful vs Stateless Architectures Explained](https://www.youtube.com/watch?v=20tpk8A_xa0)

## 1. Asli Problem Kya Hai? (The Core Why)

Imagine Swiggy’s delivery system on a peak evening. Every order needs to be assigned to a rider, tracked, and updated in real‑time. Agar hum har request ko ek alag stateless server pe handle karein, toh har request ko fresh context (user cart, rider location, payment status) fetch karna padega from database or cache. Ye latency increase karta hai, throughput drop karta hai, aur scaling bhi tricky hota hai.  

If we keep everything stateless, we lose the ability to keep session data in memory, leading to repeated DB calls, higher network traffic, and inconsistent user experience. On the other side, if we go fully stateful (each request handled by a dedicated server that keeps all state), we hit problems of **availability** (a single node failure kills the session), **scalability** (you need as many servers as sessions), and **load balancing** (hard to route to the right node).  

So the core problem is: **How to keep fast, consistent, and highly available user sessions while being able to scale horizontally?**

## 2. Core Architecture & Mechanisms

### Stateless Servers
- **Definition**: Each request is independent; no session data is stored on the server.
- **Mechanism**: Use external stores (Redis, DynamoDB) or JWT tokens to carry state.
- **Pros**: Easy to scale, simple load balancing, high fault tolerance.

### Stateful Servers
- **Definition**: Server keeps session context in memory or local storage.
- **Mechanism**: Sticky sessions, in‑process cache, or local database.
- **Pros**: Low latency for session data, no external fetch.

### Hybrid Approach
- **Sticky Sessions + External Cache**: Load balancer directs requests to the same server (via cookies or session ID), but critical data is still fetched from a fast cache.
- **Gossip Protocol**: Servers share state changes amongst themselves to keep eventual consistency.
- **Read Replica**: For read‑heavy workloads, replicas reduce load on primary.

### Key Concepts in Hinglish
- **Latency**: Time lag between request and response.  
- **Throughput**: Number of requests handled per second.  
- **Consistency**: All nodes see same data at same time (strong vs eventual).  
- **Availability**: System keeps working even if parts fail.  
- **Load Balancer**: Distributes traffic evenly, can do session stickiness.

## 3. Architecture Flow

```mermaid
graph TD
    A[Client (Browser/Phone)] --> B[Load Balancer]
    B --> C1[Stateless Service 1]
    B --> C2[Stateless Service 2]
    B --> C3[Stateless Service 3]
    C1 --> D[Redis (Session Store)]
    C2 --> D
    C3 --> D
    D --> E[Database (PostgreSQL/MySQL)]
    B --> F[Stateful Service (Sticky)]
    F --> G[Local Cache (In‑process)]
    G --> H[Database]
```

- Client hits **Load Balancer**.  
- For stateless flow, requests go to any **Stateless Service** which fetches session from **Redis**.  
- If session data is critical (like active ride), **Stateful Service** (with sticky session) keeps data in **Local Cache** for instant access.  
- All services eventually sync with **Database** for persistence.

## 4. Production Case Study

**Zomato** uses a hybrid model.  
- **Stateless API layer**: Handles user authentication, menu fetch, and order placement.  
- **Stateful Order Service**: Keeps active order state (payment status, rider ETA) in memory for sub‑second response.  
- **Redis Cluster**: Stores session tokens and quick lookups.  
- **Read Replicas**: For menu and restaurant data to boost read throughput.  

When a rider updates ETA, the stateful service updates Redis and pushes the change via **WebSocket** to the client, ensuring real‑time updates without hitting the DB again.

## 5. Trade-offs (Pros vs Cons)

| Pros | Cons |
|------|------|
| Stateless: Easy horizontal scaling, simple load balancing, high fault tolerance | Stateless: Extra latency for session fetch, higher DB traffic, complex consistency management |
| Stateful: Low latency for session data, no external fetch, instant context | Stateful: Harder to scale, single point of failure, sticky session routing complexity |
| Hybrid: Balances speed and scalability, can use read replicas | Hybrid: More moving parts, higher operational complexity, potential consistency lag |

## 6. System Design Interview Cheat Sheet

- **Define the problem**: Is session data critical? High traffic? Need real‑time updates?
- **Choose stateless vs stateful**: Use stateless for pure API calls, stateful for active sessions (orders, rides).
- **Use external cache**: Redis or Memcached for session tokens and quick lookups.
- **Sticky sessions**: Only when local in‑memory state is needed; otherwise avoid.
- **Consistency model**: Strong consistency for payments, eventual for menus/ratings.

---
