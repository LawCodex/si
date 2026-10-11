#!/usr/bin/env python3
"""Fetch Slovenian legislation in force from PIS (Pravno-informacijski sistem, https://pisrs.si).

Uses the public JSON API behind the pisrs.si web application:
  POST /api/filter/filter?cursorMark=...   -> list of acts in "Register predpisov" (acts in force)
  GET  /api/rezultat/zbirka/id/<ID>        -> metadata + list of text versions (Osnovni, NPB 1..n)
  GET  /api/rezultat/neuradno-precisceno-besedilo/<versionId> -> structured text of a version

Everything is cached under RAW (default ../_raw/si relative to the repo) so re-runs only fetch
what is missing.  Usage: python si_fetch.py [--raw DIR] [--workers 3] [--cats ustava,zakoni,...]
"""
import argparse
import concurrent.futures as cf
import datetime
import json
import os
import random
import sys
import threading
import time

import requests

API = "https://pisrs.si/api"
UA = "LawCodex/1.0 (+https://github.com/LawCodex)"

# category -> PIS "kazaloPravniAkti" code
CATS = {
    "ustava": "Ustava#65",
    "zakoni": "Zakon#66",
    "uredbe": "Uredba#69",
    "pravilniki": "Pravilnik#72",
}

_local = threading.local()


def session():
    s = getattr(_local, "s", None)
    if s is None:
        s = requests.Session()
        s.headers["User-Agent"] = UA
        s.headers["Accept"] = "application/json"
        _local.s = s
    return s


def req(method, url, delay=0.4, **kw):
    for attempt in range(8):
        try:
            r = session().request(method, url, timeout=120, **kw)
            if r.status_code == 200:
                d = r.json()
                time.sleep(delay)
                return d
            if r.status_code in (404,):
                return None
            err = f"HTTP {r.status_code}"
        except (requests.RequestException, ValueError) as e:
            err = repr(e)
        wait = min(300, 5 * 2 ** attempt) + random.random() * 3
        print(f"  retry {attempt+1} {url}: {err}; sleeping {wait:.0f}s", file=sys.stderr, flush=True)
        time.sleep(wait)
    raise RuntimeError(f"giving up on {url}")


def save_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False)
    os.replace(tmp, path)


def list_category(raw, cat, code):
    path = os.path.join(raw, "list", f"{cat}.json")
    if os.path.exists(path):
        return json.load(open(path, encoding="utf-8"))
    body = {"nazivZbirke": ["Register predpisov"], "vrstaAkta": {"osnovniBrezNovele": True},
            "kategorizacijaAkta": [code]}
    cursor, items, total = "*", [], None
    while True:
        d = req("POST", f"{API}/filter/filter", params={"cursorMark": cursor}, json=body)["data"]
        total = d["numOfAllResultsForIndex"]
        items.extend(d["seznam"] or [])
        nxt = d.get("nextCursorMark")
        print(f"  {cat}: {len(items)}/{total}", flush=True)
        if not d["seznam"] or not nxt or nxt == cursor:
            break
        cursor = nxt
    # de-duplicate by external id
    seen, out = set(), []
    for x in items:
        if x["zunanjiId"] not in seen:
            seen.add(x["zunanjiId"])
            out.append(x)
    print(f"{cat}: {len(out)} unique of {total} reported", flush=True)
    save_json(path, out)
    return out


def pick_version(meta, today):
    """Latest NPB (or the original text) already applicable today."""
    vers = ((meta.get("besedilo") or {}).get("npbVerzije")) or []
    best, bestn = None, -1
    for v in vers:
        name = (v.get("naziv") or "").strip()
        if name == "Osnovni":
            n = 0
        elif name.startswith("NPB"):
            try:
                n = int(name.split()[1])
            except (IndexError, ValueError):
                continue
        else:
            continue
        dz = v.get("datumZacetkaUporabe")
        if dz and dz[:10] > today:
            continue
        if n > bestn:
            best, bestn = v, n
    return best


def fetch_one(raw, pid, today):
    mpath = os.path.join(raw, "meta", f"{pid}.json")
    if os.path.exists(mpath):
        meta = json.load(open(mpath, encoding="utf-8"))
    else:
        d = req("GET", f"{API}/rezultat/zbirka/id/{pid}")
        meta = (d or {}).get("data")
        if meta is None:
            print(f"  no metadata for {pid}", file=sys.stderr, flush=True)
            return "nometa"
        save_json(mpath, meta)
    v = pick_version(meta, today)
    if not v:
        return "notext"
    tpath = os.path.join(raw, "text", f"{pid}_{v['id']}.json")
    if os.path.exists(tpath):
        return "cached"
    d = req("GET", f"{API}/rezultat/neuradno-precisceno-besedilo/{v['id']}")
    data = (d or {}).get("data")
    if not data:
        save_json(tpath, [])
        return "empty"
    save_json(tpath, data)
    return "ok"


def main():
    ap = argparse.ArgumentParser()
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--raw", default=os.path.join(here, "..", "..", "_raw", "si"))
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--cats", default=",".join(CATS))
    a = ap.parse_args()
    raw = os.path.abspath(a.raw)
    for sub in ("list", "meta", "text"):
        os.makedirs(os.path.join(raw, sub), exist_ok=True)
    today = datetime.date.today().isoformat()
    for cat in a.cats.split(","):
        items = list_category(raw, cat, CATS[cat])
        ids = [x["zunanjiId"] for x in items]
        stats = {}
        with cf.ThreadPoolExecutor(a.workers) as ex:
            futs = {ex.submit(fetch_one, raw, pid, today): pid for pid in ids}
            for i, f in enumerate(cf.as_completed(futs), 1):
                try:
                    r = f.result()
                except Exception as e:  # noqa
                    r = "error"
                    print(f"  ERROR {futs[f]}: {e}", file=sys.stderr, flush=True)
                stats[r] = stats.get(r, 0) + 1
                if i % 100 == 0:
                    print(f"  {cat}: {i}/{len(ids)} {stats}", flush=True)
        print(f"{cat} done: {stats}", flush=True)


if __name__ == "__main__":
    main()
