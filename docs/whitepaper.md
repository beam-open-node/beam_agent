# Beam Whitepaper

*Last updated: March 11, 2026*

---

## Decentralized Intelligence — A Censorship-Resistant Inference Network

**Ollama-powered · MoE-optimized · Progressively decentralized**

---

## Abstract

Beam is a decentralized inference network that connects GPU providers to users who need access to open-weight AI models. In its initial version (v0), each node runs the full model locally via Ollama on dedicated GPU hardware. The network is coordinated by a central control plane that handles node registration, model assignment, and request routing.

Future versions will introduce distributed multi-node inference for models too large to fit on a single machine.

**Beam is purpose-built for:**

- Open-weight models served on community-contributed GPUs
- Censorship-resistant access to AI inference
- Efficient MoE (Mixture-of-Experts) models that maximize capability per VRAM dollar
- Progressive decentralization with tokenized incentives

---

## 1. Core Architecture

### Components

- **Gateway API**: OpenAI-compatible user entrypoint
- **Scheduler / Router**: Node selection and request routing
- **Control Plane**: Node registry, health index, assignment engine, accounting
- **Node Agent**: Provider-side daemon handling registration, heartbeat, and inference
- **Ollama Runtime**: Local model serving engine with GPU acceleration

### System Flow (v0 — Single-Node)

```
User / Developer
      |
  Gateway API (OpenAI-compatible)
      |
  Scheduler / Router
      |
  Node Agent (selected node)
      |
  Ollama (local GPU inference)
```

Each inference request is routed to a single node that runs the full model. There is no block splitting or multi-node coordination in v0.

### System Flow (v1+ — Distributed, Future)

```
User / Developer
      |
  Gateway API
      |
  Scheduler / Router
      |
  Distributed Inference Chain (multiple nodes)
```

For models too large to fit on a single machine, v1 will introduce multi-node inference where the model's layers are distributed across a chain of GPU nodes.

---

## 2. Model Classes

### Class S — Single-Node (Current)

- Full model runs on one machine via Ollama
- Suited for efficient MoE architectures (e.g. Qwen 3.5 35B-A3B: 35B total params, ~3B active)
- Requires a GPU with sufficient VRAM (e.g. 24 GB for current models)
- No multi-node coordination overhead

**Active models:**

| Model | Total Params | Active Params | Min VRAM |
|---|---|---|---|
| Qwen 3.5 35B-A3B | 35 B (MoE) | ~3 B | 24 GB |

**Coming soon:** Kimi K2.5, GLM-5 (reserved, not yet available).

### Class A — Light (Future)

- 7-8B parameter models
- Single-node deployment
- Low VRAM requirements

### Class B — Large (Future)

- 13-30B parameter models
- May require multi-node inference chains
- Backbone-preferred routing

### Class C — Heavy / Ultra (Future)

- 30-100B+ parameter models (e.g. DeepSeek V3, large MoE)
- Mandatory distributed inference across multiple nodes
- Backbone node anchoring for reliability
- Node uptime requirement: >=98% (rolling 24h)

---

## 3. Node Hardware Tiers

| Tier | VRAM | Eligible Classes |
|---|---|---|
| T1 | 6-8 GB | Future lightweight models only |
| T2 | 10-16 GB | Class A (future) |
| T3 | 24+ GB | Class S (current), Class B/C (future) |

Multi-GPU machines are supported. Ollama automatically utilizes all available GPUs for inference, and total VRAM is summed across devices.

---

## 4. Privacy & Future Transport

In v0, all traffic between users, the gateway, and nodes travels over standard HTTPS.

Future versions may introduce additional transport options:

| Mode | Transport | Intended Use | Latency |
|---|---|---|---|
| Standard | HTTPS | Default usage (v0) | Lowest |
| Secure | TLS + pinned certs | Privacy-aware users | Medium |
| Onion | Tor (.onion) only | Censorship-resistant | Higher |

---

## 5. Protocol

### Authentication

All node communications are authenticated via HMAC-SHA256 signatures. Each registered node receives a `node_secret` used to sign heartbeats and API requests.

### Validation Rules

- Reject if absolute clock skew > 60 seconds
- Reject replayed `(node_id, timestamp, body_sha256)` tuples within a 5-minute window

### Node Lifecycle

```
joining -> running -> degraded -> draining -> offline
```

### Job Lifecycle

```
accepted -> routed -> running -> completed | failed | expired
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
inference_cost = base_model_cost * token_count * priority
```

| Class | Relative Cost |
|---|---|
| S (MoE, current) | 1x |
| A (7-8B, future) | 1x |
| B (13-30B, future) | 2.5x |
| C (30-100B+, future) | 6-10x |

### Node Rewards

```
reward = base_rate * uptime_factor * reliability_factor
```

- Uptime factor: proportion of time the node is online and responsive [0, 1]
- Reliability factor: penalizes inference failures and timeouts

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
- The control plane is centralized in v0

### v0 Controls

- HMAC-signed heartbeats
- Canary inference checks
- Rate limits and anomaly detection

### Threat Categories

| Threat | Mitigation |
|---|---|
| Malicious nodes returning bad outputs | Canary checks, redundant routing, reward decay, bans |
| Prompt logging by nodes | Clear disclosure; future: encrypted inference |
| Sybil attacks | Hardware benchmarks, VRAM thresholds, admission controls |
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
- Duration and tokens served

### What It Does NOT Prove

- Output correctness
- Prompt secrecy

### Eligibility Rules

A node is reward-eligible when:
- Job ID exists and signature is valid
- Node is the assigned node for that job
- Heartbeat freshness is within tolerance
- No disqualifying error flags

---

## 9. Roadmap

| Milestone | Description |
|---|---|
| M0 | Single-node Ollama inference (Class S) — **current** |
| M1 | Node agent + registry + pairing |
| M2 | Gateway API operational with Qwen 3.5 35B-A3B |
| M3 | Additional MoE models (Kimi K2.5, GLM-5) |
| M4 | Distributed multi-node inference (Class B/C) |
| M5 | Off-chain token ledger |
| M6 | On-chain settlement (optional) |
| M7 | Transport privacy options (secure, onion) |

---

## 10. Summary

> Beam is a decentralized inference network that connects GPU providers to users who need access to open-weight AI models. In v0, each node runs the full model locally via Ollama, optimized for efficient MoE architectures. Future versions will expand to distributed multi-node inference for ultra-large models, with progressive decentralization via tokenized incentives.

Users pay in stable internal credits. Nodes earn crypto tokens for work. Platform revenue comes from credit sales, fees, and treasury tokens. Value and rewards are tied to actual usage, not speculation.
