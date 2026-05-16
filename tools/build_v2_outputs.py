import csv
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "bus_driver_violence_statutes.tsv"
OUT_TSV = ROOT / "bus_driver_violence_statutes_v2.tsv"
OUT_HTML = ROOT / "factcheck_v2.html"

with BASE.open("r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f, delimiter="\t")
    rows = list(reader)
    fields = reader.fieldnames

by_state = {row["Jurisdiction"]: row for row in rows}


def upd(state, **changes):
    by_state[state].update(changes)


upd(
    "Arizona",
    **{
        "Statute number(s)": "A.R.S. section 13-1204(A)(8)(k) until Jan. 1, 2033; A.R.S. section 13-1204(A)(8)(l) after Dec. 31, 2032; 2025 Ariz. Sess. Laws ch. 172",
        "Covered worker/setting": "Public transit employee who performs duties on and off a vehicle while engaged in transferring members of the community to and from destinations in a bus, van, or shuttle",
        "Statutory language / trigger (condensed from statute)": "Aggravated assault includes an assault where the victim is a public transit employee who performs duties on and off a vehicle while engaged in transferring community members to and from destinations in a bus, van, or shuttle.",
        "Source URL(s)": "https://law.justia.com/codes/arizona/title-13/section-13-1204/; https://law.justia.com/codes/arizona/title-13/section-13-1204-version-2/; https://www.azleg.gov/legtext/57leg/1r/laws/0172.htm",
        "Notes": "V2 fact-check: current 2025 text confirms the transit category; citation now notes the parallel post-2032 version. Same 2025 chapter also added airport employees and railway workers, but those are outside the bus/public-transit-driver scope. 2026 SB1448 would add utility workers but was not chaptered/current as of this fact-check.",
    },
)

upd(
    "Colorado",
    **{
        "Notes": "V2 fact-check: signed HB25-1290 PDF confirms the section 18-9-111(1)(i) transit-worker harassment/interference language, Class 1 misdemeanor treatment, and section 32-9-160 Class 2 misdemeanor RTD interference language. This remains an interference/harassment law, not an assault reclassification.",
    },
)

upd(
    "Illinois",
    **{
        "Statute number(s)": "720 ILCS 5/12-2; 720 ILCS 5/12-3.05",
        "Statutory language / trigger (condensed from statute)": "Aggravated assault and aggravated battery include offenses against drivers, operators, employees, or passengers of a transportation facility/system.",
        "Source URL(s)": "https://www.ilga.gov/legislation/ilcs/documents/072000050K12-2.htm; https://www.ilga.gov/documents/legislation/ilcs/documents/072000050K12-3.05.htm; https://www.ilga.gov/Legislation/ILCS/Articles?ActID=1827&ChapterID=49&Print=True",
        "Notes": "V2 fact-check: moved 625 ILCS 50/1 out of the criminal statute list because it is the Public Conveyance Notice Act, a notice/signage law. It is still retained as a source/note because it describes required public notices about the penalties.",
    },
)

upd(
    "Louisiana",
    **{
        "Transit/bus-driver-specific treatment": "Yes. Battery of a bus operator is a separate offense.",
        "Covered worker/setting": "Bus operator employed by a public transit system who operates a bus, or an electronically operated cable car operator; school bus operators are excluded.",
        "Statutory language / trigger (condensed from statute)": "Battery of a bus operator is battery committed without consent when the offender has reasonable grounds to believe the victim is a bus operator; the penalty subsection applies while the operator is operating a bus.",
        "Source URL(s)": "https://legis.la.gov/Legis/Law.aspx?d=206144; https://law.justia.com/codes/louisiana/revised-statutes/title-14/rs-14-34-5-1/; https://www.legis.la.gov/Legis/ViewDocument.aspx?d=1380490",
        "Notes": "V2 fact-check: corrected overbroad v1 TSV language that said train operator. Current official and Justia text covers bus operators and electronically operated cable car operators, excluding school bus operators. Acts 2024, No. 367 increased the penalty to 72 hours-1 year and up to $1,000.",
    },
)

upd(
    "Maryland",
    **{
        "Punishment / grading": "Misdemeanor under section 7-705(f): fine up to $1,000 and imprisonment up to 1 year, or both. General transit-rule violations under section 7-705(e) carry a lower fine up to $500.",
        "Notes": "V2 fact-check: 7-705(f) interference penalty and 7-705.1 administrative transit-ban process confirmed. Added the lower 7-705(e) fine tier for non-interference transit-rule violations.",
    },
)

upd(
    "Massachusetts",
    **{
        "Source URL(s)": "https://malegislature.gov/Laws/SessionLaws/Acts/2025/Chapter79; https://malegislature.gov/Laws/GeneralLaws/PartIV/TitleI/Chapter265/Section13D",
        "Notes": "V2 fact-check: 2025 Acts ch. 79 was approved Dec. 3, 2025 and amended ch. 265, section 13D to cover public transit workers and contracted/employed transit workers; current by the May 16, 2026 review date.",
    },
)

upd(
    "Michigan",
    **{
        "Notes": "V2 fact-check: conclusion remains no current enacted public-transit-operator enhancement. 2023-2024 HB4917/HB4918 proposed new transit-operator assault provisions, but available legislative sources show proposed MCL 750.81g rather than enacted current law.",
    },
)

upd(
    "Minnesota",
    **{
        "Statute number(s)": "Minn. Stat. sections 609.2231 subd. 11, 609.855 subds. 2 and 5",
        "Statutory language / trigger (condensed from statute)": "Section 609.2231 subd. 11 covers assaulting a transit operator or intentionally throwing/transferring bodily fluids onto the operator while the operator is performing duties in/near a transit vehicle. Section 609.855 covers intentional interference/obstruction of transit-vehicle operation, with higher penalty if force, violence, or threat is used, and separately covers shooting at transit vehicles.",
        "Punishment / grading": "Transit-operator assault/bodily-fluid offense: gross misdemeanor, up to 364 days/$3,000. Interference with force/violence/threat: up to 3 years/$5,000; otherwise up to 90 days/$1,000. Shooting at transit vehicle: up to 3 years/$6,000 if unoccupied and up to 5 years/$10,000 if occupied.",
        "Notes": "V2 fact-check: core transit-operator assault and interference entries confirmed; added 609.855 subd. 5 shooting-at-transit-vehicle penalty. 2026 bills to expand transit-worker language were pending/not enacted in this review.",
    },
)

upd(
    "Nevada",
    **{
        "Notes": "V2 fact-check: transit-operator assault/battery protections remain. 2025 AB344/Chapter 328 creates a July 1, 2026 version adding utility-worker language, but it does not remove transit-operator coverage; this future-effective change is not a material correction to the current transit row as of May 16, 2026.",
    },
)

upd(
    "Tennessee",
    **{
        "Source URL(s)": "https://law.justia.com/codes/tennessee/title-39/chapter-13/part-1/section-39-13-101/; https://law.justia.com/codes/tennessee/title-39/chapter-13/part-1/section-39-13-102/",
        "Notes": "V2 fact-check: I do not agree with factcheck_v1 on Tennessee. Current 2024 Tennessee Code section 39-13-102 says subsection (d) and the related Class A misdemeanor provision in (e)(1)(A)(i) were deleted by 2018 amendment. Older 2010/2014 pages that still show transit-employee language are stale.",
    },
)

upd(
    "Virginia",
    **{
        "Notes": "V2 fact-check: current Virginia page dated 5/16/2026 confirms subsection F unchanged; historical note lists 2025 c. 361 as the most recent amendment to section 18.2-57.",
    },
)

upd(
    "Washington",
    **{
        "Notes": "V2 fact-check: RCW 9A.36.031(1)(b) transit-operator assault remains Class C felony and shows 2024 c 220 history. RCW 9.91.025 unlawful transit conduct was amended by 2025 c 234 s 1; misdemeanor characterization unchanged.",
    },
)

upd(
    "West Virginia",
    **{
        "Covered worker/setting": "Driver, conductor, motorman, captain, pilot, or other person in charge of a vehicle, aircraft, or boat used for public conveyance, acting in official capacity",
        "Statutory language / trigger (condensed from statute)": "Statute covers malicious assault, unlawful assault, battery, and assault upon the operator/person in charge of a public conveyance while acting in official capacity; the unlawful-assault tier expressly includes vehicle, aircraft, or boat.",
        "Notes": "V2 fact-check: added aircraft to the scope description for the unlawful-assault tier. Penalty ranges otherwise confirmed.",
    },
)

upd(
    "Wisconsin",
    **{
        "Notes": "V2 fact-check: 2025 Wisconsin Act 24 reorganized battery provisions. Current transit-vehicle operator/driver/passenger battery is in Wis. Stat. section 940.62(1)(e), with public-transit-vehicle definition in section 940.51(19). Do not cite former section 940.20 as current authority for this provision.",
    },
)


def default_summary():
    return {
        "status": "Confirmed / no material update found",
        "v1": "No specific v1 dispute; v2 review found no material correction beyond the existing row.",
        "finding": "Live/current source review and targeted update search did not identify a newer enacted transit-driver-specific change requiring a row edit.",
        "action": "No v2 table change.",
    }


findings = {row["Jurisdiction"]: default_summary() for row in rows}


def finding(state, status, v1, finding_text, action):
    findings[state] = {
        "status": status,
        "v1": v1,
        "finding": finding_text,
        "action": action,
    }


finding("Arizona", "Nuance updated", "Partly agree with v1. The dual-version citation point is correct; airport/railway additions are real but outside the core bus/public-transit-driver scope.", "Current 2025 Arizona text confirms public transit employee at (A)(8)(k) before 2033 and (A)(8)(l) after 2032; same chapter also added airport employees and railway workers. 2026 SB1448 is pending/engrossed, not current law in this review.", "Updated v2 citation, covered-worker language, sources, and notes.")
finding("Colorado", "Confirmed; v1 concern resolved", "Disagree with v1 framing that grades were unverified. They are verifiable from the signed PDF.", "Signed HB25-1290 text confirms 18-9-111(1)(i), Class 1 misdemeanor, and 32-9-160 Class 2 misdemeanor language.", "Kept row substance; strengthened note.")
finding("Illinois", "Nuance updated", "Agree with v1.", "625 ILCS 50/1 is the Public Conveyance Notice Act, not the criminal assault/battery statute. Criminal authority remains 720 ILCS 5/12-2 and 12-3.05.", "Moved 625 ILCS 50/1 out of statute-number column and into source/note context.")
finding("Louisiana", "Corrected", "Agree with v1.", "Current official Louisiana and Justia text covers bus operators and electronically operated cable car operators; it does not cover train operators. Acts 2024, No. 367 increased penalties.", "Corrected covered worker, trigger, notes, and sources.")
finding("Maryland", "Minor detail added", "Agree with v1 minor point.", "7-705(f) interference penalty is correct; 7-705(e) has a separate lower fine tier for general transit-rule violations.", "Added lower-tier penalty note.")
finding("Massachusetts", "Confirmed current 2025 update", "v1 listed no issue; row remains correct.", "Chapter 79 of the Acts of 2025 amended ch. 265, section 13D to cover public transit workers and contracted/employed transit workers; approved Dec. 3, 2025 and current by review date.", "Strengthened note/source currency.")
finding("Michigan", "Confirmed no enacted transit enhancement", "Agree with v1 conclusion and cache caveat.", "Public-utility-worker statutes do not cover transit; HB4917/HB4918 proposed transit-operator protections but available sources show proposed, not enacted, MCL 750.81g.", "Updated note with proposed bill context.")
finding("Minnesota", "Minor detail added", "Agree with v1 minor point.", "Core 609.2231 subd. 11 and 609.855 subd. 2 are correct; 609.855 subd. 5 also covers shooting at transit vehicles. 2026 expansion bills appear pending/not enacted.", "Added subd. 5 to statute/trigger/punishment notes.")
finding("Nevada", "Confirmed; future-effective note", "v1 listed no issue.", "NRS transit-operator coverage remains. 2025 AB344/Chapter 328 adds utility-worker language in a July 1, 2026 version but does not remove transit-operator coverage.", "Added future-effective note only.")
finding("Tennessee", "V1 rejected; original conclusion confirmed", "Disagree with v1 critical finding.", "Current 2024 Tennessee Code says section 39-13-102(d) was deleted by a 2018 amendment, along with the related Class A misdemeanor provision. v1 relied on stale 2010/2014 text.", "Kept no-current-transit-enhancement conclusion; replaced/strengthened sources and note.")
finding("Vermont", "Confirmed no enacted transit enhancement; pending bill noted", "v1 listed no issue.", "Targeted search found Vermont H.255 introduced in 2025 for public transit workers, but no enacted current-law change was identified in this review.", "No table change.")
finding("Virginia", "Minor currency note added", "Agree with v1 minor point.", "Current page dated 5/16/2026 confirms subsection F and notes 2025 c. 361 as latest amendment; transit provision unchanged.", "Added 2025 amendment note.")
finding("Washington", "Minor currency note added", "Agree with v1 minor point.", "RCW 9A.36.031 remains Class C felony for transit operator/driver assault. RCW 9.91.025 was amended by 2025 c 234 s 1; misdemeanor unchanged.", "Added amendment-history note.")
finding("West Virginia", "Minor scope detail added", "Agree with v1 minor point.", "W. Va. Code section 61-2-16a includes aircraft in the unlawful-assault tier; penalties otherwise accurate.", "Added aircraft to covered worker/setting and trigger.")
finding("Wisconsin", "Minor citation note strengthened", "Agree with v1 minor point.", "2025 Act 24 reorganized the law; section 940.62(1)(e) is current for public-transit vehicle operator/driver/passenger battery.", "Strengthened note not to cite old section 940.20 as current authority.")

with OUT_TSV.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({key: by_state[row["Jurisdiction"]][key] for key in fields})

changed_states = sorted(
    state for state, item in findings.items() if item["action"] != "No v2 table change."
)
status_counts = {}
for item in findings.values():
    status_counts[item["status"]] = status_counts.get(item["status"], 0) + 1

source_highlights = [
    ("Tennessee current code", "https://law.justia.com/codes/tennessee/title-39/chapter-13/part-1/section-39-13-102/", "Current 2024 text says subsection (d) deleted by 2018 amendment."),
    ("Louisiana official code", "https://legis.la.gov/Legis/Law.aspx?d=206144", "Current text covers bus operators/cable car operators, not train operators."),
    ("Colorado signed HB25-1290 PDF", "https://www.leg.colorado.gov/bill_files/40794/download", "Signed text confirms harassment/interference and misdemeanor grades."),
    ("Arizona current 13-1204", "https://law.justia.com/codes/arizona/title-13/section-13-1204/", "Current version confirms public transit employees plus airport and railway additions."),
    ("Washington RCW 9.91.025", "https://app.leg.wa.gov/RCW/default.aspx?cite=9.91.025", "Citation history includes 2025 c 234 s 1; misdemeanor unchanged."),
    ("Massachusetts Acts 2025 ch. 79", "https://malegislature.gov/Laws/SessionLaws/Acts/2025/Chapter79", "Adds public transit worker and contracted transit worker coverage."),
]

css = """
:root { --bg:#f7f8fb; --ink:#20242c; --muted:#657184; --line:#d9e0ea; --surface:#fff; --green:#18794e; --green-bg:#eaf8f0; --amber:#9a6200; --amber-bg:#fff4dc; --red:#a13a34; --red-bg:#ffeceb; --blue:#2754c5; --blue-bg:#eef2ff; }
* { box-sizing:border-box; }
body { margin:0; font-family:Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color:var(--ink); background:var(--bg); line-height:1.5; }
header { padding:32px 24px 20px; background:#172033; color:white; }
main { max-width:1400px; margin:0 auto; padding:22px 24px 44px; }
h1 { margin:0 0 8px; font-size:clamp(2rem,4vw,4rem); line-height:1; letter-spacing:0; }
h2 { margin:28px 0 12px; font-size:1.25rem; }
h3 { margin:0 0 8px; font-size:1rem; }
p { margin:0 0 12px; }
a { color:#1a5bd7; }
.meta { color:#c5cede; margin:0; max-width:900px; }
.grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:12px; margin:18px 0; }
.card { background:var(--surface); border:1px solid var(--line); border-radius:8px; padding:16px; box-shadow:0 10px 24px rgba(32,36,44,.05); }
.num { display:block; font-size:2rem; font-weight:800; line-height:1; }
.label { color:var(--muted); font-size:.78rem; font-weight:750; text-transform:uppercase; letter-spacing:.04em; }
.callout { border-left:5px solid var(--blue); background:var(--blue-bg); padding:14px 16px; border-radius:8px; margin:16px 0; }
.callout.warn { border-left-color:var(--amber); background:var(--amber-bg); }
.callout.bad { border-left-color:var(--red); background:var(--red-bg); }
.table-wrap { overflow:auto; border:1px solid var(--line); border-radius:8px; background:white; }
table { width:100%; border-collapse:collapse; min-width:980px; }
th,td { padding:10px 12px; border-bottom:1px solid var(--line); text-align:left; vertical-align:top; font-size:.88rem; }
th { position:sticky; top:0; background:#eef2f7; color:var(--muted); font-size:.74rem; text-transform:uppercase; letter-spacing:.04em; }
tr:last-child td { border-bottom:0; }
.badge { display:inline-flex; align-items:center; border-radius:999px; padding:4px 8px; font-size:.72rem; font-weight:800; white-space:nowrap; }
.confirmed { background:var(--green-bg); color:var(--green); }
.updated { background:var(--amber-bg); color:var(--amber); }
.rejected { background:var(--red-bg); color:var(--red); }
.source-list { display:grid; gap:8px; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); }
.source-list a { display:block; background:white; border:1px solid var(--line); border-radius:8px; padding:10px 12px; text-decoration:none; overflow-wrap:anywhere; }
.small { color:var(--muted); font-size:.85rem; }
code { background:#eef2f7; padding:1px 5px; border-radius:4px; }
footer { color:var(--muted); font-size:.85rem; padding:20px 24px 36px; max-width:1400px; margin:0 auto; }
"""


def badge_for(status):
    lowered = status.lower()
    if "rejected" in lowered:
        return "rejected"
    if lowered.startswith("confirmed / no material"):
        return "confirmed"
    return "updated"


counts_html = "".join(
    f'<div class="card"><span class="num">{count}</span><span class="label">{html.escape(status)}</span></div>'
    for status, count in sorted(status_counts.items())
)
changed_html = "".join(
    f"<li><strong>{html.escape(state)}</strong>: {html.escape(findings[state]['action'])}</li>"
    for state in changed_states
)
source_html = "".join(
    f'<a href="{html.escape(url)}"><strong>{html.escape(name)}</strong><br><span class="small">{html.escape(note)}</span></a>'
    for name, url, note in source_highlights
)

table_rows = []
for row in rows:
    jurisdiction = row["Jurisdiction"]
    finding_item = findings[jurisdiction]
    source_urls = [
        source.strip()
        for source in by_state[jurisdiction]["Source URL(s)"].split(";")
        if source.strip()
    ]
    links = "<br>".join(
        f'<a href="{html.escape(url)}">source</a>' for url in source_urls[:3]
    )
    table_rows.append(
        f"""
<tr>
  <td><strong>{html.escape(jurisdiction)}</strong></td>
  <td><span class="badge {badge_for(finding_item['status'])}">{html.escape(finding_item['status'])}</span></td>
  <td>{html.escape(finding_item['v1'])}</td>
  <td>{html.escape(finding_item['finding'])}</td>
  <td>{html.escape(finding_item['action'])}</td>
  <td>{links}</td>
</tr>"""
    )

OUT_HTML.write_text(
    f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Fact-check v2 - Transit Driver Violence Statutes</title>
  <style>{css}</style>
</head>
<body>
  <header>
    <h1>Fact-check v2</h1>
    <p class="meta">State-by-state review of bus/public-transit-driver violence statute research. Review date: May 16, 2026. This report compares <code>factcheck_v1.html</code> with current source checks and writes a corrected versioned table at <code>bus_driver_violence_statutes_v2.tsv</code>.</p>
  </header>
  <main>
    <section class="grid">
      <div class="card"><span class="num">51</span><span class="label">Jurisdictions reviewed</span></div>
      <div class="card"><span class="num">{len(changed_states)}</span><span class="label">V2 row updates or notes</span></div>
      <div class="card"><span class="num">1</span><span class="label">v1 critical finding rejected</span></div>
      <div class="card"><span class="num">0</span><span class="label">new enacted 2026 transit-driver laws found</span></div>
    </section>

    <div class="callout bad">
      <h3>Bottom line on factcheck_v1</h3>
      <p>I agree with v1 on Louisiana, Illinois, Arizona's dual-version nuance, and several minor currency/scope notes. I do not agree with v1's critical Tennessee finding: current 2024 Tennessee Code says the transit-employee subsection in section 39-13-102(d) was deleted by a 2018 amendment. I also do not agree that Colorado's penalty grades were unverified; the signed HB25-1290 PDF confirms them.</p>
    </div>

    <div class="callout warn">
      <h3>Important scope note</h3>
      <p>This review looked for enacted current statutes. Pending or future-effective items were noted where found, but were not treated as current law on May 16, 2026. Examples include Arizona SB1448, Vermont H.255, Minnesota 2026 expansion bills, Michigan transit-operator bills, and Nevada's July 1, 2026 utility-worker additions.</p>
    </div>

    <h2>Versioned Files Created</h2>
    <div class="grid">
      <div class="card"><h3>bus_driver_violence_statutes_v2.tsv</h3><p>Corrected/currented version of the 51-row TSV with the same columns as v1.</p></div>
      <div class="card"><h3>factcheck_v2.html</h3><p>This state-by-state report, including agreement/disagreement with <code>factcheck_v1.html</code>.</p></div>
    </div>

    <h2>Rows Updated in v2</h2>
    <div class="card"><ol>{changed_html}</ol></div>

    <h2>High-value Sources Checked</h2>
    <div class="source-list">{source_html}</div>

    <h2>Status Counts</h2>
    <section class="grid">{counts_html}</section>

    <h2>State-by-State Findings</h2>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Jurisdiction</th>
            <th>V2 status</th>
            <th>Agreement with factcheck_v1</th>
            <th>Finding</th>
            <th>Action</th>
            <th>Sources</th>
          </tr>
        </thead>
        <tbody>{''.join(table_rows)}</tbody>
      </table>
    </div>
  </main>
  <footer>
    Research support, not legal advice. Charging, sentencing, effective dates, and local-law coverage can depend on facts and later amendments.
  </footer>
</body>
</html>
""",
    encoding="utf-8",
)

print(f"Wrote {OUT_TSV.name}")
print(f"Wrote {OUT_HTML.name}")
