import streamlit as st
import plotly.graph_objects as go

def show_accueil():
    # En-tête de la page d'accueil avec dégradé et animation
    st.markdown("""
    <div class="main-header" style="
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        margin-bottom: 2.5rem;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    ">
        <div style="position: relative; z-index: 1;">
            <h1 style="margin: 0; font-size: 2.8em; font-weight: 800; letter-spacing: -0.5px;">📊 Plateforme d'Analyse Scolaire</h1>
            <p style="opacity: 0.9; font-size: 1.2em; margin: 0.8rem 0 0; font-weight: 300;">
                Outil complet de gestion et d'analyse des données éducatives
            </p>
        </div>
        <div style="
            position: absolute;
            top: -50px;
            right: -50px;
            width: 300px;
            height: 300px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
            z-index: 0;
        "></div>
    </div>
    """, unsafe_allow_html=True)

    # Section de présentation avec animation
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2.5rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        border-left: 5px solid #3B82F6;
    ">
        <h2 style="color: #1E3A8A; margin-top: 0;">Bienvenue sur la plateforme d'analyse scolaire</h2>
        <p style="font-size: 1.1em; line-height: 1.6; color: #475569;">
            Découvrez une nouvelle façon d'analyser et de visualiser les données éducatives 
            grâce à notre plateforme tout-en-un. Optimisez la gestion de votre établissement 
            avec des outils puissants et intuitifs.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Cartes d'information avec effets de survol
    st.markdown("""
    <style>
        .feature-card {
            transition: all 0.3s ease;
            border-radius: 12px;
            padding: 1.8rem;
            background: white;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            height: 100%;
            border: 1px solid #e2e8f0;
        }
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.1);
            border-color: #3B82F6;
        }
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            color: #3B82F6;
        }
        .feature-title {
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 0.8rem;
            color: #1E3A8A;
        }
        .feature-desc {
            color: #64748b;
            line-height: 1.6;
        }
    </style>
    """, unsafe_allow_html=True)

    # Grille de fonctionnalités
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📋</div>
            <h3 class="feature-title">Tableaux Scolaires</h3>
            <p class="feature-desc">
                Générez et analysez les tableaux scolaires annuels avec des indicateurs clés 
                et des visualisations interactives.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🏫</div>
            <h3 class="feature-title">Analyse des Salles</h3>
            <p class="feature-desc">
                Visualisez la répartition et l'utilisation des salles de classe avec des graphiques 
                et des statistiques détaillées.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <h3 class="feature-title">Statistiques Avancées</h3>
            <p class="feature-desc">
                Explorez les données avec des graphiques interactifs et des tableaux de bord 
                personnalisables.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Remplacer toute la section "Comment commencer ?" par ce code :
st.markdown("### Comment commencer ?")
    
with st.container():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #3B82F6;
            height: 100%;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        ">
            <div style="
                background: #e0f2fe;
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 1rem;
                color: #0369a1;
                font-weight: bold;
                font-size: 1.2em;
            ">1</div>
            <h3 style="color: #1E3A8A; margin-top: 0; font-size: 1.1em;">Sélectionnez une section</h3>
            <p style="color: #64748b; font-size: 0.95em; margin: 0.5em 0 0 0; line-height: 1.5;">
                Utilisez le menu de navigation sur la gauche pour accéder aux différentes fonctionnalités.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #3B82F6;
            height: 100%;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        ">
            <div style="
                background: #dbeafe;
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 1rem;
                color: #1d4ed8;
                font-weight: bold;
                font-size: 1.2em;
            ">2</div>
            <h3 style="color: #1E3A8A; margin-top: 0; font-size: 1.1em;">Explorez les données</h3>
            <p style="color: #64748b; font-size: 0.95em; margin: 0.5em 0 0 0; line-height: 1.5;">
                Visualisez et analysez les données avec nos outils interactifs.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #3B82F6;
            height: 100%;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        ">
            <div style="
                background: #e0e7ff;
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 1rem;
                color: #4338ca;
                font-weight: bold;
                font-size: 1.2em;
            ">3</div>
            <h3 style="color: #1E3A8A; margin-top: 0; font-size: 1.1em;">Exportez les résultats</h3>
            <p style="color: #64748b; font-size: 0.95em; margin: 0.5em 0 0 0; line-height: 1.5;">
                Téléchargez vos analyses et rapports au format Excel ou PDF.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Indicateurs de performance
    st.markdown("""
    <h2 style="color: #1E3A8A; margin: 2.5rem 0 1.5rem 0;">Statistiques clés</h2>
    """, unsafe_allow_html=True)

    # Graphique simple avec Plotly
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=87,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Taux de satisfaction global", 'font': {'size': 16}},
        delta={'reference': 82, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#3B82F6"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 60], 'color': 'lightgray'},
                {'range': [60, 80], 'color': 'lightblue'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90}}))

    fig.update_layout(
        height=300,
        margin=dict(l=50, r=50, t=50, b=50),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="black", family="Arial")
    )

    st.plotly_chart(fig, use_container_width=True)

    # Pied de page
    st.markdown("""
    <div style="
        margin-top: 4rem;
        padding: 2rem 0;
        text-align: center;
        color: #64748b;
        border-top: 1px solid #e2e8f0;
    ">
        <p style="margin: 0.5rem 0; font-size: 0.9em;">
            Plateforme développée avec Streamlit • © 2024 Tous droits réservés
        </p>
        <p style="margin: 0.5rem 0; font-size: 0.8em; opacity: 0.8;">
            Une solution complète pour la gestion et l'analyse des données éducatives
        </p>
    </div>
    """, unsafe_allow_html=True)

