# Node Agent Setup

*Last updated: March 1, 2026*

---

## Overview

The Beam Node Agent is the provider-side daemon that connects your GPU to the Beam decentralized inference network. It handles registration, heartbeat reporting, assignment management, and inference execution via Petals.

---

## Quick Start

### Linux / macOS

```bash
curl -fsSL https://raw.githubusercontent.com/beam-open-node/beam_agent/main/install.sh -o install.sh
bash install.sh
```

### Windows (PowerShell)

```powershell
Invoke-WebRequest -Uri https://raw.githubusercontent.com/beam-open-node/beam_agent/main/install.ps1 -OutFile install.ps1
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

### What the Installer Does

1. Downloads the correct node agent binary for your OS
2. Writes `config.yaml` with default settings
3. Sets up the Petals runtime environment
4. Starts the agent and prints a 6-digit pair code
5. You enter that code in the Rent Panel to link your machine

---

## Configuration

The agent reads configuration from `config.yaml`. Here's a reference:

```yaml
control_plane:
  url: "https://www.openbeam.me"

petals:
  port: 31337
  # public_ip: "1.2.3.4"    # Optional, auto-detect otherwise
  gpu_vram_limit: 0.9

agent:
  heartbeat_interval_sec: 15
  state_file: "node_state.json"
  transports:
    - "fast"
  # mock_inference: true      # For testing without real GPU
  # pairing_token: "paste-pairing-token-here"
  pairing_host: "127.0.0.1"
  pairing_ports:
    - 51337
    - 51338
    - 51339
    - 51340
  # onion_address: "abc123.onion"   # Required if using onion transport
  capabilities:
    supports_heavy_middle_layers: true
    max_concurrent_jobs: 1
    # max_blocks: 12
    # max_model_class: "B"
```

---

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `BEAM_CONTROL_PLANE_URL` | Control plane server URL | `http://localhost:8080` |
| `BEAM_PETALS_PYTHON` | Path to the Python interpreter with Petals installed | System Python |
| `BEAM_PAIRING_TOKEN` | Pre-set pairing token (skips interactive pairing) | — |
| `BEAM_PAIRING_PORT` | Single pairing port override | — |
| `BEAM_PAIRING_PORTS` | Comma-separated pairing port list | `51337,51338,51339,51340` |
| `BEAM_MOCK_INFERENCE` | Set `true` to run mock inference (no GPU needed) | `false` |
| `BEAM_MAX_BLOCKS` | Maximum transformer blocks the agent will serve | — |
| `BEAM_GPU_NAME` | Override GPU name detection | Auto-detect |
| `BEAM_GPU_VRAM_GB` | Override GPU VRAM detection | Auto-detect |
| `BEAM_GPU_COUNT` | Override GPU count detection | Auto-detect |
| `BEAM_SINGLE_NODE` | Enable single-node mode | `false` |
| `BEAM_HOP_COUNTS` | Override hop counts per model class (e.g. `A=1,B=1,C=1`) | — |

---

## Transport Modes

The agent supports three transport modes:

| Mode | Description |
|---|---|
| `fast` | Direct TCP + TLS — lowest latency (default) |
| `secure` | TLS with pinned certificates — privacy-aware |
| `onion` | Tor .onion services only — censorship-resistant |

To enable onion transport, set `onion_address` in your config and add `"onion"` to the transports list.

---

## Pairing Process

1. Start the node agent — it will print a 6-digit pair code
2. Open the Beam web app → Rent Panel
3. Enter the pair code to link your machine to your account
4. The agent will begin receiving assignments and serving inference

---

## Releases

Pre-built binaries are available at:
`https://github.com/beam-open-node/beam_agent/releases/latest`

Expected assets:
- `beam-node-agent-linux`
- `beam-node-agent-macos`
- `beam-node-agent-windows.exe`

---

## Support

If you encounter issues, see the [Troubleshooting Guide](./troubleshooting.md) or contact the Beam team.
