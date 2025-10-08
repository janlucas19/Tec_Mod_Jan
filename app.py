import dash
from dash import html, dcc

# Crear la app
app = dash.Dash(
    __name__,
    use_pages=True,
    assets_folder='assets',
    assets_url_path='assets'
)

# Layout de la aplicación
app.layout = html.Div([
    # Header principal
    html.Header([
        html.Div([
            html.H1("Técnicas de Modelamiento", className='header-title'),
        ], className='header-content')
    ], className='app-header'),
    
    # Barra de navegación
    html.Nav([
        html.Div([
            html.Div([
                dcc.Link(
                    f"{page['name']}", 
                    href=page["relative_path"],
                    className='nav-link'
                )
                for page in dash.page_registry.values()
            ], className='nav-links-container')
        ], className='nav-inner')
    ], className='navigation'),
    
    # Contenido principal
    html.Main([
        dash.page_container
    ], className='main-content')
])

# Ejecutar la app
if __name__ == '__main__':
    app.run(debug=True)
