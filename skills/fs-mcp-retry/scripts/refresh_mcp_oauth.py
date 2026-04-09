#!/usr/bin/env python3

import argparse
import hashlib
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    tomllib = None


DEFAULT_AUTH_ROOT = Path.home() / ".mcp-auth"

# Config search order: first match wins
CONFIG_SEARCH_PATHS = [
    Path.home() / ".claude.json",
    Path.home() / ".gemini" / "settings.json",
    Path.home() / ".codex" / "config.toml",
]


def find_default_config():
    """Auto-discover the first existing MCP config file."""
    for p in CONFIG_SEARCH_PATHS:
        if p.exists():
            return p
    return CONFIG_SEARCH_PATHS[0]  # fall back to first for error message


def load_config(config_path):
    """Load config from TOML (Codex) or JSON (Gemini/Claude Code) based on extension."""
    suffix = config_path.suffix.lower()
    if suffix == ".toml":
        if tomllib is None:
            print("python 3.11+ is required for TOML config files", file=sys.stderr)
            sys.exit(2)
        with config_path.open("rb") as f:
            raw = tomllib.load(f)
        # Normalize: Codex uses mcp_servers, return under canonical key
        return {"mcpServers": raw.get("mcp_servers", {})}
    else:
        with config_path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        # JSON configs (Gemini, Claude Code) use mcpServers
        return {"mcpServers": raw.get("mcpServers", {})}


def resolve_server(config, alias):
    servers = config.get("mcpServers", {})
    server = servers.get(alias)
    if not server:
        available = ", ".join(sorted(servers.keys())) or "(none)"
        raise ValueError(f"unknown MCP server alias: {alias}  (available: {available})")
    return server


def extract_server_url(server):
    if isinstance(server.get("url"), str):
        return server["url"]
    args = server.get("args") or []
    for value in args:
        if isinstance(value, str) and value.startswith(("http://", "https://")):
            return value
    raise ValueError("could not determine remote server URL from MCP config")


def extract_authorize_resource(server):
    args = server.get("args") or []
    for i, value in enumerate(args):
        if value in ("--resource", "--authorize-resource") and i + 1 < len(args):
            return args[i + 1]
    return ""


def extract_headers(config, alias):
    server = (config.get("mcpServers", {}) or {}).get(alias, {})
    headers = server.get("http_headers") or {}
    return dict(sorted(headers.items())) if isinstance(headers, dict) else {}


def get_server_hash(server_url, authorize_resource, headers):
    parts = [server_url]
    if authorize_resource:
        parts.append(authorize_resource)
    if headers:
        parts.append(json.dumps(headers, sort_keys=True, separators=(",", ":")))
    return hashlib.md5("|".join(parts).encode("utf-8")).hexdigest()


def find_auth_dir(auth_root):
    candidates = sorted(auth_root.glob("mcp-remote-*"))
    if not candidates:
        raise FileNotFoundError(f"no {auth_root}/mcp-remote-* directory found")
    return candidates[-1]


def read_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def fetch_json(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)


def discover_auth_metadata(server_url):
    parsed = urllib.parse.urlparse(server_url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    protected_resource_url = f"{base}/.well-known/oauth-protected-resource{parsed.path}"
    try:
        protected = fetch_json(protected_resource_url)
        servers = protected.get("authorization_servers") or []
        if servers:
            auth_server = servers[0].rstrip("/")
            return auth_server, fetch_json(f"{auth_server}/.well-known/oauth-authorization-server")
    except Exception:
        pass
    auth_server = base
    return auth_server, fetch_json(f"{auth_server}/.well-known/oauth-authorization-server")


def refresh_tokens(token_endpoint, client_id, refresh_token, scope=None):
    payload = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "refresh_token": refresh_token,
    }
    if scope:
        payload["scope"] = scope
    body = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(
        token_endpoint,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)


def main():
    parser = argparse.ArgumentParser(description="Refresh OAuth tokens for a configured MCP alias")
    parser.add_argument("alias", help="MCP server alias from the local MCP config")
    parser.add_argument("--force", action="store_true", help="force refresh even if token is not close to expiry")
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="path to MCP config file (default: auto-detect from ~/.gemini/settings.json or ~/.codex/config.toml)",
    )
    parser.add_argument(
        "--auth-root",
        type=Path,
        default=DEFAULT_AUTH_ROOT,
        help=f"path to OAuth cache root (default: {DEFAULT_AUTH_ROOT})",
    )
    args = parser.parse_args()

    try:
        config_path = args.config or find_default_config()
        config = load_config(config_path)
        server = resolve_server(config, args.alias)
        server_url = extract_server_url(server)
        authorize_resource = extract_authorize_resource(server)
        headers = extract_headers(config, args.alias)
        server_hash = get_server_hash(server_url, authorize_resource, headers)
        auth_dir = find_auth_dir(args.auth_root)
        tokens_path = auth_dir / f"{server_hash}_tokens.json"
        client_info_path = auth_dir / f"{server_hash}_client_info.json"

        if not tokens_path.exists():
            raise FileNotFoundError(f"no token bundle found for alias {args.alias} at {tokens_path}")
        if not client_info_path.exists():
            raise FileNotFoundError(f"no client info found for alias {args.alias} at {client_info_path}")

        tokens = read_json(tokens_path)
        client_info = read_json(client_info_path)
        expires_at = int(tokens.get("expires_at") or 0)
        now = int(time.time())
        seconds_left = expires_at - now if expires_at else None
        should_refresh = args.force or seconds_left is None or seconds_left < 300

        result = {
            "alias": args.alias,
            "config_path": str(config_path),
            "server_url": server_url,
            "server_hash": server_hash,
            "auth_dir": str(auth_dir),
            "refreshed": False,
            "seconds_left": seconds_left,
        }

        if not should_refresh:
            result["status"] = "token-still-valid"
            print(json.dumps(result, indent=2))
            return

        refresh_token_value = tokens.get("refresh_token")
        client_id = client_info.get("client_id")
        if not refresh_token_value:
            raise ValueError(f"no refresh_token present for alias {args.alias}")
        if not client_id:
            raise ValueError(f"no client_id present for alias {args.alias}")

        auth_server, metadata = discover_auth_metadata(server_url)
        token_endpoint = metadata.get("token_endpoint")
        if not token_endpoint:
            raise ValueError(f"no token_endpoint discovered for alias {args.alias}")

        refreshed = refresh_tokens(
            token_endpoint=token_endpoint,
            client_id=client_id,
            refresh_token=refresh_token_value,
            scope=tokens.get("scope"),
        )
        if "refresh_token" not in refreshed and refresh_token_value:
            refreshed["refresh_token"] = refresh_token_value
        if "scope" not in refreshed and tokens.get("scope"):
            refreshed["scope"] = tokens["scope"]
        if "expires_in" in refreshed:
            refreshed["expires_at"] = int(time.time()) + int(refreshed["expires_in"])

        write_json(tokens_path, refreshed)
        result.update(
            {
                "status": "refreshed",
                "refreshed": True,
                "auth_server": auth_server,
                "token_endpoint": token_endpoint,
                "new_expires_at": refreshed.get("expires_at"),
            }
        )
        print(json.dumps(result, indent=2))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(
            json.dumps(
                {
                    "alias": args.alias,
                    "status": "refresh-failed",
                    "http_status": e.code,
                    "error": body or str(e),
                },
                indent=2,
            ),
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as e:
        print(
            json.dumps(
                {
                    "alias": args.alias,
                    "status": "refresh-failed",
                    "error": str(e),
                },
                indent=2,
            ),
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
