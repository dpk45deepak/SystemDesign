# Every AWS Service You Need To Know

> Video Reference: [Every AWS Service You Need To Know](https://www.youtube.com/watch?v=n28iOV_Y_tQ)

## 1. Asli Problem Kya Hai? (The Core Why)

Picture Swiggy or IRCTC during peak hours.  
- **Traffic spikes**: 2–3x orders during festival season, 10x during a big match.  
- **Low latency**: Customers expect < 200 ms response for menu load and order placement.  
- **High availability**: 99.99% uptime is a must; a single point of failure can cost lakhs in revenue.  
- **Data consistency**: Seats in IRCTC, inventory in Swiggy must stay in sync across multiple regions.  

If you ignore these, you get timeouts, data races, and disgruntled users. AWS services are the tools to solve these problems at scale.

---

## 2. Core Architecture & Mechanisms

Below is a quick tour of the key AWS services that make this possible. I’ll keep the engineering terms in English and explain the intuition in Hinglish.

### Compute

| Service | Use Case | Intuition |
|---------|----------|-----------|
| **EC2** | General-purpose servers | Like hiring a dedicated dev who works 24/7, but you pay per hour. |
| **Lambda** | Event‑driven micro‑tasks | Think of it as a “chef” who comes in only when an order is placed, does the job, and leaves. |
| **ECS/EKS** | Container orchestration | Same as Docker + Kubernetes but managed by AWS, so no “kube‑config” headaches. |
| **Auto Scaling** | Auto‑spin up/down based on load | Like auto‑ordering fresh stock when inventory drops below threshold. |

### Storage

| Service | Use Case | Intuition |
|---------|----------|-----------|
| **S3** | Static assets (images, videos) | A huge, cheap, durable pantry that everyone can pull from. |
| **EFS** | Shared file system for containers | Like a shared drive for multiple servers to read/write. |
| **Glacier** | Archival | Store old receipts for compliance, not for quick access. |

### Database

| Service | Use Case | Intuition |
|---------|----------|-----------|
| **RDS (Aurora)** | Relational data (orders, users) | Managed MySQL/PostgreSQL with HA and automatic backups. |
| **DynamoDB** | NoSQL key‑value (menu, cart) | Extremely low latency, scales to millions of requests per second. |
| **DocumentDB** | JSON‑style documents | MongoDB‑compatible, great for flexible schemas. |

### Networking & Delivery

| Service | Use Case | Intuition |
|---------|----------|-----------|
| **VPC** | Isolated network | Your own office space with firewalls. |
| **ALB/NLB** | Load balancing | Traffic‑shaper: forwards requests to healthy instances. |
| **Route 53** | DNS & routing | Google Maps for your domain, with health checks. |
| **CloudFront** | CDN | Mirror your content at edge locations so users load fast. |

### Caching & Messaging

| Service | Use Case | Intuition |
|---------|----------|-----------|
| **ElastiCache (Redis/Memcached)** | In‑memory cache | Quick “cheat sheet” for hot data (e.g., popular menu items). |
| **SQS** | Queue for decoupling | Like a message board where workers pick jobs asynchronously. |
| **SNS** | Pub/Sub notifications | Broadcast alerts (e.g., “New order received”) to multiple subscribers. |
| **Kinesis** | Real‑time streaming | Streaming analytics for order heatmaps, fraud detection. |

### Monitoring & Security

| Service | Use Case | Intuition |
|---------|----------|-----------|
| **CloudWatch** | Metrics & logs | Dashboard for “how many orders per minute?” |
| **CloudTrail** | Audit logs | Who changed what, when. |
| **IAM** | Fine‑grained permissions | “Only the order service can write to DynamoDB.” |
| **KMS** | Encryption | Keys stored in a vault, not in your code. |
| **GuardDuty** | Threat detection | AI that looks for suspicious activity. |

### Other Handy Services

- **CloudFormation / CDK** – Infrastructure as code.  
- **CodePipeline / CodeBuild** – CI/CD.  
- **Step Functions** – Orchestrate complex workflows.  
- **Direct Connect** – Private link to on‑premise data centers.  

---

## 3. Architecture Flow

```mermaid
graph TD
  A[User] -->|HTTPS| B[CloudFront]
  B -->|Cache Miss| C[Route53]
  C -->|DNS| D[ALB]
  D -->|Round‑Robin| E[EC2 / ECS]
  D -->|Serverless| F[Lambda]
  E -->|Read/Write| G[RDS (Aurora)]
  E -->|Read/Write| H[DynamoDB]
  E -->|Cache| I[ElastiCache]
  E -->|Queue| J[SQS]
  J -->|Worker| K[EC2/Lambda]
  K -->|Publish| L[SNS]
  L -->|Notify| M[Clients]
  E -->|Logs| N[CloudWatch]
  E -->|Audit| O[CloudTrail]
```

- User hits CloudFront; if data is cached, response is immediate.  
- If not, request goes through Route 53 → ALB → backend compute.  
- Compute interacts with databases, cache, queues, and publishes events.  
- Monitoring and logging feed into CloudWatch and CloudTrail.  

---

## 4. Production Case Study

**Swiggy (Food Delivery)**

| Problem | AWS Service | How Swiggy Solves It |
|---------|-------------|----------------------|
| Real‑time order placement | **API Gateway + Lambda** | Orders trigger Lambda that writes to DynamoDB, publishes to SQS. |
| Menu and image delivery | **S3 + CloudFront** | Images stored in S3, served via CloudFront edge locations across India. |
| Inventory and seat management | **RDS Aurora** | ACID‑compliant orders, with read replicas for read‑heavy traffic. |
| Notifications | **SNS + SQS** | Push notifications to drivers and customers. |
| Monitoring & Auto‑Scaling | **CloudWatch + Auto Scaling** | Scale Lambda concurrency and EC2 instances based on CPU/Queue depth. |
| Security | **IAM + KMS** | Fine‑grained roles for services, data encrypted at rest. |

Result: Swiggy handles millions of orders daily with < 300 ms latency, 99.9% uptime, and zero data loss.

---

## 5. Trade‑offs (Pros vs Cons)

| Pros | Cons |
|------|------|
| **Managed services** – No ops overhead (RDS, Lambda, S3). | **Vendor lock‑in** – Switching away can be expensive. |
| **Automatic scaling** – Auto Scaling, Lambda concurrency. | **Cost spikes** – Under‑utilization or traffic surges can inflate bills. |
| **High availability** – Multi‑AZ deployments, read replicas. | **Complexity** – Many moving parts to orchestrate. |
| **Security & compliance** – IAM, KMS, GuardDuty. | **Cold starts** – Lambda can be slow on first invocation. |
| **Global reach** – CloudFront, Route 53. | **Latency** – Cross‑region traffic may add delays if not optimised. |

---

## 6. System Design Interview Cheat Sheet

- **Start with requirements**: traffic, latency, consistency, cost.  
- **Pick compute**: EC2 for long‑running services, Lambda for stateless ops, ECS/EKS for containers.  
- **Choose database**: RDS/Aurora for relational, DynamoDB for key‑value, DocumentDB for flexible.  
- **Add caching**: ElastiCache (Redis) for hot data, CloudFront for static assets.  
- **Decouple with messaging**: SQS/SNS/Kinesis to avoid tight coupling.  
- **Secure & monitor**: IAM roles, KMS, CloudWatch, CloudTrail, GuardDuty.  

Remember: “If you can’t explain it in 5 minutes, you don’t understand it.” Good luck!
