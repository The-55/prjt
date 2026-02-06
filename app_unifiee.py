import streamlit as st
import os
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuration de la page
st.set_page_config(
    page_title="Plateforme d'Analyse Scolaire",
    page_icon="🏫",
    layout="wide"
)

# Style CSS commun
st.markdown("""
<style>
    .main-header {
        color: #FFFFFF;
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background: linear-gradient(135deg, #3B82F6 0%, #1E3A8A 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Aller à",
    ["Accueil", "Tableaux Scolaires", "Analyse des Salles", "Totaux par École", "Ratios et Statistiques"]
)

# Fonction pour gérer les imports dynamiques
def load_module(module_name):
    try:
        module = __import__(f"modules.{module_name}", fromlist=[module_name])
        return module
    except ImportError as e:
        st.error(f"Erreur lors du chargement du module {module_name}: {str(e)}")
        return None

# Affichage de la page sélectionnée
if page == "Accueil":
    accueil = load_module("accueil")
    if accueil:
        accueil.show_accueil()
        
elif page == "Tableaux Scolaires":
    tableaux = load_module("tableaux")
    if tableaux and hasattr(tableaux, "main"):
        tableaux.main()
    elif tableaux:
        st.error("La fonction 'main' est introuvable dans le module tableaux")
    else:
        st.error("Impossible de charger le module tableaux")
        
elif page == "Analyse des Salles":
    salles = load_module("salles")
    if salles and hasattr(salles, "main"):
        salles.main()
    elif salles:
        st.error("La fonction 'main' est introuvable dans le module salles")
    else:
        st.error("Impossible de charger le module salles")
        
elif page == "Totaux par École":
    totaux = load_module("totaux")
    if totaux and hasattr(totaux, "main"):
        totaux.main()
    elif totaux:
        st.error("La fonction 'main' est introuvable dans le module totaux")
    else:
        st.error("Impossible de charger le module totaux")
        
elif page == "Ratios et Statistiques":
    ratios = load_module("ratios")
    if ratios and hasattr(ratios, "main"):
        ratios.main()
    elif ratios:
        st.error("La fonction 'main' est introuvable dans le module ratios")
    else:
        st.error("Impossible de charger le module ratios")

# Ajout d'un pied de page
st.sidebar.markdown("---")
st.sidebar.info("Plateforme d'Analyse Scolaire - © 2024")