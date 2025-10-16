import dash
from dash import html, dcc, Input, Output, callback
import plotly.graph_objects as go
import numpy as np

dash.register_page(__name__, path='/modelo-interactivo', name='Modelo Interactivo')

# Layout de la página
layout = html.Div(children=[
    html.H1("Modelo de Crecimiento Poblacional", style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px'}),
    
    # Contenedor principal - FLEXBOX para lado a lado
    html.Div(children=[
        # Columna izquierda - Parámetros del modelo
        html.Div(children=[
            html.H2("Parámetros del modelo", style={
                'color': '#2c3e50', 
                'marginBottom': '20px',
                'textAlign': 'center'
            }),
            
            # Población inicial
            html.Div([
                html.Label("Población inicial P(0):", style={
                    'fontWeight': 'bold', 
                    'color': '#2c3e50',
                    'marginBottom': '8px',
                    'display': 'block'
                }),
                dcc.Input(
                    id='poblacion-inicial',
                    type='number',
                    value=100,
                    min=1,
                    max=1000,
                    style={
                        'width': '100%',
                        'padding': '10px',
                        'border': '1px solid #bdc3c7',
                        'borderRadius': '4px',
                        'fontSize': '14px'
                    }
                )
            ], style={'marginBottom': '20px'}),
            
            # Tasa de crecimiento
            html.Div([
                html.Label("Tasa de crecimiento (r):", style={
                    'fontWeight': 'bold', 
                    'color': '#2c3e50',
                    'marginBottom': '8px',
                    'display': 'block'
                }),
                dcc.Input(
                    id='tasa-crecimiento',
                    type='number',
                    value=0.04,
                    min=0.01,
                    max=1.0,
                    step=0.01,
                    style={
                        'width': '100%',
                        'padding': '10px',
                        'border': '1px solid #bdc3c7',
                        'borderRadius': '4px',
                        'fontSize': '14px'
                    }
                )
            ], style={'marginBottom': '20px'}),
            
            # Capacidad de carga
            html.Div([
                html.Label("Capacidad de carga (K):", style={
                    'fontWeight': 'bold', 
                    'color': '#2c3e50',
                    'marginBottom': '8px',
                    'display': 'block'
                }),
                dcc.Input(
                    id='capacidad-carga',
                    type='number',
                    value=750,
                    min=100,
                    max=5000,
                    step=50,
                    style={
                        'width': '100%',
                        'padding': '10px',
                        'border': '1px solid #bdc3c7',
                        'borderRadius': '4px',
                        'fontSize': '14px'
                    }
                )
            ], style={'marginBottom': '20px'}),
            
            # Tiempo máximo
            html.Div([
                html.Label("Tiempo máximo (t):", style={
                    'fontWeight': 'bold', 
                    'color': '#2c3e50',
                    'marginBottom': '8px',
                    'display': 'block'
                }),
                dcc.Input(
                    id='tiempo-maximo',
                    type='number',
                    value=100,
                    min=10,
                    max=500,
                    step=10,
                    style={
                        'width': '100%',
                        'padding': '10px',
                        'border': '1px solid #bdc3c7',
                        'borderRadius': '4px',
                        'fontSize': '14px'
                    }
                )
            ], style={'marginBottom': '20px'}),
            
            # Información adicional
            html.Div([
                html.Small("Los cambios se aplican automáticamente", style={
                    'color': '#7f8c8d',
                    'fontStyle': 'italic',
                    'textAlign': 'center',
                    'display': 'block'
                })
            ])
            
        ], style={
            'width': '30%', 
            'display': 'inline-block',
            'verticalAlign': 'top',
            'padding': '25px',
            'backgroundColor': '#f8f9fa',
            'borderRadius': '8px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'marginRight': '2%',
            'float': 'left'  # Fuerza el float a la izquierda
        }),
        
        # Columna derecha - Gráfica
        html.Div(children=[
            html.H2("Gráfica", style={
                'color': '#2c3e50',
                'marginBottom': '20px',
                'textAlign': 'center'
            }),
            
            dcc.Graph(
                id='model-graph',
                style={'height': '500px', 'width': '100%'}
            ),
            
        ], style={
            'width': '65%', 
            'display': 'inline-block',
            'verticalAlign': 'top',
            'padding': '25px',
            'backgroundColor': 'white',
            'borderRadius': '8px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'float': 'left',  # Fuerza el float a la izquierda
            'marginLeft': '2%'
        })
    ], style={
        'padding': '20px',
        'maxWidth': '1400px',
        'margin': '0 auto',
        'display': 'block',
        'overflow': 'hidden'  # Importantísimo para contener los floats
    }),
    
    # Información del modelo (debajo de ambas columnas)
    html.Div(id='info-modelo', style={
        'textAlign': 'center', 
        'fontSize': '14px', 
        'color': '#7f8c8d',
        'marginTop': '30px',
        'padding': '15px',
        'backgroundColor': '#ecf0f1',
        'borderRadius': '5px',
        'border': '1px solid #bdc3c7',
        'maxWidth': '1400px',
        'margin': '30px auto',
        'clear': 'both'  # Limpia los floats
    })
])

# Callback para actualizar la gráfica (el mismo que antes)
@callback(
    [Output('model-graph', 'figure'),
     Output('info-modelo', 'children')],
    [Input('poblacion-inicial', 'value'),
     Input('tasa-crecimiento', 'value'),
     Input('capacidad-carga', 'value'),
     Input('tiempo-maximo', 'value')]
)
def update_graph(P0, r, K, t_max):
    # Valores por defecto si hay algún error
    if P0 is None: P0 = 100
    if r is None: r = 0.04
    if K is None: K = 750
    if t_max is None: t_max = 100
    
    # Generar datos de tiempo
    t = np.linspace(0, t_max, 200)
    
    # Modelo logístico
    # Ecuación: P(t) = K / (1 + ((K - P0)/P0) * exp(-r*t))
    P = K / (1 + ((K - P0) / P0) * np.exp(-r * t))
    
    # Crear la gráfica
    fig = go.Figure()
    
    # Línea principal de la población
    fig.add_trace(go.Scatter(
        x=t,
        y=P,
        mode='lines',
        line=dict(color='#3498db', width=4),
        name='Población P(t)',
        hovertemplate='Tiempo: %{x:.1f}<br>Población: %{y:.1f}<extra></extra>'
    ))
    
    # Línea de capacidad de carga
    fig.add_trace(go.Scatter(
        x=t,
        y=[K] * len(t),
        mode='lines',
        line=dict(color='#e74c3c', width=2, dash='dash'),
        name=f'Capacidad de carga K = {K}'
    ))
    
    # Línea de población inicial
    fig.add_trace(go.Scatter(
        x=t,
        y=[P0] * len(t),
        mode='lines',
        line=dict(color='#2ecc71', width=2, dash='dash'),
        name=f'Población inicial P(0) = {P0}'
    ))
    
    fig.update_layout(
        title=dict(
            text='<b>Crecimiento Poblacional - Modelo Logístico</b>',
            font=dict(size=16, color='#2c3e50'),
            x=0.5
        ),
        xaxis_title='Tiempo (t)',
        yaxis_title='Población P(t)',
        margin=dict(l=60, r=40, t=60, b=60),
        paper_bgcolor='white',
        plot_bgcolor='white',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.02,
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#bdc3c7',
            borderwidth=1
        )
    )
    
    fig.update_xaxes(
        showgrid=True,
        gridcolor='#ecf0f1',
        zeroline=True,
        zerolinecolor='#bdc3c7',
        showline=True,
        linecolor='#bdc3c7'
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridcolor='#ecf0f1',
        zeroline=True,
        zerolinecolor='#bdc3c7',
        showline=True,
        linecolor='#bdc3c7',
        range=[0, K * 1.1]
    )
    
    # Información del modelo
    info_text = f"Modelo Logístico: P(t) = K / [1 + ((K - P₀)/P₀) · e^(-r·t)] | P₀ = {P0}, r = {r}, K = {K}"
    
    return fig, info_text