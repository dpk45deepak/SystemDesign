# Transport Layer Explained: TCP vs UDP

> Video Reference: [Transport Layer Explained: TCP vs UDP](https://www.youtube.com/watch?v=QyrHol2Ylfo)

## 1. Asli Problem Kya Hai? (The Core Why)

Soch lo tum Swiggy se order kar rahe ho. Order place karte hi ek confirmation message tumhare phone pe aata hai aur delivery driver ko location milti hai. Agar packet loss ho jaata hai, driver ko galat address mil sakta hai ya confirmation miss ho sakta hai – customers unhappy, revenue loss.  

Ek high‑traffic system ko do cheezein chahiye:

1. **Reliability** – Order confirmation jaise critical data hamesha deliver ho.
2. **Speed** – Live location updates, live chat, aur video calls ko lag‑less hona chahiye.

Yeh dual requirement hi TCP vs UDP ka debate shuru kar deti hai. Agar hum sirf speed chahte hain aur reliability ignore karte hain, traffic jam ho sakta hai. Agar sirf reliability chahte hain aur speed ignore karte hain, user experience degrade ho jayega.

## 2. Core Architecture & Mechanisms

### TCP (Transmission Control Protocol)

- **Connection‑oriented**: Handshake (SYN → SYN‑ACK → ACK) se connection establish hota hai.  
- **Reliability**: Sequence numbers + ACKs + retransmission. Agar packet miss ho, receiver request re‑send.  
- **Flow control**: Window size se sender ko pata chalta hai receiver kitna buffer kar sakta hai.  
- **Congestion control**: Slow start, congestion avoidance.  
- **Ordered delivery**: Packets ke order ko maintain karta hai, out‑of‑order packets buffer honge.  
- **Overhead**: 20‑bytes header + 4‑byte checksum.  

**Intuition**: TCP ko aise samjho jaise IRCTC booking system. Har seat reservation ke liye ek ticket issue hota hai, aur agar koi step fail ho jaye, system retry karega. Customer ko guarantee milti hai ki ticket confirm hoga.

### UDP (User Datagram Protocol)

- **Connection‑less**: No handshake, direct datagram send.  
- **No retransmission**: Agar packet miss ho, data loss hota hai.  
- **No flow control**: Receiver ko buffer limit se pehle packet drop ho sakta hai.  
- **Low overhead**: 8‑bytes header + 2‑byte checksum.  
- **Fast**: Latency kam.  

**Intuition**: UDP ko aise samjho jaise Ola driver ka real‑time location update. Driver ko instantly apni location server ko bhejni hoti hai, loss ki chinta nahi hoti. Agar ek packet miss ho, next packet se update ho jayega.

### Decision Factors

| Factor | TCP | UDP |
|--------|-----|-----|
| Reliability | ✔️ | ❌ |
| Order | ✔️ | ❌ |
| Latency | ❌ | ✔️ |
| Overhead | ✔️ | ❌ |
| Use‑case | Transaction, file transfer, web traffic | Streaming, gaming, real‑time updates |

## 3. Architecture Flow

```mermaid
graph TD
  A[Client] -->|SYN| B[Server]
  B -->|SYN‑ACK| A
  A -->|ACK| B
  A -->|Data (TCP)| B
  B -->|ACK| A
  A -->|Data (UDP)| B
  B -->|Ack (optional)| A
```

- **TCP Handshake**: Shows three‑way handshake before data transfer.  
- **UDP Flow**: Direct datagram transfer without handshake.  

## 4. Production Case Study

**WhatsApp (WhatsApp Business API)**  
- **Signaling & Control**: Uses **TCP** (XMPP over TLS) to establish chat sessions, ensuring messages arrive in order.  
- **Media Transfer**: Uses **UDP** via WebRTC for voice/video calls. Speed aur low latency is priority; occasional packet loss is acceptable because codecs handle it.

**Uber**  
- **Ride Request & Confirmation**: **TCP** for reliability – rider’s request must reach driver, driver’s acceptance must reach rider.  
- **Real‑time Driver Location**: **UDP** over gRPC‑web for minimal delay; small packet loss is fine as GPS data is periodically refreshed.

## 5. Trade‑offs (Pros vs Cons)

| Pros | Cons |
|------|------|
| **TCP**<br>- Guaranteed delivery<br>- Ordered packets<br>- Congestion & flow control<br>- Error‑free data | - Higher latency<br>- More overhead<br>- Slower for large data bursts |
| **UDP**<br>- Low latency<br>- Minimal overhead<br>- Simple to implement<br>- Better for multicast | - No delivery guarantee<br>- No ordering<br>- No flow control<br>- Susceptible to packet loss |

## 6. System Design Interview Cheat Sheet

- **TCP vs UDP**: TCP = reliable, ordered, connection‑oriented; UDP = fast, connectionless, unordered.  
- **Handshake**: TCP uses 3‑way handshake; UDP has none.  
- **Reliability Mechanisms**: Sequence numbers, ACKs, retransmission (TCP); none (UDP).  
- **Use‑cases**: Web traffic, file transfer → TCP; VoIP, gaming, live streaming → UDP.  
- **Trade‑offs**: Higher latency vs higher reliability; choose based on application constraints (latency tolerance vs data integrity).
