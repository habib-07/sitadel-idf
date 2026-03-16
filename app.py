import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

# --- GESTION DES CHEMINS AUTOMATIQUE ---
# Cette partie permet de trouver le dossier 'processed' peu importe l'endroit où le code est lancé
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path_total = os.path.join(BASE_DIR, "processed", "sitadel_idf_total.parquet")
path_dept  = os.path.join(BASE_DIR, "processed", "sitadel_idf_dept.parquet")

# Chargement des données
sitadel_idf  = pd.read_parquet(path_total)
sitadel_dept = pd.read_parquet(path_dept)

# Conversion forcée en types Python standards pour éviter l'erreur numpy.int32
sitadel_idf["annee"]  = sitadel_idf["annee"].astype(float).astype(int)
sitadel_dept["annee"] = sitadel_dept["annee"].astype(float).astype(int)

# Préparation des listes pour les filtres
annees = sorted([int(a) for a in sitadel_idf["annee"].unique()])
depts  = sorted([str(d) for d in sitadel_dept["dept"].unique()])

# Paramètres visuels
palette = {
    "Tous":"#185FA5","Collectif":"#A32D2D",
    "Indiv_pur":"#EF9F27","Indiv_groupe":"#1D9E75","Residence":"#7F77DD"
}
dept_labels = {
    "75":"Paris","77":"Seine-et-Marne","78":"Yvelines",
    "91":"Essonne","92":"Hauts-de-Seine",
    "93":"Seine-Saint-Denis","94":"Val-de-Marne","95":"Val-d Oise"
}

# --- INITIALISATION DE L'APP ---
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server  # <--- INDISPENSABLE POUR RENDER (GUNICORN)

# Options des Dropdowns
annee_opts = [{"label": str(a), "value": int(a)} for a in annees]
dept_opts  = [{"label": f"{dept_labels.get(str(d),d)} ({d})", "value": str(d)} for d in depts]

# --- LAYOUT (STRUCTURE) ---
sidebar = dbc.Card([
    html.H5("Filtres"),
    html.Hr(),
    html.Label("Année début"),
    dcc.Dropdown(id="annee_min", options=annee_opts, value=int(annees[0]), clearable=False),
    html.Br(),
    html.Label("Année fin"),
    dcc.Dropdown(id="annee_max", options=annee_opts, value=int(annees[-1]), clearable=False),
    html.Br(),
    html.Label("Départements"),
    dcc.Dropdown(id="filtre_dept", options=dept_opts, value=depts,
                 multi=True, clearable=False)
], body=True)

tabs = dbc.Tabs([
    dbc.Tab(label="Vue d'ensemble", children=[
        dbc.Row([
            dbc.Col(dbc.Card(id="kpi_aut",   color="primary", inverse=True), width=3),
            dbc.Col(dbc.Card(id="kpi_com",   color="danger",  inverse=True), width=3),
            dbc.Col(dbc.Card(id="kpi_ratio", color="warning", inverse=True), width=3),
            dbc.Col(dbc.Card(id="kpi_evol",  color="success", inverse=True), width=3),
        ], className="mt-3 mb-3"),
        dbc.Row([
            dbc.Col(dcc.Graph(id="p_aut_com"), width=8),
            dbc.Col(dcc.Graph(id="p_pie"),     width=4),
        ])
    ]),
    dbc.Tab(label="Types logement", children=[
        dbc.Row([dbc.Col(dcc.Graph(id="p_types_evol"), width=12)], className="mt-3"),
        dbc.Row([dbc.Col(dcc.Graph(id="p_types_part"), width=12)])
    ]),
    dbc.Tab(label="Par département", children=[
        dbc.Row([
            dbc.Col(dcc.Graph(id="p_dept_aut"), width=6),
            dbc.Col(dcc.Graph(id="p_dept_com"), width=6),
        ], className="mt-3")
    ]),
])

app.layout = dbc.Container([
    dbc.Row([html.H2("SITADEL - Construction en Île-de-France",
                     className="text-primary my-3")]),
    dbc.Row([
        dbc.Col(sidebar, width=2),
        dbc.Col(tabs,    width=10)
    ])
], fluid=True)

# --- LOGIQUE DE FILTRAGE ---
def filtre(df, amin, amax, depts_sel):
    return df[
        (df["annee"] >= int(amin)) &
        (df["annee"] <= int(amax)) &
        (df["dept"].astype(str).isin([str(d) for d in depts_sel]))
    ]

# --- CALLBACKS (INTERACTIVITÉ) ---

