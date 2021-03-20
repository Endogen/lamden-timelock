import json
import uvicorn
import requests

from lamden.crypto.transaction import build_transaction
from lamden.crypto.wallet import Wallet
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates/")

URL = "https://testnet-master-1.lamden.io"


@app.get('/')
def root():
    return 'Following pages are available: /lock /unlock'


@app.get("/lock")
def lock(request: Request):
    result = "Enter data to lock tokens"
    return templates.TemplateResponse('lock.html', context={'request': request, 'result': result})


@app.post("/lock")
def lock(request: Request,
         privkey: str = Form(...),
         contract: str = Form(...),
         amount: int = Form(...),
         minutes: int = Form(...)):

    wallet = Wallet(privkey)

    nonce = requests.get(f"{URL}/nonce/{wallet.verifying_key}")
    nonce = json.loads(nonce.text)

    tx = build_transaction(
        wallet=wallet,
        processor=nonce["processor"],
        stamps=700,
        nonce=nonce["nonce"],
        contract="con_lock_test15",
        function="lock",
        kwargs={"contract": contract, "amount": amount, "minutes": minutes}
    )

    result = requests.post(URL, data=tx)
    return templates.TemplateResponse('lock.html', context={'request': request, 'result': result.text})


@app.get("/unlock")
def unlock(request: Request):
    result = "Enter UID to unlock tokens"
    return templates.TemplateResponse('unlock.html', context={'request': request, 'result': result})


@app.post("/unlock")
def unlock(request: Request, privkey: str = Form(...), uid: str = Form(...)):
    wallet = Wallet(privkey)

    nonce = requests.get(f"{URL}/nonce/{wallet.verifying_key}")
    nonce = json.loads(nonce.text)

    tx = build_transaction(
        wallet=wallet,
        processor=nonce["processor"],
        stamps=700,
        nonce=nonce["nonce"],
        contract="con_lock_test15",
        function="unlock",
        kwargs={"uid": uid}
    )

    result = requests.post(URL, data=tx)
    return templates.TemplateResponse('unlock.html', context={'request': request, 'result': result.text})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
