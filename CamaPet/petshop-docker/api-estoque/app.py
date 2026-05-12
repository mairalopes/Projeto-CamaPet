from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://db-mongo:27017/")
db = client.petshop_estoque

@app.route('/produtos', methods=['POST'])
def add_produto():
    data = request.json
    db.produtos.insert_one(data)
    return jsonify({"message": "Produto cadastrado!"}), 201

@app.route('/produtos', methods=['GET'])
def get_produtos():
    produtos = []
    for p in db.produtos.find():
        produtos.append({"nome": p["nome"], "preco": p.get("preco", 0), "quantidade": p.get("quantidade", 0)})
    return jsonify(produtos)

# Rota para buscar UM produto específico (necessário para o Editar)
@app.route('/produtos/<nome>', methods=['GET'])
def get_produto(nome):
    p = db.produtos.find_one({"nome": nome})
    if p:
        return jsonify({"nome": p["nome"], "preco": p.get("preco", 0), "quantidade": p.get("quantidade", 0)})
    return jsonify({"error": "Não encontrado"}), 404

@app.route('/produtos/<nome>', methods=['PUT'])
def update_produto(nome):
    data = request.json
    db.produtos.update_one({"nome": nome}, {"$set": data})
    return jsonify({"message": "Produto atualizado!"})

@app.route('/produtos/<nome>', methods=['DELETE'])
def delete_produto(nome):
    db.produtos.delete_one({"nome": nome})
    return jsonify({"message": "Produto removido!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)