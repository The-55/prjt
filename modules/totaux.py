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
    page_title="Analyse des Totaux par École",
    page_icon="📊",
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
    <h1 style="margin: 0; font-size: 2.5rem;">📊 Analyse des Totaux par École</h1>
    <p style="margin-top: 1rem; font-size: 1.2rem; opacity: 0.9;">Analyse des totaux annuels par école (Feuille Sheet4)</p>
</div>
""", unsafe_allow_html=True)

def clean_sheet4_data(df):
    """Nettoie et prépare les données de la feuille Sheet4"""
    
    # Renommer les colonnes pour uniformité
    rename_dict = {}
    for col in df.columns:
        col_str = str(col)
        
        if 'Région' in col_str:
            rename_dict[col] = 'Région'
        elif 'Ecole' in col_str or 'Ecole' in col_str:
            rename_dict[col] = 'Ecole'
        elif 'Nbre DP' in col_str:
            rename_dict[col] = 'Nbre DP total'
        elif 'Nbre enseign' in col_str:
            rename_dict[col] = 'Nbre enseignants total'
        elif 'Nbre Eleves' in col_str:
            rename_dict[col] = 'Nbre élèves total'
    
    df = df.rename(columns=rename_dict)
    
    # Nettoyer les données numériques
    numeric_columns = ['Nbre DP total', 'Nbre enseignants total', 'Nbre élèves total']
    
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Calculer des métriques supplémentaires
    # Ratio élèves/DP
    if 'Nbre élèves total' in df.columns and 'Nbre DP total' in df.columns:
        df['Ratio élèves/DP total'] = (df['Nbre élèves total'] / df['Nbre DP total']).round(1)
    
    # Ratio élèves/enseignants
    if 'Nbre élèves total' in df.columns and 'Nbre enseignants total' in df.columns:
        df['Ratio élèves/enseignants total'] = (df['Nbre élèves total'] / df['Nbre enseignants total']).round(1)
    
    # Ratio enseignants/DP
    if 'Nbre enseignants total' in df.columns and 'Nbre DP total' in df.columns:
        df['Ratio enseignants/DP total'] = (df['Nbre enseignants total'] / df['Nbre DP total']).round(1)
    
    # Calculer la charge par enseignant
    if 'Nbre élèves total' in df.columns and 'Nbre enseignants total' in df.columns:
        df['Charge par enseignant'] = df['Nbre élèves total'] / df['Nbre enseignants total']
    
    # Calculer l'efficacité DP (élèves par DP)
    if 'Nbre élèves total' in df.columns and 'Nbre DP total' in df.columns:
        df['Efficacité DP'] = df['Nbre élèves total'] / df['Nbre DP total']
    
    # Catégoriser les écoles par taille
    if 'Nbre élèves total' in df.columns:
        conditions = [
            df['Nbre élèves total'] >= 500,
            df['Nbre élèves total'] >= 300,
            df['Nbre élèves total'] >= 100,
            df['Nbre élèves total'] < 100
        ]
        choices = ['Très grande (≥500)', 'Grande (300-500)', 'Moyenne (100-300)', 'Petite (<100)']
        df['Catégorie taille'] = np.select(conditions, choices, default='Non définie')
    
    # Catégoriser par ratio élèves/DP
    if 'Ratio élèves/DP total' in df.columns:
        conditions = [
            df['Ratio élèves/DP total'] >= 60,
            df['Ratio élèves/DP total'] >= 40,
            df['Ratio élèves/DP total'] >= 20,
            df['Ratio élèves/DP total'] < 20
        ]
        choices = ['Très élevé (≥60)', 'Élevé (40-60)', 'Normal (20-40)', 'Faible (<20)']
        df['Catégorie ratio'] = np.select(conditions, choices, default='Non définie')
    
    # Calculer la densité (si on avait la superficie)
    # df['Densité élèves/m²'] = df['Nbre élèves total'] / df['Superficie totale']
    
    return df

def create_summary_statistics(df):
    """Crée des statistiques récapitulatives pour Sheet4"""
    
    stats = {}
    
    # Statistiques de base
    stats['Nombre d\'écoles'] = len(df)
    stats['Nombre de régions'] = df['Région'].nunique() if 'Région' in df.columns else 0
    
    # Totaux globaux
    if 'Nbre élèves total' in df.columns:
        stats['Total élèves'] = int(df['Nbre élèves total'].sum())
        stats['Moyenne élèves par école'] = df['Nbre élèves total'].mean().round(1)
        stats['Max élèves'] = int(df['Nbre élèves total'].max())
        stats['Min élèves'] = int(df['Nbre élèves total'].min())
    
    if 'Nbre enseignants total' in df.columns:
        stats['Total enseignants'] = int(df['Nbre enseignants total'].sum())
        stats['Moyenne enseignants par école'] = df['Nbre enseignants total'].mean().round(1)
    
    if 'Nbre DP total' in df.columns:
        stats['Total DP'] = int(df['Nbre DP total'].sum())
        stats['Moyenne DP par école'] = df['Nbre DP total'].mean().round(1)
    
    # Ratios moyens
    if 'Ratio élèves/DP total' in df.columns:
        stats['Ratio élèves/DP moyen'] = df['Ratio élèves/DP total'].mean().round(1)
        stats['Ratio élèves/DP max'] = df['Ratio élèves/DP total'].max().round(1)
        stats['Ratio élèves/DP min'] = df['Ratio élèves/DP total'].min().round(1)
    
    if 'Ratio élèves/enseignants total' in df.columns:
        stats['Ratio élèves/enseignants moyen'] = df['Ratio élèves/enseignants total'].mean().round(1)
    
    # Distribution par catégorie de taille
    if 'Catégorie taille' in df.columns:
        taille_counts = df['Catégorie taille'].value_counts()
        for cat, count in taille_counts.items():
            stats[f'Écoles {cat}'] = count
    
    # Distribution par catégorie de ratio
    if 'Catégorie ratio' in df.columns:
        ratio_counts = df['Catégorie ratio'].value_counts()
        for cat, count in ratio_counts.items():
            stats[f'Ratio {cat}'] = count
    
    # Statistiques par région
    if 'Région' in df.columns and 'Nbre élèves total' in df.columns:
        region_stats = df.groupby('Région').agg({
            'Nbre élèves total': ['sum', 'mean', 'count'],
            'Nbre enseignants total': 'sum',
            'Nbre DP total': 'sum'
        })
        
        for region in region_stats.index:
            stats[f'{region} - Nombre d\'écoles'] = int(region_stats.loc[region, ('Nbre élèves total', 'count')])
            stats[f'{region} - Total élèves'] = int(region_stats.loc[region, ('Nbre élèves total', 'sum')])
    
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
                    labels={x_variable: x_variable, y_variable: y_variable},
                    size='Nbre élèves total' if 'Nbre élèves total' in analysis_df.columns else None
                )
            else:
                fig = px.scatter(
                    analysis_df, 
                    x=x_variable, 
                    y=y_variable,
                    hover_data=['Ecole', 'Région'],
                    title=f"Nuage de points: {x_variable} vs {y_variable}",
                    labels={x_variable: x_variable, y_variable: y_variable},
                    size='Nbre élèves total' if 'Nbre élèves total' in analysis_df.columns else None
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
            if 'Nbre élèves total' in analysis_df.columns:
                fig = px.scatter(
                    analysis_df,
                    x=x_variable,
                    y=y_variable,
                    size='Nbre élèves total',
                    color=color_variable if color_variable and color_variable in analysis_df.columns else None,
                    hover_name='Ecole',
                    title=f"Graphique à bulles: {x_variable} vs {y_variable}",
                    size_max=60
                )
        
        elif graph_type == "Graphique en radar":
            if color_variable and color_variable in analysis_df.columns:
                # Moyenne par catégorie
                grouped = analysis_df.groupby(color_variable).agg({
                    x_variable: 'mean',
                    y_variable: 'mean'
                }).reset_index()
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatterpolar(
                    r=grouped[x_variable],
                    theta=grouped[color_variable],
                    fill='toself',
                    name=x_variable
                ))
                
                fig.add_trace(go.Scatterpolar(
                    r=grouped[y_variable],
                    theta=grouped[color_variable],
                    fill='toself',
                    name=y_variable
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, max(grouped[x_variable].max(), grouped[y_variable].max()) * 1.1]
                        )),
                    title=f"Comparaison de {x_variable} et {y_variable} par {color_variable} (Radar)"
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
        help="Le fichier doit contenir une feuille 'Sheet4' avec les totaux par école"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        try:
            # Lire uniquement la feuille Sheet4
            df = pd.read_excel(uploaded_file, sheet_name='Sheet4', engine='openpyxl')
            
            # Nettoyer les données
            df = clean_sheet4_data(df)
            
            # Afficher les informations sur la structure
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.success("✅ Fichier téléversé avec succès !")
            
            # Afficher la structure détectée
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_eleves = df['Nbre élèves total'].sum() if 'Nbre élèves total' in df.columns else 0
                st.markdown(f"""
                <div class="stat-card">
                    <h3>👥</h3>
                    <h2>{total_eleves:,}</h2>
                    <p>Élèves total</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                total_enseignants = df['Nbre enseignants total'].sum() if 'Nbre enseignants total' in df.columns else 0
                st.markdown(f"""
                <div class="stat-card">
                    <h3>👨‍🏫</h3>
                    <h2>{total_enseignants:,}</h2>
                    <p>Enseignants total</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                total_dp = df['Nbre DP total'].sum() if 'Nbre DP total' in df.columns else 0
                st.markdown(f"""
                <div class="stat-card">
                    <h3>🏫</h3>
                    <h2>{total_dp:,}</h2>
                    <p>DP total</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                ratio_moyen = df['Ratio élèves/DP total'].mean() if 'Ratio élèves/DP total' in df.columns else 0
                st.markdown(f"""
                <div class="stat-card">
                    <h3>📈</h3>
                    <h2>{ratio_moyen:.1f}</h2>
                    <p>Ratio moyen</p>
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
                        'Total écoles': f"{stats.get('Nombre d\'écoles', 0)}",
                        'Élèves/école': f"{stats.get('Moyenne élèves par école', 0):.0f}",
                        'Enseignants/école': f"{stats.get('Moyenne enseignants par école', 0):.1f}",
                        'Ratio élèves/DP': f"{stats.get('Ratio élèves/DP moyen', 0):.1f}"
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
                        # Distribution des élèves par école
                        if 'Nbre élèves total' in df.columns:
                            fig1 = px.histogram(
                                df, 
                                x='Nbre élèves total',
                                title="Distribution du nombre d'élèves par école",
                                nbins=20,
                                color_discrete_sequence=['#3B82F6']
                            )
                            fig1.update_layout(template="plotly_white", height=300,
                                             xaxis_title="Nombre d'élèves", yaxis_title="Nombre d'écoles")
                            st.plotly_chart(fig1, use_container_width=True)
                    
                    with col2:
                        # Diagramme en barres par région
                        if 'Région' in df.columns and 'Nbre élèves total' in df.columns:
                            region_totals = df.groupby('Région')['Nbre élèves total'].sum().sort_values(ascending=False)
                            fig2 = px.bar(
                                x=region_totals.index,
                                y=region_totals.values,
                                title="Total d'élèves par Région",
                                color=region_totals.values,
                                color_continuous_scale='Viridis'
                            )
                            fig2.update_layout(template="plotly_white", height=300, 
                                             xaxis_title="Région", yaxis_title="Nombre d'élèves")
                            st.plotly_chart(fig2, use_container_width=True)
                
                # Téléchargement des données nettoyées
                with st.expander("💾 Télécharger les données", expanded=False):
                    csv_data = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Télécharger les données nettoyées (CSV)",
                        data=csv_data,
                        file_name="donnees_totaux_ecoles_nettoyees.csv",
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
                            index=available_variables.index('Nbre élèves total') if 'Nbre élèves total' in available_variables else 0
                        )
                    
                    with col2:
                        y_variable = st.selectbox(
                            "Variable Y:",
                            options=available_variables,
                            index=available_variables.index('Ratio élèves/DP total') if 'Ratio élèves/DP total' in available_variables else 1
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
                                "Graphique à bulles",
                                "Graphique en radar"
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
                                    display_cols = [x_variable, y_variable]
                                    if color_variable:
                                        display_cols.append(color_variable)
                                    display_cols.extend(['Ecole', 'Région'])
                                    
                                    st.dataframe(
                                        analysis_df[display_cols].head(20),
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
                    
                    1. **Élèves vs Enseignants** : Relation entre le nombre d'élèves et d'enseignants
                    2. **Élèves vs Ratio élèves/DP** : Comment la taille influence le ratio
                    3. **Distribution par Région** : Comparer les totaux entre régions
                    4. **Ratio vs Taille école** : Comment les ratios varient avec la taille
                    5. **Enseignants vs DP** : Relation entre personnel et salles
                    
                    **Variables numériques disponibles :**
                    - Nbre élèves total, Nbre enseignants total, Nbre DP total
                    - Ratio élèves/DP total, Ratio élèves/enseignants total, Ratio enseignants/DP total
                    - Charge par enseignant, Efficacité DP
                    
                    **Variables catégorielles disponibles :**
                    - Région, Nom de l'école
                    - Catégorie taille, Catégorie ratio
                    
                    **Types de graphiques recommandés :**
                    - **Nuage de points** : Pour corrélations avec taille d'école
                    - **Box plot** : Pour comparer distributions entre catégories
                    - **Treemap** : Pour visualiser la hiérarchie par région/taille
                    - **Graphique à bulles** : Pour 3 dimensions (X, Y, taille école)
                    - **Heatmap** : Pour voir toutes les corrélations
                    - **Radar** : Pour comparaison multidimensionnelle
                    """)
            
            with tab3:
                st.markdown("## 🏆 Classements et Performances")
                
                # Classement par nombre d'élèves
                with st.expander("🥇 Classement par Nombre d'Élèves", expanded=True):
                    if 'Nbre élèves total' in df.columns and 'Ecole' in df.columns:
                        ranked_df = df.sort_values('Nbre élèves total', ascending=False)
                        ranked_df = ranked_df[['Ecole', 'Région', 'Nbre élèves total', 
                                              'Nbre enseignants total', 'Nbre DP total', 'Ratio élèves/DP total']]
                        ranked_df['Rang'] = range(1, len(ranked_df) + 1)
                        
                        st.dataframe(
                            ranked_df.head(10),
                            use_container_width=True,
                            column_config={
                                "Rang": st.column_config.NumberColumn(format="%d"),
                                "Nbre élèves total": st.column_config.NumberColumn(format="%d"),
                                "Nbre enseignants total": st.column_config.NumberColumn(format="%d"),
                                "Nbre DP total": st.column_config.NumberColumn(format="%d"),
                                "Ratio élèves/DP total": st.column_config.NumberColumn(format="%.1f")
                            }
                        )
                        
                        # Graphique du top 10
                        top10 = ranked_df.head(10)
                        fig = px.bar(
                            top10,
                            x='Ecole',
                            y='Nbre élèves total',
                            color='Région',
                            title="Top 10 des écoles par nombre d'élèves"
                        )
                        fig.update_layout(template="plotly_white", xaxis_tickangle=45)
                        st.plotly_chart(fig, use_container_width=True)
                
                # Classement par ratio élèves/DP
                with st.expander("📈 Classement par Ratio Élèves/DP", expanded=False):
                    if 'Ratio élèves/DP total' in df.columns and 'Ecole' in df.columns:
                        ratio_ranked = df.sort_values('Ratio élèves/DP total', ascending=False)
                        ratio_ranked = ratio_ranked[['Ecole', 'Région', 'Ratio élèves/DP total', 
                                                    'Nbre élèves total', 'Nbre DP total']]
                        ratio_ranked['Rang'] = range(1, len(ratio_ranked) + 1)
                        
                        st.dataframe(
                            ratio_ranked.head(10),
                            use_container_width=True,
                            column_config={
                                "Rang": st.column_config.NumberColumn(format="%d"),
                                "Ratio élèves/DP total": st.column_config.NumberColumn(format="%.1f"),
                                "Nbre élèves total": st.column_config.NumberColumn(format="%d"),
                                "Nbre DP total": st.column_config.NumberColumn(format="%d")
                            }
                        )
                
                # Analyse par catégorie de taille
                with st.expander("🏢 Analyse par Catégorie de Taille", expanded=False):
                    if 'Catégorie taille' in df.columns:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Statistiques par catégorie
                            taille_stats = df.groupby('Catégorie taille').agg({
                                'Nbre élèves total': ['mean', 'count', 'sum'],
                                'Ratio élèves/DP total': 'mean'
                            }).round(1)
                            taille_stats.columns = ['Élèves moyen', 'Nombre écoles', 'Total élèves', 'Ratio moyen']
                            
                            st.dataframe(taille_stats, use_container_width=True)
                        
                        with col2:
                            # Diagramme circulaire
                            if len(taille_stats) > 0:
                                fig = px.pie(
                                    values=taille_stats['Nombre écoles'],
                                    names=taille_stats.index,
                                    title="Répartition des écoles par taille"
                                )
                                st.plotly_chart(fig, use_container_width=True)
                
                # Analyse comparative
                with st.expander("📊 Analyse Comparative", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Écoles avec plus de 500 élèves
                        grandes_ecoles = df[df['Nbre élèves total'] >= 500]
                        if len(grandes_ecoles) > 0:
                            st.metric("Écoles ≥500 élèves", len(grandes_ecoles))
                            st.metric("Moyenne ratio grandes écoles", 
                                    f"{grandes_ecoles['Ratio élèves/DP total'].mean():.1f}")
                    
                    with col2:
                        # Écoles avec ratio élevé
                        ratio_eleve = df[df['Ratio élèves/DP total'] >= 60]
                        if len(ratio_eleve) > 0:
                            st.metric("Écoles ratio ≥60", len(ratio_eleve))
                            st.metric("Moyenne élèves ratio élevé", 
                                    f"{ratio_eleve['Nbre élèves total'].mean():.0f}")
        
        except Exception as e:
            st.error(f"❌ Erreur lors de la lecture du fichier : {str(e)}")
            st.markdown('<div class="warning-box">', unsafe_allow_html=True)
            st.info("""
            **Conseils de dépannage :**
            1. Vérifiez que le fichier contient bien une feuille nommée 'Sheet4'
            2. Ouvrez le fichier dans Excel pour vérifier sa structure
            3. Assurez-vous que les colonnes 'Région' et 'Nom de l\'école' existent
            4. Vérifiez les colonnes numériques : Nbre DP, Nbre enseign, Nbre Eleves
            """)
            st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # Afficher un exemple de structure attendue
        st.info("👆 Veuillez téléverser votre fichier Excel FIFA project.xlsx")
        
        # Exemple de structure
        with st.expander("🧾 Structure attendue de la feuille Sheet4", expanded=True):
            st.markdown("""
            **La feuille Sheet4 doit contenir au minimum ces colonnes :**
            
            1. **Région** : Région administrative
            2. **Nom de l'école** : Nom de l'établissement
            3. **Nbre DP** : Nombre total de salles de classe (DP)
            4. **Nbre enseign** : Nombre total d'enseignants
            5. **Nbre Eleves** : Nombre total d'élèves (toutes années confondues)
            
            **Métriques calculées automatiquement :**
            - Ratio élèves/DP total
            - Ratio élèves/enseignants total
            - Ratio enseignants/DP total
            - Charge par enseignant
            - Efficacité DP
            - Catégorie taille (basée sur nombre d'élèves)
            - Catégorie ratio (basée sur ratio élèves/DP)
            
            **Analyse fournie :**
            - Totaux globaux et par région
            - Distribution des tailles d'écoles
            - Classements par performance
            - Corrélations entre variables
            - Graphiques statistiques binaires
            """)

if __name__ == "__main__":
    main()