import csv, random, sqlite3, json
from datetime import datetime,timedelta
from pathlib import Path
p=Path(__file__).parent
r=random.Random(42); start=datetime(2026,5,1); cutoff=datetime(2026,11,1)
fields=['ticket_id','created_at','resolved_at','category','priority','team','sla_hours']
rows=[]
for i in range(1000):
 c=start+timedelta(hours=r.randrange(int((cutoff-start).total_seconds()/3600)))
 cat=r.choices(['Access','Hardware','Network','Software','Cloud'],[30,25,15,20,10])[0]; pri=r.choices(['P1','P2','P3','P4'],[5,20,45,30])[0]; sla={'P1':4,'P2':12,'P3':24,'P4':48}[pri]
 team={'Access':'Service Desk','Hardware':'Endpoint','Network':'Infrastructure','Software':'Service Desk','Cloud':'Infrastructure'}[cat]
 end=c+timedelta(hours=round(r.lognormvariate(0,.85)*sla*.65,2)); end=end if end<cutoff and not ((cutoff-c).days<14 and r.random()<.25) else None
 rows.append([i+1,c.isoformat(),end.isoformat() if end else '',cat,pri,team,sla])
with (p/'tickets.csv').open('w',newline='') as f: w=csv.writer(f);w.writerow(fields);w.writerows(rows)
with sqlite3.connect(':memory:') as db:
 db.execute('CREATE TABLE tickets(ticket_id INTEGER PRIMARY KEY, created_at TEXT, resolved_at TEXT, category TEXT, priority TEXT, team TEXT, sla_hours INTEGER)')
 db.executemany('INSERT INTO tickets VALUES (?,?,?,?,?,?,?)',[tuple(x if x!='' else None for x in row) for row in rows]); db.executescript((p/'analysis.sql').read_text()); print(db.execute('SELECT * FROM kpis').fetchone())
 assert db.execute('SELECT COUNT(*) FROM tickets').fetchone()[0]==1000
 assert db.execute('SELECT COUNT(*) FROM metrics WHERE resolution_hours < 0').fetchone()[0]==0
html=(p/'dashboard_template.html').read_text().replace('__DATA__',json.dumps([dict(zip(fields,row)) for row in rows])); (p/'dashboard.html').write_text(html)
