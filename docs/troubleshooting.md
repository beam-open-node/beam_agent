# Troubleshooting

*Last updated: March 11, 2026*

---

## Ollama Not Using the GPU

**Symptoms:** Inference is extremely slow, or `ollama ps` shows the model running on CPU.

**Cause:** Ollama cannot detect your NVIDIA GPU. This usually happens because `pciutils` is not installed (common on minimal cloud images like RunPod).

**Fix:**

```bash
apt-get update && apt-get install -y pciutils
```

Then reinstall Ollama so it re-detects the GPU:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Verify GPU detection:

```bash
ollama ps
```

The output should show the model loaded on a GPU device. You can also check with `nvidia-smi` that Ollama processes appear in the GPU process list.

---

## Slow Inference

**Symptoms:** Responses take a long time (e.g. 30+ seconds for short replies).

**Possible causes:**

1. **Thinking mode enabled.** Qwen 3.5 supports a "thinking" mode that generates an internal chain-of-thought before responding. If the client or control plane sends requests with thinking enabled, the model produces significantly more tokens (most of which are hidden from the user). This is expected behavior — disable thinking mode on the client side if faster responses are needed.

2. **Model cold start.** The first request after the model is loaded into VRAM takes longer because Ollama must initialize the model weights. Subsequent requests will be faster. If the model was evicted from VRAM (due to inactivity timeout), the next request triggers a reload.

3. **GPU not detected.** See "Ollama Not Using the GPU" above.

---

## Agent Not Starting

**Symptoms:** The agent exits immediately or fails to connect to Ollama.

**Check that the Ollama daemon is running:**

```bash
systemctl status ollama
```

If Ollama is not running, start it:

```bash
systemctl start ollama
```

Or, if systemd is not available (e.g. inside a container):

```bash
ollama serve &
```

Then retry starting the agent:

```bash
cd beam_agent && bash start_agent.sh
```

---

## Pairing Issues

**Symptoms:** The 6-digit pair code is displayed, but entering it in the Rent Panel fails or times out.

**Possible causes:**

1. **Network connectivity.** Ensure the machine has outbound internet access to `https://www.openbeam.me`. Test with:
   ```bash
   curl -s https://www.openbeam.me/api/v1/health
   ```

2. **Pairing port conflict.** The agent starts a local HTTP server on one of the configured pairing ports (default: 51337–51340). If all ports are in use, pairing will fail. Check with:
   ```bash
   ss -tlnp | grep 5133
   ```

3. **Code expired.** Pair codes expire after a few minutes. If the code has expired, restart the agent to generate a new one.

4. **Already paired.** If the node was previously paired to a different account, it cannot be re-paired without first being released. Contact the Beam team if you need to transfer a node.

---

## VRAM Reporting

**Symptoms:** The control plane shows incorrect VRAM for your machine.

The agent auto-detects GPU information via `nvidia-smi`. For multi-GPU machines, total VRAM is the sum across all detected GPUs.

To override the reported values, set environment variables:

```bash
export BEAM_GPU_VRAM_GB=48     # e.g. 2x 24 GB GPUs
export BEAM_GPU_COUNT=2
export BEAM_GPU_NAME="RTX 4090"
```

---

## Model Pull Fails

**Symptoms:** The installer fails during model download with a timeout or disk space error.

1. **Disk space.** The model weights are approximately 16.5 GB. Ensure you have at least 20 GB of free disk space on the volume where Ollama stores models (defaults to `~/.ollama`, or `/workspace/.ollama` on RunPod).

2. **Network timeout.** On slow connections, the download may time out. Retry:
   ```bash
   ollama pull qwen3.5:35b-a3b
   ```

3. **Custom storage path.** If your root filesystem is small, set `OLLAMA_MODELS` to a path on a larger volume before pulling:
   ```bash
   export OLLAMA_MODELS=/workspace/.ollama/models
   ollama pull qwen3.5:35b-a3b
   ```

---

## Still Stuck?

Contact the Beam team or check the project repository for the latest updates.
