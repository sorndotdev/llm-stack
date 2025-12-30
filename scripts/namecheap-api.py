#!/usr/bin/env python3
"""Namecheap API client. Reads NAMECHEAP_API_USER, NAMECHEAP_API_KEY, optionally NAMECHEAP_CLIENT_IP from env.

Usage:
  namecheap-api.py <command> [params...]

Commands:
  balance                    Get account balance
  list-domains               List all domains
  dns-list <SLD> <TLD>       Get nameservers for a domain
  dns-get <SLD> <TLD>        Get current DNS host records
  dns-set <SLD> <TLD> <file> Set DNS host records from JSON file
  help                       Show this message

Environment:
  NAMECHEAP_API_USER    (required) Namecheap account username
  NAMECHEAP_API_KEY     (required) Namecheap API key
  NAMECHEAP_CLIENT_IP   (optional) Whitelisted IP; auto-detected if omitted

setHosts JSON file format (array of records, ALL records replace existing):
[
  {
    "HostName": "@",
    "RecordType": "TXT",
    "Address": "v=spf1 ...",
    "TTL": 1800
  },
  {
    "HostName": "mail._domainkey",
    "RecordType": "TXT",
    "Address": "v=DKIM1; ..."
  }
]
"""
import json, os, sys, subprocess, urllib.parse, urllib.request, xml.etree.ElementTree as ET

API_BASE = "https://api.namecheap.com/xml.response"
NAMESPACE = "{http://api.namecheap.com/xml.response}"

def ns(tag):
    return f"{NAMESPACE}{tag}"

def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)

def api_call(params):
    api_user = os.environ.get("NAMECHEAP_API_USER") or die("NAMECHEAP_API_USER not set")
    api_key = os.environ.get("NAMECHEAP_API_KEY") or die("NAMECHEAP_API_KEY not set")
    ip = os.environ.get("NAMECHEAP_CLIENT_IP") or (
        subprocess.run(
            ["curl", "-s", "https://api.ipify.org"],
            capture_output=True, text=True, timeout=10
        ).stdout.strip()
    ) or die("Could not detect public IP; set NAMECHEAP_CLIENT_IP")

    defaults = {
        "ApiUser": api_user, "ApiKey": api_key,
        "UserName": api_user, "ClientIp": ip
    }
    merged = {**defaults, **params}
    qs = urllib.parse.urlencode(merged)
    url = f"{API_BASE}?{qs}"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
    except Exception as e:
        die(f"HTTP request failed: {e}")

    root = ET.fromstring(raw)
    status = root.get("Status")
    errors = root.find(f".//{ns('Errors')}")

    if status == "ERROR":
        msg = "; ".join(e.text or "" for e in errors.findall(f".//{ns('Error')}"))
        die(f"API error: {msg}")

    return root


def cmd_balance(args):
    root = api_call({"Command": "namecheap.users.getBalances"})
    result = root.find(f".//{ns('UserGetBalancesResult')}")
    if result is not None:
        print(f"Currency:       {result.get('Currency')}")
        print(f"Available:      {result.get('AvailableBalance')}")
        print(f"Account:        {result.get('AccountBalance')}")
        print(f"Earned:         {result.get('EarnedAmount')}")
        print(f"Withdrawable:   {result.get('WithdrawableAmount')}")

def cmd_list_domains(args):
    root = api_call({"Command": "namecheap.domains.getList"})
    results = root.find(f".//{ns('DomainGetListResult')}")
    if results is None:
        print("No domains found.")
        return
    print(f"{'Domain':<30} {'Expires':<15} {'DNS':<8} {'AutoRenew':<10}")
    print("-" * 70)
    for d in results.findall(ns("Domain")):
        name = d.get("Name", "")
        expires = d.get("Expires", "")
        our_dns = "NC" if d.get("IsOurDNS") == "true" else "ext"
        renew = "yes" if d.get("AutoRenew") == "true" else "no"
        print(f"{name:<30} {expires:<15} {our_dns:<8} {renew:<10}")

