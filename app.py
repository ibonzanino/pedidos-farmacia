from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from flasgger import Swagger

app = Flask(__name__)
app.config["SECRET_KEY"] = "chave_secreta_super_segura"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/farmacia_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SWAGGER"] = {
    "title": "Farmácia HBR API",
    "uiversion": 3,
    "description": "Documentação das rotas da Farmácia HBR",
    "version": "1.0.0",
}
swagger = Swagger(app)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# --- MODELOS (Banco de Dados) ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    # Novos campos
    nome_completo = db.Column(db.String(150), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.String(255), nullable=False)
    genero = db.Column(db.String(20))


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), nullable=False)  # Nome do arquivo na pasta static


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# --- ROTAS DE AUTENTICAÇÃO ---
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login de Usuário
    ---
    tags:
      - Autenticação
    parameters:
      - name: username
        in: formData
        type: string
        required: false
        description: Nome de usuário (Apenas para POST)
      - name: password
        in: formData
        type: string
        required: false
        description: Senha do usuário (Apenas para POST)
    responses:
      200:
        description: Exibe o formulário de login.
      302:
        description: Login realizado com sucesso (Redireciona).
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("home"))
        flash("Login inválido.")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Pegando todos os campos do formulário
        username = request.form.get("username")
        password = request.form.get("password")
        nome = request.form.get("nome")
        cpf = request.form.get("cpf")
        email = request.form.get("email")
        telefone = request.form.get("telefone")
        endereco = request.form.get("endereco")
        genero = request.form.get("genero")

        # Verificar se usuário já existe antes de tentar gravar
        if User.query.filter(
            (User.username == username) | (User.cpf == cpf) | (User.email == email)
        ).first():
            flash("Erro: Usuário, CPF ou Email já cadastrados.")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        new_user = User(
            username=username,
            password=hashed_password,
            nome_completo=nome,
            cpf=cpf,
            email=email,
            telefone=telefone,
            endereco=endereco,
            genero=genero,
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Cadastro realizado com sucesso! Faça login.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# --- ROTAS DA LOJA ---
@app.route("/")
def home():
    """
    Página Inicial / Catálogo de Produtos
    ---
    tags:
      - Loja
    description: Exibe todos os medicamentos cadastrados no banco de dados.
    responses:
      200:
        description: Página carregada com sucesso (HTML).
    """
    products = Product.query.all()
    return render_template("home.html", products=products)


@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    """
    Adiciona um item ao carrinho
    ---
    tags:
      - Carrinho
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
        description: ID do medicamento a ser adicionado
    responses:
      302:
        description: Redireciona de volta para a Home com mensagem de sucesso.
    """
    # Carrinho é um dicionário na sessão: { 'id_produto': quantidade }
    if "cart" not in session:
        session["cart"] = {}

    cart = session["cart"]
    str_id = str(product_id)

    if str_id in cart:
        cart[str_id] += 1
    else:
        cart[str_id] = 1

    session.modified = True

    flash("Produto adicionado ao carrinho com sucesso!", "success")

    return redirect(url_for("home"))


@app.route("/cart")
def cart():
    cart_ids = session.get("cart", {})
    items = []
    total_products = 0

    for p_id, qtd in cart_ids.items():
        product = db.session.get(Product, int(p_id))  # <--- Forma nova
        if product:
            total = product.price * qtd
            total_products += total
            items.append({"product": product, "qtd": qtd, "total": total})

    return render_template("cart.html", items=items, total_products=total_products)


@app.route("/update_cart/<int:product_id>/<action>")
def update_cart(product_id, action):
    cart = session.get("cart", {})
    str_id = str(product_id)

    if str_id in cart:
        if action == "add":
            cart[str_id] += 1
        elif action == "remove":
            cart[str_id] -= 1
            if cart[str_id] <= 0:
                del cart[str_id]
        elif action == "delete":
            del cart[str_id]

    session.modified = True
    return redirect(url_for("cart"))


@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    cart_ids = session.get("cart", {})
    total_products = 0

    # Recalcula total para segurança
    for p_id, qtd in cart_ids.items():
        product = db.session.get(Product, int(p_id))
        if product:
            total_products += product.price * qtd

    shipping_cost = 7.90
    grand_total = total_products + shipping_cost

    if request.method == "POST":
        # Aqui você processaria os dados do cartão (fake)
        card_number = request.form.get("card_number")
        # Lógica de limpar carrinho e enviar "email"
        session.pop("cart", None)
        return redirect(url_for("success"))

    return render_template(
        "checkout.html",
        total_products=total_products,
        shipping=shipping_cost,
        grand_total=grand_total,
    )


@app.route("/success")
@login_required
def success():
    # Não precisa passar variáveis, o Jinja2 pega o 'current_user' direto
    return render_template("success.html")


# --- INICIALIZAÇÃO DO BANCO E PRODUTOS ---
def create_dummy_data():
    if not Product.query.first():
        items = [
            Product(name="Paracetamol 750mg", price=12.50, image="remedio1.webp"),
            Product(name="Vitamina C", price=35.90, image="remedio2.webp"),
            Product(name="Dipirona Mono", price=8.20, image="remedio3.webp"),
            Product(name="Protetor Solar", price=65.00, image="remedio4.webp"),
            Product(name="Dorflex 30cp", price=22.90, image="remedio5.webp"),
            Product(name="Ômega 3", price=89.90, image="remedio6.webp"),
        ]
        db.session.bulk_save_objects(items)
        db.session.commit()
        print("6 Produtos criados com sucesso!")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_dummy_data()
    app.run(debug=True)
