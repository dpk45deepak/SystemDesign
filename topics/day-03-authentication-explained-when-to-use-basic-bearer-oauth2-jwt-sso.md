# Authentication Explained: When to Use Basic, Bearer, OAuth2, JWT & SSO

> Video Reference: [Authentication Explained: When to Use Basic, Bearer, OAuth2, JWT & SSO](https://www.youtube.com/watch?v=9JPnN1Z_iSY)

## 1. Asli Problem Kya Hai? (The Core Why)

Maan lo tum Swiggy par Biryani order kar rahe ho. Tumne app khola, cart mein item add kiya, aur payment button dabaya. HTTP protocol by default **stateless** hota hai—matlab Server ko yeh bilkul yaad nahi rehta ki picchli HTTP request kisne bheji thi.

Agar system design ke level par dekhein, toh har incoming HTTP request ke saath backend ko do cheezein jaan na zaroori hai:
1. **Authentication (Who are you?):** Kya yeh request genuinely tumhari hai ya kisi hacker ne middle mein request tamper ki hai?
2. **Authorization (What can you do?):** Agar tum logged in ho, toh kya tum iss specific user ID ka order cancel kar sakte ho ya address badal sakte ho?

Agar hum har API call par user se `username` aur `password` maangne lagein, toh User Experience (UX) destroy ho jaayega. Aur agar hum credentials ko app mein insecurely store karein, toh security breach ka massive threat hai.

Isi problem ko solve karne ke liye hum Authentication Mechanisms use karte hain. Lekin system scaling, microservices architecture, aur third-party integrations ke hisaab se sahi pattern select karna sabse bada architectural challenge hota hai.

---

## 2. Core Architecture & Mechanisms

Har authentication pattern ka apna ek specific use case aur operational complexity hoti hai. Chalo inko deep-dive karke samajhte hain.

### 1. Basic Authentication
Yeh sabse purana aur simple mechanism hai. Client har HTTP request ke `Authorization` header mein username aur password ko colon (`:`) se combine karke **Base64** encode karke bhejta hai.

* **Header Format:** `Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=`
* **Asliat:** Base64 koi encryption nahi hai, yeh sirf encoding hai. Koi bhi browser devtools khol kar ise 1 second mein decode kar sakta hai.
* **Architecture Impact:**
  * Har request par Database lookup karna padega password hash verify karne ke liye, jis se DB par massive Read Load padega (High Latency).
  * TLS/HTTPS ke bina ise production mein use karna suicide hai.
* **When to use:** Internal microservices communicate kar rahe hon jahan network strictly private VPC ke andar ho, ya simple internal administrative scripts ke liye.

### 2. Bearer Tokens & JWT (JSON Web Token)
Bearer token ka matlab hai: *"Jis banda ke paas yeh token (bearer) hai, usko access de do."*

JWT iska sabse popular implementation hai. JWT ek **Self-Contained Token** hota hai, jiske teen parts hote hain: `Header.Payload.Signature`

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IlJhaHVsIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

* **Header:** Algorithm (e.g., RS256, HS256) aur token type batata hai.
* **Payload:** Claims hotey hain jaise `user_id`, `role`, `exp` (expiry time).
* **Signature:** Central Auth Service token ko apne **Private Key** (Asymmetric) ya **Secret Key** (Symmetric) se sign karti hai.

#### Architectural Advantage: Statelessness
API Gateway ya downstream microservices ko Database ya Auth Server ko query karne ki zaroorat nahi hoti. Microservice token ke signature ko Public Key se verify kar leti hai. Isse DB round-trips zero ho jaate hain aur system **horizontally scale** kar pata hai.

#### Production Pitfall (Token Revocation):
JWT stateless hai, iska matlab agar kisi user ka account hack ho gaya ya token leak ho gaya, toh jab tak token expire nahi hota, server use stop nahi kar sakta.
* **Solution:** Short Expiry Time (e.g., 15 mins) + Refresh Token Pattern (stored in Redis) ya JWT Blacklisting via Redis Cache.

### 3. OAuth 2.0 Framework
OAuth 2.0 koi authentication protocol nahi hai, yeh ek **Delegated Authorization Framework** hai.

Iska sabse badhiya example hai: *"Login with Google on Zerodha/Swiggy"*. Tum Zerodha ko apna Google password nahi dete, lekin Zerodha ko Google se tumhari basic identity read karne ki permission mil jaati hai.

#### Core Roles in OAuth 2.0:
* **Resource Owner:** User (Tum).
* **Client:** Application (e.g., Swiggy).
* **Authorization Server:** Google / Auth0 / Keycloak.
* **Resource Server:** API Service jahan data pada hai (e.g., Google UserInfo API).

#### Recommended Flow: Authorization Code Grant with PKCE
Web aur Mobile Apps ke liye PKCE (Proof Key for Code Exchange) mandatory hai taaki authorization code interception attack na ho sake. Client ek temporary secret (`code_verifier`) banata hai aur uski hash (`code_challenge`) Auth server ko bhejta hai.

### 4. OpenID Connect (OIDC) & SSO (Single Sign-On)
OAuth 2.0 sirf *Authorization* ke liye tha. Uske upar ek Identity Layer add ki gayi jise **OpenID Connect (OIDC)** kehte hain. OIDC authentication standardize karta hai aur ek **ID Token** (jo ki ek JWT hota hai) return karta hai.

**Single Sign-On (SSO):**
Maan lo Paytm ecosystem mein Paytm Mall, Paytm Money, aur Paytm Payments Bank hain. User ko ek jagah login karna hai aur wo baaki saare platforms par automatically authenticate ho jaata hai.

* Centralized Identity Provider (IdP) ek central session cookie maintain karta hai.
* Downstream services SAML 2.0 ya OIDC/JWT federated trust ke zariye session recognize kar leti hain.

---

## 3. Architecture Flow

Niche diya gaya diagram OAuth 2.0 + JWT based production authentication flow dikhata hai jahan API Gateway JWT token ko verify karta hai.

```mermaid
sequenceDiagram
    autonumber
    actor User as User (Client App)
    participant Auth as Auth Service (IdP)
    participant Gateway as API Gateway
    participant Service as Order Microservice
    participant Cache as Redis Cache

    User->>Auth: 1. POST /login (Credentials)
    Auth->>Auth: 2. Validate Credentials & Sign JWT (Private Key)
    Auth-->>User: 3. Return Access Token (JWT) + Refresh Token

    Note over User, Gateway: Subsequent Requests with JWT Header

    User->>Gateway: 4. GET /orders (Bearer JWT)
    Gateway->>Gateway: 5. Verify Signature using Public Key & Expiry
    
    alt Token Revoked/Blacklisted?
        Gateway->>Cache: 6. Check Token in Redis Blacklist
        Cache-->>Gateway: Blacklisted Token Found
        Gateway-->>User: 401 Unauthorized
    else Token Valid
        Gateway->>Service: 7. Forward Request + Injected User-Header
        Service-->>Gateway: 8. Return Order Data
        Gateway-->>User: 9. HTTP 200 OK (Response)
    end
```

---

## 4. Production Case Study

### Netflix Passport Architecture

Netflix ke thousands of microservices hain jo billions of requests handle karti hain. Agar har microservice incoming request ke JWT token ko individually parse aur cryptographic signature check karegi, toh Latency and CPU Overhead dangerously high ho jaayega.

#### Netflix Solution:
1. **Edge Auth Termination:** Central Edge Gateway (Zuul/Envoy) Client Token (OAuth/JWT) ko terminate karta hai aur User Identity ko single point par validate karta hai.
2. **Passport Tokens (Internal Identity):** Gateway external JWT ko ek internal binary serialized format mein convert karta hai jise **Passport** kehte hain.
3. **Propagated Context:** Yeh Passport internal gRPC/HTTP headers ke zariye internal microservices (Movie Service, Billing Service, Billing DB) mein Pass-through hota hai.
4. **HMAC Signing:** Passport HMAC se signed hota hai jisse downstream services secure rehti hain aur expensive Asymmetric Crypto verification ki zaroorat nahi padti.

---

## 5. Trade-offs (Pros vs Cons)

| Mechanism | Pros | Cons | Ideal Use Case |
| :--- | :--- | :--- | :--- |
| **Basic Auth** | Extremely simple to set up, zero state storage needed. | Credentials sent in every request; impossible to revoke without changing password; highly insecure without TLS. | Internal microservice-to-microservice scripts in safe private network. |
| **Bearer Token (JWT)** | **Stateless**, high scalability, zero DB lookups at API Gateway, cross-domain friendly. | Immediate token revocation is difficult; large payload size adds bandwidth overhead; payload is readable (Base64). | Microservices architecture, Mobile Apps, Modern REST APIs. |
| **OAuth 2.0** | Third-party delegation without sharing credentials, granular permission scopes. | High architectural complexity, multiple redirect flows, network round-trips. | "Log in with Google/GitHub", Third-party API integrations (e.g., Zapier). |
| **SSO (OIDC / SAML)** | Unified user experience across multiple domains, centralized identity & access management. | Single point of failure (if IdP goes down, everything breaks), complex setup. | Enterprise systems, large multi-app ecosystems (e.g., Tata Neu, Reliance Digital apps). |

---

## 6. System Design Interview Cheat Sheet

1. **Authentication vs Authorization:** Pehle identify karo interview question mein Identity establish ho rahi hai (AuthN via JWT/OIDC) ya Permissions manage ho rahi hain (AuthZ via OAuth2 Scopes/RBAC).
2. **Never store Passwords as Plaintext or Base64:** Always usesalted, slow hashing algorithms like **bcrypt**, **Argon2**, or **PBKDF2** to store passwords in database.
3. **Asymmetric Key Rotation for JWT:** Production systems mein JWT sign karne ke liye **RS256 (Public/Private Key)** use karo. API Gateways JWKS (JSON Web Key Sets) endpoint se public keys dynamic cache karke tokens verify kar sakte hain.
4. **Token Storage in Web Security:** JWT tokens ko `LocalStorage` mein mat rakho (XSS Vulnerable). Always store sensitive tokens in **HttpOnly, Secure, SameSite Cookies** to prevent script access.
5. **Revocation Strategy:** Interviewer jab poochhe *"Stateless JWT ko instantly block kaise karoge?"*, toh **Short-lived Access Token (15m)** + **Long-lived Refresh Token in Redis (7 days)** aur **Token Blacklisting Pattern** ka combo architecture propose karo.
