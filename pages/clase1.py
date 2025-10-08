import dash
from dash import html, dcc

dash.register_page(__name__, path='/clase1', name='Constante de carga k')

layout = html.Div([
    html.H2("Clase 1: La constante de carga eléctrica k"),
    
    html.P("""
        La constante de carga eléctrica, también conocida como constante de Coulomb (k),
        es un parámetro fundamental en la Ley de Coulomb, que describe la fuerza entre dos
        cargas eléctricas puntuales.
    """),
    
    html.Div([
        html.P("Ley de Coulomb:"),
        html.P("F = k * (|q₁ * q₂|) / r²"),
    ], className='formula'),

    html.P("""
        Donde:
        - F es la fuerza eléctrica entre las cargas.
        - q₁ y q₂ son las magnitudes de las cargas.
        - r es la distancia entre ellas.
        - k es la constante de Coulomb, cuyo valor es aproximadamente:
          k = 8.99 × 10⁹ N·m²/C².
    """),
    
    html.P("""
        En esta clase analizaremos cómo varía la fuerza al modificar las cargas y la distancia.
    """),
    
    html.Div([
        dcc.Graph(
            figure={
                "data": [{
                    "x": [0.5, 1, 2, 3, 4, 5],
                    "y": [8.99e9/(r**2) for r in [0.5, 1, 2, 3, 4, 5]],
                    "type": "line",
                    "name": "Fuerza (N)"
                }],
                "layout": {
                    "title": "Variación de la fuerza con la distancia (q₁=q₂=1 C)",
                    "xaxis": {"title": "Distancia (m)"},
                    "yaxis": {"title": "Fuerza (N)"}
                }
            }
        )
    ], className='graph-container')
])

