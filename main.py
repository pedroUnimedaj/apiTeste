from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# Lista simples para armazenar dados (em produção usaria BD)
dados_recebidos = []

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "API funcionando!",
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            "GET / - Esta página",
            "POST /dados - Recebe dados via POST",
            "GET /dados - Lista dados recebidos",
            "GET /ping - Teste de conectividade"
        ]
    })

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({
        "status": "pong",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/dados', methods=['POST'])
def receber_dados():
    try:
        # Pega dados do JSON ou form-data
        if request.is_json:
            dados = request.get_json()
        else:
            dados = request.form.to_dict()
        
        # Adiciona timestamp
        dados['timestamp'] = datetime.now().isoformat()
        dados['id'] = len(dados_recebidos) + 1
        
        # Armazena os dados
        dados_recebidos.append(dados)
        
        return jsonify({
            "status": "sucesso",
            "mensagem": "Dados recebidos com sucesso!",
            "dados_recebidos": dados,
            "total_registros": len(dados_recebidos)
        }), 201
        
    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": f"Erro ao processar dados: {str(e)}"
        }), 400

@app.route('/dados', methods=['GET'])
def listar_dados():
    return jsonify({
        "status": "sucesso",
        "total_registros": len(dados_recebidos),
        "dados": dados_recebidos
    })

@app.route('/dados/<int:id>', methods=['GET'])
def obter_dado(id):
    try:
        dado = next((d for d in dados_recebidos if d['id'] == id), None)
        if dado:
            return jsonify({
                "status": "sucesso",
                "dados": dado
            })
        else:
            return jsonify({
                "status": "erro",
                "mensagem": "Registro não encontrado"
            }), 404
    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": f"Erro: {str(e)}"
        }), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)