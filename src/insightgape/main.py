#!/usr/bin/env python
"""InsightGape CLI."""

import sys
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
import os

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
        crew = InsightGapeCrew()
        result = crew.audit_crew().kickoff(inputs=inputs)

    # Dynamic MD from report_task output
    date_str = datetime.now().strftime("%Y-%m-%d")
    md_path = OUTPUTS_DIR / f"{date_str}_{ticker}_audit.md"
    pdf_path = md_path.with_suffix(".pdf")

    # Write report from last task raw
    report_content = result.tasks_output[-1].raw
    with open(md_path, "w") as f:
        f.write(report_content)

    # PDF
    try:
        HTML(str(md_path)).write_pdf(str(pdf_path))
        console.print(f"[green]✅ MD/PDF: {pdf_path}")
    except Exception as e:
        console.print(f"[yellow]⚠️ PDF fail: {e}")

    # DB log
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO audits (ticker, date, md_path, pdf_path) VALUES (?, ?, ?, ?)",
        (ticker, datetime.now().isoformat(), str(md_path), str(pdf_path)),
    )
    conn.commit()
    conn.close()
    console.print(f"[green]✅ Logged DB!")


def show_history(console: Console):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM audits ORDER BY date DESC LIMIT 10")
    rows = cur.fetchall()
    conn.close()
    if not rows:
        console.print("[yellow]No audits!")
        return
    table = Table("ID", "Ticker", "Date", "MD", "PDF", title="History")
    for row in rows:
        table.add_row(*map(str, row))
    console.print(table)


def run():
    init_db()
    console = Console()
    while True:
        console.clear()
        console.print(
            Panel(Text("🕵️‍♂️ InsightGape Auditor", style="bold cyan"), style="blue")
        )
        choice_key = Prompt.ask(
            "Opción [1/2/3/q]", choices=["1", "2", "3", "q"], default="1"
        )
        if choice_key == "q":
            break
        elif choice_key == "1":
            ticker = Prompt.ask("Ticker (TSLA)")
            if Confirm.ask("Audit?"):
                run_audit(ticker, console)
                Prompt.ask("Enter...")
        elif choice_key == "2":
            show_history(console)
            Prompt.ask("Enter...")
        elif choice_key == "3":
            console.print(
                f"ALPHA_VANTAGE: {'✅' if os.getenv('ALPHA_VANTAGE_KEY') else '❌'}"
            )
            console.print(f"SERPER: {'✅' if os.getenv('SERPER_API_KEY') else '❌'}")
            Prompt.ask("Enter...")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        init_db()
        Console().print("Demo TSLA...")
        run_audit("TSLA", Console())
    else:
        run()
