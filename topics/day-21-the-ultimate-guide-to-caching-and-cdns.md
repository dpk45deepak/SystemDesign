# The Ultimate Guide to Caching and CDNs

> Video Reference: [The Ultimate Guide to Caching and CDNs](https://www.youtube.com/watch?v=RCdAGvtTYI0)

## 1. Asli Problem Kya Hai? (The Core Why)

Imagine Swiggy ke app pe ek menu page. Har user click karta hai “See all restaurants” – ye ek **GET** request hai. Agar har request pe backend ko database se 200 restaurants fetch karne padte hain, toh latency badh jaata hai, server load badh jaata hai, aur traffic peak time (e.g., 8‑10 pm) me app crash ho sakta hai.  

**Problem**: High read traffic + slow DB queries → high latency + low throughput.  

**Dikkat**:  
- Users ko 3‑4 seconds lagna, unka order cancel ho sakta.  
- Backend cost badhegi, scaling ki jarurat.  
- Consistency issues – data stale ho sakta.

Caching + CDNs ka main aim: **"Speed up read path"** by storing hot data close to user, reduce DB hits, and lower latency.

---

## 2. Core Architecture & Mechanisms

### 2.1 Caching Basics

- **Cache**: In‑memory store (Redis, Memcached) ya local RAM.  
- **Cache Miss** → fetch from origin, store in cache, return to user.  
- **Cache Hit** → directly serve from cache, zero DB round‑trip.  

### 2.2 Types of Caches

| Level | Example | Use‑Case |
|-------|---------|----------|
| **Edge Cache** (CDN) | CloudFront, Akamai | Static assets, images, JS/CSS |
| **Reverse Proxy Cache** | Varnish, Nginx | API responses, dynamic pages |
| **Application Cache** | Redis, Memcached | Session data, query results |

### 2.3 Cache Invalidation Strategies

1. **Time‑to‑Live (TTL)** – auto‑expire after X seconds.  
2. **Write‑through** – update cache when DB updates.  
3. **Cache‑aside (Lazy Loading)** – read‑only, load on miss.  
4. **Event‑driven** – publish‑subscribe (e.g., Redis Pub/Sub) to notify cache to evict.

### 2.4 CDN (Content Delivery Network)

- **Edge servers** distributed globally; nearest to user serves content.  
- **Cache-Control** headers decide how long CDN should keep content.  
- **Stale‑while‑revalidate**: serve stale content while fetching fresh one.  
- **Cache hit ratio** = (hits / total requests) × 100.  

### 2.5 Consistency vs Availability

- **Strong Consistency**: always latest data (hard with CDN).  
- **Eventual Consistency**: may serve slightly stale data (acceptable for menu lists).  
- Use **Cache‑Aside** + **TTL** for eventual consistency; keep critical data in DB.

### 2.6 Load Balancing & Read Replicas

- **Read Replicas**: offload read traffic from master DB.  
- **Load Balancer**: distributes requests to replicas or cache nodes.  
- Combine with CDN to push reads even further away from origin.

---

## 3. Architecture Flow

```mermaid
graph TD
    A[User] -->|HTTPS GET| B[Load Balancer]
    B -->|Check Cache| C[Reverse Proxy Cache (Varnish)]
    C -->|Cache Hit| D[Serve Cached Response]
    C -->|Cache Miss| E[API Gateway]
    E -->|Read from DB| F[Read Replica]
    F -->|Data| G[API Response]
    G -->|Store in Cache| C
    G -->|Return to User| D
    subgraph CDN
        H[Edge Server] -->|Cache-Control| G
    end
```

---

## 4. Production Case Study

**Zerodha (Trading Platform)**  
- **Problem**: Real‑time stock quotes to millions of users with sub‑100 ms latency.  
- **Solution**:  
  - **Edge CDN** (Akamai) caches static chart assets and lightweight APIs.  
  - **Redis Cluster** (in‑memory) holds the latest tick data for 10 k symbols.  
  - **Cache‑Aside**: when market data API updates, Zerodha pushes a message to Redis Pub/Sub; all cache nodes invalidate relevant keys.  
  - **Read Replicas**: heavy analytical queries run on replicas, keeping the master for writes.  
- **Result**: 70% reduction in backend load, latency dropped from 200 ms to 30 ms, cost saved by avoiding 3× database instances.

---

## 5. Trade-offs (Pros vs Cons)

| Pros | Cons |
|------|------|
| **Lower latency** – data served close to user. | **Stale data risk** – eventual consistency can show outdated info. |
| **Reduced backend load** – fewer DB hits. | **Cache invalidation complexity** – must coordinate updates. |
| **Scalable read traffic** – CDNs handle spikes. | **Extra cost** – CDN subscriptions, in‑memory stores. |
| **Improved user experience** – faster page loads. | **Cache miss penalty** – first request still slow. |
| **Better bandwidth usage** – static assets cached. | **Consistency trade‑off** – may need additional mechanisms for critical data. |

---

## 6. System Design Interview Cheat Sheet

- **Cache hierarchy**: CDN (edge) → Reverse Proxy → Application Cache.  
- **Invalidate on write**: use publish‑subscribe or write‑through pattern.  
- **TTL tuning**: balance freshness vs hit ratio; use `Cache‑Control: max-age`.  
- **Read‑only workloads**: favor read replicas + cache to offload DB.  
- **Consistency**: explain strong vs eventual, and when each is acceptable.
