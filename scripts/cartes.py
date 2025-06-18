from IPython.display import HTML, display
import warnings
import folium
import html

def generer_carte_stations(points, variables=None):
    """
    Génère une carte interactive Folium affichant les stations météo.

    Chaque station est représentée par un point (cercle rouge) positionné selon sa latitude et sa longitude.
    Le popup associé à chaque point affiche la moyenne des variables spécifiées (ex. température, humidité…).

    Paramètres :
    - points : liste de dictionnaires contenant les clés 'lat', 'lon', 'nom', et les variables numériques à afficher.
    - variables : liste de chaînes correspondant aux noms des variables à afficher dans le popup.
                 Si None, seule la température ('T') est affichée.

    Retour :
    - Un objet folium.Map prêt à être affiché dans un notebook.
    """
    if variables is None:
        variables = ["T"]

    m = folium.Map(location=[47, 1.6], zoom_start=6)

    for p in points:
        popup_content = f"<strong>Station {p['nom']}</strong><br>"
        for var in variables:
            if var in p:
                popup_content += f"{var} moyenne : {p[var]:.2f}<br>"

        folium.CircleMarker(
            location=[p["lat"], p["lon"]],
            radius=5,
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.6,
            popup=folium.Popup(popup_content, max_width=250)
        ).add_to(m)

    return m

def afficher_carte_iframe(carte, width="100%", height="500px"):
    """
    Affiche une carte Folium dans une iframe personnalisée avec style CSS défini.
    
    :param folium_map: objet folium.Map
    :param width: largeur CSS (ex: "100%", "800px", "40%")
    :param height: hauteur CSS (ex: "500px", "600px")
    """
    html_code = carte.get_root().render()
    escaped_html = html.escape(html_code)
    iframe_html = f'<iframe srcdoc="{escaped_html}" style="width:{width}; height:{height}; border:none;"></iframe>'
    warnings.filterwarnings("ignore", message="Consider using IPython.display.IFrame instead")
    display(HTML(iframe_html))