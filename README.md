# 💊 Farmácia HBR - Sistema de Pedidos Online

Este é um projeto de e-commerce simplificado para uma farmácia, desenvolvido em **Python** com **Flask** e banco de dados **MySQL**. O sistema gerencia desde o cadastro de usuários (com dados completos como CPF e Endereço) até a simulação de checkout e confirmação de pedido.

![Status](https://img.shields.io/badge/Status-Concluido-brightgreen) ![Python](https://img.shields.io/badge/Python-3.x-blue) ![Flask](https://img.shields.io/badge/Flask-3.0-red)

## 🚀 Funcionalidades

- **Autenticação de Usuários:** Login e Cadastro seguro (com hash de senha) incluindo dados como CPF, Endereço e Gênero.
- **Catálogo de Produtos:** Listagem dinâmica de medicamentos vindos do banco de dados MySQL.
- **Carrinho de Compras:** Adicionar, remover e alterar quantidades (gerenciado via Sessão).
- **Checkout Simulado:** Resumo do pedido, cálculo de frete fixo e formulário de pagamento (simulação).
- **Design Responsivo:** Interface moderna e adaptável para mobile usando **Tailwind CSS**, com menu hambúrguer funcional.
- **Painel do Usuário:** Exibição personalizada de nome, endereço e confirmação de envio no pós-venda.

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python, Flask
- **Banco de Dados:** MySQL (via PyMySQL e SQLAlchemy)
- **Frontend:** HTML5, Jinja2, Tailwind CSS (CDN)
- **Autenticação:** Flask-Login

## ⚙️ Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:

- [Python 3.x](https://www.python.org/)
- [MySQL Server](https://dev.mysql.com/downloads/installer/) (ou XAMPP/WAMP)
- Git

## 📝 Passo a Passo de Instalação

### 1\. Clone o repositório

```bash
git clone [https://github.com/ibonzanino/pedidos-farmacia.git](https://github.com/ibonzanino/pedidos-farmacia.git)
cd pedidos-farmacia
```

### 2\. Crie e ative um ambiente virtual (Opcional)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3\. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4\. Configuração do Banco de Dados

1.  Abra seu gerenciador MySQL (Workbench, PHPMyAdmin, etc).
2.  Crie o banco de dados vazio:

```sql
CREATE DATABASE farmacia_db;
```

3.  Verifique no arquivo `app.py` se a conexão está correta para o seu usuário (exemplo para root sem senha):

```python
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/farmacia_db"
```

### 5\. Execute a aplicação

```bash
python app.py
```

> **Nota:** Na primeira execução, o sistema criará automaticamente as tabelas no MySQL e cadastrará 6 produtos de exemplo.

Acesse no navegador: **http://127.0.0.1:5000**

## 📂 Estrutura de Pastas

```text
/
├── app.py              # Lógica principal (Rotas, Models, Configuração)
├── requirements.txt    # Dependências do projeto
├── static/             # Imagens (Produtos, Logo) e CSS
└── templates/          # Arquivos HTML (Base, Home, Cart, Checkout, etc)
```

## 🤝 Contribuição

Contribuições são bem-vindas\! Sinta-se à vontade para abrir issues ou enviar pull requests.

## 📄 Licença

Este projeto é de livre uso para fins educacionais.
