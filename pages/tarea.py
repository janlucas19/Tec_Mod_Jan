import dash
from dash import html, dcc, Input, Output, callback
import plotly.graph_objects as go
import numpy as np

dash.register_page(__name__, path='/modelo-epidemiologico', name='Modelo Epidemiológico')

# Layout de la página
layout = html.Div(children=[
    html.H2("Modelo Epidemiológico SIR", style={'textAlign': 'center', 'color': 'darkred', 'marginBottom': '30px'}),
    
    # Contenedor principal
    html.Div(children=[
        # Panel de controles izquierdo
        html.Div(children=[
            html.H3("Parámetros del Modelo", style={'color': 'darkred', 'marginBottom': '20px'}),
            
            # Población total
            html.Div([
                html.Label("Población total (N):", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.Input(
                    id='epidemia-poblacion-total',
                    type='number',
                    value=1000,
                    min=100,
                    max=100000,
                    style={'width': '100%', 'padding': '8px', 'marginBottom': '15px'}
                )
            ]),
            
            # Infectados iniciales
            html.Div([
                html.Label("Infectados iniciales (I₀):", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.Input(
                    id='epidemia-infectados-iniciales',
                    type='number',
                    value=1,
                    min=1,
                    max=100,
                    style={'width': '100%', 'padding': '8px', 'marginBottom': '15px'}
                )
            ]),
            
            # Tasa de contagio
            html.Div([
                html.Label("Tasa de contagio (β):", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.Input(
                    id='epidemia-tasa-contagio',
                    type='number',
                    value=0.3,
                    min=0.01,
                    max=1.0,
                    step=0.01,
                    style={'width': '100%', 'padding': '8px', 'marginBottom': '15px'}
                ),
                html.Small("Probabilidad de contagio por contacto", style={'color': '#666'})
            ]),
            
            # Tasa de recuperación
            html.Div([
                html.Label("Tasa de recuperación (γ):", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.Input(
                    id='epidemia-tasa-recuperacion',
                    type='number',
                    value=0.1,
                    min=0.01,
                    max=1.0,
                    step=0.01,
                    style={'width': '100%', 'padding': '8px', 'marginBottom': '15px'}
                ),
                html.Small("1/γ = días promedio de enfermedad", style={'color': '#666'})
            ]),
            
            # Tiempo máximo
            html.Div([
                html.Label("Días a simular:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.Input(
                    id='epidemia-tiempo-maximo',
                    type='number',
                    value=100,
                    min=10,
                    max=365,
                    style={'width': '100%', 'padding': '8px', 'marginBottom': '15px'}
                )
            ]),
            
            # Número básico de reproducción
            html.Div([
                html.Label("R₀ calculado:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.Input(
                    id='epidemia-r0',
                    type='number',
                    value=3.0,
                    disabled=True,
                    style={'width': '100%', 'padding': '8px', 'marginBottom': '15px', 'backgroundColor': '#f0f0f0'}
                ),
                html.Small("R₀ = β/γ", style={'color': '#666'})
            ])
            
        ], style={
            'width': '30%', 
            'display': 'inline-block',
            'verticalAlign': 'top',
            'padding': '25px',
            'backgroundColor': '#fff5f5',
            'borderRadius': '10px',
            'marginRight': '20px',
            'boxShadow': '0 2px 5px rgba(0,0,0,0.1)'
        }),
        
        # Panel de gráfico derecho
        html.Div(children=[
            html.H3("Evolución de la Epidemia", style={'color': 'darkred', 'marginBottom': '20px'}),
            
            dcc.Graph(
                id='epidemia-model-graph',
                style={'height': '400px', 'width': '100%'}
            ),
            
            html.Div(id='epidemia-info-modelo', style={
                'textAlign': 'center', 
                'fontSize': '14px', 
                'marginTop': '20px',
                'padding': '15px',
                'backgroundColor': '#ffe6e6',
                'borderRadius': '8px',
                'border': '1px solid #ffcccc'
            })
            
        ], style={
            'width': '65%', 
            'display': 'inline-block',
            'verticalAlign': 'top',
            'padding': '25px',
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'boxShadow': '0 2px 5px rgba(0,0,0,0.1)'
        })
    ], style={'padding': '20px'}),
    
    # Información adicional
    html.Div([
        html.Hr(style={'margin': '30px 0'}),
        html.Div([
            html.H4("🦠 Información del Modelo SIR", style={'color': 'darkred'}),
            html.P("""
            El modelo SIR divide la población en tres grupos:
            """),
            html.Ul([
                html.Li("🇸 Susceptibles: Personas que pueden contraer la enfermedad"),
                html.Li("🦠 Infectados: Personas que tienen la enfermedad y pueden contagiar"),
                html.Li("✅ Recuperados: Personas que se han recuperado y son inmunes")
            ]),
            html.P("""
            Ecuaciones diferenciales del modelo:
            """),
            html.Ul([
                html.Li("dS/dt = -β·S·I/N"),
                html.Li("dI/dt = β·S·I/N - γ·I"),
                html.Li("dR/dt = γ·I")
            ]),
            html.P("""
            Donde R₀ = β/γ es el número básico de reproducción. Si R₀ > 1, la epidemia crece.
            """)
        ], style={'padding': '20px', 'backgroundColor': '#fff0f0', 'borderRadius': '8px'})
    ])
])

# Función para resolver el modelo SIR usando el método de Euler
def resolver_sir_euler(N, I0, beta, gamma, t_max):
    # Condiciones iniciales
    S = [N - I0]  # Susceptibles iniciales
    I = [I0]      # Infectados iniciales
    R = [0]       # Recuperados iniciales
    
    # Resolver usando el método de Euler
    for t in range(1, t_max):
        # Calcular las derivadas
        dS = -beta * S[-1] * I[-1] / N
        dI = beta * S[-1] * I[-1] / N - gamma * I[-1]
        dR = gamma * I[-1]
        
        # Actualizar los valores
        S_new = S[-1] + dS
        I_new = I[-1] + dI
        R_new = R[-1] + dR
        
        # Asegurar que no sean negativos
        S_new = max(0, S_new)
        I_new = max(0, I_new)
        R_new = max(0, R_new)
        
        S.append(S_new)
        I.append(I_new)
        R.append(R_new)
    
    return S, I, R

# Callback único
@callback(
    [Output('epidemia-model-graph', 'figure'),
     Output('epidemia-info-modelo', 'children'),
     Output('epidemia-r0', 'value')],
    [Input('epidemia-poblacion-total', 'value'),
     Input('epidemia-infectados-iniciales', 'value'),
     Input('epidemia-tasa-contagio', 'value'),
     Input('epidemia-tasa-recuperacion', 'value'),
     Input('epidemia-tiempo-maximo', 'value')]
)
def update_graph_epidemia(N, I0, beta, gamma, t_max):
    # Valores por defecto
    if N is None: N = 1000
    if I0 is None: I0 = 1
    if beta is None: beta = 0.3
    if gamma is None: gamma = 0.1
    if t_max is None: t_max = 100
    
    # Calcular R0
    R0 = beta / gamma if gamma > 0 else 0
    
    # Resolver el modelo SIR
    S, I, R = resolver_sir_euler(N, I0, beta, gamma, t_max)
    
    # Tiempo
    t = list(range(t_max))
    
    # Crear gráfica
    fig = go.Figure()
    
    # Susceptibles
    fig.add_trace(go.Scatter(
        x=t,
        y=S,
        mode='lines',
        line=dict(color='blue', width=3),
        name='Susceptibles (S)',
        hovertemplate='Día: %{x}<br>Susceptibles: %{y:.0f}<extra></extra>'
    ))
    
    # Infectados
    fig.add_trace(go.Scatter(
        x=t,
        y=I,
        mode='lines',
        line=dict(color='red', width=3),
        name='Infectados (I)',
        hovertemplate='Día: %{x}<br>Infectados: %{y:.0f}<extra></extra>'
    ))
    
    # Recuperados
    fig.add_trace(go.Scatter(
        x=t,
        y=R,
        mode='lines',
        line=dict(color='green', width=3),
        name='Recuperados (R)',
        hovertemplate='Día: %{x}<br>Recuperados: %{y:.0f}<extra></extra>'
    ))
    
    # Encontrar el pico de infectados
    pico_infectados = max(I)
    dia_pico = I.index(pico_infectados)
    
    # Marcar el pico de infectados
    fig.add_trace(go.Scatter(
        x=[dia_pico],
        y=[pico_infectados],
        mode='markers+text',
        marker=dict(color='darkred', size=12, symbol='star'),
        text=[f' Pico: {pico_infectados:.0f}'],
        textposition='top center',
        name='Pico de infectados',
        hovertemplate=f'Día pico: {dia_pico}<br>Infectados máx: {pico_infectados:.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text=f'<b>Modelo Epidemiológico SIR - R₀ = {R0:.2f}</b>',
            font=dict(size=16, color='darkred'),
            x=0.5
        ),
        xaxis_title='Días',
        yaxis_title='Número de Personas',
        margin=dict(l=50, r=30, t=50, b=50),
        paper_bgcolor='white',
        plot_bgcolor='white',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.02
        )
    )
    
    fig.update_xaxes(
        showgrid=True,
        gridcolor='lightgray',
        zeroline=True,
        zerolinecolor='black'
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridcolor='lightgray',
        zeroline=True,
        zerolinecolor='black'
    )
    
    # Información del modelo
    if R0 > 1:
        situacion = "📈 EPIDEMIA CRECIENTE"
    else:
        situacion = "📉 EPIDEMIA CONTROLADA"
    
    info_text = f"{situacion} | R₀ = {R0:.2f} | Pico: {pico_infectados:.0f} infectados (día {dia_pico})"
    
    return fig, info_text, round(R0, 2)