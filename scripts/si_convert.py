#!/usr/bin/env python3
"""Convert PIS (pisrs.si) JSON cached by si_fetch.py into LawCodex Markdown.

Usage: python si_convert.py [--raw DIR] [--out REPO_DIR] [--retrieved YYYY-MM-DD]
"""
import argparse
import base64
import datetime
import glob
import html
import json
import os
import re
import sys
import unicodedata

from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

SITE = "https://pisrs.si"
CATS = ["ustava", "zakoni", "uredbe", "pravilniki"]
BY_YEAR = {"zakoni", "uredbe", "pravilniki"}

# structural divisions, outermost first
DIVISIONS = ["del", "poglavje", "oddelek", "pododdelek", "odsek"]
ART_RE = re.compile(r"^[»„\"]?\s*\d+\s*\.\s*(?:[a-zčšž]\s*)?člen\b\.?\s*$", re.I)

SEMAFOR_STATUS = {
    "Veljaven predpis": "in_force",
    "Veljaven predpis, ki se še ne uporablja": "in_force",
    "Objavljen predpis, ki še ne velja": "in_force",
}


class MD(MarkdownConverter):
    def convert_img(self, el, text, *args, **kw):
        src = el.get("src") or ""
        if src.startswith("/"):
            src = SITE + src
        alt = (el.get("alt") or "").strip()
        if src.startswith("data:"):
            return f"[slika{': ' + alt if alt else ''}]"
        return f"![{alt}]({src})" if src else ""


_md = MD(heading_style="ATX", bullets="-", strip=["span", "font", "div", "p"], escape_underscores=True,
         escape_asterisks=True)


def slugify(s, maxlen=80):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    if len(s) > maxlen:
        s = s[:maxlen].rsplit("-", 1)[0]
    return s or "predpis"


def norm_ws(s):
    s = s.replace(" ", " ").replace("​", "")
    return re.sub(r"[ \t\r\n]+", " ", s).strip()


def esc_text(t):
    t = t.replace("\\", "\\\\").replace("*", "\\*").replace("`", "\\`")
    t = t.replace("<", "&lt;").replace(">", "&gt;") if ("<" in t or ">" in t) else t
    t = re.sub(r"(?<![0-9A-Za-zÀ-ž])_|_(?![0-9A-Za-zÀ-ž])", r"\\_", t)
    t = t.replace("[", "\\[").replace("]", "\\]")
    return t


def inline(v):
    """HTML fragment -> one line of Markdown."""
    if v is None:
        return ""
    if "<" not in v and "&" not in v:
        return esc_text(norm_ws(v))
    v = re.sub(r"<br\s*/?>", " ", v, flags=re.I)
    return norm_ws(_md.convert(v))


def plain(v):
    if v is None:
        return ""
    v = re.sub(r"<br\s*/?>", " ", v, flags=re.I)
    return norm_ws(html.unescape(re.sub(r"<[^>]+>", "", v)))


def block_html(v):
    """Tables and other complex blocks: keep cleaned HTML."""
    soup = BeautifulSoup(v, "html.parser")
    for t in soup.find_all(True):
        for a in list(t.attrs):
            if a not in ("colspan", "rowspan", "href", "src", "alt"):
                del t.attrs[a]
        if t.name == "img" and t.get("src", "").startswith("/"):
            t["src"] = SITE + t["src"]
    out = str(soup)
    out = re.sub(r"\n\s*\n+", "\n", out)
    return out.strip()


def is_simple_table(v):
    return "<table" in v and not re.search(r"(colspan|rowspan)=\"?([2-9]|\d\d)", v) and v.count("<table") == 1


def table_md(v):
    soup = BeautifulSoup(v, "html.parser")
    rows = []
    for tr in soup.find_all("tr"):
        cells = [inline(c.decode_contents()).replace("|", "\\|") for c in tr.find_all(["td", "th"])]
        rows.append(cells)
    rows = [r for r in rows if r]
    if not rows:
        return ""
    n = max(len(r) for r in rows)
    if n < 1:
        return ""
    rows = [r + [""] * (n - len(r)) for r in rows]
    lines = ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * n]
    lines += ["| " + " | ".join(r) + " |" for r in rows[1:]]
    return "\n".join(lines)


def escape_para_start(s):
    # avoid accidental headings / lists / quotes for normal paragraphs
    if re.match(r"^\d+\.\s", s):
        s = re.sub(r"^(\d+)\.", r"\1\\.", s, count=1)
    elif re.match(r"^[#>+]", s):
        s = "\\" + s
    elif re.match(r"^[-*]\s*$", s):
        s = "\\" + s
    return s


DATA_IMG = re.compile(r'src="data:image/([a-zA-Z0-9.+-]+);base64,([^"]+)"')


