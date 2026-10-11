# How Signed URLs & Cookies Protect Your Cloud Data

> Video Reference: [How Signed URLs & Cookies Protect Your Cloud Data](https://www.youtube.com/watch?v=Bbp6peXp0WU)

## 1. Asli Problem Kya Hai? (The Core Why)

Imagine Swiggy’s delivery driver app. हर delivery driver को अपने गाड़ी में order details, map, और payment info मिलना चाहिए, लेकिन ये data सिर्फ़ authorized users (drivers, customers) के लिए ही होनी चाहिए. अगर कोई hacker public S3 bucket URL को copy कर ले, तो वो किसी भी user की order details या even private media files तक पहुँच सकता है.  

**Why this problem exists?**  
- Cloud storage services (S3, CloudFront, Azure Blob) are cheap and scalable, but by default they expose data to the internet.  
- High‑traffic Indian platforms store thousands of media files, PDFs, and dynamic content.  
- A single leaked URL can lead to data breach, loss of revenue, and regulatory fines (GDPR, India’s IT Act).

**If not solved**:  
- Unauthorized users can download or modify files.  
- Sensitive customer data leaks (e.g., payment receipts).  
- Brand trust erodes – customers may stop using your app.

## 2. Core Architecture & Mechanisms

### Signed URLs
- **What**: URL with embedded cryptographic signature + expiry timestamp.  
- **How**: Cloud provider (S3, CloudFront, GCS) verifies signature using a shared secret or IAM role before serving the object.  
- **Intuition**: Think of it like a QR code that is valid only for 5 minutes; after that, it’s useless.

### Signed Cookies
- **What**: Set of cookies (e.g., `CloudFront-Policy`, `CloudFront-Signature`) that grant access to multiple URLs or entire paths.  
- **How**: Browser automatically sends cookies with each request; the CDN checks the policy and signature.  
- **Intuition**: Like giving a driver a temporary pass that works for the whole zone until midnight.

### Common Flow
1. **Request**: User clicks “Download Invoice” → frontend asks backend for a signed URL.  
2. **Generate**: Backend uses SDK (e.g., `boto3`, `aws-sdk-go`) to create signed URL with a short TTL (e.g., 2 min).  
3. **Serve**: User’s browser hits the signed URL; CDN verifies signature → serves file.  
4. **Expiration**: After TTL, the URL is invalid; further requests fail (HTTP 403).  

### Security Benefits
- **Fine‑grained control**: Limit access to specific objects or paths.  
- **Time‑bound**: Reduces window for misuse.  
- **No need for IAM policies** on every request; lightweight cryptographic check.

### Performance Considerations
- **Latency**: Signing is done on backend; CDN verification is in‑memory, negligible overhead.  
- **Throughput**: High‑traffic sites can issue millions of signed URLs per day; use caching or rate‑limit if needed.  
- **Scalability**: Works across edge locations; no single point of failure.

## 3. Architecture Flow

```mermaid
graph TD
    A[User] -->|Clicks "Download"| B[Frontend]
    B -->|Request signed URL| C[Backend Service]
    C -->|Generate signed URL (TTL=5m)| D[Cloud Provider SDK]
    D -->|Return signed URL| C
    C -->|Send signed URL to frontend| B
    B -->|Browser fetches signed URL| E[CDN Edge]
    E -->|Verify Signature & Expiry| F[Cloud Storage]
    F -->|Serve Object| E
    E -->|Return Object| B
    B -->|Download to User| A
```

## 4. Production Case Study

**Netflix** uses signed URLs for streaming DRM‑protected content.  
- **Scenario**: When a user starts a movie, Netflix’s backend generates a signed URL that grants access to the CDN edge for a few minutes.  
- **Why**: Prevents users from saving the direct link and re‑streaming elsewhere.  
- **Result**: Reduced unauthorized downloads, improved bandwidth usage, and compliance with licensing agreements.

Another example: **Zomato** serves menu images from S3.  
- They use signed URLs with 30‑second TTL for menu thumbnails to ensure that only authenticated users can view images while the image cache expires quickly, preventing stale data leaks.

## 5. Trade-offs (Pros vs Cons)

| Pros | Cons |
|------|------|
| Fine‑grained, time‑bounded access control | Requires backend logic to generate signatures |
| No need to expose IAM credentials on client | Slight increase in request latency (signature verification) |
| Works across global CDN edge locations | Must manage key rotation and expiration policies |
| Easy to audit (log signed URL usage) | Potential for URL leakage if not secured over HTTPS |
| Scalable for millions of requests | Requires secure storage of signing keys (KMS, Vault) |

## 6. System Design Interview Cheat Sheet

- **Explain the threat model**: unauthenticated access to public cloud storage.  
- **Describe signed URLs vs signed cookies**: single object vs path‑wide access.  
- **Mention TTL importance**: balances usability and security.  
- **Talk about key management**: use KMS or Vault; rotate keys regularly.  
- **Highlight CDN verification**: low‑latency, edge‑based signature checks.
