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
    page_title="Analyse des Ratios et Salles de Classe",
    page_icon="📈",
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
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# En-tête de l'application
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0; font-size: 2.5rem;">📈 Analyse des Ratios et Capacités des Salles</h1>
    <p style="margin-top: 1rem; font-size: 1.2rem; opacity: 0.9;">Analyse des données de ratios et utilisation des salles de classe (Feuille Sheet3)</p>
</div>
""", unsafe_allow_html=True)

def clean_sheet3_data(df):
    """Nettoie et prépare les données de la feuille Sheet3"""
    
    # Renommer les colonnes pour uniformité
    rename_dict = {}
    for col in df.columns:
        col_str = str(col)
        
        if 'Région' in col_str:
            rename_dict[col] = 'Région'
        elif 'Ecole' in col_str or 'Ecole' in col_str:
            rename_dict[col] = 'Ecole'
        elif 'Ratio maximum approximatif' in col_str:
            rename_dict[col] = 'Ratio maximum'
        elif 'Ratio minimum approximatif' in col_str:
            rename_dict[col] = 'Ratio minimum'
        elif 'Ratio moyen' in col_str:
            rename_dict[col] = 'Ratio moyen'
        elif 'Écart-type du ratio moyen/max' in col_str:
            rename_dict[col] = 'Écart-type moyen/max'
        elif 'Écart-type du ratio min/max' in col_str:
            rename_dict[col] = 'Écart-type min/max'
        elif 'Nombre total de salles de classe dans l\'école' in col_str:
            rename_dict[col] = 'Total salles'
        elif 'Salle de classe utilisée' in col_str:
            rename_dict[col] = 'Salles utilisées'
        elif 'Salle de classe non utilisée' in col_str:
            rename_dict[col] = 'Salles non utilisées'
        elif 'Autre usage' in col_str:
            rename_dict[col] = 'Autres usages'
        elif 'Motif autre usage' in col_str:
            rename_dict[col] = 'Motif autre usage'
        elif 'Taille de la salle' in col_str or 'mètres carrés' in col_str:
            rename_dict[col] = 'Taille salle'
    
    df = df.rename(columns=rename_dict)
    
    # Nettoyer les données numériques
    numeric_columns = [
        'Ratio maximum', 'Ratio minimum', 'Ratio moyen',
        'Écart-type moyen/max', 'Écart-type min/max',
        'Total salles', 'Salles utilisées', 'Salles non utilisées', 'Autres usages'
    ]
    
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Calculer des métriques supplémentaires
    if 'Salles utilisées' in df.columns and 'Total salles' in df.columns:
        df['Taux utilisation (%)'] = (df['Salles utilisées'] / df['Total salles'] * 100).round(1)
    
    if 'Salles non utilisées' in df.columns and 'Total salles' in df.columns:
        df['Taux non utilisation (%)'] = (df['Salles non utilisées'] / df['Total salles'] * 100).round(1)
    
    if 'Autres usages' in df.columns and 'Total salles' in df.columns:
        df['Taux autres usages (%)'] = (df['Autres usages'] / df['Total salles'] * 100).round(1)
    
    # Calculer l'écart ratio (max-min)
    if 'Ratio maximum' in df.columns and 'Ratio minimum' in df.columns:
        df['Écart ratio'] = (df['Ratio maximum'] - df['Ratio minimum']).round(1)
    
    # Catégoriser les écoles par taux d'utilisation
    if 'Taux utilisation (%)' in df.columns:
        conditions = [
            df['Taux utilisation (%)'] >= 90,
            df['Taux utilisation (%)'] >= 70,
            df['Taux utilisation (%)'] >= 50,
            df['Taux utilisation (%)'] < 50
        ]
        choices = ['Très élevé (≥90%)', 'Élevé (70-90%)', 'Moyen (50-70%)', 'Faible (<50%)']
        df['Catégorie utilisation'] = np.select(conditions, choices, default='Non défini')
    
    return df

def create_summary_statistics(df):
    """Crée des statistiques récapitulatives pour Sheet3"""
    
    stats = {}
    
    # Statistiques de base
    stats['Nombre d\'écoles'] = len(df)
    stats['Nombre de régions'] = df['Région'].nunique() if 'Région' in df.columns else 0
    
    # Statistiques sur les ratios
    ratio_cols = ['Ratio maximum', 'Ratio minimum', 'Ratio moyen']
    for col in ratio_cols:
        if col in df.columns:
            stats[f'{col} - Moyenne'] = df[col].mean()
            stats[f'{col} - Médiane'] = df[col].median()
            stats[f'{col} - Min'] = df[col].min()
            stats[f'{col} - Max'] = df[col].max()
            stats[f'{col} - Écart-type'] = df[col].std()
    
    # Statistiques sur les salles
    salle_cols = ['Total salles', 'Salles utilisées', 'Salles non utilisées', 'Autres usages']
    for col in salle_cols:
        if col in df.columns:
            stats[f'{col} - Total'] = df[col].sum()
            stats[f'{col} - Moyenne par école'] = df[col].mean()
    
    # Taux d'utilisation
    if 'Taux utilisation (%)' in df.columns:
        stats['Taux utilisation moyen'] = df['Taux utilisation (%)'].mean()
        stats['École meilleur taux'] = df.loc[df['Taux utilisation (%)'].idxmax(), 'Ecole'] if 'Ecole' in df.columns else 'N/A'
        stats['Meilleur taux (%)'] = df['Taux utilisation (%)'].max()
        stats['École plus faible taux'] = df.loc[df['Taux utilisation (%)'].idxmin(), 'Ecole'] if 'Ecole' in df.columns else 'N/A'
        stats['Plus faible taux (%)'] = df['Taux utilisation (%)'].min()
    
    # Distribution par région
    if 'Région' in df.columns:
        region_stats = df['Région'].value_counts()
        for region, count in region_stats.items():
            stats[f'Écoles en {region}'] = count
    
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
                    hover_data=['Ecole', 'Région'],
                    title=f"Nuage de points: {x_variable} vs {y_variable}",
                    labels={x_variable: x_variable, y_variable: y_variable}
                )
            else:
                fig = px.scatter(
                    analysis_df, 
                    x=x_variable, 
                    y=y_variable,
                    hover_data=['Ecole', 'Région'],
                    title=f"Nuage de points: {x_variable} vs {y_variable}",
                    labels={x_variable: x_variable, y_variable: y_variable}
                )
                
        elif graph_type == "Histogramme":
            fig = px.histogram(
                analysis_df, 
                x=x_variable,
                title=f"Distribution de {x_variable}",
                labels={x_variable: x_variable, 'count': 'Nombre d\'écoles'},
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
                    hover_data=['Ecole', 'Région']
                )
            else:
                fig = px.box(
                    analysis_df, 
                    y=x_variable,
                    title=f"Distribution de {x_variable}",
                    points="all",
                    hover_data=['Ecole', 'Région']
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
        
        elif graph_type == "Treemap":
            if color_variable and color_variable in analysis_df.columns:
                fig = px.treemap(
                    analysis_df,
                    path=[color_variable, 'Ecole'],
                    values=x_variable,
                    title=f"Treemap de {x_variable} par {color_variable}"
                )
        
        elif graph_type == "Graphique à bulles":
            if 'Total salles' in analysis_df.columns:
                fig = px.scatter(
                    analysis_df,
                    x=x_variable,
                    y=y_variable,
                    size='Total salles',
                    color=color_variable if color_variable and color_variable in analysis_df.columns else None,
                    hover_name='Ecole',
                    title=f"Graphique à bulles: {x_variable} vs {y_variable}",
                    size_max=60
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
        help="Le fichier doit contenir une feuille 'Sheet3' avec les données des ratios et salles"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        try:
            # Lire uniquement la feuille Sheet3
            df = pd.read_excel(uploaded_file, sheet_name='Sheet3', engine='openpyxl')
            
            # Nettoyer les données
            df = clean_sheet3_data(df)
            
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
                    <p>Écoles analysées</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="stat-card">
                    <h3>📊</h3>
                    <h2>{len(df.columns)}</h2>
                    <p>Variables</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                ratio_moyen = df['Ratio moyen'].mean() if 'Ratio moyen' in df.columns else 0
                st.markdown(f"""
                <div class="stat-card">
                    <h3>📈</h3>
                    <h2>{ratio_moyen:.1f}</h2>
                    <p>Ratio moyen</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                taux_utilisation = df['Taux utilisation (%)'].mean() if 'Taux utilisation (%)' in df.columns else 0
                st.markdown(f"""
                <div class="stat-card">
                    <h3>⚡</h3>
                    <h2>{taux_utilisation:.0f}%</h2>
                    <p>Taux utilisation</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Créer des onglets pour différentes fonctionnalités
            tab1, tab2, tab3 = st.tabs(["📋 Vue d'ensemble", "📈 Analyse Statistique", "🏆 Classements"])
            
            with tab1:
                # Aperçu des données
                with st.expander("🔍 Aperçu des données brutes", expanded=True):
                    st.dataframe(df.head(20), use_container_width=True)
                    st.caption(f"Dimensions : {df.shape[0]} lignes × {df.shape[1]} colonnes")
                
                # Statistiques récapitulatives
                with st.expander("📊 Statistiques descriptives", expanded=True):
                    stats = create_summary_statistics(df)
                    
                    # Afficher les métriques clés
                    st.subheader("📊 Métriques Clés")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    key_metrics = {
                        'Ratio maximum': f"{stats.get('Ratio maximum - Moyenne', 0):.1f}",
                        'Ratio minimum': f"{stats.get('Ratio minimum - Moyenne', 0):.1f}",
                        'Total salles': f"{stats.get('Total salles - Total', 0):.0f}",
                        'Taux utilisation': f"{stats.get('Taux utilisation moyen', 0):.1f}%"
                    }
                    
                    for i, (key, value) in enumerate(key_metrics.items()):
                        with [col1, col2, col3, col4][i]:
                            st.markdown(f"""
                            <div class="metric-card">
                                <h4>{key}</h4>
                                <h3>{value}</h3>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Afficher un tableau des statistiques détaillées
                    st.subheader("📈 Statistiques détaillées")
                    st.dataframe(pd.DataFrame(stats).T, use_container_width=True)
                
                # Visualisations rapides
                with st.expander("📊 Visualisations rapides", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Histogramme du ratio moyen
                        if 'Ratio moyen' in df.columns:
                            fig1 = px.histogram(
                                df, 
                                x='Ratio moyen',
                                title="Distribution du Ratio Moyen",
                                nbins=20,
                                color_discrete_sequence=['#3B82F6']
                            )
                            fig1.update_layout(template="plotly_white", height=300)
                            st.plotly_chart(fig1, use_container_width=True)
                    
                    with col2:
                        # Diagramme en barres par région
                        if 'Région' in df.columns and 'Ratio moyen' in df.columns:
                            region_avg = df.groupby('Région')['Ratio moyen'].mean().sort_values(ascending=False)
                            fig2 = px.bar(
                                x=region_avg.index,
                                y=region_avg.values,
                                title="Ratio Moyen par Région",
                                color=region_avg.values,
                                color_continuous_scale='Viridis'
                            )
                            fig2.update_layout(template="plotly_white", height=300, 
                                             xaxis_title="Région", yaxis_title="Ratio moyen")
                            st.plotly_chart(fig2, use_container_width=True)
                
                # Téléchargement des données nettoyées
                with st.expander("💾 Télécharger les données", expanded=False):
                    csv_data = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Télécharger les données nettoyées (CSV)",
                        data=csv_data,
                        file_name="donnees_ratios_salles_nettoyees.csv",
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
                            index=available_variables.index('Ratio moyen') if 'Ratio moyen' in available_variables else 0
                        )
                    
                    with col2:
                        y_variable = st.selectbox(
                            "Variable Y:",
                            options=available_variables,
                            index=available_variables.index('Taux utilisation (%)') if 'Taux utilisation (%)' in available_variables else 1
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
                                "Graphique en violon",
                                "Treemap",
                                "Graphique à bulles"
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
                                # Afficher un aperçu des données d'analyse
                                with st.expander("🔍 Voir les données d'analyse", expanded=False):
                                    # Créer une liste unique de colonnes à afficher
                                    display_cols = [x_variable, y_variable]
                                    if color_variable and color_variable not in display_cols:
                                        display_cols.append(color_variable)
                                    
                                    # Ajouter les colonnes de base sans doublons
                                    base_cols = ['Ecole', 'Région']
                                    for col in base_cols:
                                        if col not in display_cols:
                                            display_cols.append(col)
                                    
                                    # Filtrer pour ne garder que les colonnes existantes
                                    existing_cols = [col for col in display_cols if col in analysis_df.columns]
                                    
                                    # Supprimer les doublons
                                    existing_cols = list(dict.fromkeys(existing_cols))
                                    
                                    st.dataframe(
                                        analysis_df[existing_cols].head(20),
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
                    
                    1. **Ratio moyen vs Taux utilisation** : Relation entre le ratio élèves/salle et l'utilisation des salles
                    2. **Total salles vs Ratio maximum** : Comment la taille de l'école influence le ratio maximum
                    3. **Distribution par Région** : Comparer les ratios entre différentes régions
                    4. **Écart ratio vs Écart-type** : Relation entre la variabilité des ratios
                    5. **Salles utilisées vs Ratio moyen** : Impact de l'utilisation sur le ratio
                    
                    **Variables numériques disponibles :**
                    - Ratio maximum, Ratio minimum, Ratio moyen
                    - Écart-type moyen/max, Écart-type min/max, Écart ratio
                    - Total salles, Salles utilisées, Salles non utilisées, Autres usages
                    - Taux utilisation (%), Taux non utilisation (%), Taux autres usages (%)
                    
                    **Variables catégorielles disponibles :**
                    - Région, Nom de l'école, Catégorie utilisation
                    - Motif autre usage, Taille salle
                    
                    **Types de graphiques recommandés :**
                    - **Nuage de points** : Pour corrélations entre variables numériques
                    - **Box plot** : Pour comparer distributions entre régions
                    - **Treemap** : Pour visualiser la hiérarchie des données
                    - **Graphique à bulles** : Pour 3 dimensions (X, Y, taille)
                    - **Heatmap** : Pour voir toutes les corrélations
                    """)
            
            with tab3:
                st.markdown("## 🏆 Classements et Performances")
                
                # Classement par ratio moyen
                with st.expander("🥇 Classement par Ratio Moyen", expanded=True):
                    if 'Ratio moyen' in df.columns and 'Ecole' in df.columns:
                        ranked_df = df.sort_values('Ratio moyen', ascending=False)
                        ranked_df = ranked_df[['Ecole', 'Région', 'Ratio moyen', 'Ratio maximum', 'Ratio minimum']]
                        ranked_df['Rang'] = range(1, len(ranked_df) + 1)
                        
                        st.dataframe(
                            ranked_df.head(10),
                            use_container_width=True,
                            column_config={
                                "Rang": st.column_config.NumberColumn(format="%d"),
                                "Ratio moyen": st.column_config.NumberColumn(format="%.1f"),
                                "Ratio maximum": st.column_config.NumberColumn(format="%.1f"),
                                "Ratio minimum": st.column_config.NumberColumn(format="%.1f")
                            }
                        )
                        
                        # Graphique du top 10
                        top10 = ranked_df.head(10)
                        fig = px.bar(
                            top10,
                            x='Ecole',
                            y='Ratio moyen',
                            color='Région',
                            title="Top 10 des écoles par Ratio Moyen"
                        )
                        fig.update_layout(template="plotly_white", xaxis_tickangle=45)
                        st.plotly_chart(fig, use_container_width=True)
                
                # Classement par taux d'utilisation
                with st.expander("⚡ Classement par Taux d'Utilisation", expanded=False):
                    if 'Taux utilisation (%)' in df.columns and 'Ecole' in df.columns:
                        usage_ranked = df.sort_values('Taux utilisation (%)', ascending=False)
                        usage_ranked = usage_ranked[['Ecole', 'Région', 'Taux utilisation (%)', 'Salles utilisées', 'Total salles']]
                        usage_ranked['Rang'] = range(1, len(usage_ranked) + 1)
                        
                        st.dataframe(
                            usage_ranked.head(10),
                            use_container_width=True,
                            column_config={
                                "Rang": st.column_config.NumberColumn(format="%d"),
                                "Taux utilisation (%)": st.column_config.NumberColumn(format="%.1f%%"),
                                "Salles utilisées": st.column_config.NumberColumn(format="%d"),
                                "Total salles": st.column_config.NumberColumn(format="%d")
                            }
                        )
                
                # Analyse par région
                with st.expander("📍 Analyse par Région", expanded=False):
                    if 'Région' in df.columns:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Moyenne par région
                            region_stats = df.groupby('Région').agg({
                                'Ratio moyen': 'mean',
                                'Taux utilisation (%)': 'mean',
                                'Ecole': 'count'
                            }).round(1)
                            region_stats = region_stats.rename(columns={'Ecole': 'Nombre d\'écoles'})
                            
                            st.dataframe(region_stats, use_container_width=True)
                        
                        with col2:
                            # Graphique radar des régions
                            if len(region_stats) > 0:
                                fig = px.line_polar(
                                    region_stats.reset_index(),
                                    r='Ratio moyen',
                                    theta='Région',
                                    line_close=True,
                                    title="Ratios moyens par Région (Radar)"
                                )
                                fig.update_traces(fill='toself')
                                st.plotly_chart(fig, use_container_width=True)
        
        except Exception as e:
            st.error(f"❌ Erreur lors de la lecture du fichier : {str(e)}")
            st.markdown('<div class="warning-box">', unsafe_allow_html=True)
            st.info("""
            **Conseils de dépannage :**
            1. Vérifiez que le fichier contient bien une feuille nommée 'Sheet3'
            2. Ouvrez le fichier dans Excel pour vérifier sa structure
            3. Assurez-vous que les colonnes 'Région' et 'Nom de l\'école' existent
            """)
            st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # Afficher un exemple de structure attendue
        st.info("👆 Veuillez téléverser votre fichier Excel FIFA project.xlsx")
        
        # Exemple de structure
        with st.expander("🧾 Structure attendue de la feuille Sheet3", expanded=True):
            st.markdown("""
            **La feuille Sheet3 doit contenir au minimum ces colonnes :**
            
            1. **Région** : Région administrative
            2. **Nom de l'école** : Nom de l'établissement
            3. **Ratio maximum approximatif** : Ratio élèves/salle maximum
            4. **Ratio minimum approximatif** : Ratio élèves/salle minimum
            5. **Ratio moyen** : Ratio élèves/salle moyen
            6. **Écart-type du ratio moyen/max** : Variabilité des ratios
            7. **Écart-type du ratio min/max** : Variabilité des ratios
            8. **Nombre total de salles de classe dans l'école** : Total des salles
            9. **Salle de classe utilisée** : Salles en utilisation normale
            10. **Salle de classe non utilisée** : Salles non utilisées
            11. **Autre usage** : Salles à usage spécial
            12. **Motif autre usage** : Description de l'usage spécial
            13. **Taille de la salle** : Dimensions des salles
            
            **Métriques calculées automatiquement :**
            - Taux d'utilisation (%)
            - Taux de non-utilisation (%)
            - Taux autres usages (%)
            - Écart ratio (max-min)
            - Catégorie d'utilisation
            """)

if __name__ == "__main__":
    main()