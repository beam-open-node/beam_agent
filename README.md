# Beam Node Agent

The Beam Node Agent is the provider-side daemon that connects your GPU to the Beam inference network. Each node runs the full model locally via [Ollama](https://ollama.com), serving inference requests from the Beam control plane.

*Last updated: March 11, 2026*

---

## Prerequisites

| Requirement | Details |
|---|---|
| **OS** | Linux (Ubuntu 20.04+ recommended) |
| **GPU** | NVIDIA GPU with up-to-date drivers and sufficient VRAM (e.g. RTX 4090 24 GB) |
| **Network** | Outbound internet access to reach the control plane |

---

## Quick Start

```bash
curl -fsSL https://raw.githubusercontent.com/beam-open-node/beam_agent/main/setup_runpod.sh | bash
```

### What the Installer Does

1. Installs Ollama and pulls the active model (~16.5 GB, stored on `/workspace` if available)
2. Clones this repository and sets up the Python environment
3. Writes `config.yaml` and `start_agent.sh`
4. Starts the agent and prints a **6-digit pair code** — enter it in the Rent Panel at [openbeam.me](https://www.openbeam.me)

To restart after a pod reboot:

```bash
cd beam_agent && bash start_agent.sh
```

---

## Active Model

| Model | Parameters | Active Params | Class |
|---|---|---|---|
| Qwen 3.5 35B-A3B | 35 B (MoE) | ~3 B | S |

Coming soon: Kimi K2.5, GLM-5 (reserved, not yet available).

---

## Configuration

The agent reads its settings from `config.yaml`, which the installer creates for you. Key options include the control-plane URL, Ollama endpoint, and pairing ports.

See the full reference: [docs/configuration.md](docs/configuration.md)

---

## Environment Variables

Override any config value with an environment variable. The most common ones:

| Variable | Description | Default |
|---|---|---|
| `BEAM_CONTROL_PLANE_URL` | Control plane server URL | `https://www.openbeam.me` |
| `BEAM_OLLAMA_URL` | Ollama API base URL | `http://localhost:11434` |
| `BEAM_OLLAMA_MODEL` | Ollama model tag to serve | `qwen3.5:35b-a3b` |
| `BEAM_GPU_NAME` | GPU name reported to control plane (auto-detected via nvidia-smi) | — |
| `BEAM_GPU_VRAM_GB` | GPU VRAM in GB (auto-detected) | — |
| `BEAM_GPU_COUNT` | Number of GPUs (auto-detected) | — |
| `BEAM_PAIRING_TOKEN` | Pre-set pairing token (skips interactive pairing) | — |
| `BEAM_MOCK_INFERENCE` | `true` to run without a real GPU | `false` |

Full list: [docs/node-agent-setup.md](docs/node-agent-setup.md#environment-variables)

---

## Documentation

| Doc | Description |
|---|---|
| [Node Agent Setup](docs/node-agent-setup.md) | Full setup guide and environment variables |
| [Configuration Reference](docs/configuration.md) | Complete `config.yaml` field reference |
| [Troubleshooting](docs/troubleshooting.md) | Known issues and debugging tips |
| [API Reference](docs/api-reference.md) | Control-plane API endpoints |
| [Whitepaper](docs/whitepaper.md) | Architecture, tokenomics, and roadmap |

---

## Support

If you get stuck, see the [Troubleshooting Guide](docs/troubleshooting.md) or contact the Beam team.
