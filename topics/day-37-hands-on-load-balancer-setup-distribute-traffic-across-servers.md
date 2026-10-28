# Hands‑On Load Balancer Setup: Distribute Traffic Across Servers

> Video Reference: [Hands‑On Load Balancer Setup: Distribute Traffic Across Servers](https://www.youtube.com/watch?v=CyWTPmlkOzU)

## 1. Asli Problem Kya Hai? (The Core Why)

Imagine **Swiggy** ka order‑taking system jab ek din ke peak hour me 10,000 orders aate hain. Agar sirf ek server handle kare, toh latency badhegi, time‑outs honge aur customers ko “Sorry, server down” dikhai dega. Ye **availability** ko directly affect karta hai. Agar traffic evenly distribute na ho, toh kuch servers over‑loaded honge while dusre idle rahenge – ye **throughput** waste karta hai. Load balancer is problem ka solution hai: traffic ko multiple servers me evenly split karke **latency** kam karta hai aur **availability** badhata hai.

## 2. Core Architecture & Mechanisms

Load balancer ek traffic‑controller hota hai jo incoming HTTP/HTTPS requests ko backend servers ke pool me forward karta hai. Key mechanisms:

### 2.1 Load‑Balancing Algorithms
- **Round Robin** – requests sequentially rotate across servers. Simple, but ignores server load.
- **Least Connections** – forwards to server with fewest active connections, good for variable request sizes.
- **IP Hash** – same client IP always goes to same server, useful for session persistence without sticky sessions.

### 2.2 Health Checks
Backend servers ko regular ping kiya jata hai (HTTP GET /health) to ensure they are alive. If a server fails health check, load balancer stops sending traffic to it till it recovers. This keeps **consistency** and **availability** high.

### 2.3 Session Persistence (Sticky Sessions)
For e‑commerce or banking, user session data might be stored in memory of a particular server. Load balancer can maintain session persistence using cookies or source‑IP hashing so the same user always hits the same server.

### 2.4 SSL Termination
Load balancer can decrypt TLS traffic once, reducing CPU load on backend servers and allowing them to focus on business logic.

### 2.5 Global Load Balancing
Multiple data centers across regions (e.g., Mumbai, Delhi) can be coordinated by a global load balancer which routes users to the nearest region, reducing latency.

## 3. Architecture Flow

```mermaid
graph TD
    A[Client (Browser/App)] -->|HTTPS Request| B[Load Balancer]
    B --> C1[Health Check]
    B --> D1[Server Pool]
    D1 -->|Round Robin| E1[Server 1]
    D1 -->|Round Robin| E2[Server 2]
    D1 -->|Round Robin| E3[Server 3]
    E1 --> F[Database]
    E2 --> F
    E3 --> F
    F -->|Read/Write| G[Cache (Redis)]
    G --> E1
    G --> E2
    G --> E3
```

*Client* hits the **Load Balancer**. It performs **Health Checks** and forwards the request to one of the three servers based on chosen algorithm. Servers interact with **Database** and **Cache** to serve the request.

## 4. Production Case Study

### Zomato’s Real‑World Implementation

Zomato uses **AWS Application Load Balancer (ALB)** in front of a fleet of EC2 instances behind an **Auto Scaling Group**. Key points:

- **Dynamic Scaling**: ALB automatically distributes traffic to instances that are healthy and ready, scaling up/down based on CloudWatch metrics (CPU, request count).
- **Health Checks**: Custom `/health` endpoint checks database connectivity and internal metrics.
- **Sticky Sessions**: For certain user flows (e.g., cart operations), ALB uses application‑controlled cookies to keep sessions consistent.
- **Global Accelerator**: For international traffic, Zomato uses AWS Global Accelerator to route users to the nearest regional ALB, reducing latency.

Result: Even during 2‑hour peak windows, Zomato maintains < 200 ms average latency and 99.9% uptime.

## 5. Trade‑offs (Pros vs Cons)

| Pros | Cons |
|------|------|
| **Scalability** – easily add more backend servers. | **Complexity** – requires proper health‑check implementation. |
| **High Availability** – failover on server failure. | **Cost** – additional load balancer instance(s) and data transfer. |
| **Traffic Distribution** – balanced load reduces bottlenecks. | **Latency** – extra hop can add microseconds of delay. |
| **SSL Termination** – offloads decryption work. | **Single Point of Failure** – if LB fails, entire system is down (mitigate with HA). |
| **Centralized Logging/Monitoring** – easier to track traffic patterns. | **Stateful Applications** – need sticky sessions or external session store. |

## 6. System Design Interview Cheat Sheet

- **Define problem scope**: traffic volume, latency targets, failover requirements.
- **Choose LB type**: Layer‑4 (TCP) vs Layer‑7 (HTTP) based on protocol needs.
- **Select balancing algorithm**: Round Robin for simplicity, Least Connections for variable workloads.
- **Implement health checks**: HTTP/HTTPS endpoints + graceful draining.
- **Plan for persistence**: sticky sessions vs external session store.
- **Consider global routing**: use CDN or global LB for multi‑region deployments.
