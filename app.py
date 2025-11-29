from flask import Flask, request, jsonify
from queues.filaLances import filaLances
from tinydb import TinyDB, Query
import datetime

app = Flask(__name__)

# TinyDB (substitui DynamoDB)
db = TinyDB("./schema/baseDadosLances.json")
LancesTable = db.table("lances")
VencedoresTable = db.table("vencedores")


# ---------------------------
# Rota 1: Efetuar Lance (POST)
# ---------------------------
@app.route("/lance", methods=["POST"])
def receberLance():
    data = request.json

    lance = {
        "valor": data.get("valor"),
        "moeda": data.get("moeda"),
        "produto": data.get("produto"),
        "usuario": data.get("usuario"),
        "timestamp": datetime.datetime.now().isoformat()
    }

    # Adiciona o lance na fila
    filaLances.put(lance)

    return jsonify({
        "mensagem": "Lance recebido e colocado na fila",
        "lance": lance
    }), 201


# ------------------------------------------
# Função: Escolher o vencedor (lógica interna)
# ------------------------------------------
def escolheLanceVencedor(produto):
    vencedor = None
    maior_valor = -1
    lances_processados = []

    # Enquanto houver lances na fila
    while not filaLances.empty():
        lance = filaLances.get()

        # Registrar no TinyDB
        LancesTable.insert(lance)

        # Só considera lances do produto desejado
        if lance["produto"] == produto:
            if lance["valor"] > maior_valor:
                maior_valor = lance["valor"]
                vencedor = lance

        lances_processados.append(lance)

    # Se encontrou vencedor, salva também no TinyDB
    if vencedor:
        VencedoresTable.insert(vencedor)

    return vencedor, lances_processados


# ---------------------------------------
# Rota 2: Finalizar Leilão (GET/POST)
# ---------------------------------------
@app.route("/finalizar/<produto>", methods=["GET"])
def finalizarLeilao(produto):
    vencedor, lances = escolheLanceVencedor(produto)

    if not vencedor:
        return jsonify({
            "mensagem": f"Nenhum lance encontrado para o produto '{produto}'"
        }), 404

    return jsonify({
        "produto": produto,
        "vencedor": vencedor,
        "total_lances_processados": len(lances)
    })


# ---------------------------
# Rota auxiliar: Listar tudo
# ---------------------------
@app.route("/lances", methods=["GET"])
def listarLances():
    return jsonify(LancesTable.all())


@app.route("/vencedores", methods=["GET"])
def listarVencedores():
    return jsonify(VencedoresTable.all())


if __name__ == "__main__":
    app.run(debug=True)
