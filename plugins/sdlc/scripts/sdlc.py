#!/usr/bin/env python3
"""Project-side helper of the sdlc plugin.

.sdlc.yml is the single source of truth. This script reads it and renders the
files derived from it (AGENTS.md managed block, CLAUDE.md import, Makefile,
BACKLOG.md, .sdlc/state.json). Hooks and commands call it; the mod panel will
too. Standard library only: macOS ships Python 3.9 without PyYAML, so .sdlc.yml
stays a flat subset of YAML (scalars and lists) parsed below.

Usage:
  sdlc.py init --profiles python-uv[:dir],... --modules spec,plan,... [--autonomy] [--force]
  sdlc.py render
  sdlc.py get <key>
  sdlc.py status [--json]
  sdlc.py next [--item <slug>]
  sdlc.py set modules|autonomy|stop_check <value>
"""
import argparse
import json
import os
import sys

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = ".sdlc.yml"
STATE = os.path.join(".sdlc", "state.json")
BEGIN = "<!-- sdlc:begin (generated from .sdlc.yml, edit there then run /sdlc:sync) -->"
END = "<!-- sdlc:end -->"

MODULES = [
    "spec", "plan", "decisions", "tdd", "review", "commit",
    "release", "ci", "docker", "pr", "handoff", "retro",
]
DEFAULTS = {"version": 1, "profiles": [], "modules": [], "autonomy": False, "stop_check": True}
TARGETS = ["dev", "test", "lint", "build"]


def die(msg):
    print("sdlc: " + msg, file=sys.stderr)
    sys.exit(1)


# --- flat YAML -------------------------------------------------------------

def _scalar(raw):
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "'\"":
        return raw[1:-1]
    if raw in ("true", "false"):
        return raw == "true"
    if raw.isdigit():
        return int(raw)
    return raw


def parse_yaml(text):
    data, key = {}, None
    for line in text.splitlines():
        line = line.split(" #")[0].rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        stripped = line.strip()
        if stripped.startswith("- ") and key is not None:
            data.setdefault(key, [])
            data[key].append(_scalar(stripped[2:]))
            continue
        if ":" not in stripped:
            die("cannot parse line: " + line)
        key, value = stripped.split(":", 1)
        key, value = key.strip(), value.strip()
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [_scalar(v) for v in inner.split(",")] if inner else []
        elif value == "":
            data[key] = []
        else:
            data[key] = _scalar(value)
    return data


def dump_config(cfg):
    def lst(values):
        return "[" + ", ".join(values) + "]"
    return (
        "# sdlc configuration: single source of truth, see AGENTS.md for its effect.\n"
        "version: {version}\n"
        "# Stack profiles, as name or name:subdir for monorepos.\n"
        "profiles: {profiles}\n"
        "# Optional modules: {all}\n"
        "modules: {modules}\n"
        "# true lets the AI move through phases without stopping at each gate.\n"
        "autonomy: {autonomy}\n"
        "# Run `make lint test` before the AI ends a turn.\n"
        "stop_check: {stop_check}\n"
    ).format(
        version=cfg["version"],
        profiles=lst(cfg["profiles"]),
        all=", ".join(MODULES),
        modules=lst(cfg["modules"]),
        autonomy=str(cfg["autonomy"]).lower(),
        stop_check=str(cfg["stop_check"]).lower(),
    )


def load_config():
    if not os.path.exists(CONFIG):
        die("no .sdlc.yml here; run /sdlc:init first")
    with open(CONFIG) as f:
        cfg = dict(DEFAULTS, **parse_yaml(f.read()))
    unknown = [m for m in cfg["modules"] if m not in MODULES]
    if unknown:
        die("unknown modules: " + ", ".join(unknown))
    for spec in cfg["profiles"]:
        load_profile(spec.split(":")[0])
    return cfg


def load_profile(name):
    path = os.path.join(PLUGIN_ROOT, "profiles", name + ".yml")
    if not os.path.exists(path):
        available = sorted(p[:-4] for p in os.listdir(os.path.join(PLUGIN_ROOT, "profiles")))
        die("unknown profile {}; available: {}".format(name, ", ".join(available)))
    with open(path) as f:
        return parse_yaml(f.read())


