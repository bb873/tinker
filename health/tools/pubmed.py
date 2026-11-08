#!/usr/bin/env python3
"""PubMed helper for research agents. Uses NCBI E-utilities through the session proxy.

Usage:
  python3 -I pubmed.py search "query terms" [max=8]   -> PMID | year | journal | title
  python3 -I pubmed.py abstract PMID [PMID ...]        -> title, journal, year, abstract text
  python3 -I pubmed.py page URL ["regex"]              -> plain text of an allowlisted page (first 6000 chars, or context around regex matches)
"""
import sys, json, re, html, urllib.request, urllib.parse, xml.etree.ElementTree as ET
E = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "health-research-agent/1.0"})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
def search(q, n=8):
    ids = json.loads(get(E + "esearch.fcgi?db=pubmed&retmode=json&sort=relevance&retmax=%d&term=%s" % (n, urllib.parse.quote(q))))["esearchresult"]["idlist"]
    if not ids: print("no results"); return
    s = json.loads(get(E + "esummary.fcgi?db=pubmed&retmode=json&id=" + ",".join(ids)))["result"]
    for i in ids:
        r = s[i]; print(f"{i} | {r.get('pubdate','')[:4]} | {r.get('source','')} | {r.get('title','')}")
def abstract(ids):
    root = ET.fromstring(get(E + "efetch.fcgi?db=pubmed&retmode=xml&id=" + ",".join(ids)))
    for a in root.findall(".//PubmedArticle"):
        pmid = a.findtext(".//PMID"); t = "".join(a.find(".//ArticleTitle").itertext())
        j = a.findtext(".//Journal/Title"); y = a.findtext(".//PubDate/Year") or a.findtext(".//PubDate/MedlineDate")
        ab = " ".join("".join(x.itertext()) for x in a.findall(".//AbstractText"))
        pt = ", ".join(p.text for p in a.findall(".//PublicationType"))
        print(f"PMID {pmid} | {y} | {j}\nTITLE: {t}\nTYPE: {pt}\nABSTRACT: {ab or '(none)'}\n")
def page(url, pat=None):
    t = get(url); t = re.sub(r"(?s)<(script|style).*?</\1>", "", t); t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"\s+", " ", html.unescape(t))
    if not pat: print(t[:6000]); return
    hits = [m.start() for m in re.finditer(pat, t, re.I)][:6]
    if not hits: print("pattern not found"); return
    for h in hits: print("..." + t[max(0,h-300):h+900] + "...\n")
if __name__ == "__main__":
    c = sys.argv[1]
    if c == "search": search(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 8)
    elif c == "abstract": abstract(sys.argv[2:])
    elif c == "page": page(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
