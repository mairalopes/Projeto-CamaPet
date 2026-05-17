from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# 1. Conexão corrigida com os dados exatos do seu docker-compose.yml
def obter_conexao():
    return psycopg2.connect(
        host="db-postgres",
        database="petshop_db",   # <-- Atualizado
        user="user_pet",         # <-- Atualizado
        password="password123"
    )

# 2. Truque de Mestre: Criar a tabela automaticamente se ela não existir
def inicializar_banco():
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                pet VARCHAR(100) NOT NULL
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Banco de dados inicializado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao inicializar o banco: {e}")

# Inicia a criação da tabela antes de liberar as rotas
inicializar_banco()

# --- ROTAS DO CRUD ---

@app.route('/clientes', methods=['POST'])
def adicionar_cliente():
    data = request.json
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO clientes (nome, pet) VALUES (%s, %s);",
        (data['nome'], data['pet'])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Cliente registado com sucesso!"}), 201

@app.route('/clientes', methods=['GET'])
def obter_clientes():
    conn = obter_conexao()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id, nome, pet FROM clientes ORDER BY id DESC;")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(clientes)

@app.route('/clientes/<int:id>', methods=['GET'])
def obter_cliente(id):
    conn = obter_conexao()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id, nome, pet FROM clientes WHERE id = %s;", (id,))
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()
    if cliente:
        return jsonify(cliente)
    return jsonify({"error": "Cliente não encontrado"}), 404

@app.route('/clientes/<int:id>', methods=['PUT'])
def atualizar_cliente(id):
    data = request.json
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE clientes SET nome = %s, pet = %s WHERE id = %s;",
        (data['nome'], data['pet'], id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Cliente atualizado!"})

@app.route('/clientes/<int:id>', methods=['DELETE'])
def eliminar_cliente(id):
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = %s;", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Cliente removido!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)