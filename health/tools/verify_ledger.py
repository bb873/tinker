#!/usr/bin/env python3
"""Re-fetch every PMID in research ledgers and check that the quoted text appears in the abstract or title.
Usage: python3 -I verify_ledger.py file1.md [file2.md ...]
Prints per-row status: VERIFIED (quote found), PARTIAL (>=60% of quote words found in order-insensitive match), NOT_FOUND, NO_PMID (URL sources, checked separately)."""
import sys, re, json, urllib.request, xml.etree.ElementTree as ET, html
E="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
def getb(u): return urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"ledger-verifier"}),timeout=60).read()
def get(u):
    b=getb(u)
    if b[:2] in (b"\xff\xfe",b"\xfe\xff") or b.count(b"\x00")>len(b)//4: return b.decode("utf-16","replace")
    return b.decode("utf-8","replace")
def url_for(src):
    m=re.search(r"(?:https?://)?((?:www\.)?(?:va\.gov/vetapp|law\.cornell\.edu|va\.gov/find-forms)[^\s|]*)",src)
    if m:
        h=m.group(1)
        return "https://"+(h if h.startswith("www.") else "www."+h)
    m=re.search(r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",src)
    if m and "aily" in src: return "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid="+m.group(1)
    return None
def norm(s): return re.sub(r"[^a-z0-9.%]+"," ",html.unescape(s).lower()).strip()
rows=[]
for f in sys.argv[1:]:
    for line in open(f):
        if not re.match(r"\|\s*S\d+[a-z]?\s*\|",line): continue
        cells=[c.strip() for c in line.strip().strip("|").split("|")]
        sid=cells[0]; src=cells[1]
        q=" ".join(re.findall(r'"([^"]{8,})"',line))
        pm=[] if url_for(src) else re.findall(r"\b(\d{7,8})\b",src)
        rows.append((f.split("/")[-1],sid,src,pm[0] if pm else None,q))
pmids=sorted({r[3] for r in rows if r[3]})
text={}
for i in range(0,len(pmids),50):
    root=ET.fromstring(get(E+"efetch.fcgi?db=pubmed&retmode=xml&id="+",".join(pmids[i:i+50])))
    for a in root.findall(".//PubmedArticle"):
        p=a.findtext(".//PMID"); text[p]=norm(" ".join(a.itertext()))
stats={}
for f,sid,src,pm,q in rows:
    if not pm:
        u=url_for(src)
        if not u: st="NO_URL"
        else:
            try: t=norm(re.sub(r"<[^>]+>"," ",get(u)))
            except Exception as e: t=""; 
            if not t: st="FETCH_FAIL"
            elif not q: st="NO_QUOTE"
            else:
                segs=[norm(x) for x in re.split(r"\.\.\.|…",q) if len(norm(x))>12]
                if segs and all(x in t for x in segs): st="VERIFIED"
                else:
                    w=[x for x in norm(q).split() if len(x)>3]; hit=sum(x in t for x in w)
                    st="PARTIAL" if w and hit/len(w)>=0.6 else "NOT_FOUND"
    elif pm not in text: st="PMID_MISSING"
    elif not q: st="NO_QUOTE"
    else:
        segs=[norm(s) for s in re.split(r"\.\.\.|…",q) if len(norm(s))>12]
        if segs and all(s in text[pm] for s in segs): st="VERIFIED"
        else:
            w=[x for x in norm(q).split() if len(x)>3]; hit=sum(x in text[pm] for x in w)
            st="PARTIAL" if w and hit/len(w)>=0.6 else "NOT_FOUND"
    stats[st]=stats.get(st,0)+1
    print(f"{f}\t{sid}\t{pm or src[:60]}\t{st}")
print("SUMMARY",json.dumps(stats))
