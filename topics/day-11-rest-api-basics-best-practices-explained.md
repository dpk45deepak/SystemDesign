# REST API Basics & Best Practices Explained

> Video Reference: [REST API Basics & Best Practices Explained](https://www.youtube.com/watch?v=DkSeXHS0kAQ)

## 1. Asli Problem Kya Hai? (The Core Why)

Imagine **Swiggy** is running a peak‑time order surge. Thousands of customers hit the “Place Order” button, but the backend has to:
- Translate the request into a database write,
- Update inventory,
- Notify kitchen and rider.

If each request goes through a monolithic API layer, the latency spikes, throughput drops, and a single buggy endpoint can bring the whole service down.  
Yahi problem hai: **scalable, reliable, and fast communication between services**. Agar hum isko ignore karte, customers ko “Order not received” errors milenge, revenue loss, and brand damage.

## 2. Core Architecture & Mechanisms

### a) Resource‑Based Design
REST mein har entity (order, restaurant, user) ko ek **URL** se represent kiya jata hai.  
- GET /orders/123 → read order  
- POST /orders → create order  
- PUT /orders/123 → update order  
- DELETE /orders/123 → delete

### b) Statelessness
Every HTTP request contains all the info needed to process it. Server doesn’t store session data.  
- **Pros**: Easy to scale horizontally (any instance can handle any request).  
- **Cons**: Need to embed auth tokens (JWT) or send cookies with each call.

### c) Idempotency
Same request multiple times should give same result.  
- PUT, DELETE are naturally idempotent.  
- POST should use an **idempotency key** (e.g., X-Idempotency-Token) to avoid duplicate orders in Swiggy.

### d) Caching & CDN
Use **ETags** and **Cache‑Control** headers to reduce repeated DB hits.  
- Swiggy’s menu endpoint can be cached on CloudFront for 5‑10 minutes.

### e) Pagination & Filtering
Large result sets (e.g., 10k restaurants) need paging.  
- `GET /restaurants?offset=0&limit=50`  
- Use **cursor** based pagination for better performance on large datasets.

### f) Versioning
Keep backward compatibility.  
- `/api/v1/orders` vs `/api/v2/orders` – new fields, new logic.

### g) Error Handling
Return meaningful HTTP status codes and a JSON body with `errorCode` and `message`.  
- 400 Bad Request, 401 Unauthorized, 404 Not Found, 429 Too Many Requests, 500 Internal Server Error.

## 3. Architecture Flow

```mermaid
graph TD
    A[Client (Mobile/Web)] -->|HTTPS| B[API Gateway]
    B -->|Route| C[Order Service]
    C -->|DB Call| D[Read/Write Replica]
    C -->|Publish| E[Kafka Topic: order.created]
    E -->|Consume| F[Inventory Service]
    F -->|Update| D
    E -->|Consume| G[Notification Service]
    G -->|Push| H[FCM/APNs]
```

- **API Gateway** handles authentication, rate limiting, and routing.  
- **Order Service** is stateless; it talks to read/write replicas for DB ops.  
- **Kafka** decouples services, improving throughput and resilience.

## 4. Production Case Study

**Uber** uses a **RESTful API layer** for its rider app.  
- Rider requests `GET /v1/rides?lat=xx&lon=yy`.  
- Gateway validates JWT, enforces rate limits, then forwards to **Rides Service**.  
- Rides Service uses **Consistent Hashing** to pick a **Read Replica** for quick lookup, while writes go to the master.  
- All responses are cached in **Redis** for 2 seconds to handle bursty traffic during surge events.  
Result: Uber can serve millions of ride requests per hour with <200 ms latency.

## 5. Trade-offs (Pros vs Cons)

| Pros | Cons |
|------|------|
| Easy to understand & implement. | Limited to stateless operations; stateful workflows need workarounds. |
| Horizontal scalability due to statelessness. | Requires careful caching strategy to avoid stale data. |
| Rich ecosystem of tools (Swagger, Postman, etc.). | Overhead of HTTP headers and body can increase payload size. |
| Clear resource mapping aids in versioning & deprecation. | Large payloads (e.g., file uploads) are less efficient than gRPC or GraphQL. |
| Idempotency & caching reduce duplicate processing. | Complex transactions across services need compensating actions. |

## 6. System Design Interview Cheat Sheet

- **REST Principles**: Resource URLs, HTTP verbs, statelessness, cacheability.  
- **Scalability**: Use API Gateway, load balancer, stateless services, read/write replicas.  
- **Reliability**: Idempotency keys for POST, circuit breakers, graceful degradation.  
- **Security**: JWT/OAuth, rate limiting, input validation, TLS everywhere.  
- **Observability**: Structured logging, distributed tracing, metrics (latency, throughput) with Prometheus/Grafana.