class ImageSaver:
    """Writes inline base64 images to slike/<cat>/[<year>/]<id>/<n>.<ext> and returns relative links."""

    def __init__(self, out, md_dir, rel_dir):
        self.out, self.md_dir, self.rel_dir, self.n = out, md_dir, rel_dir, 0

    def __call__(self, v):
        if "data:image" not in v:
            return v

        def sub(m):
            ext = {"jpeg": "jpg", "svg+xml": "svg", "x-wmf": "wmf"}.get(m.group(1).lower(), m.group(1).lower())
            try:
                data = base64.b64decode(m.group(2))
            except Exception:  # noqa
                return 'src=""'
            self.n += 1
            d = os.path.join(self.out, self.rel_dir)
            os.makedirs(d, exist_ok=True)
            fp = os.path.join(d, f"{self.n}.{ext}")
            with open(fp, "wb") as f:
                f.write(data)
            WRITTEN_IMG.add(os.path.relpath(fp, self.out))
            return 'src="' + os.path.relpath(fp, self.md_dir).replace(os.sep, "/") + '"'

        return DATA_IMG.sub(sub, v)


WRITTEN_IMG = set()


def render(items, imgsub=lambda v: v):
    present = {x.get("struktura") for x in items}
    levels, lvl = {}, 2
    for d in DIVISIONS:
        if d in present:
            levels[d] = lvl
            lvl += 1
    art_level = lvl
    out = []
    appendix = False  # after the first <hr>: notes on amending acts (rendered without headings)
    pending_title = None

    def para(s):
        if s:
            out.append(s)

    def flush_title():
        nonlocal pending_title
        if pending_title:
            para(f"**{pending_title}**")
            pending_title = None

    for x in items:
        st = (x.get("struktura") or "").strip()
        v = imgsub(x.get("vsebina") or "")
        if not v.strip():
            continue
        if "<hr" in v and plain(v) == "":
            flush_title()
            out.append("---")
            appendix = True
            continue
        if "<table" in v:
            flush_title()
            para(table_md(v) if is_simple_table(v) else block_html(v))
            continue
        if st in DIVISIONS:
            flush_title()
            t = inline(v)
            if appendix:
                para(f"**{t}**")
            else:
                para("#" * levels[st] + " " + t.replace("\\[", "[").replace("\\]", "]"))
            continue
        if st in ("clen", "naslov_clena"):
            t = inline(v)
            if not appendix and ART_RE.match(plain(v)):
                if art_level <= 6:
                    para("#" * art_level + " " + plain(v))
                else:
                    para(f"**{plain(v)}**")
                if pending_title:
                    para(f"**{pending_title}**")
                    pending_title = None
            elif appendix:
                para(f"**{t}**")
            else:
                if pending_title:
                    flush_title()
                pending_title = t
            continue
        flush_title()
        if st in ("naslov",):
            para(f"**{inline(v)}**")
        elif st in ("opozorilo", "npb"):
            para(f"*{inline(v)}*")
        elif "<img" in v and st in ("slika", "enacba", "spremenjena_slika", "spremenjena_enacba"):
            para(inline(v))
        elif st in ("alinea", "alinea_za_odstavkom", "alinea_za_stevilcno_tocko", "alinea_za_crkovno_tocko",
                    "alinea_za_podtocko", "alinea_novele", "spremenjena_alinea"):
            s = inline(v)
            s = re.sub(r"^[-–—]\s*", "- ", s) if re.match(r"^[-–—]\s", s) else escape_para_start(s)
            para(s)
        elif st in ("stevilcna_tocka", "spremenjena_stevilcna_tocka"):
            para(inline(v))
        else:
            para(escape_para_start(inline(v)))
    flush_title()
    md = "\n\n".join(out)
    return md


