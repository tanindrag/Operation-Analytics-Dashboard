-- Elapsed clock hours, not business hours. Snapshot: 2026-11-01.
CREATE VIEW metrics AS SELECT *, (julianday(resolved_at)-julianday(created_at))*24 AS resolution_hours,
(julianday('2026-11-01')-julianday(created_at))*24 AS age_hours FROM tickets;
CREATE VIEW kpis AS SELECT COUNT(*) AS total, COUNT(resolved_at) AS resolved,
COUNT(*)-COUNT(resolved_at) AS backlog, ROUND(AVG(resolution_hours),2) AS avg_resolution_hours,
ROUND(100.0*SUM(CASE WHEN resolution_hours <= sla_hours+0.000001 THEN 1 ELSE 0 END)/NULLIF(COUNT(resolved_at),0),2) AS resolved_sla_pct,
SUM(CASE WHEN resolved_at IS NULL AND age_hours>sla_hours THEN 1 ELSE 0 END) AS overdue_open FROM metrics;
CREATE VIEW by_team AS SELECT team, COUNT(*) AS tickets, COUNT(*)-COUNT(resolved_at) AS backlog, ROUND(AVG(resolution_hours),2) AS avg_hours FROM metrics GROUP BY team;
CREATE VIEW by_category AS SELECT category, COUNT(*) AS tickets, SUM(CASE WHEN resolution_hours>sla_hours+0.000001 THEN 1 ELSE 0 END) AS resolved_breaches FROM metrics GROUP BY category;
