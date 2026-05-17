from flask import Flask, render_template_string, request, redirect
import requests

app = Flask(__name__)

ESTILO_CSS = """
<style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; padding: 40px; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 80vh; }
    .container { max-width: 1000px; width: 100%; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin-bottom: 20px; }
    .login-box { max-width: 400px; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); text-align: center; border-top: 5px solid #28a745; }
    h1 { color: #2c3e50; text-align: center; margin-bottom: 20px; }
    h2 { color: #2c3e50; border-bottom: 2px solid #28a745; padding-bottom: 10px; margin-top: 10px; }
    table { width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 30px; }
    th, td { padding: 12px; text-align: left; border-bottom: 1px solid #eee; }
    th { background-color: #f8f9fa; color: #666; text-transform: uppercase; font-size: 11px; }
    .btn { padding: 6px 12px; border: none; border-radius: 6px; cursor: pointer; text-decoration: none; font-size: 12px; font-weight: bold; color: white; display: inline-block; margin-right: 5px; }
    .btn-green { background-color: #28a745; }
    .btn-green:hover { background-color: #218838; }
    .btn-block { width: 100%; margin-top: 10px; padding: 12px; font-size: 15px; }
    form { background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
    .form-group { margin-bottom: 15px; text-align: left; }
    .form-group label { display: block; margin-bottom: 5px; color: #666; font-weight: bold; font-size: 14px; }
    .form-control { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; }
    .inline-form input { padding: 10px; border: 1px solid #ddd; border-radius: 4px; margin-right: 10px; width: 28%; }
    
    /* ESTILOS NOVOS PARA AS ABAS */
    .tab-navigation { display: flex; gap: 10px; margin-bottom: 25px; border-bottom: 2px solid #eee; padding-bottom: 10px; }
    .tab-btn { background-color: #e9ecef; border: none; padding: 12px 24px; font-size: 14px; font-weight: bold; color: #495057; border-radius: 6px; cursor: pointer; transition: all 0.3s; }
    .tab-btn:hover { background-color: #dee2e6; }
    .tab-btn.active { background-color: #28a745; color: white; }
    .tab-pane { display: none; }
    .tab-pane.active { display: block; }
</style>
"""

SCRIPT_JS = """
<script>
    function alternarAba(idAba, botao) {
        // Esconde todas as abas
        document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));
        // Remove o estado ativo de todos os botões
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        
        // Mostra a aba selecionada e ativa o botão clicado
        document.getElementById(idAba).classList.add('active');
        botao.classList.add('active');
        
        // Guarda a aba atual no navegador para não resetar ao atualizar a página
        localStorage.setItem('abaAtiva', idAba);
    }

    // Mantém a aba aberta se o usuário cadastrar/excluir algo
    document.addEventListener("DOMContentLoaded", function() {
        let abaGuardada = localStorage.getItem('abaAtiva');
        if (abaGuardada) {
            let botao = document.querySelector(`[onclick*="${abaGuardada}"]`);
            if (botao) alternarAba(abaGuardada, botao);
        }
    });
</script>
"""

@app.route('/')
def login_view():
    return f"""
    {ESTILO_CSS}
    <div class="login-box">
        <h1>🐾 PetShop Login</h1>
        <p style="color: #666; margin-bottom: 25px;">Identifique-se para aceder ao sistema</p>
        <form action="/autenticar" method="POST" style="background: none; padding: 0; margin: 0;">
            <div class="form-group">
                <label>E-mail do Utilizador</label>
                <input type="email" name="email" class="form-control" placeholder="exemplo@petshop.com" required>
            </div>
            <div class="form-group">
                <label>Senha de Acesso</label>
                <input type="password" name="senha" class="form-control" placeholder="••••••••" required>
            </div>
            <button type="submit" class="btn btn-green btn-block">CADASTRAR / ENTRAR</button>
        </form>
    </div>
    """

