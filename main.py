from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.routes import transactions, payouts
from app.config import APP_NAME, CORS_ALLOW_ORIGINS, AUTO_REFRESH_SECONDS
from app.db import cur

app = FastAPI(title=APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in CORS_ALLOW_ORIGINS.split(",")] if CORS_ALLOW_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["Transactions"])
app.include_router(payouts.router, prefix="/api/v1/payouts", tags=["Payouts"])

@app.get("/health")
def health():
    return {"ok": True, "service": APP_NAME}

@app.get("/dashboard")
def dashboard():
    cur.execute("""SELECT id, card_last4, protocol, amount, payout_type, payout_network,
                          payout_target, result_status, reference, created_at
                   FROM transactions ORDER BY id DESC LIMIT 200""")
    rows = cur.fetchall()
    html = f"""
    <html>
    <head>
      <title>{APP_NAME} Dashboard</title>
      <meta http-equiv="refresh" content="{AUTO_REFRESH_SECONDS}">
      <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f7f7f7; }}
        table {{ border-collapse: collapse; width: 100%; background: #fff; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; font-size: 14px; }}
        th {{ background: #f0f0f0; }}
        tr:nth-child(even) {{ background: #fafafa; }}
      </style>
    </head>
    <body>
      <h1>{APP_NAME} — Transactions</h1>
      <p>Auto-refresh: {AUTO_REFRESH_SECONDS}s</p>
      <table>
        <tr>
          <th>ID</th><th>Card Last4</th><th>Protocol</th><th>Amount</th>
          <th>Payout Type</th><th>Network</th><th>Target</th>
          <th>Status</th><th>Reference</th><th>Created</th>
        </tr>
    """
    for r in rows:
        html += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td><td>{r[6]}</td><td>{r[7]}</td><td>{r[8]}</td><td>{r[9]}</td></tr>"
    html += """
      </table>
    </body>
    </html>
    """
    return HTMLResponse(html)
