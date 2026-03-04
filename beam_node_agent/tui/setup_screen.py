"""3-step setup wizard shown when no config.yaml exists."""
from __future__ import annotations

import os

import yaml
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Middle, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Label,
    Static,
)

_DEFAULT_CONTROL_PLANE = "https://www.openbeam.me"
_DEFAULT_CONFIG_PATH = "config.yaml"

_STEPS = ["Control Plane", "Config File", "Confirm & Start"]


class SetupScreen(Screen):
    """Interactive wizard to create config.yaml and start the agent."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back", show=False),
    ]

    CSS = """
    SetupScreen {
        align: center middle;
    }

    #wizard-box {
        width: 70;
        height: auto;
        border: round $primary;
        padding: 1 2;
        background: $surface;
    }

    #step-indicator {
        text-align: center;
        color: $text-muted;
        margin-bottom: 1;
    }

    #step-title {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }

    .field-label {
        margin-top: 1;
        color: $text-muted;
    }

    Input {
        margin-top: 0;
    }

    #confirm-summary {
        background: $panel;
        padding: 1;
        margin: 1 0;
    }

    #btn-row {
        margin-top: 2;
        align: center middle;
    }

    Button {
        margin: 0 1;
    }

    #error-msg {
        color: $error;
        margin-top: 1;
        text-align: center;
    }
    """

    def __init__(self, config_path: str = _DEFAULT_CONFIG_PATH) -> None:
        super().__init__()
        self._config_path = config_path
        self._step = 0
        self._control_plane_url = _DEFAULT_CONTROL_PLANE

    # ------------------------------------------------------------------
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Center():
            with Middle():
                with Vertical(id="wizard-box"):
                    yield Static("", id="step-indicator")
                    yield Static("", id="step-title")
                    # Step 0 – control plane URL
                    yield Label("Control Plane URL:", classes="field-label", id="lbl-cp")
                    yield Input(
                        placeholder=_DEFAULT_CONTROL_PLANE,
                        id="input-cp",
                        value=_DEFAULT_CONTROL_PLANE,
                    )
                    # Step 1 – config path
                    yield Label("Config file path:", classes="field-label", id="lbl-cfg")
                    yield Input(
                        placeholder=_DEFAULT_CONFIG_PATH,
                        id="input-cfg",
                        value=self._config_path,
                    )
                    # Step 2 – confirm summary
                    yield Static("", id="confirm-summary")
                    yield Static("", id="error-msg")
                    with Center(id="btn-row"):
                        yield Button("Back", id="btn-back", variant="default")
                        yield Button("Continue", id="btn-next", variant="primary")
        yield Footer()

    def on_mount(self) -> None:
        self._render_step()

    # ------------------------------------------------------------------
    def _render_step(self) -> None:
        total = len(_STEPS)
        indicator = self.query_one("#step-indicator", Static)
        indicator.update(f"Step {self._step + 1} of {total}  —  {_STEPS[self._step]}")

        title = self.query_one("#step-title", Static)
        title.update(_STEPS[self._step])

        # Show/hide widgets per step
        lbl_cp = self.query_one("#lbl-cp")
        input_cp = self.query_one("#input-cp", Input)
        lbl_cfg = self.query_one("#lbl-cfg")
        input_cfg = self.query_one("#input-cfg", Input)
        summary = self.query_one("#confirm-summary", Static)
        back_btn = self.query_one("#btn-back", Button)
        next_btn = self.query_one("#btn-next", Button)

        lbl_cp.display = self._step == 0
        input_cp.display = self._step == 0
        lbl_cfg.display = self._step == 1
        input_cfg.display = self._step == 1
        summary.display = self._step == 2
        back_btn.disabled = self._step == 0

        if self._step == 2:
            cfg_path = self.query_one("#input-cfg", Input).value.strip() or _DEFAULT_CONFIG_PATH
            cp_url = self.query_one("#input-cp", Input).value.strip() or _DEFAULT_CONTROL_PLANE
            summary.update(
                f"[b]Control Plane:[/b] {cp_url}\n"
                f"[b]Config file:[/b]   {cfg_path}\n\n"
                f"This will write [bold]{cfg_path}[/bold] and start the agent."
            )
            next_btn.label = "Write Config & Start"
        else:
            next_btn.label = "Continue"

        self.query_one("#error-msg", Static).update("")

    # ------------------------------------------------------------------
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-back" and self._step > 0:
            self._step -= 1
            self._render_step()
        elif event.button.id == "btn-next":
            self._advance()

    def _advance(self) -> None:
        error = self.query_one("#error-msg", Static)
        if self._step == 0:
            self._step = 1
            self._render_step()
        elif self._step == 1:
            cfg_val = self.query_one("#input-cfg", Input).value.strip() or _DEFAULT_CONFIG_PATH
            parent = os.path.dirname(os.path.abspath(cfg_val))
            if not os.path.isdir(parent):
                error.update(f"Directory does not exist: {parent}")
                return
            self._step = 2
            self._render_step()
        elif self._step == 2:
            self._write_config_and_start()

    def _write_config_and_start(self) -> None:
        error = self.query_one("#error-msg", Static)
        cp_url = (
            self.query_one("#input-cp", Input).value.strip() or _DEFAULT_CONTROL_PLANE
        ).rstrip("/")
        cfg_path = (
            self.query_one("#input-cfg", Input).value.strip() or _DEFAULT_CONFIG_PATH
        )

        config_data = {
            "control_plane": {"url": cp_url},
            "petals": {"port": 31337, "gpu_vram_limit": 0.9},
            "agent": {
                "heartbeat_interval_sec": 15,
                "state_file": "node_state.json",
                "transports": ["fast"],
                "pairing_host": "127.0.0.1",
                "pairing_ports": [51337, 51338, 51339, 51340],
                "capabilities": {
                    "supports_heavy_middle_layers": True,
                    "max_concurrent_jobs": 1,
                },
            },
        }

        try:
            with open(cfg_path, "w") as fh:
                yaml.dump(config_data, fh, default_flow_style=False)
        except OSError as exc:
            error.update(f"Failed to write config: {exc}")
            return

        # Signal the app to transition to the dashboard
        from beam_node_agent.tui.app import StartDashboard

        self.app.post_message(StartDashboard(config_path=cfg_path))
