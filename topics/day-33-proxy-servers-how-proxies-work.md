# Proxy Servers: How Proxies Work

> Video Reference: [Proxy Servers: How Proxies Work](https://www.youtube.com/watch?v=sYhKiPzGPYc)

## 1. Asli Problem Kya Hai? (The Core Why)

Imagine Swiggy’s order system during a big sale.  
Every user’s request (GET `/menu`, POST `/order`, etc.) hits the public API gateway.  
If we let every request go directly to the microservice that fetches restaurant data,  
we quickly hit **rate limits**, **latency spikes**, and **service crashes**.  

- **Rate Limiting**: 1 lakh orders in 10 seconds → 10k req/s → backend can’t keep up.  
- **Security & Privacy**: Direct client access means every microservice sees raw client IPs.  
- **Caching & Load Balancing**: Repeating same menu fetches waste compute.  

If we don’t solve this, Swiggy’s UX degrades, orders fail, and brand trust erodes.  
Proxy servers sit in the middle to handle these problems.

## 2. Core Architecture & Mechanisms

### 2.1 What Is a Proxy?

A **proxy** is a server that receives client requests, possibly transforms them, and forwards them to the actual destination.  
It can be **transparent**, **reverse**, or **forward** depending on where it sits.

- **Forward Proxy**: Client → Proxy → Internet (used in corporate networks).  
- **Reverse Proxy**: Client → Proxy → Backend services (our focus).  
- **Transparent Proxy**: No client awareness, just intercepts traffic.

### 2.2 Key Functions of a Reverse Proxy

| Function | Why It Matters | Example |
|----------|----------------|---------|
| **Load Balancing** | Distributes traffic across multiple service instances to improve throughput. | Swiggy’s menu service behind Nginx LB. |
| **Caching** | Stores frequent responses to reduce latency and backend load. | Nginx caches restaurant menus for 60s. |
| **Rate Limiting & Throttling** | Prevents spikes from overwhelming services. | API Gateway limits 100 req/s per user. |
| **SSL/TLS Termination** | Offloads encryption work from backend. | HTTPS termination at CloudFront. |
| **Authentication & Authorization** | Centralises security checks. | Auth0 token validation at API Gateway. |
| **Observability** | Aggregates metrics, logs, tracing. | Prometheus scrape from Envoy. |

### 2.3 Typical Technology Stack

- **Nginx / HAProxy**: Classic L7/L4 load balancers.  
- **Envoy**: Modern service mesh proxy, supports gRPC, mTLS, retries.  
- **AWS API Gateway / Azure API Management**: Managed reverse proxies.  
- **Istio / Linkerd**: Service mesh with built‑in proxies.

### 2.4 How Requests Flow

1. **Client** → **Reverse Proxy** (e.g., Envoy).  
2. Proxy checks **rate limits** and **auth**.  
3. If **cache hit**, serve from memory.  
4. Else, **forward** to the appropriate backend instance.  
5. Backend responds → **Proxy** may **rewrite** headers, **retry** on failure, **log**.  
6. Response goes back to **Client**.

## 3. Architecture Flow

```mermaid
graph TD
  Client[Client App]
  APIGW[API Gateway (Nginx/Envoy)]
  Cache[Cache (Redis/Memory)]
  Auth[Auth Service]
  LB[Load Balancer]
  Backend1[Order Service 1]
  Backend2[Order Service 2]
  DB[(Database)]

  Client -->|HTTPS| APIGW
  APIGW -->|Auth Check| Auth
  Auth -->|Token Valid| APIGW
  APIGW -->|Cache Lookup| Cache
  Cache -->|Hit| APIGW
  Cache -->|Miss| LB
  LB -->|Round Robin| Backend1
  LB -->|Round Robin| Backend2
  Backend1 -->|Read/Write| DB
  Backend2 -->|Read/Write| DB
  Backend1 -->|Response| APIGW
  Backend2 -->|Response| APIGW
  APIGW -->|HTTPS| Client
```

## 4. Production Case Study

### Uber’s Use of Proxies

Uber runs a massive microservice ecosystem (drivers, riders, pricing, fraud).  
They deploy **Envoy** as a sidecar for every service instance. Key points:

- **Service Mesh**: Envoy handles intra‑cluster traffic, providing retries, circuit breaking, and mTLS.  
- **Observability**: Envoy injects OpenTelemetry traces, enabling Uber to see latency per hop.  
- **Zero‑Downtime Deploys**: Using Envoy’s weighted routing, they shift traffic gradually during releases.  
- **Global Edge**: CloudFront + Nginx at edge caches static assets (maps, icons) to cut latency.

Result: Uber can scale to millions of requests per second while maintaining SLA of < 200ms for core flows.

## 5. Trade‑offs (Pros vs Cons)

| Pros | Cons |
|------|------|
| **Scalability**: Distributes load, increases throughput. | **Single Point of Failure** if not replicated. |
| **Security**: Central auth, TLS termination, IP whitelisting. | **Added Latency** due to extra hop. |
| **Observability**: Unified metrics, logs, tracing. | **Complexity**: Configuration, debugging. |
| **Caching**: Reduces backend load, speeds up responses. | **Cache Staleness**: Requires eviction strategy. |
| **Rate Limiting**: Protects services from spikes. | **Cost**: Extra server resources, cloud charges. |

## 6. System Design Interview Cheat Sheet

- **Reverse Proxy** vs **Forward Proxy** – know the difference and typical use cases.  
- **Key Functions**: Load balancing, caching, auth, rate limiting, TLS termination, observability.  
- **Popular Implementations**: Nginx, HAProxy, Envoy, Istio, AWS API Gateway.  
- **Common Patterns**: Circuit breaker, retries, timeout, weighted routing.  
- **Trade‑offs**: Extra hop adds latency but gives scalability & security; ensure high availability of proxies.
