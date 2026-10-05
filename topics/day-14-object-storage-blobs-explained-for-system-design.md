# Object Storage (BLOBs) Explained for System Design

> Video Reference: [Object Storage (BLOBs) Explained for System Design](https://www.youtube.com/watch?v=dEcQK4-pqiw)

## 1. Asli Problem Kya Hai? (The Core Why)

Picture Swiggy’s kitchen order queue. Har order ek JSON payload hota, but customers also want to upload photos of their food, receipts, or custom spice lists.  
- **High volume**: 10k orders a minute, each with an image or PDF.  
- **Size variance**: From 50 KB images to 10 MB PDFs.  
- **Global access**: Delivery partners in Mumbai, Delhi, Kolkata need fast read/write.  
- **Durability requirement**: No data loss even if a datacenter goes down.

If we tried to store these blobs in a relational DB, we’d hit:
- **Schema rigidity** – blobs stored as BLOB columns cause table bloat.  
- **Performance hit** – large objects block read/write paths, increasing latency.  
- **Scalability issue** – DB nodes struggle to handle millions of concurrent uploads.  
Result: slow UI, timeouts, and unhappy users. Hence, we need a dedicated **Object Storage** layer.

## 2. Core Architecture & Mechanisms

### Storage Nodes & Object Metadata
- **Object** = binary data + key (e.g., `swiggy/orders/2024-10-05/12345.jpg`).  
- Each **storage node** holds a partition of objects.  
- **Metadata Service** (like a lightweight key‑value store) keeps mapping: key → {node, offset, size, checksum}.  
- Clients hit the metadata service first; it replies with the node location.

### Replication & Erasure Coding
- **Replication**: Store 3‑copy of every object across 3 zones.  
- **Erasure Coding**: For large objects, split into `k` data + `m` parity chunks; rebuildable from any `k` chunks.  
- Trade‑off: Replication = higher durability, lower bandwidth; erasure coding = storage efficient, higher compute.

### Consistency & Availability
- **Eventual consistency**: Write goes to primary node, then async replicates.  
- **Strong consistency**: Optional quorum reads (`Read‑Repair` or `Read‑Quorum`).  
- Use **Gossip Protocol** for node health checks and topology updates.

### API Layer
- **PUT** / **GET** / **DELETE** exposed via REST/HTTP.  
- Supports **Range GET** for partial downloads (useful for video streaming).  
- **Multipart upload** for large files, reducing retry overhead.

### Cache & CDN
- Frequently read objects (e.g., popular recipe images) go to **Edge Cache** (e.g., CloudFront, Akamai).  
- In‑region **Redis** or **Memcached** can cache metadata for hot paths.

## 3. Architecture Flow

```mermaid
graph TD
  Client[Client App] --> LB[Load Balancer]
  LB -->|PUT| Metadata[Metadata Service]
  Metadata -->|Return| StorageNode[Storage Node]
  StorageNode -->|Store Object| BlobStore[Blob Store]
  LB -->|GET| Metadata
  Metadata -->|Return| StorageNode
  StorageNode -->|Read Object| Client
  subgraph CDN
    CDN[CDN Edge] -->|Cache| StorageNode
  end
```

## 4. Production Case Study

**Amazon S3** – The industry standard.  
- Uses **MD5 checksums** for data integrity.  
- Implements **Versioning** and **Lifecycle Policies** (move to Glacier after 30 days).  
- **Cross‑Region Replication** for global apps like **Netflix**: user uploads in Mumbai are replicated to US‑East for faster playback.  

**Uber** – Stores driver‑uploaded documents, ride‑captured images, and map tiles.  
- Uses a custom **S3‑compatible** service called **S3‑Compatible Object Store** hosted on AWS S3 and GCP Cloud Storage.  
- Employs **multipart upload** for large video clips from rides.  

## 5. Trade-offs (Pros vs Cons)

| Pros | Cons |
|------|------|
| *Scalable* – can handle petabytes of data. | *Latency* can be higher due to extra hops. |
| *Durable* – multi‑zone replication or erasure coding. | *Consistency* is usually eventual; strong consistency requires extra reads. |
| *Cost‑effective* – cheaper than spinning up DB nodes for blobs. | *Complexity* – need metadata service, replication logic, and monitoring. |
| *Flexible* – any binary format, no schema. | *Operational overhead* – backup, restore, and disaster recovery plans. |
| *Global access* – CDN + edge caching. | *Vendor lock‑in* if using proprietary APIs. |

## 6. System Design Interview Cheat Sheet

- **Define problem**: Size, volume, durability, latency, access patterns.  
- **Choose storage**: Replicated objects vs erasure coding; decide k/m.  
- **Metadata service**: Lightweight KV store, consistent hashing for node placement.  
- **API design**: PUT/GET/DELETE with multipart support; Range GET for streaming.  
- **Consistency model**: Eventual by default; add read‑repair or quorum if required.

---
