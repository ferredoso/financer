# Financer — Sistema de Controle Financeiro Pessoal

Aplicação web desenvolvida em Python com Flask para controle de finanças pessoais. O sistema permite que múltiplos usuários se cadastrem e gerenciem suas próprias receitas e despesas de forma segura e independente.

## Funcionalidades

- Cadastro e login de usuários com senha criptografada
- Cada usuário visualiza apenas suas próprias transações
- Registro de receitas e despesas com categoria
- Cálculo automático de saldo
- Gráficos de gastos por categoria
- Histórico completo de transações

## Tecnologias utilizadas

- **Python** — linguagem principal
- **Flask** — framework web
- **SQLite** — banco de dados relacional
- **Flask-Login** — autenticação de usuários
- **Werkzeug** — criptografia de senhas
- **Chart.js** — gráficos interativos
- **HTML5 + CSS3** — interface moderna com tema escuro

## Estrutura do projeto

financer/
├── app.py              # Rotas e lógica principal
├── database.py         # Conexão e criação do banco de dados
├── requirements.txt    # Dependências do projeto
├── templates/
│   ├── index.html      # Página principal
│   ├── relatorios.html # Página de gráficos
│   ├── login.html      # Página de login
│   └── cadastro.html   # Página de cadastro
└── static/
    └── style.css       # Estilos da interface

## Como rodar o projeto localmente

**1. Clone o repositório**
\```bash
git clone https://github.com/ferredoso/financer.git
cd financer
\```

**2. Crie e ative o ambiente virtual**
\```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
\```

**3. Instale as dependências**
\```bash
pip install -r requirements.txt
\```

**4. Inicie o servidor**
\```bash
python app.py
\```

**5. Acesse no navegador**
\```
http://127.0.0.1:5000
\```

## 👨‍💻 Autor

Feito por **Seu Nome** — [LinkedIn](www.linkedin.com/in/
gabriel-cardoso-ferreira)
) · [GitHub](https://github.com/ferredoso)
