from fastapi import FastAPI
from pydantic import BaseModel
import http.client
import json
import ssl

app = FastAPI()

class DadosProcedimento(BaseModel):
    nome: str
    telefone: str
    email: str
    procedimento: int

@app.post("/procedimento")
def receber_dados(dados: DadosProcedimento):
    # Monta o payload para o Botmaker
    payload = {
        "chat": {
            "channelId": "unimedaj-whatsapp-555433241462",
            "contactId": "5554984379155"
        },
        "intentIdOrName": "modeloatendi",
        "variables": {
            "nome": dados.nome,
            "email": dados.email,
            "contato": dados.telefone,
            "guia": dados.procedimento,
            "procedimento": "procedimento x",
            "motivo": "Solicitação de procedimento"  
            },
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "access-token": "eyJhbGciOiJIUzUxMiJ9.eyJidXNpbmVzc0lkIjoidW5pbWVkYWoiLCJuYW1lIjoiUGVkcm8gT3R0b25pIiwiYXBpIjp0cnVlLCJpZCI6IjFTcXFSdDJvQTlhWHAyZXRtNG52UVloMHBWMDMiLCJleHAiOjE4ODA5MDU1OTcsImp0aSI6IjFTcXFSdDJvQTlhWHAyZXRtNG52UVloMHBWMDMifQ.tzBoALcGBdrHShxn-h7I7fcNSSIa4Jzmj4P4nJwGFvMYXD3pn6h36iyO-_R9S58P_NB0zx25VRD0lGw9FZrQIw"
    }

    conn = http.client.HTTPSConnection("api.botmaker.com", context=ssl._create_unverified_context())
    conn.request("POST", "/v2.0/chats-actions/trigger-intent", json.dumps(payload), headers)

    res = conn.getresponse()
    data = res.read()
    conn.close()

    try:
        response_data = json.loads(data.decode("utf-8"))
    except json.JSONDecodeError:
        response_data = {"erro": "Resposta inválida da API Botmaker", "raw": data.decode("utf-8")}

    return {
        "mensagem": "Dados recebidos e enviados com sucesso!",
        "resposta_botmaker": response_data,
        "status_code": res.status
    }
