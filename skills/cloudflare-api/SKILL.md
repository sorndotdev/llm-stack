---
name: cloudflare-api
description: Use this skill when a task requires interacting with the Cloudflare API, such as querying and managing Namecheap DNS records, zones and account settings.
---

# Cloudflare API

## Script Usage

* [P0] REQUIRED: Use script `<path>/scripts/cloudflare/cloudflare-api.py` for all Cloudflare API operations.
* The script reads env vars `CLOUDFLARE_ACCOUNT_ID` and `CLOUDFLARE_API_TOKEN` automatically.

## Commands

| Command      | Arguments       | Description                                        |
|--------------|-----------------|----------------------------------------------------|
| `verify`     | —               | Verify API token is valid and active               |
| `zones`      | —               | List all zones in the account                      |
| `zone-info`  | `<zone>`        | Get zone details (name, status, nameservers, plan) |
| `dns-list`   | `<zone>`        | List all DNS records in a zone                     |
| `dns-get`    | `<zone> <name>` | Get DNS record(s) matching a name or ID            |
| `dns-export` | `<zone>`        | Export zone as BIND configuration text             |

## Zone Parameter

`<zone>` accepts either a **zone name** (e.g. `snapstock.app`) or a **zone ID** (32 hex chars).
The script resolves names to IDs automatically.

## Important Constraints

| Constraint           | Detail                                                                                                          |
|----------------------|-----------------------------------------------------------------------------------------------------------------|
| Read-only by default | The current script only provides read commands. DNS modifications require adding more API calls.                |
| Pagination           | `dns-list` returns up to 100 records. For more, add `?page=N` support.                                          |
| Token permissions    | The token must have the appropriate permissions (e.g. `Zone:DNS:Read`, `Zone:DNS:Write`) for the commands used. |

## DNS Record Structure

Each DNS record has these fields:

```
{
  "id": "...",
  "type": "A | AAAA | CNAME | TXT | MX | ...",
  "name": "snapstock.app",        // full DNS name
  "content": "192.0.2.1",         // record value
  "ttl": 1,                       // 1 = automatic, else seconds
  "proxied": true,                 // proxied through Cloudflare
  "zone_id": "...",
  "zone_name": "snapstock.app",
  "created_on": "...",
  "modified_on": "..."
}
```

## Typical Workflow

```
# 1. Verify token works
<path>/scripts/cloudflare/cloudflare-api.py verify

# 2. List zones to find snapstock.app zone ID
<path>/scripts/cloudflare/cloudflare-api.py zones

# 3. List all DNS records for a zone
<path>/scripts/cloudflare/cloudflare-api.py dns-list snapstock.app

# 4. Find a specific record
<path>/scripts/cloudflare/cloudflare-api.py dns-get snapstock.app www

# 5. Export BIND config for backup
<path>/scripts/cloudflare/cloudflare-api.py dns-export snapstock.app
```
