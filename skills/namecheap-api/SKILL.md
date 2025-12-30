---
name: namecheap-api
description: Use this skill when a task requires interacting with the Namecheap API, such as querying and managing Namecheap DNS records.
---

## Namecheap

Use this skill when a task requires interacting with the Namecheap API (domain management, DNS records).

## Script Usage

* [P0] REQUIRED: Use script `<path>/scripts/namecheap-api.py` for all Namecheap API operations.
* The script reads env vars `NAMECHEAP_API_USER`, `NAMECHEAP_API_KEY`, and `NAMECHEAP_CLIENT_IP` automatically.
* The client IP is auto-detected via api.ipify.org when `NAMECHEAP_CLIENT_IP` is not set.

## Commands

| Command        | Arguments            | Description                                          |
|----------------|----------------------|------------------------------------------------------|
| `balance`      | —                    | Get account balance                                  |
| `list-domains` | —                    | List all domains with expiry, DNS type, auto-renew   |
| `dns-list`     | `<SLD> <TLD>`        | Get nameservers and detect if using Namecheap DNS    |
| `dns-get`      | `<SLD> <TLD>`        | Get current DNS host records as JSON                 |
| `dns-set`      | `<SLD> <TLD> <file>` | Set DNS host records from a JSON file (replaces all) |

## Important Constraints

| Constraint                             | Detail                                                                                                      |
|----------------------------------------|-------------------------------------------------------------------------------------------------------------|
| Domain must use **Namecheap BasicDNS** | `dns-get` / `dns-set` fail with error 2030288 if using external nameservers. Use `dns-list` first to check. |
| `dns-set` **replaces ALL records**     | Always call `dns-get` first, merge, then write back the full set.                                           |
| SLD/TLD split                          | `snapstock.app` → SLD=`snapstock`, TLD=`app`. Domain must be registered with Namecheap.                     |
| IP whitelisting                        | The calling IP must be whitelisted in Namecheap account settings (Profile → Tools → API Access).            |

## DNS JSON File Format

```json
[
  {
    "HostName": "@",
    "RecordType": "TXT",
    "Address": "v=spf1 ip4:... -all",
    "TTL": 1800
  },
  {
    "HostName": "www",
    "RecordType": "A",
    "Address": "1.2.3.4",
    "TTL": 1800
  }
]
```

## Typical Workflow

1. Check if domain uses Namecheap DNS: `<path>/scripts/namecheap-api.py dns-list snapstock app`
2. If yes, fetch current records `<path>/scripts/namecheap-api.py dns-get snapstock app > records.json`
3. Edit records.json, then apply `<path>/scripts/namecheap-api.py dns-set snapstock app records.json`
4. If no (e.g. Cloudflare), use the external provider's API
