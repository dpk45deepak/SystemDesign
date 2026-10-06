# Map Reduce explained with example | System Design

> Video Reference: [Map Reduce explained with example | System Design](https://www.youtube.com/watch?v=neoXVthw22Q)

## 1. Asli Problem Kya Hai? (The Core Why)

Imagine Swiggy ke paas har din 20 lakh orders aa rahe hain.  
Business ka ek kaam: *“Har 5 minute pe pata karna ki kaun se dishes sabse zyada order ho rahi hain, aur har city ka average delivery time kya hai”*.  

- **High throughput data**: 20 lakh rows per day → 1.2 crore rows per hour.  
- **Low latency insight**: 5 minutes ke andar dashboard update.  
- **Data is distributed**: Orders stored across multiple shards (different regions).  

Agar hum ek single server pe aggregate karne ki koshish karein, toh:

- **Scalability issue**: CPU, memory aur I/O bottlenecks.  
- **Latency spikes**: 5 minutes ka window miss ho jayega.  
- **Fault tolerance**: Agar koi node fail ho gaya, poora job fail ho jayega.

Yehhi problem hai jiske liye *Map Reduce* ka use hota hai: data ko parallelly process karke aggregate results quickly aur reliably nikalna.

## 2. Core Architecture & Mechanisms

### Map Phase
- **Input**: Raw order logs (key: order_id, value: order details).  
- **Operation**: Har mapper (worker node) local data read karta hai, aur *key-value pairs* emit karta hai.  
  - Example: `(dish_id, 1)` for count, or `(city, delivery_time)` for average.  
- **Goal**: Data ko *shuffle* ke liye key ke basis pe bucket karna.  
- **Intuition**: Think of it as every waiter (mapper) collecting dishes sold in their own table and writing a small note about each dish.

### Shuffle & Sort
- **Network transfer**: Mappers ke outputs ko reducers ke paas bheja jata hai, key ke basis pe partition hota hai.  
- **Sorting**: Same keys group ho jaate hain, taaki reducer ek key ke saare values ek sath process kar sake.  
- **Load balancing**: Partitioning algorithm (hash partition) ensures each reducer gets roughly equal load.

### Reduce Phase
- **Input**: Sorted list of key-value pairs per key.  
- **Operation**: Reducer aggregates (sum, avg, max, etc.).  
- **Output**: Final result set (e.g., `dish_id -> total_count`).  
- **Fault tolerance**: If a reducer fails, its partition is retried on another node.

### Key Engineering Terms (English)
- **Latency**: Time taken for a single job to finish.  
- **Throughput**: Number of records processed per unit time.  
- **Consistency**: Each job produces deterministic output given same input.  
- **Availability**: System keeps running even if some nodes fail.  
- **Load Balancer**: Not a separate component here, but partitioning acts like an internal load balancer.

### Why Map Reduce?
- **Parallelism**: Multiple mappers + reducers.  
- **Scalability**: Add more nodes to handle more data.  
- **Fault tolerance**: Hadoop/YARN/YARN‑like frameworks automatically retry failed tasks.  
- **Simplicity**: Developers write only map and reduce functions; framework handles distribution.

## 3. Architecture Flow

```mermaid
graph TD
    A[Raw Order Logs] -->|Splits| B[Mapper 1]
    A -->|Splits| C[Mapper 2]
    A -->|Splits| D[Mapper 3]
    B -->|Emit (dish_id,1)| E[Shuffle & Sort]
    C -->|Emit (dish_id,1)| E
    D -->|Emit (dish_id,1)| E
    E -->|Partitioned by dish_id| F[Reducer 1]
    E -->|Partitioned by dish_id| G[Reducer 2]
    F -->|Aggregate count| H[Result: dish_id -> total_count]
    G -->|Aggregate count| H
    H --> I[Analytics Dashboard]
```

## 4. Production Case Study

**Zomato Analytics Platform**  
Zomato processes ~5 million orders/day. They use a *Hadoop* cluster for batch analytics:

1. **Data ingestion**: Kafka streams push order events into HDFS.  
2. **Map Phase**: Each mapper reads a partition of the log file, emits `(restaurant_id, 1)` for order count.  
3. **Shuffle**: Data is partitioned by `restaurant_id` across reducers.  
4. **Reduce Phase**: Each reducer sums counts per restaurant, producing total orders per restaurant for the day.  
5. **Post‑processing**: Results stored in a ClickHouse cluster for real‑time dashboards.

Result: Zomato can update *Top Restaurants* leaderboard every 5 minutes with negligible latency, even during peak traffic. If a mapper node dies, the framework re‑runs the map task on another node, ensuring high availability.

## 5. Trade-offs (Pros vs Cons)

| Pros | Cons |
|------|------|
| **Scalable parallel processing** – multiple nodes handle huge data. | **Batch nature** – not suitable for real‑time streaming (latency can be minutes). |
| **Fault tolerance** – framework retries failed tasks automatically. | **Resource overhead** – requires separate cluster, storage, and job scheduling. |
| **Simplicity for developers** – only map/reduce functions. | **Complexity in debugging** – errors hidden across distributed tasks. |
| **Consistent results** – deterministic aggregation. | **Data shuffling cost** – network I/O can be high if key distribution is skewed. |
| **Cost effective** – can run on commodity hardware. | **Limited to key-value paradigm** – not ideal for complex queries. |

## 6. System Design Interview Cheat Sheet

- **Map Reduce basics**: Map emits `(key, value)` → shuffle groups by key → Reduce aggregates.  
- **Key terms**: *Mapper*, *Reducer*, *Shuffle & Sort*, *Partitioner*, *Job Tracker* (or *YARN*).  
- **Scalability trick**: Add more nodes; each new node splits workload.  
- **Fault tolerance**: MapReduce retries failed tasks; data replicated in HDFS.  
- **When to use**: Large batch analytics (sales reports, log processing, word count). Not for low‑latency real‑time ops.
