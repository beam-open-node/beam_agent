# Configuration Reference

*Last updated: March 11, 2026*

---

## Overview

The Beam Node Agent uses a layered configuration system:

1. **Defaults** — Built-in sensible defaults
2. **Config file** — YAML file (default: `config.yaml`)
3. **Environment variables** — Override any config value

Environment variables take the highest precedence.

---

## Config File Structure

```yaml
control_plane:
  url: "https://www.openbeam.me"

ollama:
  base_url: "http://localhost:11434"
  model_tag: "qwen3.5:35b-a3b"

agent:
  heartbeat_interval_sec: 15
  max_retries: 5
  state_file: "node_state.json"
  pairing_token: null        # Pre-set pairing token
  pairing_host: "0.0.0.0"
  pairing_ports:
    - 51337
    - 51338
    - 51339
    - 51340
  mock_inference: false      # Set true for testing without GPU
  capabilities:
    max_concurrent_jobs: 1
    max_model_class: "S"
    preferred_model_id: null  # null = accept any assigned model
```

---

## Section Reference

### control_plane

| Field | Type | Default | Description |
|---|---|---|---|
| `url` | string | `https://www.openbeam.me` | Beam control plane server URL |

### ollama

| Field | Type | Default | Description |
|---|---|---|---|
| `base_url` | string | `http://localhost:11434` | Base URL of the local Ollama API |
| `model_tag` | string | `qwen3.5:35b-a3b` | Ollama model tag to pull and serve |

### agent

| Field | Type | Default | Description |
|---|---|---|---|
| `heartbeat_interval_sec` | int | `15` | Seconds between heartbeats to the control plane |
| `max_retries` | int | `5` | Maximum retry attempts for failed operations |
| `state_file` | string | `node_state.json` | Path to persist node identity (node_id, node_secret) |
| `pairing_token` | string | `null` | Pre-set pairing token to skip interactive pairing |
| `pairing_host` | string | `0.0.0.0` | Host for the local pairing HTTP server |
| `pairing_ports` | list | `[51337, ...]` | Ports to try for the local pairing server |
| `mock_inference` | bool | `false` | Enable mock inference responses (no GPU needed) |

### capabilities

| Field | Type | Default | Description |
|---|---|---|---|
| `max_concurrent_jobs` | int | `1` | Maximum inference jobs this node handles simultaneously |
| `max_model_class` | string | `"S"` | Maximum model class to accept: `S` (current). Future classes: `A`, `B`, `C` |
| `preferred_model_id` | string | `null` | Preferred model identifier. `null` = accept any assigned model |
