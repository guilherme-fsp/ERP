from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'
app.permanent_session_lifetime = timedelta(hours=1)
# Banco de dados simples (dicionário)
usuarios = {}

# Página inicial
@app.route('/')
def home():
    return render_template('index.html')

def definir_empresa(email):
    dominios_empresa = {
        "empresa1.com": "empresa1",
        "empresa2.com": "empresa2"
    }

    dominio = email.split('@')[-1]  # Pega o domínio do e-mail
    return dominios_empresa.get(dominio, "empresa_padrao")  # Define empresa padrão se não encontrar

# Página de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'] 
        username = request.form['username']

        empresa = definir_empresa(email)
        
        # Verificar se o usuário já existe
        if email in usuarios:
            flash('Usuário já existe!')
            return redirect(url_for('cadastro'))
        
        # Armazenar o novo usuário no "banco de dados"
        usuarios[email] = {"username": username, "password": password, "empresa": empresa, }
        flash('Usuário cadastrado com sucesso!')
        return redirect(url_for('login'))
    
    return render_template('cadastro.html')


# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')


        if email in usuarios and usuarios[email]["password"] == password:
            session['email'] = email  # <-- Salvando email na sessão
            session['empresa'] = usuarios[email]["empresa"]  
            session['username'] = usuarios[email]["username"]  # Salvando o nome do usuário na sessão
            print("Sessão após login:", session)  # <-- Depuração
            return redirect(url_for('dashboard'))
        else:
            flash('E-mail ou senha inválidos!')
            return redirect(url_for('login'))

    return render_template('login.html')

#Pagina pós login
@app.route('/landpage')
def landpage():
    if 'email' in session:  # Verifica se o usuário está logado
        empresa = session.get('empresa', 'empresa_padrao')
        return render_template(f'landpage_{empresa}.html', username=session['email'])
    else:
        flash('Você precisa estar logado para acessar o sistema.')
        return redirect(url_for('login'))  # Se não estiver logado, redireciona para login
    

@app.route('/logout')
def logout():
    session.pop('email', None)  # Remove o usuário da sessão
    flash('Você saiu da conta!')
    return redirect(url_for('login'))  # Redireciona para a página de login


@app.route('/dashboard')
def dashboard():
     if 'email' in session:
        return render_template('dashboard.html', username=session['email'])
     return redirect(url_for('login'))

@app.route('/obra')
def obra():
    if 'username' in session:
        return render_template('obra.html', username=session['username'])
    return redirect(url_for('obra'))

@app.route('/engenharia')
def engenharia():
    if 'username' in session:
        return render_template('engenharia.html', username=session['username'])
    return redirect(url_for('engenharia'))

@app.route('/suprimento')
def suprimento():
    if 'username' in session:
        return render_template('suprimento.html', username=session['username'])
    return redirect(url_for('suprimento'))

@app.route('/compra')
def compra():
    if 'username' in session:
        return render_template('compra.html', username=session['username'])
    return redirect(url_for('compra'))


@app.route('/financeiro')
def financeiro():
    if 'username' in session:
        return render_template('financeiro.html', username=session['username'])
    return redirect(url_for('financeiro'))


@app.route('/venda')
def venda():
    if 'username' in session:
        return render_template('venda.html', username=session['username'])
    return redirect(url_for('venda'))


@app.route('/pagamento')
def pagamento():
    if 'username' in session:
        return render_template('pagamento.html', username=session['username'])
    return redirect(url_for('pagamento'))

@app.route('/cadastrar')
def cadastrar():
    if 'username' in session:
        return render_template('cadastrar.html', username=session['username'])
    return redirect(url_for('cadastrar'))

@app.route('/permissoes')
def permissoes():
    if 'username' in session:
        return render_template('permissoes.html', username=session['username'])
    return redirect(url_for('permissoes'))
    

if __name__ == '__main__':
    app.run(debug=True)