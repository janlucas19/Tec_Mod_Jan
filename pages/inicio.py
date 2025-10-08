import dash
from dash import html

dash.register_page(__name__, path='/', name='Inicio')

layout = html.Div([
    html.H2("Bienvenido al curso de Técnicas de Modelamiento Matemático"),
    html.P("""
        En esta plataforma exploraremos distintos conceptos aplicados al modelamiento,
        comenzando por la constante de carga eléctrica y su importancia en los sistemas físicos.
    """),
    html.P("Selecciona una página del menú superior para continuar.")
])
