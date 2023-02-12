# Importation des modules nécessaires pour Flask et SQLAlchemy
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

# Initialisation de l'application Flask
app = Flask(__name__)

# Configuration de la base de données SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:crepinho@localhost/mydatabase'
app.config['SECRET_KEY'] = 'mysecretkey'
db = SQLAlchemy(app)

# Définition de la classe Utilisateur qui correspond à une table de la base de données
class Utilisateur(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(80))
  last_name = db.Column(db.String(80))
  email = db.Column(db.String(120), unique=True)
  password = db.Column(db.String(120))
  
  # Initialisation des informations pour un utilisateur
  def __init__(self, first_name, last_name, email, password):
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.password = password

# Route principale qui affiche la page d'accueil
@app.route("/")
def home():
  return render_template("home.html")

@app.route("/reussie")
def reussie():
    return render_template("reussie.html")

@app.route("/connecter")
def connecter():
    return render_template("connecter.html")

# Route pour l'enregistrement d'un nouvel utilisateur
@app.route("/register", methods=["GET", "POST"])
def register():
  if request.method == "POST":
    # Récupération des informations saisies par l'utilisateur
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    password_confirm = request.form['password_confirm']
    # Vérification que les mots de passe saisis sont identiques
    if password == password_confirm:
      # Création d'un nouvel utilisateur
      new_user = Utilisateur(first_name=first_name, last_name=last_name, email=email, password=password)
      # Ajout de l'utilisateur à la session de la base de données
      db.session.add(new_user)
      # Validation des modifications à la base de données
      db.session.commit()
      # Redirection vers la page d'accueil
      return redirect("/reussie")
    else:
      # Affichage d'un message d'erreur si les mots de passe sont différents
      return "Password confirmation failed."
  # Affichage du formulaire d'enregistrement si la requête est de type GET
  return render_template("register.html")



# Cette fonction gère la page de connexion. 
@app.route("/login", methods=["GET", "POST"])
def login():
  # Si la méthode utilisée pour accéder à la page est POST (c'est-à-dire que l'utilisateur a soumis un formulaire)
  if request.method == "POST":
    # Récupère les informations de connexion (email et mot de passe) envoyées dans le formulaire
    email = request.form['email']
    password = request.form['password']
    # Vérifie si les informations correspondent à un utilisateur existant dans la base de données
    user = Utilisateur.query.filter_by(email=email, password=password).first()
    # Si un utilisateur correspondant a été trouvé
    if user:
      # Stocker l'email de l'utilisateur dans la session pour le maintenir connecté
      session['email'] = email
      # Rediriger l'utilisateur vers la page d'accueil
      return redirect("/connecter")
    else:
      # Sinon, retourner un message indiquant que la connexion a échoué
      return ""
  # Si la méthode utilisée pour accéder à la page est GET (c'est-à-dire que l'utilisateur accède simplement à la page)
  return render_template("login.html")

# Cette fonction gère la déconnexion de l'utilisateur.
@app.route("/logout")
def logout():
  # Supprime l'email de l'utilisateur de la session pour le déconnecter
  session.pop('email', None)
  # Rediriger l'utilisateur vers la page d'accueil
  return redirect("/")

# Vérifie si le script est exécuté en tant que programme principal
if __name__ == "__main__":
  # Crée toutes les tables nécessaires dans la base de données (si elles n'existent pas déjà)
  db.create_all()
  # Démarre l'application Flask en mode debug (avec des informations supplémentaires pour le débogage)
  app.run(debug=True)

