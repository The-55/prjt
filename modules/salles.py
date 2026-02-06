import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Analyse des Salles de Classe",
    page_icon="🏫",
    layout="wide"
)

# Style CSS personnalisé
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
    .upload-section {
        background: #f0f9ff;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border: 2px dashed #3B82F6;
    }
    .success-message {
        background: #dcfce7;
        color: #166534;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #10b981;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .info-box {
        background: #e0f2fe;
        color: #075985;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #0ea5e9;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .warning-box {
        background: #fef3c7;
        color: #92400e;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #f59e0b;
        margin: 1rem 0;
    }
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
        border-top: 4px solid #3B82F6;
    }
    .graph-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# En-tête de l'application
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0; font-size: 2.5rem;">🏫 Analyse des Salles de Classe</h1>
    <p style="margin-top: 1rem; font-size: 1.2rem; opacity: 0.9;">Analyse des données d'infrastructure des salles de classe (Feuille Sheet5)</p>
</div>
""", unsafe_allow_html=True)

def clean_sheet5_data(df):
    """Nettoie et prépare les données de la feuille Sheet5"""
    
    # Vérifier si nous avons les bonnes colonnes
    required_columns = ['Moughataa', 'Ecole']
    
    # Renommer les colonnes pour uniformité
    rename_dict = {}
    for col in df.columns:
        if 'Moughataa' in str(col):
            rename_dict[col] = 'Moughataa'
        elif 'Ecole' in str(col) or 'Ecole' in str(col):
            rename_dict[col] = 'Ecole'
        elif 'Etat général de la salle' in str(col):
            rename_dict[col] = 'Etat général'
        elif 'Longueur de la salle' in str(col):
            rename_dict[col] = 'Longueur (m)'
        elif 'Largeur de la salle' in str(col):
            rename_dict[col] = 'Largeur (m)'
        elif 'La superficie de la salle' in str(col):
            rename_dict[col] = 'Superficie (m²)'
        elif 'Etat de la porte de la salle est-elle' in str(col):
            rename_dict[col] = 'Etat de la porte'
        elif 'La fenêtre est-elle' in str(col):
            rename_dict[col] = 'Etat des fenêtres'
        elif 'Type d\'aération' in str(col):
            rename_dict[col] = 'Type d\'aération'
        elif 'Fenêtres' in str(col) and df[col].dtype in [np.int64, np.float64]:
            rename_dict[col] = 'Nombre de fenêtres'
        elif 'Nombre de prises de la salle' in str(col):
            rename_dict[col] = 'Nombre de prises'
        elif 'Espace de projection prévu' in str(col):
            rename_dict[col] = 'Espace projection'
        elif 'La salle nécessite-t-elle une réhabilitation' in str(col):
            rename_dict[col] = 'Réhabilitation nécessaire'
        elif 'Besoins en mobilier' in str(col):
            rename_dict[col] = 'Besoins mobilier'
    
    df = df.rename(columns=rename_dict)
    
    # Nettoyer les données numériques
    numeric_columns = ['Longueur (m)', 'Largeur (m)', 'Superficie (m²)', 
                      'Nombre de fenêtres', 'Nombre de prises']
    
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Calculer la superficie si nécessaire
    if 'Superficie (m²)' not in df.columns and 'Longueur (m)' in df.columns and 'Largeur (m)' in df.columns:
        df['Superficie (m²)'] = df['Longueur (m)'] * df['Largeur (m)']
    
    return df

def create_summary_statistics(df):
    """Crée des statistiques récapitulatives"""
    
    stats = {}
    
    # Statistiques de base
    stats['Nombre de salles'] = len(df)
    stats['Nombre d\'écoles'] = df['Ecole'].nunique()
    stats['Nombre de Moughataas'] = df['Moughataa'].nunique()
    
    # Statistiques numériques
    numeric_cols = ['Longueur (m)', 'Largeur (m)', 'Superficie (m²)', 
                   'Nombre de fenêtres', 'Nombre de prises']
    
    for col in numeric_cols:
        if col in df.columns:
            stats[f'{col} - Moyenne'] = df[col].mean()
            stats[f'{col} - Médiane'] = df[col].median()
            stats[f'{col} - Min'] = df[col].min()
            stats[f'{col} - Max'] = df[col].max()
    
    # Statistiques catégorielles
    categorical_cols = ['Etat général', 'Etat de la porte', 'Etat des fenêtres',
                       'Type d\'aération', 'Espace projection', 
                       'Réhabilitation nécessaire', 'Besoins mobilier']
    
    for col in categorical_cols:
        if col in df.columns:
            value_counts = df[col].value_counts()
            for value, count in value_counts.items():
                if pd.notnull(value):
                    stats[f'{col} - {value}'] = count
    
    return pd.Series(stats)

def create_binary_statistical_graphs(df, x_variable, y_variable, graph_type, color_variable=None):
    """Crée des graphiques statistiques binaires"""
    
    # Préparer les données
    analysis_df = df.copy()
    
    # Vérifier que les variables existent
    if x_variable not in analysis_df.columns:
        st.error(f"❌ Variable X '{x_variable}' non trouvée dans les données")
        return None, None
    
    if y_variable not in analysis_df.columns:
        st.error(f"❌ Variable Y '{y_variable}' non trouvée dans les données")
        return None, None
    
    # Créer le graphique en fonction du type sélectionné
    fig = None
    
    try:
        if graph_type == "Nuage de points":
            if color_variable and color_variable in analysis_df.columns:
                fig = px.scatter(
                    analysis_df, 
                    x=x_variable, 
                    y=y_variable,
                    color=color_variable,
                    hover_data=['Ecole', 'Moughataa'],
                    title=f"Nuage de points: {x_variable} vs {y_variable}",
                    labels={x_variable: x_variable, y_variable: y_variable}
                )
            else:
                fig = px.scatter(
                    analysis_df, 
                    x=x_variable, 
                    y=y_variable,
                    hover_data=['Ecole', 'Moughataa'],
                    title=f"Nuage de points: {x_variable} vs {y_variable}",
                    labels={x_variable: x_variable, y_variable: y_variable}
                )
                
        elif graph_type == "Histogramme":
            fig = px.histogram(
                analysis_df, 
                x=x_variable,
                title=f"Distribution de {x_variable}",
                labels={x_variable: x_variable, 'count': 'Nombre de salles'},
                color=color_variable if color_variable and color_variable in analysis_df.columns else None,
                nbins=20
            )
            
        elif graph_type == "Diagramme en barres":
            if color_variable and color_variable in analysis_df.columns:
                # Regrouper par variable de couleur
                grouped_data = analysis_df.groupby(color_variable).agg({
                    x_variable: 'mean',
                    y_variable: 'mean'
                }).reset_index()
                
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                
                fig.add_trace(
                    go.Bar(
                        x=grouped_data[color_variable],
                        y=grouped_data[x_variable],
                        name=x_variable,
                        marker_color='#3B82F6'
                    ),
                    secondary_y=False
                )
                
                fig.add_trace(
                    go.Scatter(
                        x=grouped_data[color_variable],
                        y=grouped_data[y_variable],
                        name=y_variable,
                        mode='lines+markers',
                        marker_color='#EF4444',
                        line=dict(width=3)
                    ),
                    secondary_y=True
                )
                
                fig.update_layout(
                    title=f"Moyenne de {x_variable} et {y_variable} par {color_variable}",
                    xaxis_title=color_variable,
                    showlegend=True
                )
                
                fig.update_yaxes(title_text=x_variable, secondary_y=False)
                fig.update_yaxes(title_text=y_variable, secondary_y=True)
            else:
                # Simple bar chart
                fig = px.bar(
                    analysis_df,
                    x=x_variable,
                    y=y_variable,
                    title=f"{x_variable} vs {y_variable}"
                )
            
        elif graph_type == "Box plot":
            if color_variable and color_variable in analysis_df.columns:
                fig = px.box(
                    analysis_df, 
                    x=color_variable, 
                    y=x_variable,
                    title=f"Distribution de {x_variable} par {color_variable}",
                    points="all",
                    hover_data=['Ecole', 'Moughataa']
                )
            else:
                fig = px.box(
                    analysis_df, 
                    y=x_variable,
                    title=f"Distribution de {x_variable}",
                    points="all",
                    hover_data=['Ecole', 'Moughataa']
                )
        
        elif graph_type == "Carte thermique (heatmap)":
            # Sélectionner uniquement les colonnes numériques pour la corrélation
            numeric_df = analysis_df.select_dtypes(include=[np.number])
            
            if len(numeric_df.columns) > 1:
                corr_matrix = numeric_df.corr()
                
                fig = px.imshow(
                    corr_matrix,
                    text_auto=True,
                    title="Matrice de corrélation entre variables numériques",
                    color_continuous_scale='RdBu',
                    aspect="auto"
                )
            else:
                st.warning("⚠️ Pas assez de variables numériques pour créer une heatmap")
                return None, None
        
        elif graph_type == "Diagramme circulaire":
            if x_variable in analysis_df.columns:
                value_counts = analysis_df[x_variable].value_counts()
                
                fig = px.pie(
                    values=value_counts.values,
                    names=value_counts.index,
                    title=f"Répartition de {x_variable}"
                )
        
        elif graph_type == "Graphique en violon":
            if color_variable and color_variable in analysis_df.columns:
                fig = px.violin(
                    analysis_df,
                    x=color_variable,
                    y=x_variable,
                    box=True,
                    points="all",
                    title=f"Distribution de {x_variable} par {color_variable}"
                )
            else:
                fig = px.violin(
                    analysis_df,
                    y=x_variable,
                    box=True,
                    points="all",
                    title=f"Distribution de {x_variable}"
                )
    
    except Exception as e:
        st.error(f"❌ Erreur lors de la création du graphique: {str(e)}")
        return None, None
    
    if fig:
        # Personnaliser le graphique
        fig.update_layout(
            template="plotly_white",
            hovermode="closest",
            height=500,
            font=dict(size=12)
        )
    
    return fig, analysis_df

def main():
    # Section de téléversement
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "📤 Téléversez votre fichier Excel (FIFA project.xlsx)",
        type=['xlsx', 'xls'],
        help="Le fichier doit contenir une feuille 'Sheet5' avec les données des salles de classe"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        try:
            # Lire uniquement la feuille Sheet5
            df = pd.read_excel(uploaded_file, sheet_name='Sheet5', engine='openpyxl')
            
            # Nettoyer les données
            df = clean_sheet5_data(df)
            
            # Afficher les informations sur la structure
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.success("✅ Fichier téléversé avec succès !")
            
            # Afficher la structure détectée
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="stat-card">
                    <h3>🏫</h3>
                    <h2>{len(df)}</h2>
                    <p>Salles analysées</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="stat-card">
                    <h3>📊</h3>
                    <h2>{len(df.columns)}</h2>
                    <p>Colonnes</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="stat-card">
                    <h3>🏢</h3>
                    <h2>{df['Ecole'].nunique()}</h2>
                    <p>Écoles</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="stat-card">
                    <h3>📍</h3>
                    <h2>{df['Moughataa'].nunique()}</h2>
                    <p>Moughataas</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Créer des onglets pour différentes fonctionnalités
            tab1, tab2 = st.tabs(["📋 Vue d'ensemble des Données", "📈 Analyse Statistique"])
            
            with tab1:
                # Aperçu des données
                with st.expander("🔍 Aperçu des données brutes", expanded=True):
                    st.dataframe(df.head(20), use_container_width=True)
                    st.caption(f"Dimensions : {df.shape[0]} lignes × {df.shape[1]} colonnes")
                
                # Statistiques récapitulatives
                with st.expander("📊 Statistiques descriptives", expanded=True):
                    stats = create_summary_statistics(df)
                    
                    # Afficher les statistiques principales
                    col1, col2, col3, col4 = st.columns(4)
                    
                    stats_to_show = {
                        'Nombre de salles': stats.get('Nombre de salles', 'N/A'),
                        'Nombre d\'écoles': stats.get('Nombre d\'écoles', 'N/A'),
                        'Superficie moyenne': f"{stats.get('Superficie (m²) - Moyenne', 0):.1f} m²",
                        'Longueur moyenne': f"{stats.get('Longueur (m) - Moyenne', 0):.1f} m"
                    }
                    
                    for i, (key, value) in enumerate(stats_to_show.items()):
                        with [col1, col2, col3, col4][i]:
                            st.metric(key, value)
                    
                    # Afficher un tableau des statistiques détaillées
                    st.dataframe(pd.DataFrame(stats).T, use_container_width=True)
                
                # Distribution des variables catégorielles
                with st.expander("📊 Distribution des variables catégorielles", expanded=False):
                    categorical_cols = ['Etat général', 'Etat de la porte', 'Etat des fenêtres',
                                      'Type d\'aération', 'Espace projection', 
                                      'Réhabilitation nécessaire', 'Besoins mobilier']
                    
                    available_categorical = [col for col in categorical_cols if col in df.columns]
                    
                    if available_categorical:
                        selected_cat = st.selectbox(
                            "Sélectionnez une variable catégorielle:",
                            options=available_categorical
                        )
                        
                        if selected_cat:
                            value_counts = df[selected_cat].value_counts()
                            fig = px.bar(
                                x=value_counts.index,
                                y=value_counts.values,
                                title=f"Distribution de {selected_cat}",
                                labels={'x': selected_cat, 'y': 'Nombre de salles'}
                            )
                            fig.update_layout(template="plotly_white")
                            st.plotly_chart(fig, use_container_width=True)
                    
                # Téléchargement des données nettoyées
                with st.expander("💾 Télécharger les données", expanded=False):
                    csv_data = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Télécharger les données nettoyées (CSV)",
                        data=csv_data,
                        file_name="donnees_salles_classe_nettoyees.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            
            with tab2:
                st.markdown("## 📈 Analyse Statistique Binaire")
                st.markdown("Générez des graphiques pour analyser les relations entre différentes variables.")
                
                # Section de sélection des paramètres
                with st.container():
                    st.markdown("### ⚙️ Paramètres de l'analyse")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        # Sélection des variables
                        available_variables = list(df.columns)
                        numeric_vars = df.select_dtypes(include=[np.number]).columns.tolist()
                        categorical_vars = df.select_dtypes(include=['object']).columns.tolist()
                        
                        x_variable = st.selectbox(
                            "Variable X:",
                            options=available_variables,
                            index=0 if available_variables else None
                        )
                    
                    with col2:
                        y_variable = st.selectbox(
                            "Variable Y:",
                            options=available_variables,
                            index=1 if len(available_variables) > 1 else 0
                        )
                    
                    with col3:
                        # Sélection du type de graphique
                        graph_type = st.selectbox(
                            "Type de graphique:",
                            options=[
                                "Nuage de points", 
                                "Histogramme", 
                                "Diagramme en barres", 
                                "Box plot", 
                                "Carte thermique (heatmap)",
                                "Diagramme circulaire",
                                "Graphique en violon"
                            ],
                            index=0
                        )
                    
                    # Options avancées
                    with st.expander("⚙️ Options avancées", expanded=False):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            color_variable = st.selectbox(
                                "Variable de couleur (optionnel):",
                                options=["Aucune"] + categorical_vars,
                                index=0
                            )
                            if color_variable == "Aucune":
                                color_variable = None
                        
                        with col2:
                            filter_variable = st.selectbox(
                                "Filtrer par (optionnel):",
                                options=["Aucun filtre"] + categorical_vars,
                                index=0
                            )
                            
                            if filter_variable != "Aucun filtre" and filter_variable in df.columns:
                                filter_values = df[filter_variable].unique()
                                selected_filter = st.multiselect(
                                    f"Valeurs de {filter_variable}:",
                                    options=filter_values,
                                    default=filter_values[:5] if len(filter_values) > 5 else filter_values
                                )
                    
                    # Bouton pour générer le graphique
                    generate_graph_button = st.button(
                        "📊 Générer le graphique",
                        type="primary",
                        use_container_width=True
                    )
                
                # Section d'affichage des résultats
                if generate_graph_button:
                    with st.spinner("🔄 Génération du graphique en cours..."):
                        try:
                            # Appliquer les filtres
                            filtered_df = df.copy()
                            
                            if filter_variable != "Aucun filtre" and filter_variable in df.columns and 'selected_filter' in locals():
                                filtered_df = filtered_df[filtered_df[filter_variable].isin(selected_filter)]
                            
                            # Créer le graphique
                            fig, analysis_df = create_binary_statistical_graphs(
                                filtered_df, x_variable, y_variable, graph_type, color_variable
                            )
                            
                            if fig:
                                # Afficher le graphique
                                st.markdown('<div class="graph-card">', unsafe_allow_html=True)
                                st.plotly_chart(fig, use_container_width=True)
                                st.markdown('</div>', unsafe_allow_html=True)
                                
                                # Afficher les statistiques
                                st.markdown("### 📊 Statistiques descriptives")
                                
                                # Calculer les statistiques de base
                                if x_variable in numeric_vars:
                                    col1, col2, col3, col4 = st.columns(4)
                                    
                                    with col1:
                                        st.metric(
                                            f"Moyenne {x_variable}",
                                            f"{analysis_df[x_variable].mean():.2f}"
                                        )
                                    
                                    with col2:
                                        st.metric(
                                            f"Médiane {x_variable}",
                                            f"{analysis_df[x_variable].median():.2f}"
                                        )
                                    
                                    with col3:
                                        st.metric(
                                            f"Min {x_variable}",
                                            f"{analysis_df[x_variable].min():.2f}"
                                        )
                                    
                                    with col4:
                                        st.metric(
                                            f"Max {x_variable}",
                                            f"{analysis_df[x_variable].max():.2f}"
                                        )
                                
                                # Afficher un aperçu des données d'analyse
                                with st.expander("🔍 Voir les données d'analyse", expanded=False):
                                    st.dataframe(
                                        analysis_df[[x_variable, y_variable] + 
                                                   ([color_variable] if color_variable else []) +
                                                   ['Ecole', 'Moughataa']].head(20),
                                        use_container_width=True
                                    )
                                    
                                    # Option pour télécharger les données d'analyse
                                    csv_data = analysis_df.to_csv(index=False).encode('utf-8')
                                    st.download_button(
                                        label="📥 Télécharger les données d'analyse (CSV)",
                                        data=csv_data,
                                        file_name=f"donnees_analyse_{x_variable}_vs_{y_variable}.csv",
                                        mime="text/csv",
                                        use_container_width=True
                                    )
                            
                        except Exception as e:
                            st.error(f"❌ Erreur lors de la génération du graphique : {str(e)}")
                
                # Section d'exemples d'analyses
                with st.expander("💡 Exemples d'analyses possibles", expanded=True):
                    st.markdown("""
                    **Exemples d'analyses binaires intéressantes :**
                    
                    1. **Superficie vs Nombre de prises** : Relation entre la taille de la salle et l'équipement électrique
                    2. **Etat général vs Besoins mobilier** : Comment l'état de la salle influence les besoins en mobilier
                    3. **Distribution par Moughataa** : Comparer les équipements entre différentes régions
                    4. **Corrélations numériques** : Identifier les relations entre variables quantitatives
                    
                    **Variables numériques disponibles :**
                    - Longueur (m), Largeur (m), Superficie (m²)
                    - Nombre de fenêtres, Nombre de prises
                    
                    **Variables catégorielles disponibles :**
                    - Etat général, Etat de la porte, Etat des fenêtres
                    - Type d'aération, Espace projection
                    - Réhabilitation nécessaire, Besoins mobilier
                    - Moughataa, Nom de l'école
                    
                    **Conseils :**
                    - Utilisez le nuage de points pour identifier des tendances
                    - L'histogramme montre la distribution d'une variable
                    - Le box plot permet de comparer les distributions entre catégories
                    - La carte thermique révèle les corrélations entre toutes les variables numériques
                    """)
        
        except Exception as e:
            st.error(f"❌ Erreur lors de la lecture du fichier : {str(e)}")
            st.markdown('<div class="warning-box">', unsafe_allow_html=True)
            st.info("""
            **Conseils de dépannage :**
            1. Vérifiez que le fichier contient bien une feuille nommée 'Sheet5'
            2. Ouvrez le fichier dans Excel pour vérifier sa structure
            3. Assurez-vous que les colonnes 'Moughataa' et 'Nom de l\'école' existent
            """)
            st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # Afficher un exemple de structure attendue
        st.info("👆 Veuillez téléverser votre fichier Excel FIFA project.xlsx")
        
        # Exemple de structure
        with st.expander("🧾 Structure attendue de la feuille Sheet5", expanded=True):
            st.markdown("""
            **La feuille Sheet5 doit contenir au minimum ces colonnes :**
            
            1. **Moughataa** : Région administrative
            2. **Nom de l'école** : Nom de l'établissement
            3. **Etat général de la salle** : État de conservation
            4. **Longueur de la salle** : En mètres
            5. **Largeur de la salle** : En mètres
            6. **La superficie de la salle** : En mètres carrés
            7. **Etat de la porte de la salle** : Description de l'état
            8. **La fenêtre est-elle** : Description de l'état
            9. **Type d'aération** : Méthode d'aération
            10. **Fenêtres** : Nombre de fenêtres
            11. **Nombre de prises de la salle** : Nombre de prises électriques
            12. **Espace de projection prévu ?** : Disponibilité d'espace
            13. **La salle nécessite-t-elle une réhabilitation ?** : Oui/Non
            14. **Besoins en mobilier ?** : Oui/Non
            
            **Note :** L'application nettoiera automatiquement les noms de colonnes
            """)

if __name__ == "__main__":
    main()