# --- rendering -------------------------------------------------------------

def read(path):
    with open(path) as f:
        return f.read()


def write(path, text):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w") as f:
        f.write(text)


def phases(cfg):
    mods = cfg["modules"]
    return ([p for p in ("spec", "plan") if p in mods] + ["implement"]
            + (["review"] if "review" in mods else []) + ["commit"])


def render_block(cfg):
    templates = os.path.join(PLUGIN_ROOT, "templates")
    profiles = ", ".join(cfg["profiles"]) or "none"
    gates = read(os.path.join(templates, "autonomy-on.md" if cfg["autonomy"] else "autonomy-off.md"))
    core = read(os.path.join(templates, "core.md")).format(
        profiles=profiles,
        modules=", ".join(cfg["modules"]) or "none",
        phases=" -> ".join(phases(cfg)),
        gates=gates.strip(),
    )
    parts = [core.strip()]
    for mod in MODULES:
        if mod in cfg["modules"]:
            parts.append(read(os.path.join(templates, "modules", mod + ".md")).strip())
    return BEGIN + "\n" + "\n\n".join(parts) + "\n" + END


def render_agents(cfg):
    block = render_block(cfg)
    if not os.path.exists("AGENTS.md"):
        name = os.path.basename(os.getcwd())
        write("AGENTS.md", "# {}\n\n{}\n\n## Project notes\n\n"
              "Free-form notes about this project go here, outside the generated block.\n".format(name, block))
        return
    text = read("AGENTS.md")
    if BEGIN in text and END in text:
        head, rest = text.split(BEGIN, 1)
        tail = rest.split(END, 1)[1]
        write("AGENTS.md", head + block + tail)
    else:
        write("AGENTS.md", text.rstrip() + "\n\n" + block + "\n")


def render_claude_md():
    if not os.path.exists("CLAUDE.md"):
        write("CLAUDE.md", "@AGENTS.md\n")
    elif "@AGENTS.md" not in read("CLAUDE.md"):
        write("CLAUDE.md", "@AGENTS.md\n\n" + read("CLAUDE.md"))


def render_makefile(cfg):
    if os.path.exists("Makefile"):
        return False
    lines = ["# Uniform entry points (generated by sdlc for profiles: {}).".format(", ".join(cfg["profiles"])),
             "# Edit freely: sdlc never overwrites an existing Makefile.",
             ".PHONY: " + " ".join(TARGETS), ""]
    for target in TARGETS:
        lines.append(target + ":")
        for spec in cfg["profiles"]:
            name, _, subdir = spec.partition(":")
            cmd = load_profile(name).get(target)
            if not cmd:
                continue
            if subdir:
                # A leading @ (silent recipe) must stay first on the line.
                silent = "@" if cmd.startswith("@") else ""
                cmd = "{}cd {} && {}".format(silent, subdir, cmd.lstrip("@"))
            lines.append("\t" + cmd)
        lines.append("")
    write("Makefile", "\n".join(lines))
    return True


def ensure_lines(path, wanted):
    existing = read(path).splitlines() if os.path.exists(path) else []
    missing = [w for w in wanted if w not in existing]
    if missing:
        prefix = "\n" if existing and existing[-1] != "" else ""
        with open(path, "a") as f:
            f.write(prefix + "\n".join(missing) + "\n")


def render_agent_docs(cfg):
    # The vendored skills read their tracker and domain-doc layout from docs/agents/.
    wanted = []
    if {"spec", "plan"} & set(cfg["modules"]):
        wanted.append("issue-tracker.md")
    if "decisions" in cfg["modules"]:
        wanted.append("domain.md")
    for name in wanted:
        path = os.path.join("docs", "agents", name)
        if not os.path.exists(path):
            write(path, read(os.path.join(PLUGIN_ROOT, "templates", "agents", name)))


def render(cfg):
    render_agents(cfg)
    render_claude_md()
    render_agent_docs(cfg)
    made = render_makefile(cfg)
    if not os.path.exists("BACKLOG.md"):
        write("BACKLOG.md", read(os.path.join(PLUGIN_ROOT, "templates", "BACKLOG.md")))
    if not os.path.exists(STATE):
        write(STATE, json.dumps({"item": None, "phase": None}, indent=2) + "\n")
    ensure_lines(".gitignore", [".env", ".env.*", "!.env.example"])
    print("rendered AGENTS.md, CLAUDE.md" + (", Makefile" if made else " (Makefile kept)"))