@app.callback(
    Output("kpi_aut","children"), Output("kpi_com","children"),
    Output("kpi_ratio","children"), Output("kpi_evol","children"),
    Input("annee_min","value"), Input("annee_max","value"), Input("filtre_dept","value")
)
def update_kpis(amin, amax, depts_sel):
    df = filtre(sitadel_dept, amin, amax, depts_sel)
    df_tous = df[df["type_lgt"]=="Tous"]
    
    aut   = int(df_tous["log_aut"].sum())
    com   = int(df_tous["log_com"].sum())
    ratio = round(com/aut*100, 1) if aut > 0 else 0
    
    last = int(amax)
    aut_l = int(df_tous[df_tous["annee"] == last]["log_aut"].sum())
    aut_p = int(df_tous[df_tous["annee"] == (last - 1)]["log_aut"].sum())
    
    evol = round((aut_l - aut_p) / aut_p * 100, 1) if aut_p > 0 else 0
    sign = "+" if evol > 0 else ""
    
    def kpi(t, v):
        return dbc.CardBody([html.H6(t), html.H3(str(v))])
        
    return (kpi("Autorisations", f"{aut:,}".replace(",", " ")),
            kpi("Mises en chantier", f"{com:,}".replace(",", " ")),
            kpi("Taux réalisation", f"{ratio}%"),
            kpi(f"Évol {last}/{last-1}", f"{sign}{evol}%"))

@app.callback(Output("p_aut_com","figure"),
              Input("annee_min","value"), Input("annee_max","value"), Input("filtre_dept","value"))
def p_aut_com(amin, amax, depts_sel):
    df = filtre(sitadel_dept, amin, amax, depts_sel)
    df = df[df["type_lgt"]=="Tous"].groupby("annee")[["log_aut","log_com"]].sum().reset_index()
    
    fig = go.Figure()
    fig.add_bar(x=df["annee"], y=df["log_aut"], name="Autorisations", marker_color="#185FA5")
    fig.add_scatter(x=df["annee"], y=df["log_com"], name="Mises en chantier",
                    mode="lines+markers", line=dict(color="#A32D2D", width=2))
    
    fig.update_layout(title="Autorisations vs mises en chantier",
                      template="plotly_white", legend=dict(orientation="h"))
    return fig

@app.callback(Output("p_pie","figure"),
              Input("annee_min","value"), Input("annee_max","value"), Input("filtre_dept","value"))
def p_pie(amin, amax, depts_sel):
    df = filtre(sitadel_dept, amax, amax, depts_sel)
    df = df[df["type_lgt"]!="Tous"].groupby("type_lgt")["log_aut"].sum().reset_index()
    
    fig = px.pie(df, names="type_lgt", values="log_aut",
                 color="type_lgt", color_discrete_map=palette,
                 title=f"Répartition par type ({int(amax)})")
    fig.update_layout(template="plotly_white")
    return fig

@app.callback(Output("p_types_evol","figure"),
              Input("annee_min","value"), Input("annee_max","value"), Input("filtre_dept","value"))
def p_types_evol(amin, amax, depts_sel):
    df = filtre(sitadel_dept, amin, amax, depts_sel)
    df = df[df["type_lgt"]!="Tous"].groupby(["annee","type_lgt"])["log_aut"].sum().reset_index()
    
    fig = px.line(df, x="annee", y="log_aut", color="type_lgt",
                  color_discrete_map=palette, markers=True,
                  title="Évolution par type",
                  labels={"log_aut":"Logements","annee":"Année","type_lgt":"Type"})
    fig.update_layout(template="plotly_white")
    return fig

@app.callback(Output("p_types_part","figure"),
              Input("annee_min","value"), Input("annee_max","value"), Input("filtre_dept","value"))
def p_types_part(amin, amax, depts_sel):
    df = filtre(sitadel_dept, amin, amax, depts_sel)
    df = df[df["type_lgt"]!="Tous"].groupby(["annee","type_lgt"])["log_aut"].sum().reset_index()
    
    fig = px.bar(df, x="annee", y="log_aut", color="type_lgt",
                 barmode="stack", color_discrete_map=palette,
                 title="Répartition par type (%)",
                 labels={"log_aut":"Logements","annee":"Année","type_lgt":"Type"})
    fig.update_layout(template="plotly_white", barnorm="percent", yaxis_title="Part (%)")
    return fig

@app.callback(Output("p_dept_aut","figure"), Output("p_dept_com","figure"),
              Input("annee_min","value"), Input("annee_max","value"), Input("filtre_dept","value"))
def p_dept(amin, amax, depts_sel):
    df = filtre(sitadel_dept, amin, amax, depts_sel)
    df = df[df["type_lgt"]=="Tous"].groupby(["annee","dept_lib"])[["log_aut","log_com"]].sum().reset_index()
    
    fa = px.bar(df, x="annee", y="log_aut", color="dept_lib",
                title="Autorisations par département",
                labels={"log_aut":"Logements","annee":"Année","dept_lib":"Dép."})
    fa.update_layout(template="plotly_white")
    
    fc = px.bar(df, x="annee", y="log_com", color="dept_lib",
                title="Mises en chantier par département",
                labels={"log_com":"Logements","annee":"Année","dept_lib":"Dép."})
    fc.update_layout(template="plotly_white")
    
    return fa, fc

# --- DÉMARRAGE ---
if __name__ == "__main__":
    app.run(debug=True, port=8051)