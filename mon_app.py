import streamlit as st
from streamlit_authenticator import Authenticate
from streamlit_option_menu import option_menu
import pandas as pd

# Charger les données des comptes depuis un fichier CSV
df = pd.read_csv("users.csv")  # Assure-toi que ce fichier est bien dans ton dossier Streamlit

# Convertir les données du CSV en format de dictionnaire attendu par Authenticate
lesDonneesDesComptes = {'usernames': {}}

for _, row in df.iterrows():
    lesDonneesDesComptes['usernames'][row['name']] = {
        'name': row['name'],
        'password': row['password'],
        'email': row['email'],
        'failed_login_attemps': row['failed_login_attempts'],
        'logged_in': row['logged_in'],
        'role': row['role'],
    }

# Initialiser l'authentification
authenticator = Authenticate(
    lesDonneesDesComptes,  # Les données des comptes
    "cookie name",         # Le nom du cookie
    "cookie key",          # La clé du cookie
    30,                    # Durée du cookie (en jours)
)

# Afficher le formulaire de connexion
authenticator.login()

# Vérifier l'état d'authentification
if st.session_state["authentication_status"]:
    # Créer la sidebar avec le menu
    with st.sidebar:
        # Message de bienvenue avec le nom de l'utilisateur
        st.write(f"Bienvenue, {st.session_state['username']}!")
        
        # Créer le menu avec les options Accueil et Photos
        selection = option_menu(
            menu_title=None,
            options=["Accueil", "Photos"]
        )

        # Bouton de déconnexion
        authenticator.logout("Déconnexion", "sidebar")

    # Afficher le contenu en fonction du choix de l'utilisateur
    if selection == "Accueil":
        st.title("Bienvenue sur ma page !")
        # Remplacement de l'image locale par l'URL fournie
        st.image("https://i.postimg.cc/p5Q5K4J5/hello.png", use_container_width=True)  

    elif selection == "Photos":
        st.title("Bienvenue sur l'album photo de mon chat")

        # Afficher des photos depuis les URLs fournies
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image("https://i.postimg.cc/1gTFSpzX/cat1.png", use_container_width=True)  
        with col2:
            st.image("https://i.postimg.cc/hzddtfJr/cat2.png", use_container_width=True)  
        with col3:
            st.image("https://i.postimg.cc/xNVbJnMS/cat3.png", use_container_width=True)  

elif st.session_state["authentication_status"] is False:
    st.error("Le username ou le password est/sont incorrect")
elif st.session_state["authentication_status"] is None:
    st.warning('Les champs username et mot de passe doivent être remplis')
