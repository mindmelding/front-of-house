#!/usr/bin/env python3
"""mcp_call: a stdlib-only client for the overlay's MCP context source.

Fallback for the sweep when the host did not mount the connector's tools. Reads the
first server in overlay/mcp.json (Streamable HTTP), expands ${VAR} from the environment
or overlay/secrets.env, and speaks JSON-RPC over HTTP. Never writes anything.

  mcp_call.py tools                          list the server's tools
  mcp_call.py call <tool> ['<json args>']    call one tool; prints the text content
  mcp_call.py call <tool> --file <args.json> same, arguments from a file
  mcp_call.py accounts [--since <iso>] [--category sell-side]
                                             Moonbase adapter: page list_accounts with activity,
                                             one row per account, newest event first

Overlay resolution: $FOH_OVERLAY, then ./overlay, then ~/.front-of-house/overlay.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

PROTOCOL = "2025-06-18"


def overlay_dir():
    env = os.environ.get("FOH_OVERLAY")
    if env:
        return Path(env).expanduser()
    local = Path.cwd() / "overlay"
    return local if local.exists() else Path.home() / ".front-of-house" / "overlay"


def secrets(overlay):
    out = {}
    f = overlay / "secrets.env"
    if f.exists():
        for line in f.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                out[k.strip().removeprefix("export ").strip()] = v.strip().strip('"').strip("'")
    return out


def expand(s, env):
    missing = []

    def sub(m):
        k = m.group(1)
        if k in env:
            return env[k]
        missing.append(k)
        return ""

    return re.sub(r"\$\{(\w+)\}", sub, s), missing


class Client:
    def __init__(self, url, headers):
        self.url, self.headers, self.session, self._id = url, headers, None, 0

    def _post(self, body, expect_result=True):
        h = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream",
             "MCP-Protocol-Version": PROTOCOL, **self.headers}
        if self.session:
            h["Mcp-Session-Id"] = self.session
        req = urllib.request.Request(self.url, data=json.dumps(body).encode(), headers=h, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                sid = r.headers.get("Mcp-Session-Id")
                if sid:
                    self.session = sid
                ctype = r.headers.get("Content-Type", "")
                raw = r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:500]
            sys.exit(f"HTTP {e.code} from {self.url}: {detail}")
        if not expect_result:
            return None
        msgs = []
        if "text/event-stream" in ctype:
            for line in raw.splitlines():
                if line.startswith("data:"):
                    data = line[5:].strip()
                    if data:
                        try:
                            msgs.append(json.loads(data))
                        except json.JSONDecodeError:
                            pass
        elif raw.strip():
            msgs.append(json.loads(raw))
        for m in msgs:
            if m.get("id") == body.get("id"):
                if "error" in m:
                    sys.exit(f"rpc error: {json.dumps(m['error'])[:800]}")
                return m.get("result")
        sys.exit(f"no response for id {body.get('id')} (content-type {ctype}); raw: {raw[:300]}")

    def rpc(self, method, params=None):
        self._id += 1
        return self._post({"jsonrpc": "2.0", "id": self._id, "method": method, "params": params or {}})

    def connect(self):
        self.rpc("initialize", {"protocolVersion": PROTOCOL, "capabilities": {},
                                "clientInfo": {"name": "front-of-house", "version": "0.1"}})
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"}, expect_result=False)


def load_server():
    overlay = overlay_dir()
    cfg = json.loads((overlay / "mcp.json").read_text())
    name, srv = next(iter(cfg["mcpServers"].items()))
    env = {**secrets(overlay), **os.environ}
    url, miss = expand(srv["url"], env)
    headers, missing = {}, list(miss)
    for k, v in (srv.get("headers") or {}).items():
        headers[k], m = expand(v, env)
        missing += m
    if missing:
        sys.exit(f"unset variable(s) for server {name!r}: {', '.join(sorted(set(missing)))} (set in env or overlay/secrets.env)")
    return name, url, headers


def main(argv):
    if len(argv) < 2 or argv[1] not in ("tools", "call", "accounts"):
        print(__doc__)
        return 2
    name, url, headers = load_server()
    c = Client(url, headers)
    c.connect()
    if argv[1] == "accounts":
        opts = dict(zip(argv[2::2], argv[3::2]))
        accounts(c, since=opts.get("--since"), category=opts.get("--category"))
        return 0
    if argv[1] == "tools":
        res = c.rpc("tools/list")
        for t in res.get("tools", []):
            print(f"{t['name']}: {t.get('description', '').strip().splitlines()[0][:160] if t.get('description') else ''}")
            print("   args: " + json.dumps(t.get("inputSchema", {}).get("properties", {}))[:400])
        return 0
    if len(argv) < 3:
        print(__doc__)
        return 2
    tool = argv[2]
    args = {}
    if len(argv) > 3:
        if argv[3] == "--file":
            args = json.loads(Path(argv[4]).read_text())
        else:
            args = json.loads(argv[3])
    res = c.rpc("tools/call", {"name": tool, "arguments": args})
    if res.get("isError"):
        print("TOOL ERROR", file=sys.stderr)
    printed = False
    for item in res.get("content", []):
        if item.get("type") == "text":
            print(item["text"]); printed = True
        else:
            print(json.dumps(item)[:2000]); printed = True
    if res.get("structuredContent") and not printed:
        print(json.dumps(res["structuredContent"], indent=2))
    return 1 if res.get("isError") else 0


def call_json(c, tool, args):
    res = c.rpc("tools/call", {"name": tool, "arguments": args})
    if res.get("isError"):
        sys.exit("tool error: " + " ".join(i.get("text", "") for i in res.get("content", []))[:800])
    if res.get("structuredContent"):
        return res["structuredContent"]
    text = "".join(i.get("text", "") for i in res.get("content", []) if i.get("type") == "text")
    return json.loads(text)


def accounts(c, since=None, category=None):
    """Page list_accounts with activity and print one compact row per account, newest first."""
    rows, cursor = [], None
    while True:
        args = {"activity": True}
        if cursor:
            args["cursor"] = cursor
        page = call_json(c, "list_accounts", args)
        rows += page.get("accounts", [])
        cursor = page.get("nextCursor")
        if not cursor:
            break
    rows = [r for r in rows if (not category or r.get("category") == category)
            and (not since or (r.get("newestEventAt") or "") >= since)]
    rows.sort(key=lambda r: r.get("newestEventAt") or "", reverse=True)
    for r in rows:
        types = ", ".join(f"{t['type'].rsplit('.', 1)[-1]}:{t['count']}@{(t.get('lastAt') or '')[:16]}" for t in r.get("eventTypes", []))
        print(f"{(r.get('newestEventAt') or '-')[:19]}  {r.get('category', '?'):12s} {r['name'][:36]:36s} {r['id'].rsplit('/', 1)[-1]:>5s}  n={r.get('eventsCount', 0):<4} {types}")
    print(f"# {len(rows)} account(s)")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
