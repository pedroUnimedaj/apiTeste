from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class DadosProcedimento(BaseModel):
    nome: str
    telefone: str
    email: str
    procedimento: int

@app.post("/procedimento")
def receber_dados(dados: DadosProcedimento):
    return {"mensagem": "Dados recebidos com sucesso!", "dados": dados}
