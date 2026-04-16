#!/usr/bin/env python
import sys
import os
import warnings
from datetime import datetime
from pathlib import Path
import sqlite3
from weasyprint import HTML
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.status import Status
from rich.text import Text
from dotenv import load_dotenv

load_dotenv()
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

from insightgape.crew import InsightGapeCrew

DB_PATH = "audits.db"
OUTPUTS_DIR = Path("outputs")
OUTPUTS_DIR.mkdir(exist_ok=True)


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS audits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT,
            date TEXT,
            md_path TEXT,
            pdf_path TEXT
        )
    """)
    conn.commit()
    conn.close()


def run_audit(ticker: str, console: Console):
    inputs = {"ticker": ticker.upper()}
    status = Status(f"Running Black Box Audit for {ticker}...", spinner="dots")
    with Live(status, refresh_per_second=10):
        result = InsightGapeCrew().audit_crew().kickoff(inputs=inputs, verbose=2)

    # Assume report_task outputs to fixed path or extract
    date_str = datetime.now().strftime("%Y-%m-%d")
    md_path = OUTPUTS_DIR / f"{date_str}_{ticker}_audit.md"
    pdf_path = md_path.with_suffix(".pdf")

    # Generate PDF
    try:
        HTML(str(md_path)).write_pdf(str(pdf_path))
        console.print(f"[green]✅ PDF generated: {pdf_path}")
    except Exception as e:
        console.print(f"[yellow]⚠️ PDF failed: {e}")

    # Save to DB
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO audits (ticker, date, md_path, pdf_path) VALUES (?, ?, ?, ?)",
        (ticker, datetime.now().isoformat(), str(md_path), str(pdf_path)),
    )
    conn.commit()
    conn.close()
    console.print(f"[green]Audit logged in DB!")


def show_history(console: Console):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM audits ORDER BY date DESC LIMIT 10")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        console.print("[yellow]No audits yet!")
        return

    table = Table("ID", "Ticker", "Date", "MD Path", "PDF Path", title="Audit History")
    for row in rows:
        table.add_row(*[str(x) for x in row])
    console.print(table)


def main():
    init_db()
    console = Console()

    while True:
        console.clear()
        console.print(
            Panel.fit(
                Text(
                    "🕵️‍♂️  InsightGape Auditor\nBlack Box Corporate Narrative Audit",
                    style="bold cyan",
                ),
                style="bold blue",
            )
        )

        choices = ["1. Nueva Auditoría", "2. Historial", "3. Config", "q. Salir"]
        choice = Prompt.ask("Opción", choices=choices, default="1")

        if choice == "1":
            ticker = Prompt.ask("Ticker (ej. TSLA)")
            if Confirm.ask("Ejecutar audit?"):
                run_audit(ticker, console)
                Prompt.ask("Presiona Enter para continuar")
        elif choice == "2":
            show_history(console)
            Prompt.ask("Presiona Enter")
        elif choice == "3":
            console.print(
                f"[green]✅ ALPHA_VANTAGE_KEY: {'OK' if os.getenv('ALPHA_VANTAGE_KEY') else 'Missing'}"
            )
            console.print(
                f"[green]✅ SERPER_API_KEY: {'OK' if os.getenv('SERPER_API_KEY') else 'Missing'}"
            )
            Prompt.ask("Presiona Enter")
        else:
            break


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        init_db()
        console = Console()
        run_audit("TSLA", console)
    else:
        main()