# Configuration de la barre latérale améliorée
def setup_sidebar():
    st.markdown("""
    <style>
        /* Style global pour la barre latérale */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1E3A8A 0%, #1e40af 100%);
            min-width: 280px !important;
            max-width: 320px !important;
            padding-top: 2rem;
        }
        
        /* Titre de la barre latérale */
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 2rem;
            padding-bottom: 2rem;
            background: rgba(255, 255, 255, 0.1);
            margin-bottom: 2rem;
        }
        
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3 {
            color: white !important;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        
        /* Style des liens et boutons */
        .stButton > button {
            width: 100%;
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 0.8rem 1rem;
            margin: 0.5rem 0;
            font-weight: 500;
            text-align: left;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background: rgba(255, 255, 255, 0.2);
            border-color: rgba(255, 255, 255, 0.3);
            transform: translateX(5px);
        }
        
        .stButton > button:active {
            background: rgba(255, 255, 255, 0.3);
        }
        
        /* Style pour les sections */
        .sidebar-section {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 1rem;
            margin: 1rem 0;
            border-left: 4px solid #3B82F6;
        }
        
        .sidebar-section-title {
            color: #93c5fd !important;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.8rem;
            font-weight: 600;
        }
        
        /* Style pour les séparateurs */
        .sidebar-divider {
            height: 1px;
            background: rgba(255, 255, 255, 0.1);
            margin: 1.5rem 0;
        }
        
        /* Logo et branding */
        .sidebar-logo {
            text-align: center;
            margin-bottom: 2rem;
            padding: 1rem;
        }
        
        .sidebar-logo h2 {
            color: white !important;
            font-size: 1.5em;
            margin-bottom: 0.3rem;
        }
        
        .sidebar-logo p {
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.9em;
        }
        
        /* Style pour le footer de la sidebar */
        .sidebar-footer {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 1rem;
            background: rgba(0, 0, 0, 0.2);
            text-align: center;
        }
        
        .sidebar-footer p {
            color: rgba(255, 255, 255, 0.6);
            font-size: 0.8em;
            margin: 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # Logo et branding
    st.sidebar.markdown("""
    <div class="sidebar-logo">
        <h2>📊 ÉduAnalytics</h2>
        <p>Plateforme d'Analyse Scolaire</p>
    </div>
    """, unsafe_allow_html=True)

    # Navigation principale
    st.sidebar.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-section-title">Navigation Principale</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Boutons de navigation
    if st.sidebar.button("🏠 Accueil", key="home"):
        st.session_state.page = "accueil"
    
    if st.sidebar.button("📋 Tableaux Scolaires", key="tableaux"):
        st.session_state.page = "tableaux"
    
    if st.sidebar.button("🏫 Analyse des Salles", key="salles"):
        st.session_state.page = "salles"
    
    if st.sidebar.button("📈 Statistiques", key="stats"):
        st.session_state.page = "statistiques"
    
    if st.sidebar.button("👥 Gestion des Élèves", key="eleves"):
        st.session_state.page = "eleves"
    
    if st.sidebar.button("📊 Rapports", key="rapports"):
        st.session_state.page = "rapports"
    
    # Séparateur
    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    # Outils rapides
    st.sidebar.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-section-title">Outils Rapides</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("📥 Importer des Données", key="import"):
        st.session_state.page = "import"
    
    if st.sidebar.button("📤 Exporter les Résultats", key="export"):
        st.session_state.page = "export"
    
    if st.sidebar.button("⚙️ Paramètres", key="settings"):
        st.session_state.page = "settings"
    
    # Séparateur
    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    # Indicateur d'état
    st.sidebar.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-section-title">Statut du Système</div>
        <div style="color: white; font-size: 0.9em;">
            <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                <span>Statut :</span>
                <span style="color: #4ade80;">● Actif</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                <span>Données :</span>
                <span>2,548 enregistrements</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                <span>Dernière MAJ :</span>
                <span>Aujourd'hui</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer de la sidebar
    st.sidebar.markdown("""
    <div class="sidebar-footer">
        <p>Version 2.1.0 • © 2024</p>
    </div>
    """, unsafe_allow_html=True)

# Pour utiliser dans votre application principale
if __name__ == "__main__":
    # Configuration de la page
    st.set_page_config(
        page_title="Plateforme d'Analyse Scolaire",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialisation de l'état de la page
    if 'page' not in st.session_state:
        st.session_state.page = "accueil"
    
    # Configuration de la barre latérale
    setup_sidebar()
    
    # Affichage de la page en fonction de la navigation
    if st.session_state.page == "accueil":
        show_accueil()
    else:
        st.title(f"Page : {st.session_state.page}")
        st.info("Cette page est en cours de développement...")