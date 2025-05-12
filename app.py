from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import csv

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

DATA_FILE = "stock.csv"

@app.get("/", response_class=HTMLResponse)
async def root():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        rows = list(reader)
    html = open("static/index.html", "r", encoding="utf-8").read()
    rows_html = "".join([f"<tr><td>{'</td><td>'.join(r)}</td></tr>" for r in rows])
    return html.replace("{{ROWS}}", rows_html)

@app.post("/add")
async def add(
    produit: str = Form(...),
    imei: str = Form(...),
    serial: str = Form(...),
    date_entree: str = Form(...),
    garantie: str = Form(...)
):
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([produit, imei, serial, date_entree, garantie])
    return RedirectResponse("/", status_code=303)
