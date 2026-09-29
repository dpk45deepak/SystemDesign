# How to Scale Like a Senior Engineer (Servers, DBs, LBs, SPOFs)

> Video Reference: [How to Scale Like a Senior Engineer (Servers, DBs, LBs, SPOFs)](https://www.youtube.com/watch?v=iPaXlFUHJp0)

## 1. Asli Problem Kya Hai? (The Core Why)

Imagine Swiggy ka order‑processing system. 24×7 peak traffic pe 30,000 orders per minute aa rahe hain, 90% orders 2‑3 seconds ke andar deliver honi chahiye. Agar servers ya DBs ek hi node pe depend kare, toh ek choti si failure (power outage, network glitch) se poora order flow ruk sakta hai. Customers ko cancel karna padega, ratings drop, revenue loss – ek SPOF (Single Point Of Failure) se business ka risk badh jaata hai. Isliye scaling ka pehla kaam hai: **high availability** aur **low latency** ko guarantee karna while handling massive load.

## 2. Core Architecture & Mechanisms

### Servers

- **Horizontal Scaling**: Instead of one powerful machine, use multiple cheap instances. Kubernetes ya EC2 auto‑scaling se traffic ke hisaab se pods add / remove hote hain.
- **Statelessness**: Session data ko Redis ya JWT me store karo. Agar koi pod crash ho jaye, koi dusra pod usko handle kar sakta hai.

### Databases

- **Master‑Slave Replication**: Primary node writes accept kare, secondaries read requests serve karte hain. Read traffic 80‑90% hota hai, isliye read replicas se load kaafi reduce hota hai.
- **Sharding**: Customer data ko user ID ke hash se multiple shards me divide karo. Aise large tables pe query latency kam hoti hai.
- **Caching**: Redis/ElastiCache me hot data store karo. 10‑20% read queries ko DB se bypass kar sakte ho.

### Load Balancers

- **Layer‑4 vs Layer‑7**: TCP/L4 LB (Nginx, HAProxy) traffic ko simple round‑robin se distribute kare. HTTP/HTTPS (L7) LB (AWS ELB, CloudFront) path, host ya cookie ke basis pe intelligent routing deta hai.
- **Health Checks**: LB automatically unhealthy instances ko remove kar deta hai, ensuring no traffic goes to a failed node.

### Avoiding SPOFs

- **Multiple Data Centers**: Geo‑distributed clusters se region‑wide outage ka risk kam hota hai. DNS failover (Route 53) se traffic automatically nearest healthy DC pe jata hai.
- **Graceful Degradation**: Agar DB down ho, fallback to cache or limited feature set (e.g., show only menu, not live order status) – user experience degrade ho sakta hai, but system stays alive.
- **Circuit Breaker Pattern**: Service calls fail hone par temporary block karke downstream systems ko protect karo.

## 3. Architecture Flow

```mermaid
graph TD
    A[Users (Swiggy App)] -->|HTTPS| B[API Gateway]
    B -->|Round Robin| C[Load Balancer]
    C -->|LB| D[App Server Cluster]
    D -->|Cache| E[Redis]
    D -->|Read| F[Read Replicas]
    D -->|Write| G[Master DB]
    E -->|Fallback| F
    F -->|Read| G
    G -->|Replication| H[Read Replica 2]
    H -->|Read| F
    subgraph "High Availability"
        I[Health Check] --> C
    end
```

## 4. Production Case Study

**Uber**:  
- Uses **microservices** deployed on Kubernetes across multiple AZs.  
- **Gossip Protocol** se cluster state keep hoti hai; every node knows health of others.  
- **Read‑only replicas** (up to 10) per region handle surge during peak hours.  
- **Elastic Load Balancer** with weighted routing based on real‑time latency metrics.  
- **Multi‑region failover**: if one region’s AZ goes down, traffic rerouted to another region’s cluster with minimal latency impact.

## 5. Trade‑offs (Pros vs Cons)

| Pros | Cons |
|------|------|
| **High Availability** – no single point of failure, graceful degradation. | **Complexity** – multiple components, monitoring, and coordination overhead. |
| **Scalability** – horizontal scaling allows handling spikes. | **Cost** – more instances, replicas, and data transfer. |
| **Performance** – read replicas and caching reduce latency. | **Consistency Issues** – eventual consistency may affect user experience. |
| **Resilience** – automatic failover, circuit breakers protect downstream services. | **Operational Overhead** – need for robust CI/CD, auto‑scaling policies. |
| **Flexibility** – can add or remove services independently. | **Latency** – additional hops (LB, cache) can add microseconds of delay. |

## 6. System Design Interview Cheat Sheet

- **Start with core problem**: identify latency, throughput, availability requirements.
- **Decouple components**: make services stateless, use cache, read replicas.
- **Choose right LB**: L4 for simple traffic, L7 for advanced routing.
- **Avoid SPOFs**: use multi‑region, health checks, circuit breakers.
- **Plan for failure**: graceful degradation, failover strategies, monitoring + alerts.

---
