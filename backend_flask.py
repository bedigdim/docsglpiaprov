
from flask import Flask, request
import requests
import re

app = Flask(__name__)

@app.route("/webhook/whatsapp", methods=["POST"])
def receber_resposta():
    data = request.form
    mensagem = data.get("body", "").upper()
    telefone = data.get("from")

    match = re.search(r"(APROVAR|REJEITAR)\\s+(\\d+)", mensagem)
    if match:
        acao = match.group(1)
        ticket_id = match.group(2)

        if acao == "APROVAR":
            atualizar_status_glpi(ticket_id, status=4)
        elif acao == "REJEITAR":
            atualizar_status_glpi(ticket_id, status=5)

    return "OK", 200

def atualizar_status_glpi(ticket_id, status):
    headers = {
        "App-Token": "SEU_APP_TOKEN",
        "Authorization": "user_token SEU_USER_TOKEN"
    }
    url = f"https://seu-glpi.com/apirest.php/Ticket/{ticket_id}"
    data = {
        "input": {
            "status": status
        }
    }
    r = requests.put(url, headers=headers, json=data)
    print("Chamado atualizado:", r.status_code, r.text)

if __name__ == "__main__":
    app.run(port=5000)