def yq(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


DATE_RE = re.compile(r"z dne (\d{1,2})\.\s*(\d{1,2})\.\s*(\d{4})")


def consolidation_date(items):
    """Latest publication date among the acts listed in the NPB preamble ("... z dne D. M. YYYY")."""
    best = None
    for x in items:
        if x.get("struktura") == "naslov":
            break
        for d, m, y in DATE_RE.findall(plain(x.get("vsebina") or "")):
            try:
                iso = datetime.date(int(y), int(m), int(d)).isoformat()
            except ValueError:
                continue
            best = max(best, iso) if best else iso
    return best


def act_type(cat, pid, title):
    t = title.lower()
    if cat == "ustava":
        if pid == "USTA1":
            return "constitution"
        if "amandma" in t:
            return "constitutional_amendment"
        return "constitutional_act"
    if cat == "zakoni":
        if "zakonik" in t.split("(")[0]:
            return "code"
        if t.startswith("zakon o ratifikaciji"):
            return "ratification_act"
        return "act"
    if cat == "uredbe":
        return "decree"
    return "regulation"


def pick_text(raw, pid, meta):
    vers = ((meta.get("besedilo") or {}).get("npbVerzije")) or []
    names = {v["id"]: v.get("naziv") for v in vers}
    files = glob.glob(os.path.join(raw, "text", f"{pid}_*.json"))
    best = None
    for f in files:
        vid = int(os.path.basename(f)[len(pid) + 1:-5])
        if vid in names:
            n = names[vid]
            rank = 0 if n == "Osnovni" else int(re.sub(r"\D", "", n) or 0)
            if best is None or rank > best[0]:
                best = (rank, f, n)
    return best


def convert(raw, out, retrieved):
    counts, missing = {}, []
    written = set()
    for cat in CATS:
        lp = os.path.join(raw, "list", f"{cat}.json")
        if not os.path.exists(lp):
            continue
        for item in json.load(open(lp, encoding="utf-8")):
            pid = item["zunanjiId"]
            mp = os.path.join(raw, "meta", f"{pid}.json")
            if not os.path.exists(mp):
                missing.append((cat, pid, item.get("nazivAkta"), "no metadata fetched"))
                continue
            meta = json.load(open(mp, encoding="utf-8"))
            ev = meta.get("evidencniPodatki") or {}
            title = norm_ws(ev.get("naslov") or item.get("nazivAkta") or pid)
            pt = pick_text(raw, pid, meta)
            if not pt:
                missing.append((cat, pid, title, "no text in PIS" + (
                    f" (source: {meta.get('virPovezaveOblike')})" if meta.get("virPovezaveOblike") else "")))
                continue
            rank, tf, vname = pt
            items = json.load(open(tf, encoding="utf-8"))
            if not items:
                missing.append((cat, pid, title, "empty text"))
                continue
            pub = ev.get("objavljeno") or item.get("datumObjave")
            year = (pub or ev.get("sprejeto") or "0000")[:4]
            slug = slugify(title)
            fname = f"{pid}-{slug}.md"
            d = os.path.join(out, cat, year) if cat in BY_YEAR else os.path.join(out, cat)
            imgdir = os.path.join("slike", cat, year, pid) if cat in BY_YEAR else os.path.join("slike", cat, pid)
            body = render(items, ImageSaver(out, d, imgdir))
            os.makedirs(d, exist_ok=True)
            path = os.path.join(d, fname)
            semafor = ((ev.get("semafor") or {}).get("naziv")) or ""
            fm = ["---", f"title: {yq(title)}", f"identifier: {yq(pid)}"]
            if ev.get("kratica"):
                fm.append(f"abbreviation: {yq(ev['kratica'])}")
            fm += [f"type: {act_type(cat, pid, title)}", "jurisdiction: si", "language: sl"]
            if ev.get("vrstaAkta"):
                fm.append(f"act_kind: {yq(ev['vrstaAkta'])}")
            date = ev.get("sprejeto") or pub
            if date:
                fm.append(f"date: {date[:10]}")
            if pub:
                fm.append(f"published: {pub[:10]}")
            if ev.get("veljaOd"):
                fm.append(f"in_force_from: {ev['veljaOd'][:10]}")
            cd = consolidation_date(items) if rank > 0 else None
            if cd:
                fm.append(f"last_amended: {cd}")
            fm.append(f"status: {SEMAFOR_STATUS.get(semafor, 'unknown')}")
            if semafor:
                fm.append(f"pis_status: {yq(semafor)}")
            fm.append(f"text_version: {yq(vname + (' (neuradno prečiščeno besedilo)' if rank > 0 else ' (izvirno besedilo)'))}")
            if ev.get("citat"):
                fm.append(f"citation: {yq(plain(ev['citat']))}")
            if ev.get("organSprejetja"):
                fm.append(f"adopted_by: {yq(norm_ws(ev['organSprejetja']))}")
            if ev.get("eva"):
                fm.append(f"eva: {yq(ev['eva'])}")
            if ev.get("epa"):
                fm.append(f"epa: {yq(ev['epa'])}")
            if ev.get("sop"):
                fm.append(f"sop: {yq(ev['sop'])}")
            fm += [f"source: {yq(f'{SITE}/pregledPredpisa?id={pid}')}", f"retrieved: {retrieved}", "---", ""]
            text = "\n".join(fm) + f"\n# {title}\n\n" + body.strip() + "\n"
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            written.add(os.path.relpath(path, out))
            counts[cat] = counts.get(cat, 0) + 1
    # remove stale files
    for cat in CATS:
        for p in glob.glob(os.path.join(out, cat, "**", "*.md"), recursive=True):
            if os.path.relpath(p, out) not in written:
                os.remove(p)
    for p in glob.glob(os.path.join(out, "slike", "**", "*.*"), recursive=True):
        if os.path.relpath(p, out) not in WRITTEN_IMG:
            os.remove(p)
    with open(os.path.join(raw, "missing.tsv"), "w", encoding="utf-8") as f:
        for row in missing:
            f.write("\t".join(str(c) for c in row) + "\n")
    print("written:", counts, "missing:", len(missing))
    mc = {}
    for row in missing:
        mc[row[0]] = mc.get(row[0], 0) + 1
    print("missing per category:", mc)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=os.path.join(here, "..", "..", "_raw", "si"))
    ap.add_argument("--out", default=os.path.join(here, ".."))
    ap.add_argument("--retrieved", default=datetime.date.today().isoformat())
    a = ap.parse_args()
    convert(os.path.abspath(a.raw), os.path.abspath(a.out), a.retrieved)


if __name__ == "__main__":
    main()
