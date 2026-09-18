# NEXT
Backfill days 11-17 as proper one-file-per-day loads.

$ cd ~/payflow
$ for d in 11 12 13 14 15 16 17; do python gen.py 2026-09-$d; done
$ gcloud storage cp transactions_2026-09-1*.csv gs://YOUR_BUCKET/raw/
$ then bq load each one into its own $YYYYMMDD partition (--replace, quoted table name)

Rule from now on: ONE FILE = ONE DAY. No multi-date files ever again.

## Where I stopped
payflow_raw.transactions is partitioned on created_at (DAY).
Idempotent load proven: ran 20260918 partition load twice, count stayed 100.
Only the 18th is in the table right now. Old multi-date files are unusable.
Committed.

## Open question
Doing 7 bq load commands by hand is stupid. Can I write a bash loop for it?
Once that loop exists -- isn't that basically what an orchestrator does?

## Then
Re-run mart_daily_revenue.sql once all 8 days are loaded. Expect ~24 rows
(8 days x 3 statuses x 1 currency).

## Parked (Session 4)
Automate it -- file lands, gets uploaded and loaded without a human.
Composer DAG vs GCS trigger + Cloud Function. Which and why?