# Beam Whitepaper

*Last updated: March 1, 2026*

---

## Decentralized Intelligence — A Censorship-Resistant Inference Network

**Petals-first · Heavy-model-capable · Onion-routable**

---

## Abstract

Beam is a decentralized inference fabric that uses Petals-style multi-host execution to run AI models too large for single machines. The network is backed by a hybrid of community GPUs and backbone infrastructure, with optional Tor/onion routing and progressive tokenized incentives.

**This is not a general-purpose "cheap ChatGPT."** Beam is purpose-built for:

- Ultra-large open models (Kimi-class, 30B–100B+)
- Censorship-resistant access
- User-contributed GPU compute
- Programmable, transport-aware inference routing

---

## 1. Core Architecture

### Components

- **Gateway API**: OpenAI-compatible user entrypoint
- **Scheduler / Router**: Chain construction and failover decisions
- **Control Plane**: Node registry, health index, assignment engine, accounting
- **Node Agent**: Provider-side daemon handling registration, heartbeat, and assignment
- **Petals Server**: Block-serving runtime for distributed transformer inference

### System Flow

```
User / Developer
      ↓
  Gateway API (OpenAI-compatible, transport-aware)
      ↓
  Scheduler / Router
      ↓
  Petals Client
      ↓
  Petals Swarm (Backbone + Community Nodes)
```

---

## 2. Model Classes

### Class A — Light (7–8B)
- Short inference chains
- Opportunistic routing allowed
- Suitable for single-node deployment

### Class B — Large (13–30B)
- Backbone-preferred routing
- Limited churn tolerance
- Multi-hop inference chains

### Class C — Heavy / Ultra (30–100B+)
- Mandatory backbone anchoring
- Early and final layers must use backbone nodes
- Node uptime requirement: ≥98% (rolling 24h)
- No hot block reassignment

---

## 3. Node Hardware Tiers

| Tier | VRAM | Heavy Model Eligibility |
|---|---|---|
| T1 | 6–8 GB | No |
| T2 | 10–12 GB | No |
| T3 | 16–24+ GB | Yes (middle layers only) |

Backbone nodes may exceed T3 specifications.

---

## 4. Transport & Privacy

### Transport Modes

| Mode | Transport | Intended Use | Latency |
|---|---|---|---|
| Fast | Direct TCP + TLS | Default usage | Lowest |
| Secure | TLS + pinned certs | Privacy-aware users | Medium |
| Onion | Tor (.onion) only | Censorship-resistant | Higher |

### Onion Routing Rules

- Onion nodes expose only `.onion` services
- Onion requests route exclusively through onion-capable nodes
- Separate scoring pools for onion vs clearnet
- At least one onion backbone node per heavy model

**Important:** Tor hides *who* you are, not *what* you send.

---

## 5. Protocol

### Authentication

All node communications are authenticated via HMAC-SHA256 signatures. Each registered node receives a `node_secret` used to sign heartbeats and API requests.

### Validation Rules

- Reject if absolute clock skew > 60 seconds
- Reject replayed `(node_id, timestamp, body_sha256)` tuples within a 5-minute window

### Node Lifecycle

```
joining → running → degraded → draining → offline
```

### Job Lifecycle

```
accepted → chained → running → completed | failed | expired
```

---

## 6. Tokenomics

### Token Overview

- **Token name**: DI (placeholder)
- **Type**: Utility accounting unit (off-chain in v0; on-chain in v1)
- Users interact with internal credits (not crypto)
- Nodes earn internal reward units (v0) or crypto DI tokens (v1)

### Inference Pricing

```
inference_cost = base_model_cost × chain_length × transport_factor × priority
```

| Class | Relative Cost |
|---|---|
| A (7–8B) | 1× |
| B (13–30B) | 2.5× |
| C (Kimi-class) | 6–10× |

### Node Rewards

```
reward = base_rate × uptime_factor × block_weight × transport_bonus × reliability_factor
```

- Uptime factor ∈ [0, 1]
- Block weight: higher for early/final layers
- Transport bonus: >1 for secure/onion nodes
- Reliability factor: penalizes failures

### Anti-Ponzi Guarantees

- No guaranteed returns
- Rewards strictly tied to measurable work
- No referral-for-yield loops
- No fixed emission schedules
- User credits cannot be traded or speculated on

---

## 7. Security & Threat Model

### Known Realities

- Nodes can see prompts in v0
- Nodes can log data
- Tor mitigates metadata leakage, not content exposure

### v0 Controls

- HMAC-signed heartbeats
- Canary inference checks
- Transport-segmented routing
- Rate limits and anomaly detection

### Threat Categories

| Threat | Mitigation |
|---|---|
| Malicious nodes returning bad outputs | Canary checks, redundant routing, reward decay, bans |
| Prompt logging by nodes | Clear disclosure, onion routing for metadata |
| Sybil attacks | Hardware benchmarks, VRAM thresholds, admission controls |
| Traffic correlation on Tor | Onion-only pools, no clearnet fallback |
| Gateway API abuse | Rate limiting, token pricing, anomaly detection |

### Explicit Non-Guarantees

The system does **not** guarantee:
- Prompt confidentiality
- Output correctness
- Resistance to state-level adversaries
- Trustless inference

---

## 8. Proof-of-Inference (PoInf)

### What It Proves

- Node participated in inference
- Duration and block range served

### What It Does NOT Prove

- Output correctness
- Prompt secrecy

### Eligibility Rules

A node is reward-eligible when:
- Job ID exists and signature is valid
- Node appears in the assigned chain for that job
- Reported assignment overlaps expected block range
- Heartbeat freshness is within tolerance
- No disqualifying error flags

---

## 9. Roadmap

| Milestone | Description |
|---|---|
| M0 | Local Petals swarm |
| M1 | Node app + registry |
| M2 | Gateway operational |
| M3 | Heavy model stabilized |
| M4 | Onion routing live |
| M5 | Off-chain token ledger |
| M6 | On-chain settlement (optional) |

---

## 10. Summary

> Beam is a censorship-resistant inference network for models that cannot run on single machines, built on Petals, stabilized by backbone nodes, and progressively decentralized via tokenized incentives.

Users pay in stable internal credits. Nodes earn crypto tokens for work. Platform revenue comes from credit sales, fees, and treasury tokens. Value and rewards are tied to actual usage, not speculation.
