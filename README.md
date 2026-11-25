# IT & Operations Analytics Dashboard
A guided portfolio demonstration for IT service management, using 1,000 reproducible synthetic tickets (May–October 2026). No real client data. Built with AI assistance; review and reproduce the code before presenting it as your own work.

## Run
Open `dashboard.html` in a browser (offline, no installation). To regenerate the CSV and dashboard and execute the SQL checks, run `python build.py` from this folder (Python 3, standard library only).

## Analysis
`analysis.sql` creates metric, KPI, team and category views in SQLite. `build.py` generates ticket timestamps, priorities, categories, teams and SLA targets with a fixed random seed, loads the dataset into SQLite and runs integrity checks. Dashboard filters by team, priority and creation month. SLA targets are illustrative, not contractual; elapsed hours include weekends. Resolved SLA denominator excludes open tickets; overdue open tickets are separate. Snapshot is 1 November 2026.

## Interview preparation
Explain the difference between backlog and SLA compliance, the denominator choice, how the dataset is generated, and why real service-desk data would require business-hour calendars, reopened-ticket handling and data privacy safeguards. Try adding a new category, altering SLA thresholds and verifying the SQL outputs against the unfiltered dashboard. Publish only after reviewing the code and being able to explain it.
