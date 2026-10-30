#!/usr/bin/env python3
"""Update the TUM people page (index.shtml) to match mikegeo98.github.io.

Usage on webvm:
    python3 tum_page_update.py --dry-run /var/www/sites/wwwdb/people/sites/georgoulakis/index.shtml
    python3 tum_page_update.py           /var/www/sites/wwwdb/people/sites/georgoulakis/index.shtml

Every edit must match exactly once; otherwise nothing is written and the
script says which edit failed. A timestamped backup is written next to the file.
"""
import difflib, re, shutil, sys, time

REMOVE_SESAME_ENTRY = True   # the SESAME'24 work-in-progress paper was dropped from the website too

SITE = "https://mikegeo98.github.io/"

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    if len(args) != 1:
        print(__doc__); sys.exit(2)
    path = args[0]
    with open(path, encoding="utf-8") as f:
        orig = f.read()
    s = orig
    log = []

    def once(pattern, repl, label, flags=re.S):
        nonlocal s
        hits = re.findall(pattern, s, flags)
        if len(hits) != 1:
            print(f"ABORT: edit '{label}' matched {len(hits)} times (expected 1). Nothing written.")
            sys.exit(1)
        s = re.sub(pattern, repl, s, count=1, flags=flags)
        log.append(label)

    # 1. Research Area: the five directions from the website
    once(r"(Research\s+Area.*?<ul>)(.*?)(</ul>)",
         lambda m: m.group(1) + """
                <li>Cloud database architectures</li>
                <li>Metadata management and caching</li>
                <li>Modern hardware and efficient computing</li>
                <li>Serverless query processing</li>
                <li>Benchmarking cloud analytics</li>
        """ + m.group(3),
         "research area list")

    # 2. Link to the personal website right under the profile card
    once(r"(<h2>\s*Research\s+Area)",
         lambda m: ("<p style=\"margin: 12px 0 18px\">For up-to-date research, publications and student topics see my personal website: "
                    f"<a href=\"{SITE}\"><strong>mikegeo98.github.io</strong></a></p>\n\n" + m.group(1)),
         "website link above research area")

    # 3. Publications: stale links and typos
    once(r"Mateusz, Gienieczko", "Mateusz Gienieczko", "stray comma in author list")
    once(r'<a target="_blank" href="https://dbtest-workshop\.github\.io/">Datenbank-Spektrum</a>',
         '<a target="_blank" href="https://link.springer.com/journal/13222">Datenbank-Spektrum, 2026</a>',
         "Datenbank-Spektrum venue link")
    once(r'<a target="_blank" href="https://vldb\.org/2026/">Demo@SIGMOD 2026\s*</a>',
         '<a target="_blank" href="https://2026.sigmod.org/">Demo @ SIGMOD 2026</a>',
         "SIGMOD demo venue link")
    once(r'<a target="_blank" href="https://vldb\.org/2026/">PVLDB 2025 \(Accepted, to be presented in VLDB 2026\)\s*</a>',
         '<a target="_blank" href="https://vldb.org/2026/">PVLDB 18(13), 2025 (presented at VLDB 2026)</a>',
         "PVLDB venue text")
    if REMOVE_SESAME_ENTRY:
        once(r'\s*<div class="publication"[^>]*>\s*<div class="title"><a href="[^"]*SESAME24_EuroSys\.pdf">.*?</div>\s*</div>',
             "\n", "remove SESAME'24 entry")

    # 4. Replace the commented-out Scholar line with a visible Links block
    once(r'<!--\s*<p><a href="https://scholar\.google\.com/citations\?user=gez8X_8AAAAJ[^"]*">Google Scholar</a></p>\s*-->',
         f"""<h2>Links</h2>
<p>
        <a href="{SITE}">Personal website</a> &middot;
        <a href="https://scholar.google.com/citations?user=gez8X_8AAAAJ&amp;hl=en">Google Scholar</a> &middot;
        <a href="https://github.com/mikegeo98">GitHub</a> &middot;
        <a href="https://www.linkedin.com/in/michalis-georgoulakis-misegiannis-26355322b">LinkedIn</a>
</p>""",
         "links block")

    # 5. Teaching: NGDS seminar row and the Praktikum role
    once(r'(<tr><td><b>SS 2026:</b>\s*</td><td><a href="/teaching/ss26/cbdp-lab">Praktikum: Cloud-Based Data Processing</a>)(</td></tr>)',
         lambda m: ('<tr><td><b>WS 2026/2027:</b> </td><td><a href="/teaching/ws2627/nextgen/">Seminar: Next-Generation Data Systems</a> (co-organizer)</td></tr>\n  '
                    + m.group(1) + " (lead organizer)" + m.group(2)),
         "teaching rows")

    # 6. Available topics: point at the directions and the website
    once(r"I am happy to supervise Bachelor's theses \(BT\), Master's theses \(MT\), and Guided Research \(GR\) projects on any of my interests or on the open topics below\.",
         "I am happy to supervise Bachelor's theses (BT), Master's theses (MT), and Guided Research (GR) projects in any of the research directions above. "
         f"Current ideas are listed on my <a href=\"{SITE}#students\">personal website</a>.",
         "available topics text")

    if s == orig:
        print("Nothing to change."); return
    if dry:
        sys.stdout.writelines(difflib.unified_diff(orig.splitlines(True), s.splitlines(True), "index.shtml (current)", "index.shtml (updated)"))
        print("\nDry run only. Edits that would apply:", ", ".join(log))
        return
    backup = f"{path}.bak-{time.strftime('%Y%m%d-%H%M%S')}"
    shutil.copy2(path, backup)
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)
    print("Applied:", ", ".join(log)); print("Backup:", backup)

if __name__ == "__main__":
    main()