@app.route('/autenticar', methods=['POST'])
def autenticar():
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    # O Orquestrador consome as duas APIs independentes
    clientes = requests.get("http://api-clientes:5000/clientes").json()
    produtos = requests.get("http://api-estoque:5001/produtos").json()
    
    # Monta as linhas da tabela de Clientes
    linhas_clientes = ""
    for c in clientes:
        linhas_clientes += f"""
        <tr>
            <td>{c['id']}</td>
            <td>{c['nome']}</td>
            <td>🐾 {c['pet']}</td>
            <td>
                <a href="/editar_cliente_view/{c['id']}" class="btn btn-green">EDITAR</a>
                <a href="/eliminar_cliente/{c['id']}" class="btn btn-green">EXCLUIR</a>
            </td>
        </tr>
        """

    # Monta as linhas da tabela de Produtos
    linhas_produtos = ""
    for p in produtos:
        linhas_produtos += f"""
        <tr>
            <td>{p['nome']}</td>
            <td>R$ {p['preco']}</td>
            <td>{p['quantidade']} u.</td>
            <td>
                <a href="/editar_produto_view/{p['nome']}" class="btn btn-green">EDITAR</a>
                <a href="/eliminar_produto/{p['nome']}" class="btn btn-green">EXCLUIR</a>
            </td>
        </tr>
        """

    return f"""
    {ESTILO_CSS}
    <div class="container">
        <h1>🐾 Painel de Controle PetShop</h1>
        <div style="text-align: center; margin-bottom: 20px; color: #666;">
            Clientes Ativos: <b>{len(clientes)}</b> | Itens no Estoque: <b>{len(produtos)}</b>
            <br><br>
            <a href="/" style="color: #999; text-decoration: none; font-size: 12px;">← Sair do Sistema</a>
        </div>

        <div class="tab-navigation">
            <button class="tab-btn active" onclick="alternarAba('aba-clientes', this)">👥 Clientes e Pets</button>
            <button class="tab-btn" onclick="alternarAba('aba-estoque', this)">📦 Estoque de Produtos</button>
        </div>

        <div id="aba-clientes" class="tab-pane active">
            <h2>👥 Gestão de Clientes</h2>
            <form action="/cadastrar_cliente" method="POST" class="inline-form">
                <input type="text" name="nome" placeholder="Nome do Dono" required>
                <input type="text" name="pet" placeholder="Nome do Pet (Ex: Bob)" required>
                <button type="submit" class="btn btn-green" style="width: 20%;">REGISTAR CLIENTE</button>
            </form>
            <table>
                <thead>
                    <tr><th>ID</th><th>Dono do Pet</th><th>Nome do Animal</th><th style="width: 180px;">Ações</th></tr>
                </thead>
                <tbody>{linhas_clientes if linhas_clientes else '<tr><td colspan="4" style="text-align:center;">Nenhum cliente registado.</td></tr>'}</tbody>
            </table>
        </div>

        <div id="aba-estoque" class="tab-pane">
            <h2>📦 Gestão de Estoque</h2>
            <form action="/cadastrar_produto" method="POST" class="inline-form">
                <input type="text" name="nome" placeholder="Nome do Produto" required>
                <input type="number" step="0.01" name="preco" placeholder="Preço (R$)" required>
                <input type="number" name="quantidade" placeholder="Qtd" required>
                <button type="submit" class="btn btn-green" style="width: 20%;">ADICIONAR PRODUTO</button>
            </form>
            <table>
                <thead>
                    <tr><th>Produto</th><th>Preço</th><th>Estoque</th><th style="width: 180px;">Ações</th></tr>
                </thead>
                <tbody>{linhas_produtos if linhas_produtos else '<tr><td colspan="4" style="text-align:center;">Nenhum produto em estoque.</td></tr>'}</tbody>
            </table>
        </div>
    </div>
    {SCRIPT_JS}
    """

# --- ROTAS DE AÇÃO PARA CLIENTES ---
@app.route('/cadastrar_cliente', methods=['POST'])
def cadastrar_cliente():
    data = {"nome": request.form['nome'], "pet": request.form['pet']}
    requests.post("http://api-clientes:5000/clientes", json=data)
    return redirect('/dashboard')

@app.route('/editar_cliente_view/<int:id>')
def editar_cliente_view(id):
    c = requests.get(f"http://api-clientes:5000/clientes/{id}").json()
    return f"""
    {ESTILO_CSS}
    <div class="container">
        <h1>Editar Cliente</h1>
        <form action="/atualizar_cliente/{id}" method="POST">
            <div class="form-group">
                <label>Nome do Dono</label>
                <input type="text" name="nome" class="form-control" value="{c['nome']}" required>
            </div>
            <div class="form-group">
                <label>Nome do Pet</label>
                <input type="text" name="pet" class="form-control" value="{c['pet']}" required>
            </div>
            <button type="submit" class="btn btn-green">GUARDAR ALTERAÇÕES</button>
            <a href="/dashboard" style="color: #666; margin-left: 15px; text-decoration: none;">Cancelar</a>
        </form>
    </div>
    """

@app.route('/atualizar_cliente/<int:id>', methods=['POST'])
def atualizar_cliente(id):
    data = {"nome": request.form['nome'], "pet": request.form['pet']}
    requests.put(f"http://api-clientes:5000/clientes/{id}", json=data)
    return redirect('/dashboard')

@app.route('/eliminar_cliente/<int:id>')
def eliminar_cliente(id):
    requests.delete(f"http://api-clientes:5000/clientes/{id}")
    return redirect('/dashboard')


# --- ROTAS DE AÇÃO PARA PRODUTOS ---
@app.route('/cadastrar_produto', methods=['POST'])
def cadastrar_produto():
    data = {"nome": request.form['nome'], "preco": float(request.form['preco']), "quantidade": int(request.form['quantidade'])}
    requests.post("http://api-estoque:5001/produtos", json=data)
    return redirect('/dashboard')

@app.route('/editar_produto_view/<nome>')
def editar_produto_view(nome):
    p = requests.get(f"http://api-estoque:5001/produtos/{nome}").json()
    return f"""
    {ESTILO_CSS}
    <div class="container">
        <h1>Editar Produto</h1>
        <form action="/atualizar_produto/{nome}" method="POST">
            <p>Editando o item: <b>{nome}</b></p>
            <div class="form-group">
                <label>Preço Venda</label>
                <input type="number" step="0.01" name="preco" class="form-control" value="{p['preco']}" style="width: 30%;" required>
            </div>
            <div class="form-group">
                <label>Quantidade em Estoque</label>
                <input type="number" name="quantidade" class="form-control" value="{p['quantidade']}" style="width: 30%;" required>
            </div>
            <button type="submit" class="btn btn-green">GUARDAR ALTERAÇÕES</button>
            <a href="/dashboard" style="color: #666; margin-left: 15px; text-decoration: none;">Cancelar</a>
        </form>
    </div>
    """

@app.route('/atualizar_produto/<nome>', methods=['POST'])
def atualizar_produto(nome):
    data = {"preco": float(request.form['preco']), "quantidade": int(request.form['quantidade'])}
    requests.put(f"http://api-estoque:5001/produtos/{nome}", json=data)
    return redirect('/dashboard')

@app.route('/eliminar_produto/<nome>')
def eliminar_produto(nome):
    requests.delete(f"http://api-estoque:5001/produtos/{nome}")
    return redirect('/dashboard')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)