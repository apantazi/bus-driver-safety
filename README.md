# Bus Driver / Public Transit Worker Violence Statutes

Research date: 2026-05-16.

Main files:

- `index.html`: interactive browser app for searching, sorting, filtering, and inspecting each state.
- `bus_driver_violence_statutes.tsv`: spreadsheet-friendly source table.

Raw downloaded source pages/PDFs used during research are in `source_cache/`.

To run the app locally:

```powershell
python -m http.server 8000
```

Then open `http://127.0.0.1:8000/`.

Scope:

- Covers all 50 states plus the District of Columbia.
- Focus is current state/D.C. statutes for violence against public transit drivers, public transit workers, bus drivers, school bus drivers, and closely related transit-operation interference or bus-hijacking offenses.
- Local ordinances are not exhaustively surveyed. A local example is included for Alaska because Anchorage has an on-point public-transit-worker assault ordinance and no comparable state transit-driver enhancement was located.
- The "statutory language / trigger" column is a condensed description of the operative statutory language. Use the source URLs for exact current code text.
- This is research support, not legal advice. Charging, grading, sentencing ranges, enhancements, and effective dates can depend on facts, criminal history, amendments, local ordinances, and sentencing statutes.

Method notes:

- I treated state/D.C. primary code pages, official bill/session-law pages, and official legislative PDFs as preferred sources.
- A 2012 ATU/JPI secondary chart was used only as a historical checklist, not as current authority.
- Several older chart entries have changed: Wisconsin's transit-battery coverage is now in Wis. Stat. section 940.62, Colorado enacted a new 2025 transit-worker interference/harassment law, Maryland added a 2025 transit-ban provision, Arizona added a 2025 public-transit-employee aggravated-assault provision, and Massachusetts broadened its transit-worker assault-and-battery coverage in 2025.
