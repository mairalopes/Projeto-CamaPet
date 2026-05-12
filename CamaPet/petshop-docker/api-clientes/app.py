from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host="db-postgres",
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS')
    )

@app.route('/clientes', methods=['POST'])
def add_cliente():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO clientes (nome, pet) VALUES (%s, %s) RETURNING id', (data['nome'], data['pet']))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": new_id, "message": "Cliente cadastrado!"}), 201

@app.route('/clientes', methods=['GET'])
def get_clientes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM clientes')
    rows = cur.fetchall()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)