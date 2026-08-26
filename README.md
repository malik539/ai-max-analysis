# AI Max Search Term Audit — 5 Google Ads accounts

Forensic audit of Google Ads **AI Max**-generated search terms across five
orthodontic / dental accounts, covering **July 27 – August 25, 2026** (identical
window in all five source files).

**Deliverables**

- [`report/ai-max-audit.html`](report/ai-max-audit.html) — the full report (self-contained, theme-aware).
- [`report/ai-max-brief.html`](report/ai-max-brief.html) — a 3-page executive brief; prints to exactly 3 A4 pages.
- [`report/AI-Max-Audit-Brief.pdf`](report/AI-Max-Audit-Brief.pdf) — that brief as a PDF.

## Headline result

| | AI Max | Keyword-matched |
|---|---:|---:|
| Search terms | 3,608 | 3,319 |
| Spend | $3,409 | $5,206 |
| Conversions | 17.64 | 37.62 |
| Conversion rate | 6.61% | 9.57% |
| Cost per conversion | **$193** | **$138** |
| Relevant terms | 41.3% | 81.4% |
| Irrelevant + wasteful terms | 24.7% | 6.1% |
| Spend on irrelevant terms | 27.0% | 1.8% |

**Verdict:** keep AI Max enabled under tight controls; restrict hard on Ortho
Excellence and Holt Orthodontics. Confidence: High on the relevance/waste
findings, Medium on the account-level CPA rankings.

## Layout

```
analysis/
  load.py       source .xlsx -> tidy dataframe (drops "Total:" rows)
  classify.py   per-account intent classifier (5 relevance classes)
  metrics.py    AI Max vs keyword-matched aggregates
  charts.py       shared SVG chart primitives (stacked, grouped, hbars)
  build.py        renders report/ai-max-audit.html
  build_brief.py  renders report/ai-max-brief.html (3 x A4)
  head.html       full-report stylesheet
  brief_head.html brief stylesheet (print rules: @page A4, fixed 297mm pages)
data/
  classified_search_terms.csv   all 6,927 terms with assigned class + reason
  metrics.json                  every figure used in the report
report/
  ai-max-audit.html             the report
```

## Reproducing

```bash
pip install pandas openpyxl
cd analysis && python3 metrics.py   # prints the comparison tables
python3 build.py                    # regenerates the full report
python3 build_brief.py              # regenerates the 3-page brief
```

Source files are the five Google Ads "Search terms report" .xlsx exports. Every
spend and conversion figure reconciles exactly to the `Total: Search terms` line
of each source file.

## Method notes

Relevance is judged **per account**, against the services each practice actually
advertises (read from its own campaigns, ad groups, and keyword-matched terms) —
"emergency dentist" is highly relevant for South Florida and irrelevant for
Sabinsky. Classes: Highly Relevant, Relevant / Acceptable, Borderline / Low
Intent, Irrelevant, Clearly Wasteful. Boundaries are stated in §02 of the report.

Three limits are flagged prominently in the report and apply to every figure:
Google withholds 29–45% of spend behind "Other search terms"; the exports carry
no conversion values or action names, so primary and secondary conversions cannot
be separated; and 267 AI Max clicks over 30 days is a thin base for efficiency
conclusions (though ample for relevance conclusions).
