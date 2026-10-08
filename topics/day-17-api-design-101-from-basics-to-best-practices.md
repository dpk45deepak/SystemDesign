# API Design 101: From Basics to Best Practices

> Video Reference: [API Design 101: From Basics to Best Practices](https://www.youtube.com/watch?v=pH7ZT9cOL0k)

## 1. Asli Problem Kya Hai? (The Core Why)

Socho ek Swiggy driver app. Order place hota hai, driver ko route, menu, payment details dikhana hota hai. Agar API slow ya buggy ho, to driver ko real‑time updates nahi milte, aur customers ko wrong ETA dikhaya jata hai. High traffic ke time (e.g., Diwali, New Year) 10k orders ek second mein aate hain. Agar API design acha nahi hai, to latency badh jati hai, throughput drop hota hai, aur ultimately users ka trust lose ho jata hai. Isliye, API design ka core problem yeh hai ki hum scalable, reliable, aur user‑friendly interface banayein jo demand ko smoothly handle kare.

## 2. Core Architecture & Mechanisms

### 2.1 Statelessness
API ko stateless rakhna important hai. Har request ko independent treat karo; session data server side store mat karo. Isse horizontal scaling easy hota hai. Example: Paytm ki transaction API har request ko token ke through authenticate karta hai, aur koi session store nahi karta.

### 2.2 Versioning
`/v1/`, `/v2/` pattern se API evolve hoti rehti hai. Clients backward compatible rehte hain. Zerodha ke API ek example: `GET /api/v1/quotes` to `GET /api/v2/quotes?fields=price,volume`.

### 2.3 Pagination & Throttling
Large datasets (e.g., all train schedules) ko paginated return karo. `limit` aur `offset` ya cursor based approach use karo. Rate limiting (e.g., 100 req/min per user) prevents abuse. IRCTC uses pagination for seat availability lists.

### 2.4 Caching & CDN
Read‑heavy endpoints (menu items) ko edge cache (CloudFront, Akamai) pe store karo. Cache‑control headers set karo: `Cache-Control: public, max-age=60`. This reduces origin load.

### 2.5 Error Handling & Idempotency
Clear HTTP status codes (200 OK, 400 Bad Request, 404 Not Found, 429 Too Many Requests, 500 Internal Server Error). Idempotent POSTs ke liye `Idempotency-Key` header. Ola’s booking API uses this to avoid duplicate rides.

### 2.6 Security
Use HTTPS, JWT tokens, OAuth2 for third‑party access. Implement input validation, OWASP best practices. Paytm’s APIs are signed with HMAC to ensure authenticity.

### 2.7 Monitoring & Observability
Track latency, error rate, throughput using Prometheus + Grafana. Use distributed tracing (Jaeger). This helps spot bottlenecks quickly.

## 3. Architecture Flow

```mermaid
graph TD
    A[Client (Mobile/Web)] -->|HTTPS| B[API Gateway]
    B -->|Route+Auth| C[Load Balancer]
    C -->|Round Robin| D{Microservice}
    D -->|Read| E[Read Replica]
    D -->|Write| F[Write Replica]
    D -->|Cache| G[Redis]
    D -->|Logs/Tracing| H[Observability Stack]
    E -->|Data| I[Database]
    F -->|Data| I
    G -->|Data| I
```

## 4. Production Case Study

**Uber** uses a layered API design:

- **API Gateway** (NGINX) handles TLS termination, request routing, rate limiting.
- **Service Mesh** (Istio) provides fine‑grained traffic control and observability.
- **Stateless microservices** (written in Go) expose REST/GRPC endpoints. Each service has its own database.
- **Cache layer** (Redis) stores frequently accessed data like driver locations.
- **Event‑driven architecture** with Kafka for asynchronous updates (e.g., ride status).
- **Versioned APIs** allow incremental rollouts without breaking existing clients.

Result: Uber handles millions of requests per second with sub‑200 ms latency during peak hours.

## 5. Trade-offs (Pros vs Cons)

| Pros | Cons |
|------|------|
| Stateless APIs scale horizontally | Requires more stateless design effort |
| Clear versioning keeps backward compatibility | Version proliferation can clutter documentation |
| Pagination reduces payload size | Client-side complexity increases |
| Caching boosts read performance | Cache invalidation can be tricky |
| Idempotency prevents duplicate writes | Extra header handling needed |
| Observability aids rapid debugging | Adds operational overhead |

## 6. System Design Interview Cheat Sheet

- **Stateless + Cache**: Always start with stateless design, then add caching for read‑heavy endpoints.
- **Versioning first**: `/v1/`, `/v2/` to avoid breaking changes.
- **Rate limiting**: Protect backend from abuse and ensure QoS.
- **Pagination**: Use cursor or limit/offset based on data size.
- **Observability**: Monitor latency, error rate, and use tracing to pinpoint issues.
