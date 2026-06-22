from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import conectar, criar_tabelas
from datetime import date

app = Flask(__name__)
app.secret_key = 'chave-secreta-troque-em-producao'
criar_tabelas()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Usuario(UserMixin):
    def __init__(self, id, nome, email):
        self.id = id
        self.nome = nome
        self.email = email

@app.template_filter('moeda')
def formatar_moeda(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")        

@login_manager.user_loader
def carregar_usuario(user_id):
    conn = conectar()
    usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if usuario:
        return Usuario(usuario['id'], usuario['nome'], usuario['email'])
    return None

# Cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = generate_password_hash(request.form['senha'])
        try:
            conn = conectar()
            conn.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)',
                         (nome, email, senha))
            conn.commit()
            conn.close()
            flash('Conta criada com sucesso! Faça login.', 'sucesso')
            return redirect(url_for('login'))
        except:
            flash('Email já cadastrado.', 'erro')
    return render_template('cadastro.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        conn = conectar()
        usuario = conn.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()
        conn.close()
        if usuario and check_password_hash(usuario['senha'], senha):
            user_obj = Usuario(usuario['id'], usuario['nome'], usuario['email'])
            login_user(user_obj)
            return redirect(url_for('index'))
        flash('Email ou senha incorretos.', 'erro')
    return render_template('login.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Página principal
@app.route('/')
@login_required
def index():
    conn = conectar()
    transacoes = conn.execute(
        'SELECT * FROM transacoes WHERE usuario_id = ? ORDER BY data DESC',
        (current_user.id,)
    ).fetchall()
    total_receitas = conn.execute(
        'SELECT SUM(valor) FROM transacoes WHERE usuario_id = ? AND tipo = "receita"',
        (current_user.id,)
    ).fetchone()[0] or 0
    total_despesas = conn.execute(
        'SELECT SUM(valor) FROM transacoes WHERE usuario_id = ? AND tipo = "despesa"',
        (current_user.id,)
    ).fetchone()[0] or 0
    saldo = total_receitas - total_despesas
    conn.close()
    return render_template('index.html',
        transacoes=transacoes,
        total_receitas=total_receitas,
        total_despesas=total_despesas,
        saldo=saldo
    )

# Adicionar transação
@app.route('/adicionar', methods=['POST'])
@login_required
def adicionar():
    tipo = request.form['tipo']
    descricao = request.form['descricao']
    valor = float(request.form['valor'])
    categoria = request.form['categoria']
    data = date.today().strftime('%d/%m/%Y')
    conn = conectar()
    conn.execute('''
        INSERT INTO transacoes (usuario_id, tipo, descricao, valor, categoria, data)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (current_user.id, tipo, descricao, valor, categoria, data))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Deletar transação
@app.route('/deletar/<int:id>')
@login_required
def deletar(id):
    conn = conectar()
    conn.execute('DELETE FROM transacoes WHERE id = ? AND usuario_id = ?',
                 (id, current_user.id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Relatórios
@app.route('/relatorios')
@login_required
def relatorios():
    conn = conectar()
    despesas = conn.execute('''
        SELECT categoria, SUM(valor) FROM transacoes
        WHERE usuario_id = ? AND tipo = "despesa"
        GROUP BY categoria
    ''', (current_user.id,)).fetchall()
    receitas = conn.execute('''
        SELECT categoria, SUM(valor) FROM transacoes
        WHERE usuario_id = ? AND tipo = "receita"
        GROUP BY categoria
    ''', (current_user.id,)).fetchall()
    conn.close()
    return render_template('relatorios.html', despesas=despesas, receitas=receitas)

if __name__ == '__main__':
    app.run(debug=True)