# --- commands --------------------------------------------------------------

def cmd_init(args):
    if os.path.exists(CONFIG) and not args.force:
        die(".sdlc.yml already exists; edit it and run /sdlc:sync, or pass --force")
    cfg = dict(DEFAULTS)
    cfg["profiles"] = [p for p in args.profiles.split(",") if p]
    cfg["modules"] = [m for m in args.modules.split(",") if m]
    cfg["autonomy"] = args.autonomy
    write(CONFIG, dump_config(cfg))
    render(load_config())


def cmd_get(args):
    cfg = load_config()
    if args.key not in cfg:
        sys.exit(1)
    value = cfg[args.key]
    if isinstance(value, list):
        print(" ".join(str(v) for v in value))
    elif isinstance(value, bool):
        print(str(value).lower())
    else:
        print(value)


def cmd_next(args):
    """Advance the current item to its next phase: the gate approval."""
    cfg = load_config()
    state = json.loads(read(STATE)) if os.path.exists(STATE) else {}
    order = phases(cfg)
    if not state.get("phase"):
        if not args.item:
            die("no item in progress; pass --item <slug> to start one")
        state = {"item": args.item, "phase": order[0]}
    elif args.item and args.item != state["item"]:
        die("item {} is still in progress (phase {})".format(state["item"], state["phase"]))
    elif state["phase"] == order[-1]:
        print("done: " + state["item"])
        state = {"item": None, "phase": None}
    else:
        current = state["phase"]
        # A module switched off mid-item: restart from the first remaining phase.
        state["phase"] = order[order.index(current) + 1] if current in order else order[0]
    write(STATE, json.dumps(state, indent=2) + "\n")
    print("current: {} / {}".format(state["item"] or "no item", state["phase"] or "idle"))


def cmd_set(args):
    """Change one setting and re-render: what the mod's panel calls."""
    cfg = load_config()
    if args.key == "modules":
        cfg["modules"] = [m for m in args.value.split(",") if m]
    elif args.key in ("autonomy", "stop_check"):
        if args.value not in ("true", "false"):
            die(args.key + " takes true or false")
        cfg[args.key] = args.value == "true"
    else:
        die("set takes modules, autonomy or stop_check")
    write(CONFIG, dump_config(cfg))
    render(load_config())


def cmd_status(args):
    cfg = load_config()
    state = json.loads(read(STATE)) if os.path.exists(STATE) else {}
    if args.json:
        print(json.dumps({
            "modules": cfg["modules"],
            "allModules": MODULES,
            "autonomy": cfg["autonomy"],
            "phases": phases(cfg),
            "item": state.get("item"),
            "phase": state.get("phase"),
        }))
        return
    print("profiles: " + (", ".join(cfg["profiles"]) or "none"))
    print("modules:  " + (", ".join(cfg["modules"]) or "none"))
    print("phases:   " + " -> ".join(phases(cfg)))
    print("mode:     " + ("autonomous" if cfg["autonomy"] else "gated"))
    print("current:  {} / {}".format(state.get("item") or "no item", state.get("phase") or "idle"))


def main():
    parser = argparse.ArgumentParser(prog="sdlc")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init")
    p.add_argument("--profiles", required=True)
    p.add_argument("--modules", default="")
    p.add_argument("--autonomy", action="store_true")
    p.add_argument("--force", action="store_true")
    sub.add_parser("render")
    p = sub.add_parser("get")
    p.add_argument("key")
    p = sub.add_parser("status")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("next")
    p.add_argument("--item")
    p = sub.add_parser("set")
    p.add_argument("key")
    p.add_argument("value")
    args = parser.parse_args()
    if args.cmd == "init":
        cmd_init(args)
    elif args.cmd == "set":
        cmd_set(args)
    elif args.cmd == "next":
        cmd_next(args)
    elif args.cmd == "render":
        render(load_config())
    elif args.cmd == "get":
        cmd_get(args)
    else:
        cmd_status(args)


if __name__ == "__main__":
    main()
