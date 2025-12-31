#!/usr/bin/env python3
"""Cloudflare API client. Reads CLOUDFLARE_ACCOUNT_ID, CLOUDFLARE_API_TOKEN from env.

Usage:
  cloudflare-api.py <command> [params...]

Commands:
  verify                     Verify API token is valid
  zones                      List all zones in account
  zone-info <zone>           Get zone details (name or ID)
  dns-list <zone>            List all DNS records in a zone
  dns-get <zone> <name>      Get a specific DNS record by name
  dns-export <zone>          Export zone as BIND config
  help                       Show this message

<zone> can be a zone name (e.g. snapstock.app) or zone ID.

Environment:
  CLOUDFLARE_ACCOUNT_ID   (required) Cloudflare account ID
  CLOUDFLARE_API_TOKEN    (required) Cloudflare API token
"""
import json, os, sys, urllib.request, urllib.error

API_BASE = "https://api.cloudflare.com/client/v4"

def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)

def api_headers():
    token = os.environ.get("CLOUDFLARE_API_TOKEN") or die("CLOUDFLARE_API_TOKEN not set")
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

def api_get(path):
    headers = api_headers()
    url = f"{API_BASE}{path}"
    try:
        req = urllib.request.Request(url, headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        die(f"HTTP {e.code} on GET {path}: {body}")
    except Exception as e:
        die(f"Request failed: {e}")
    data = json.loads(raw)
    if not data.get("success"):
        msgs = "; ".join(e.get("message", str(e)) for e in data.get("errors", []))
        die(f"API error: {msgs}")
    return data.get("result")

def api_paginated_get(path):
    """GET with auto-pagination."""
    results = []
    page = 1
    while True:
        sep = "&" if "?" in path else "?"
        data = api_get(f"{path}{sep}page={page}&per_page=100")
        results.extend(data if isinstance(data, list) else [data])
        info = getattr(api_get, "_pagination", {})
        # Cloudflare pagination varies; try result_info
        break  # simplified for now
    return results

def resolve_zone(zone_arg):
    """Return zone ID given a name or ID."""
    zones = api_get(f"/zones?per_page=50")
    # Check if arg is already a zone ID (32 hex chars)
    if len(zone_arg) == 32 and all(c in "0123456789abcdef" for c in zone_arg):
        for z in zones:
            if z["id"] == zone_arg:
                return zone_arg
    # Look up by name
    for z in zones:
        if z["name"] == zone_arg or z["id"] == zone_arg:
            return z["id"]
    die(f"Zone '{zone_arg}' not found in account")

def cmd_verify(args):
    headers = api_headers()
    account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID") or die("CLOUDFLARE_ACCOUNT_ID not set")
    req = urllib.request.Request(
        f"{API_BASE}/accounts/{account_id}/tokens/verify",
        headers=headers, method="GET"
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read().decode("utf-8")
    data = json.loads(raw)
    result = data.get("result", {})
    print(f"Token ID:     {result.get('id')}")
    print(f"Status:       {result.get('status')}")
    print(f"Success:      {data.get('success')}")
    if data.get("messages"):
        for m in data["messages"]:
            print(f"Message:      {m.get('message')}")

def cmd_zones(args):
    zones = api_get("/zones?per_page=50")
    print(f"{'Zone':<30} {'ID':<35} {'Plan':<20} {'Status':<10}")
    print("-" * 100)
    for z in zones:
        name = z.get("name", "")
        zid = z.get("id", "")
        plan = z.get("plan", {}).get("name", "")
        status = z.get("status", "")
        print(f"{name:<30} {zid:<35} {plan:<20} {status:<10}")

def cmd_zone_info(args):
    if not args:
        die("Usage: cloudflare-api.py zone-info <zone>")
    zone_id = resolve_zone(args[0])
    zone = api_get(f"/zones/{zone_id}")
    info = zone if isinstance(zone, dict) else zone[0]
    print(f"ID:           {info.get('id')}")
    print(f"Name:         {info.get('name')}")
    print(f"Status:       {info.get('status')}")
    print(f"Plan:         {info.get('plan', {}).get('name', '')}")
    print(f"Nameservers:  {', '.join(info.get('name_servers', []))}")
    print(f"Paused:       {info.get('paused')}")
    print(f"Type:         {info.get('type')}")

def cmd_dns_list(args):
    if not args:
        die("Usage: cloudflare-api.py dns-list <zone>")
    zone_id = resolve_zone(args[0])
    records = api_get(f"/zones/{zone_id}/dns_records?per_page=100")
    print(f"{'Name':<40} {'Type':<6} {'TTL':<6} {'Content':<60} {'Proxied':<8} {'ID':<35}")
    print("-" * 160)
    for r in records:
        name = r.get("name", "")
        rtype = r.get("type", "")
        ttl = r.get("ttl", 1)
        if ttl == 1: ttl_str = "auto"
        else: ttl_str = str(ttl)
        content = r.get("content", "")
        proxied = str(r.get("proxied", ""))
        rid = r.get("id", "")
        print(f"{name:<40} {rtype:<6} {ttl_str:<6} {content:<60} {proxied:<8} {rid:<35}")

def cmd_dns_get(args):
    if len(args) < 2:
        die("Usage: cloudflare-api.py dns-get <zone> <name>")
    zone_id = resolve_zone(args[0])
    name = args[1]
    records = api_get(f"/zones/{zone_id}/dns_records?per_page=100")
    matches = [r for r in records if r.get("name") == name or r.get("id") == name]
    if not matches:
        # Try partial match
        matches = [r for r in records if name in r.get("name", "")]
    if not matches:
        print(f"No records found matching '{name}'")
        return
    print(json.dumps(matches, indent=2))

def cmd_dns_export(args):
    if not args:
        die("Usage: cloudflare-api.py dns-export <zone>")
    zone_id = resolve_zone(args[0])
    token = os.environ.get("CLOUDFLARE_API_TOKEN") or die("CLOUDFLARE_API_TOKEN not set")
    headers = api_headers()
    url = f"{API_BASE}/zones/{zone_id}/dns_records/export"
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8")
    print(raw)

def cmd_help(args):
    print(__doc__)

CMDS = {
    "verify": cmd_verify,
    "zones": cmd_zones,
    "zone-info": cmd_zone_info,
    "dns-list": cmd_dns_list,
    "dns-get": cmd_dns_get,
    "dns-export": cmd_dns_export,
    "help": cmd_help,
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        cmd_help([])
        sys.exit(1)
    CMDS[sys.argv[1]](sys.argv[2:])
