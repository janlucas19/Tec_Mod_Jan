import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np

##################################################

# Datos para el modelo matemático
x = np.linspace(0, 10, 100)
y = x**2  # Función cuadrática como ejemplo

# Crear un scatter plot
trace = go.Scatter(
    x=x,
    y=y,
    mode='lines+markers',
    line=dict(
        dash='dot',
        color='black',
        width=2
    ),
    marker=dict(
        color='red',
        symbol='circle',
        size=6
    ),
    name='y = x²',
    hovertemplate='x: %{x:.2f}<br>y: %{y:.2f}<extra></extra>'
)

# Crear la figura
fig = go.Figure(data=trace)

fig.update_layout(
    title=dict(
        text='<b>Ejemplo de Modelamiento Matemático</b>',
        font=dict(
            size=20,
            color='darkblue'
        ),
        x=0.5,
        y=0.93
    ),
    xaxis_title='Variable x',
    yaxis_title='Función y(x)',
    margin=dict(l=40, r=40, t=50, b=40),
    paper_bgcolor='lightgray',
    plot_bgcolor='white',
    font=dict(
        family='Arial',
        size=11,
        color='black'
    )
)

fig.update_xaxes(
    showgrid=True, gridwidth=1, gridcolor='lightgray',
    zeroline=True, zerolinewidth=2, zerolinecolor='blue',
    showline=True, linecolor='black', linewidth=2, mirror=True,
)

fig.update_yaxes(
    showgrid=True, gridwidth=1, gridcolor='lightgray',
    zeroline=True, zerolinewidth=2, zerolinecolor='blue',
    showline=True, linecolor='black', linewidth=2, mirror=True,
)

##################################################

dash.register_page(__name__, path='/', name='Inicio')

layout = html.Div(children=[
    # Contenedor izquierdo
    html.Div(children=[
        html.H2("Técnicas de Modelamiento Matemático", className="title"),

        dcc.Markdown("""
        Bienvenido(a) al curso de Técnicas de Modelamiento Matemático, donde aprenderás a representar 
        fenómenos del mundo real mediante herramientas matemáticas para analizarlos y proponer soluciones efectivas.
        
        El curso te permitirá formular, analizar y validar modelos matemáticos, aplicando métodos algebraicos, 
        analíticos y computacionales. A través de ejemplos reales, desarrollarás la capacidad de conectar la 
        teoría matemática con problemas prácticos en campos como la ingeniería, la economía o la biología.
        """, mathjax=True),

        dcc.Markdown("""
        El **objetivo principal** es que adquieras una visión integral del proceso de modelamiento: 
        desde la comprensión del problema hasta la interpretación y comunicación de resultados.
        
        En este curso exploraremos diferentes tipos de modelos matemáticos, incluyendo:
        - Modelos lineales y no lineales
        - Modelos de optimización
        - Modelos basados en ecuaciones diferenciales
        - Modelos estadísticos y probabilísticos
        """, mathjax=True),
    ], className="content left"),

    # Contenedor derecho
    html.Div(children=[
        html.H2("Ejemplo Gráfico", className="title"),

        dcc.Graph(
            figure=fig,
            style={'height': '400px', 'width': '100%'},
        ),
        
        dcc.Markdown("""
        **Gráfico de ejemplo:** Esta gráfica muestra una función cuadrática $y = x^2$, 
        que representa un modelo matemático simple pero fundamental en muchas aplicaciones.
        """, mathjax=True)
    ], className="content right")
], className="page-container")
