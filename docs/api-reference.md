# API Reference

*Last updated: March 1, 2026*

---

## Overview

The Beam Gateway API provides an **OpenAI-compatible** interface for submitting inference requests to the decentralized network. All API endpoints use JSON for request and response bodies.

**Base URL**: `https://www.openbeam.me/api/v1`

---

## Authentication

All API requests require authentication via API key or session token.

```
Authorization: Bearer <your-api-key>
```

---

## Inference

### Chat Completions

`POST /chat/completions`

Submit a chat-style inference request.

**Request Body:**

```json
{
  "model": "tiiuae/falcon-7b-instruct",
  "messages": [
    { "role": "system", "content": "You are a helpful assistant." },
    { "role": "user", "content": "Explain quantum computing." }
  ],
  "max_tokens": 256,
  "temperature": 0.7,
  "stream": false
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `model` | string | Yes | Model identifier (e.g. `tiiuae/falcon-7b-instruct`) |
| `messages` | array | Yes | Array of message objects with `role` and `content` |
| `max_tokens` | int | No | Maximum tokens to generate (default: 256) |
| `temperature` | float | No | Sampling temperature 0.0–2.0 (default: 1.0) |
| `stream` | bool | No | Enable streaming response (default: false) |

**Response:**

```json
{
  "id": "chat-abc123",
  "object": "chat.completion",
  "created": 1709251200,
  "model": "tiiuae/falcon-7b-instruct",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Quantum computing uses quantum bits..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 24,
    "completion_tokens": 128,
    "total_tokens": 152
  }
}
```

---

## Transport Modes

You can specify a transport mode for privacy-aware routing:

```json
{
  "model": "tiiuae/falcon-7b-instruct",
  "messages": [...],
  "transport": "onion"
}
```

| Mode | Description | Latency Impact |
|---|---|---|
| `fast` | Direct TCP + TLS (default) | Lowest |
| `secure` | TLS with pinned certificates | Medium |
| `onion` | Tor .onion routing only | Higher |

---

## Node Registration

### Register Node

`POST /nodes/register`

Register a new GPU node with the network.

**Request Body:**

```json
{
  "protocol_version": "1.0",
  "machine_fingerprint": "sha256_hex_string",
  "gpu": {
    "name": "RTX 4090",
    "vram_gb": 24,
    "count": 1
  },
  "software": {
    "node_agent_version": "0.1.0",
    "petals_version": "2.3.0"
  },
  "transports": ["fast"],
  "capabilities": {
    "supports_heavy_middle_layers": true,
    "max_concurrent_jobs": 1
  }
}
```

**Response:**

```json
{
  "protocol_version": "1.0",
  "node_id": "uuid",
  "node_secret": "base64_string",
  "assignment": {
    "model_id": "tiiuae/falcon-7b-instruct",
    "block_range": [0, 16]
  },
  "heartbeat_interval_sec": 15
}
```

---

## Heartbeat

### Send Heartbeat

`POST /nodes/heartbeat`

**Signed request required.** Nodes must include HMAC authentication headers.

**Required Headers:**

| Header | Description |
|---|---|
| `X-Node-Id` | The node's unique identifier |
| `X-Timestamp` | Unix timestamp (seconds) |
| `X-Body-SHA256` | SHA-256 hash of the request body |
| `X-Signature` | HMAC-SHA256 signature |

**Signature Computation:**

```
canonical_string = timestamp + "\n" + sha256(body)
signature = HMAC_SHA256(node_secret, canonical_string)
```

**Request Body:**

```json
{
  "protocol_version": "1.0",
  "node_id": "uuid",
  "timestamp": 1709251200,
  "status": "running",
  "metrics": {
    "uptime_sec": 3600,
    "tokens_processed": 128000,
    "req_ok": 512,
    "req_err": 3,
    "p50_latency_ms": 180,
    "p95_latency_ms": 540
  },
  "active_jobs": [],
  "current_assignment": {
    "model_id": "tiiuae/falcon-7b-instruct",
    "block_range": [0, 16],
    "assignment_epoch": 42
  }
}
```

---

## Assignment

### Fetch Assignment

`GET /nodes/{node_id}/assignment`

**Signed request required.**

**Response:**

```json
{
  "protocol_version": "1.0",
  "model_id": "tiiuae/falcon-7b-instruct",
  "block_range": [0, 16],
  "assignment_epoch": 42,
  "effective_at": 1709251200,
  "initial_peers": ["/ip4/..."]
}
```

---

## Error Codes

All error responses follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE_STRING",
    "message": "Human readable description",
    "request_id": "req_uuid",
    "details": {}
  }
}
```

### Authentication & Identification Errors

| Error Code | HTTP Status | Description |
|---|---|---|
| `MISSING_HEADERS` | 400 | Required headers (X-Node-Id, X-Signature, etc.) are missing |
| `INVALID_SIGNATURE` | 401 | HMAC signature verification failed |
| `CLOCK_SKEW` | 401 | Request timestamp is outside the allowed window (>60s) |
| `REPLAY_DETECTED` | 401 | This signed request has already been processed |
| `UNKNOWN_NODE` | 403 | Node ID is not found in the registry |
| `NODE_BANNED` | 403 | Node is permanently banned from the network |

### Business Logic Errors

| Error Code | HTTP Status | Description |
|---|---|---|
| `INVALID_SCHEMA` | 400 | Request body does not match the JSON schema |
| `UNSUPPORTED_VERSION` | 400 | Protocol version is not supported |
| `NODE_FINGERPRINT_MISMATCH` | 409 | Machine fingerprint does not match the registered node |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests from this node/user |
| `NO_CAPACITY` | 503 | Scheduler cannot find a valid chain for the request |
| `JOB_NOT_FOUND` | 404 | Job ID referenced does not exist |
| `PAIRING_TOKEN_INVALID` | 400 | Pairing token is invalid or already used |
| `PAIRING_TOKEN_EXPIRED` | 400 | Pairing token has expired |
| `NODE_ALREADY_CLAIMED` | 409 | Node is already linked to another user |
| `NODE_NOT_ELIGIBLE` | 409 | Node does not meet eligibility requirements |

### Internal Errors

| Error Code | HTTP Status | Description |
|---|---|---|
| `INTERNAL_ERROR` | 500 | Unexpected server-side failure |
| `UPSTREAM_TIMEOUT` | 504 | Timeout communicating with upstream services |

---

## Model Classes

| Class | Model Size | Example |
|---|---|---|
| A (Light) | 7–8B parameters | `tiiuae/falcon-7b-instruct` |
| B (Large) | 13–30B parameters | — |
| C (Heavy) | 30–100B+ parameters | Kimi-class models |

---

## Rate Limits

- Default: 60 requests per minute per API key
- Burst: Up to 10 concurrent requests
- Rate limit headers are included in responses:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`
