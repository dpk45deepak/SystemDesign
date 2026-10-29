# REST vs GraphQL

> Video Reference: [REST vs GraphQL](https://www.youtube.com/watch?v=FI_jvrgT52E)

## 1. Asli Problem Kya Hai? (The Core Why)

Maan lo Swiggy ka delivery system hai. Frontend (app) ko ek order ke liye restaurant details, menu, delivery time, payment status, aur user reviews sab chahiye. Agar hum REST use karein, toh har ek resource ke liye alag endpoint call karna padega:

```
GET /orders/123
GET /restaurants/45
GET /menus/45
GET /payments/123
GET /reviews?restaurant=45
```

Yeh 5 alag HTTP requests hote hain, network latency badh jaati hai, mobile data consume hota hai, aur backend ko multiple database hits karne padte hain. Agar user slow network pe ho, to app lagne lagta hai. Is problem ko solve na karne se user churn, poor UX, aur higher server load hota hai.

GraphQL ek single endpoint `/graphql` hota hai, jahan ek query bheji jaati hai:

```graphql
{
  order(id: "123") {
    id
    status
    restaurant {
      id
      name
      menu {
        items {
          id
          name
          price
        }
      }
    }
    payment {
      status
      method
    }
    reviews {
      rating
      comment
    }
  }
}
```

Ek request, ek response – exactly what the client needs. Network overhead kam hota hai, data usage reduce hota hai, aur developer ko apni UI ko update karne ke liye alag endpoints se deal nahi karna padta.

## 2. Core Architecture & Mechanisms

### REST

- **Stateless**: Har request self-contained hoti hai. Server koi session maintain nahi karta.
- **Resource-Oriented**: URL se resource identify hota hai (`/users/1`).
- **CRUD Operations**: `GET`, `POST`, `PUT`, `DELETE` se map kiya jata hai.
- **Cacheable**: Responses ko HTTP caching headers ke through re-use kiya ja sakta hai.
- **Versioning**: API v1, v2, etc. maintain karna padta hai.

### GraphQL

- **Single Endpoint**: `/graphql` – sab kuch waha se handle hota hai.
- **Schema-Driven**: Types, Queries, Mutations define karte hain ki data structure kya hoga.
- **Declarative Queries**: Client batata hai exactly kis data ki jarurat hai; server sirf wohi return karta hai.
- **Resolvers**: Backend logic jo fields ke liye data fetch karta hai. Ye single resolver ya batched resolvers (DataLoader) ho sakte hain.
- **Strong Typing**: Compile-time checks via schema, client-side IDE support.
- **Real-time (Subscriptions)**: WebSocket based push notifications.

### Intuition in Hinglish

- REST ka socho ek bhari thali jisme sab items alag plates pe diye jate hain. Agar tumhe sirf ek item chahiye, phir bhi poori thali le jaate ho.
- GraphQL ka socho ek menu card. Tum decide karte ho ki kaun kaun se dishes chahiye, aur chef sirf wahi banata hai.

## 3. Architecture Flow

```mermaid
graph TD
  A[Client] -->|HTTP POST /graphql| B[GraphQL Server]
  B -->|Resolver 1| C[Database]
  B -->|Resolver 2| D[Cache (Redis)]
  C -->|Data| B
  D -->|Data| B
  B -->|Response| A
```

- Client ek GraphQL query bhejta hai.
- Server query ko parse karta hai, schema se validate karta hai.
- Resolvers decide karte hain ki data kaun se source se chahiye (DB, cache, external API).
- Data resolve hota hai, ek single JSON response client ko milta hai.

## 4. Production Case Study

**Uber** uses GraphQL extensively for its driver and rider apps. Initially they had separate REST endpoints for trip status, driver location, payment, and ratings. It caused 20+ round-trips on app launch, leading to delays in ride confirmations. After migrating to GraphQL:

- **Reduced network calls** from ~15 to 1 per trip request.
- **Faster UI updates** because driver location updates are pushed via Subscriptions.
- **Better cache control**: Frequently accessed data like driver profiles cached in Redis.
- **Developer productivity**: Frontend teams could iterate faster without backend coordination for new fields.

Uber’s GraphQL layer sits behind a load balancer, uses rate limiting, and is deployed across multiple regions for low latency.

## 5. Trade-offs (Pros vs Cons)

| Pros | Cons |
|------|------|
| Single endpoint reduces network overhead | Learning curve for schema & resolvers |
| Precise data fetching (no over-fetching) | Requires careful batching to avoid N+1 queries |
| Strong typing & IDE support | More complex server logic (resolver composition) |
| Real-time subscriptions (WebSocket) | Versioning is implicit; breaking changes harder to manage |
| Flexible client-side evolution | Initial setup cost (schema design, tooling) |
| Easier caching per field | Requires a robust caching strategy to avoid duplicate DB hits |

## 6. System Design Interview Cheat Sheet

- **REST**: Stateless, resource-oriented, CRUD, cacheable, versioning.
- **GraphQL**: Single endpoint, schema-driven, declarative queries, resolvers, strong typing, subscriptions.
- **When to choose?**: High-traffic, mobile-optimized apps (Swiggy, IRCTC) → GraphQL; simple CRUD APIs, microservices with clear boundaries → REST.
- **Common pitfalls**: N+1 problem, over-fetching vs under-fetching, caching complexity.
- **Performance knobs**: DataLoader batching, query complexity analysis, persisted queries, response caching.

---
