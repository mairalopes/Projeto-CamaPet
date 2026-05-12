from flask import Flask, render_template_string, request, redirect
import requests

app = Flask(__name__)

# CSS unificado para as páginas
ESTILO_CSS = """
<style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; padding: 40px; }
    .container { max-width: 900px; margin: auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
    h1 { color: #2c3e50; text-align: center; }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    th, td { padding: 15px; text-align: left; border-bottom: 1px solid #eee; }
    th { background-color: #f8f9fa; color: #666; text-transform: uppercase; font-size: 12px; }
    .btn { padding: 8px 12px; border: none; border-radius: 6px; cursor: pointer; text-decoration: none; font-size: 13px; font-weight: bold; color: white; display: inline-block; margin-right: 5px; }
    .btn-green { background-color: #28a745; }
    .btn-green:hover { background-color: #218838; }
    form { background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 30px; }
    input { padding: 10px; border: 1px solid #ddd; border-radius: 4px; margin-right: 10px; width: 20%; }
</style>
"""

@app.route('/resumo')
def resumo():
    clientes = requests.get("http://api-clientes:5000/clientes").json()
    produtos = requests.get("http://api-estoque:5001/produtos").json()
    
    linhas_produtos = ""
    for p in produtos:
        linhas_produtos += f"""
        <tr>
            <td>{p['nome']}</td>
            <td>R$ {p['preco']}</td>
            <td>{p['quantidade']}</td>
            <td>
                <a href="/editar_view/{p['nome']}" class="btn btn-green">EDITAR</a>
                <a href="/deletar_produto/{p['nome']}" class="btn btn-green">EXCLUIR</a>
            </td>
        </tr>
        """

    return f"""
    {ESTILO_CSS}
    <div class="container">
        <h1>🐾 Painel Administrativo PetShop</h1>
        <div style="text-align: center; margin-bottom: 20px; color: #666;">
            Clientes: <b>{len(clientes)}</b> | Produtos: <b>{len(produtos)}</b>
        </div>

        <form action="/cadastrar_produto" method="POST">
            <h3>Novo Produto</h3>
            <input type="text" name="nome" placeholder="Nome" required>
            <input type="number" step="0.01" name="preco" placeholder="Preço" required>
            <input type="number" name="quantidade" placeholder="Qtd" required>
            <button type="submit" class="btn btn-green" style="width: 15%;">ADICIONAR</button>
        </form>

        <table>
            <thead>
                <tr>
                    <th>Produto</th>
                    <th>Preço</th>
                    <th>Estoque</th>
                    <th style="width: 200px;">Ações</th>
                </tr>
            </thead>
            <tbody>{linhas_produtos}</tbody>
        </table>
    </div>
    """

# Tela de Edição
@app.route('/editar_view/<nome>')
def editar_view(nome):
    p = requests.get(f"http://api-estoque:5001/produtos/{nome}").json()
    return f"""
    {ESTILO_CSS}
    <div class="container">
        <h1>Editar Produto</h1>
        <form action="/atualizar_produto/{nome}" method="POST">
            <p>Editando: <b>{nome}</b></p>
            <input type="hidden" name="nome" value="{p['nome']}">
            Preço: <input type="number" step="0.01" name="preco" value="{p['preco']}" required>
            Quantidade: <input type="number" name="quantidade" value="{p['quantidade']}" required>
            <br><br>
            <button type="submit" class="btn btn-green">SALVAR ALTERAÇÕES</button>
            <a href="/resumo" style="color: #666; margin-left: 15px;">Cancelar</a>
        </form>
    </div>
    """

@app.route('/cadastrar_produto', methods=['POST'])
def cadastrar_produto():
    data = {"nome": request.form['nome'], "preco": float(request.form['preco']), "quantidade": int(request.form['quantidade'])}
    requests.post("http://api-estoque:5001/produtos", json=data)
    return redirect('/resumo')

@app.route('/atualizar_produto/<nome>', methods=['POST'])
def atualizar_produto(nome):
    data = {"preco": float(request.form['preco']), "quantidade": int(request.form['quantidade'])}
    requests.put(f"http://api-estoque:5001/produtos/{nome}", json=data)
    return redirect('/resumo')

@app.route('/deletar_produto/<nome>')
def deletar_produto(nome):
    requests.delete(f"http://api-estoque:5001/produtos/{nome}")
    return redirect('/resumo')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)