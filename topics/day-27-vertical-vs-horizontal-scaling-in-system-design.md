# Vertical vs Horizontal Scaling in System Design

> Video Reference: [Vertical vs Horizontal Scaling in System Design](https://www.youtube.com/watch?v=1v687z1rhNA)

## 1. Asli Problem Kya Hai? (The Core Why)

Soch lo ki **Swiggy** ka delivery engine ek din me 3 lakh orders handle kare.  
Agar pehle se 50 servers ek saath kaam kar rahe hain aur ek din traffic 3X ho jata hai, to kya hota?  

- **Latency badh jaati** – users ko order place karne me 5‑10 second lagne lage.
- **Throughput low ho jata** – server per request count kam ho jata, system crash hone lagta.
- **Availability issue** – ek server down ho jaye to uske users ke liye poora service down ho sakta.

Yeh sab issues ka root cause hota hai **scaling** ka na hona – ya to *vertical* (existing server ko upgrade karna) ya *horizontal* (naye servers add karna). Agar isko ignore kiya, to user experience degrade hoti hai, revenue loss hota, aur brand damage hota.

## 2. Core Architecture & Mechanisms

### Vertical Scaling (Scale‑Up)

- **Ek hi machine ko** zyada CPU, RAM, SSD se upgrade karna.  
- *Pros*: Simpler deployment, codebase same rehta.  
- *Cons*: **Cost** high, **capacity ceiling** (hardware limits), **downtime** during upgrade.

### Horizontal Scaling (Scale‑Out)

- **Multiple identical machines** add karna, load balancer ke through requests distribute karna.  
- *Pros*: Linear performance increase, high availability, easy to add capacity.  
- *Cons*: Need for **statelessness**, **data consistency** challenges, **network overhead**.

#### Key Concepts

- **Load Balancer**: Traffic ko evenly split karta hai across servers.  
- **Statelessness**: Application ko session data external store (Redis, DynamoDB) me rakhna padta hai.  
- **Consistent hashing**: Data partitioning ko balance karne ke liye use hota hai.  
- **Read Replicas**: Read-heavy workloads ke liye secondary DB copies.  
- **Gossip Protocol**: Cluster nodes ko health status share karne ke liye.  
- **Latency vs Throughput**: Vertical scaling se latency kam ho sakti, throughput limited. Horizontal scaling se throughput badhta, latency thoda increase ho sakta (network hops).

## 3. Architecture Flow

```mermaid
graph TD
    A[Client] -->|HTTPS| B[Load Balancer]
    B --> C{Server Pool}
    C -->|Request 1| D[App Server 1]
    C -->|Request 2| E[App Server 2]
    C -->|Request 3| F[App Server 3]
    D --> G[Cache (Redis)]
    E --> G
    F --> G
    G --> H[Primary DB]
    H --> I[Read Replicas]
    G --> I
    I --> H
```

*Explanation*:  
- Clients hit **Load Balancer**.  
- LB forwards requests to one of the **App Servers** (stateless).  
- App Server talks to **Cache** or **DB**.  
- **Read Replicas** handle read traffic, reducing load on primary.

## 4. Production Case Study

**Swiggy (Delivery Platform)**  
- Uses a **microservice architecture** with hundreds of services.  
- Each service runs in **Docker containers** orchestrated by **Kubernetes**.  
- For high‑traffic periods (festival season), they **scale out** horizontally by adding more pod replicas.  
- Load is distributed by **Envoy** (service mesh) acting as a sidecar proxy.  
- **Read‑heavy services** (menu catalog) use **Elasticsearch** with multiple shards (horizontal scaling).  
- **Cache** layer (Redis) is also horizontally sharded across multiple nodes.  
- Result: Swiggy handles > 5 lakh orders per day with < 200 ms latency.

## 5. Trade‑offs (Pros vs Cons)

| Pros (Vertical) | Cons (Vertical) |
|-----------------|-----------------|
| Simple deployment, single point of control | Limited by hardware, expensive |
| No need for stateless design | Downtime during upgrade |
| Lower network overhead | Scalability ceiling |

| Pros (Horizontal) | Cons (Horizontal) |
|-------------------|-------------------|
| Linear performance, high availability | Requires statelessness & distributed data |
| Zero downtime scaling | Added network hops increase latency |
| Easier to add capacity | More complex monitoring, consistency |
| Cost-effective at scale (commodity servers) | Load balancer and inter-node traffic cost |

## 6. System Design Interview Cheat Sheet

- **Define the problem**: traffic spikes, latency, throughput, consistency.
- **Vertical scaling**: upgrade CPU/RAM, cost, capacity limits.
- **Horizontal scaling**: add nodes, load balancer, stateless design.
- **Key trade‑offs**: latency vs throughput, consistency vs availability.
- **Real‑world example**: Swiggy’s microservices + Kubernetes + cache + replicas.
