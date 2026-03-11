import json
import logging
import time
import urllib.request
import urllib.error
from typing import List, Optional

log = logging.getLogger(__name__)


class OllamaWrapper:
    """
    Drop-in replacement for PetalsWrapper that delegates inference to a
    local Ollama instance.  Implements the same public interface so the
    rest of NodeAgent doesn't need to know which backend is active.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model_tag: str = "qwen3.5:35b-a3b",
    ):
        self.base_url = base_url.rstrip("/")
        self.model_tag = model_tag
        self._running = False
        self._started_at: Optional[int] = None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _api(self, path: str, payload: Optional[dict] = None, timeout: float = 10.0) -> dict:
        """Make a JSON request to the Ollama HTTP API."""
        url = f"{self.base_url}{path}"
        if payload is not None:
            data = json.dumps(payload).encode()
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        else:
            req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())

    def _model_loaded(self) -> bool:
        """Check whether the target model is available in Ollama."""
        try:
            data = self._api("/api/tags")
            models = data.get("models", [])
            for m in models:
                if m.get("name", "").startswith(self.model_tag):
                    return True
            return False
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Public interface (mirrors PetalsWrapper)
    # ------------------------------------------------------------------

    def start(self, model_id: str, block_range: str, initial_peers: Optional[list] = None):
        """
        Ensure the model is pulled and ready in Ollama.
        block_range and initial_peers are accepted for interface compat but ignored.
        """
        if self._running:
            log.info("OllamaWrapper already marked as running.")
            return

        log.info(
            "OllamaWrapper.start: model_id=%s (ollama_tag=%s), block_range=%s (ignored)",
            model_id, self.model_tag, block_range,
        )

        # Pull model if not already present (streaming progress).
        if not self._model_loaded():
            log.info("Model %s not found locally — pulling via Ollama...", self.model_tag)
            try:
                url = f"{self.base_url}/api/pull"
                data = json.dumps({"name": self.model_tag, "stream": True}).encode()
                req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=600) as resp:
                    for line in resp:
                        try:
                            chunk = json.loads(line)
                            status = chunk.get("status", "")
                            if "pulling" in status or "downloading" in status:
                                total = chunk.get("total", 0)
                                completed = chunk.get("completed", 0)
                                if total:
                                    pct = completed / total * 100
                                    log.info("Pull progress: %s (%.1f%%)", status, pct)
                            elif status:
                                log.info("Pull: %s", status)
                        except Exception:
                            pass
                log.info("Model pull complete: %s", self.model_tag)
            except Exception as exc:
                log.error("Failed to pull model %s: %s", self.model_tag, exc)
                raise

        self._running = True
        self._started_at = int(time.time())
        log.info("OllamaWrapper is ready (model=%s).", self.model_tag)

    def stop(self):
        """No-op — Ollama is an external daemon, we don't manage its lifecycle."""
        self._running = False
        log.info("OllamaWrapper stopped (Ollama daemon still running).")

    def is_running(self) -> bool:
        """Check if Ollama is reachable and the model is available."""
        if not self._running:
            return False
        try:
            self._api("/api/tags", timeout=5)
            return True
        except Exception:
            return False

    def local_p2p_addrs(self) -> List[str]:
        """No P2P addresses in single-node Ollama mode."""
        return []

    def status_snapshot(self) -> dict:
        now = int(time.time())
        running = self.is_running()
        uptime_sec = None
        if running and self._started_at is not None:
            uptime_sec = max(0, now - self._started_at)
        return {
            "running": running,
            "started_at": self._started_at,
            "uptime_sec": uptime_sec,
            "last_exit_code": None,
            "last_exit_at": None,
        }

    def recent_logs(self, limit: int = 50) -> list[str]:
        return []
