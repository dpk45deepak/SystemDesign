# The Essential Guide to Load Balancing Strategies and Techniques

> Video Reference: [The Essential Guide to Load Balancing Strategies and Techniques](https://www.youtube.com/watch?v=mpQfVNcLHGA)

## 1. Asli Problem Kya Hai? (The Core Why)

Soch lo aap Swiggy ki delivery system ko handle kar rahe ho. 
Ek din Mumbai me 10,000 orders ek saath aate hain – peak lunch hour.  
Agar sab requests ek hi server pe direct jaaye, toh:

- **Latency** badh jaayegi, order status update slow ho jayega.
- **Throughput** drop karega, aur 30% orders time pe deliver nahi honge.
- Server crash ka risk badh jayega – ek single point of failure.

Load Balancing solve karta hai: traffic ko multiple servers me evenly distribute karke, **availability** aur **resilience** badhata hai. Agar ek server down ho jata hai, baki servers traffic le lete hain, aur users ko minimal disruption feel hota hai.

## 2. Core Architecture & Mechanisms

### 2.1. Load Balancer Types

| Type | Working | Use-case |
|------|---------|----------|
| **Layer 4 (Transport)** | IP + Port based routing | High throughput, simple health checks (TCP/UDP) |
| **Layer 7 (Application)** | URL, headers, cookies | Content based routing (e.g., `/food`, `/offers`) |
| **Global (DNS)** | Geo‑based routing | IRCTC’s ticket booking across multiple regions |

### 2.2. Routing Algorithms

- **Round Robin** – sequentially send request to each backend. Simple, works when all servers are similar.
- **Least Connections** – send to the server with the fewest active connections. Good when traffic is uneven.
- **Weighted Round Robin / Weighted Least Connections** – servers with higher specs get more traffic.
- **Sticky Sessions** – maintain session affinity using cookies or IP hash. Useful for cart data in e‑commerce.

### 2.3. Health Checks & Graceful Draining

- **Active Health Checks** – load balancer pings `/health` endpoint.
- **Passive Health Checks** – monitor response time/5xx errors.
- **Graceful Draining** – when a server is marked unhealthy, finish existing connections before cutting off new ones.

### 2.4. Advanced Patterns

- **Cache‑Based LB** – CDN edge servers (CloudFront, Akamai) cache static content globally.
- **Gossip Protocol** – for distributed systems to share health status (used in Cassandra, Consul).
- **Read Replica LB** – read queries go to replicas, writes to primary. Improves read throughput.

## 3. Architecture Flow

```mermaid
graph TD
    Client[Client (Browser/App)]
    LB[Load Balancer]
    LB -->|Round Robin| Server1[App Server 1]
    LB -->|Round Robin| Server2[App Server 2]
    LB -->|Round Robin| Server3[App Server 3]
    subgraph DB[Database Layer]
        Primary[Primary DB]
        Replica1[Read Replica 1]
        Replica2[Read Replica 2]
    end
    Server1 -->|Read| Replica1
    Server2 -->|Read| Replica2
    Server3 -->|Read| Replica1
    Server1 -->|Write| Primary
    Server2 -->|Write| Primary
    Server3 -->|Write| Primary
```

## 4. Production Case Study

### Uber’s Global Traffic Management

- **Problem**: Riders from 100+ cities, millions of concurrent trips.
- **Solution**: Uber uses a multi‑tiered load balancing:
  - **DNS Level**: Route users to nearest regional data center.
  - **Edge LB (NGINX)**: Handles HTTPS termination, rate limiting.
  - **Service Mesh (Istio)**: Provides fine‑grained routing, retries, circuit breakers.
  - **Read Replica LB**: Ride history queries go to replicas.
- **Result**: 99.9% uptime, latency < 150 ms even during Delhi’s peak rush.

## 5. Trade-offs (Pros vs Cons)

| Pros | Cons |
|------|------|
| **Scalability** – easily add more servers. | **Complexity** – configuration and monitoring overhead. |
| **Fault tolerance** – traffic shifts automatically on failure. | **Cost** – extra instances and LB appliances increase spend. |
| **Performance** – lower latency & higher throughput. | **Session stickiness** can lead to uneven load if not tuned. |
| **Global reach** – geo‑routing improves user experience. | **Single point of failure** if LB itself fails (mitigated with HA). |
| **Observability** – health checks & metrics per backend. | **Security** – misconfigured LB can expose internal IPs. |

## 6. System Design Interview Cheat Sheet

- **Define the problem scope** – traffic volume, latency goals, regional constraints.
- **Choose LB type** – Layer 4 for high‑speed, Layer 7 for content‑aware routing.
- **Pick routing algorithm** – Round Robin for uniform servers, Weighted Least Connections for heterogeneous resources.
- **Health checks & graceful draining** – ensure zero‑downtime deployments.
- **Consider read/write split** – use read replicas + LB to boost throughput.

---