def cmd_dns_list(args):
    if len(args) < 2:
        die("Usage: namecheap-api.py dns-list <SLD> <TLD>")
    sld, tld = args[0], args[1]
    root = api_call({"Command": "namecheap.domains.dns.getList", "SLD": sld, "TLD": tld})
    result = root.find(f".//{ns('DomainDNSGetListResult')}")
    if result is None:
        die("No DNS info returned")
    using_nc = result.get("IsUsingOurDNS") == "true"
    print(f"Domain:       {result.get('Domain')}")
    print(f"Using NC DNS: {using_nc}")
    print(f"PremiumDNS:   {result.get('IsPremiumDNS')}")
    print(f"FreeDNS:      {result.get('IsUsingFreeDNS')}")
    servers = [ns_el.text for ns_el in result.findall(ns("Nameserver")) if ns_el.text]
    if servers:
        print("Nameservers:")
        for s in servers:
            print(f"  - {s}")
    if not using_nc:
        print()
        print("WARNING: Domain is NOT using Namecheap DNS.")
        print("namecheap.domains.dns.setHosts will NOT work.")
        print("Use the DNS provider's API instead (e.g. Cloudflare).")

def cmd_dns_get(args):
    if len(args) < 2:
        die("Usage: namecheap-api.py dns-get <SLD> <TLD>")
    sld, tld = args[0], args[1]
    root = api_call({"Command": "namecheap.domains.dns.getHosts", "SLD": sld, "TLD": tld})
    result = root.find(f".//{ns('DomainDNSGetHostsResult')}")
    if result is None:
        die("No host records returned")
    using_nc = result.get("IsUsingOurDNS") == "true"
    if not using_nc:
        die("Domain is not using Namecheap DNS; use the external provider's API")

    records = []
    for host in result.findall(ns("host")):
        records.append({
            "HostName": host.get("Name"),
            "RecordType": host.get("Type"),
            "Address": host.get("Address"),
            "MXPref": host.get("MXPref"),
            "TTL": host.get("TTL"),
            "AssociatedAppTitle": host.get("AssociatedAppTitle"),
            "FriendlyName": host.get("FriendlyName"),
            "IsActive": host.get("IsActive"),
            "IsDDNSEnabled": host.get("IsDDNSEnabled"),
        })
    print(json.dumps(records, indent=2))

def cmd_dns_set(args):
    if len(args) < 3:
        die("Usage: namecheap-api.py dns-set <SLD> <TLD> <json_file>")
    sld, tld, json_file = args[0], args[1], args[2]
    with open(json_file) as f:
        records = json.load(f)

    params = {"Command": "namecheap.domains.dns.setHosts", "SLD": sld, "TLD": tld}
    for i, rec in enumerate(records, start=1):
        params[f"HostName{i}"] = rec["HostName"]
        params[f"RecordType{i}"] = rec["RecordType"]
        params[f"Address{i}"] = rec["Address"]
        if "MXPref" in rec:
            params[f"MXPref{i}"] = str(rec["MXPref"])
        if "TTL" in rec:
            params[f"TTL{i}"] = str(rec.get("TTL", 1800))
        elif "EmailType" in rec:
            # for MX records
            params[f"EmailType{i}"] = rec["EmailType"]

    root = api_call(params)
    result = root.find(f".//{ns('DomainDNSSetHostsResult')}")
    if result is not None:
        success = result.get("IsSuccess") == "true"
        print(f"Domain:  {result.get('Domain')}")
        print(f"Success: {success}")
        if success:
            print(f"Set {len(records)} DNS record(s)")

def cmd_help(args):
    print(__doc__)

CMDS = {
    "balance": cmd_balance,
    "list-domains": cmd_list_domains,
    "dns-list": cmd_dns_list,
    "dns-get": cmd_dns_get,
    "dns-set": cmd_dns_set,
    "help": cmd_help,
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        cmd_help([])
        sys.exit(1)
    CMDS[sys.argv[1]](sys.argv[2:])