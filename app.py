import dash
from dash.dependencies import Input, Output, State
from datetime import date
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd
import dash_table
import plotly.express as px
from sqlalchemy import create_engine
import psycopg2 as ps
import pandas as pd
import plotly.graph_objects as go
#import pyodbc


# Parameters of database :
colors = {
    #'background': '#111111',
    #'text': '#7FDBFF'
    'background': '#fafafa',
    'text': '#7FDBFF',
    'color': '#333333'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '5%',
    'margin-right': '5%',
    'padding': '5px 5px',
    'text-align': 'justify',
    'margin-top': '2%'

}

taab_STYLE = {
    'margin-left': '5%',
   ### 'margin-right': '5%',
    'padding': '5px 5px'
}

#Create three unequal columns that floats next to each other */
column = {
  'float': 'right',
  'padding': '0px',
  'margin-top': '3%',
  'margin-right': '0%',
  'color': 'white'
}

left = {
  'width': '25%'
}

right = {
  'width': '25%'
}

middle = {
  'width': '50%'
}

#Clear floats after the columns
row1 = {
  'content': "",
  'display': 'table',
  'clear': 'both'
}


# conection to DB
host = '157.230.55.87'
port = 5432
user = 'postgres'
database = 'AMVA'

try:
    #conn = ps.connect(host=host,database=database,user=user,password=password,port=port)
    conn = ps.connect(host=host,database=database,user=user,port=port)
except ps.OperationalError as e:
    raise e
else:
    print('Connected!')

# Query -----RICARDO

#mult_idx = ['idruta', 'idvehiculo', 'idempresa', 'secuenciarecorrido', 'recorridoincumplido',\
#            'consecutivoregistro' , 'fecharegistro' , 'longitud', 'latitud', 'pasajerossuben',\
#            'pasajerosbajan', 'velocidad', 'margendesviacion']


#SQL_Query = pd.read_sql(
#    '''
#    SELECT idruta, idvehiculo, secuenciarecorrido, consecutivoregistro, recorridoincumplido, fecharegistro, distanciarecorrido, pasajerossuben, pasajerosbajan, longitud, latitud, velocidad 
#    FROM eventosmodelom LIMIT 20000
#    '''
#    , conn)


# Query EDA

SQL_Query = pd.read_sql( 
     '''
     SELECT idvehiculo, recorridoincumplido, fecharegistro, distanciarecorrido, pasajerossuben, pasajerosbajan, longitud, latitud, velocidad
     FROM eventosmodelom
     WHERE (idruta = 0 AND pasajerossuben <> 0 AND fecharegistro BETWEEN '2019-11-18 06:00:00' AND '2019-11-18 08:00:00')
     ''',
    conn)

SQL_Query1 = pd.read_sql( 
     '''
     SELECT idvehiculo, recorridoincumplido, fecharegistro, distanciarecorrido, pasajerossuben, pasajerosbajan, longitud, latitud, velocidad
     FROM eventosmodelom
     WHERE (idruta = 0 AND pasajerossuben <> 0 AND fecharegistro BETWEEN '2019-11-18 08:00:00' AND '2019-11-18 10:00:00')
     ''',
    conn)

SQL_Query2 = pd.read_sql( 
     '''
     SELECT idvehiculo, recorridoincumplido, fecharegistro, distanciarecorrido, pasajerossuben, pasajerosbajan, longitud, latitud, velocidad
     FROM eventosmodelom
     WHERE (idruta = 0 AND pasajerossuben <> 0 AND fecharegistro BETWEEN '2019-11-18 10:00:00' AND '2019-11-18 12:00:00')
     ''',
    conn)    

# Metrica # de Registros Totales
SQL_ALL = pd.read_sql(
    '''
    SELECT COUNT(0) 
    FROM eventosmodelom 
    WHERE fecharegistro BETWEEN '2019-11-18 06:00:00' AND '2019-11-18 08:00:00'
    ''', 
    conn)

SQL_ALL1 = pd.read_sql(
    '''
    SELECT COUNT(0) 
    FROM eventosmodelom 
    WHERE fecharegistro BETWEEN '2019-11-18 08:00:00' AND '2019-11-18 10:00:00'
    ''', 
    conn)

SQL_ALL2 = pd.read_sql(
    '''
    SELECT COUNT(0) 
    FROM eventosmodelom 
    WHERE fecharegistro BETWEEN '2019-11-18 10:00:00' AND '2019-11-18 12:00:00'
    ''', 
    conn)

Nregistros = SQL_ALL + SQL_ALL1 + SQL_ALL2
NregistrosT = Nregistros.iloc[0]['count']    


# Metrica # de Registros NA

SQL_NA = pd.read_sql(
    '''
    SELECT COUNT(0) 
    FROM eventosmodelom 
    WHERE idruta = 0 AND fecharegistro BETWEEN '2019-11-18 06:00:00' AND '2019-11-18 08:00:00'
    ''', 
    conn)

SQL_NA1 = pd.read_sql(
    '''
    SELECT COUNT(0) 
    FROM eventosmodelom 
    WHERE idruta = 0 AND fecharegistro BETWEEN '2019-11-18 08:00:00' AND '2019-11-18 10:00:00'
    ''', 
    conn)

SQL_NA2 = pd.read_sql(
    '''
    SELECT COUNT(0) 
    FROM eventosmodelom 
    WHERE idruta = 0 AND fecharegistro BETWEEN '2019-11-18 10:00:00' AND '2019-11-18 12:00:00'
    ''', 
    conn)

registrosNA = SQL_NA + SQL_NA1 + SQL_NA2
registrosNAT = registrosNA.iloc[0]['count']


# Metrica # de idvehiculos

SQL_VEH = pd.read_sql(
    '''
    SELECT DISTINCT idvehiculo 
    FROM eventosmodelom 
    WHERE idruta = 0 AND fecharegistro BETWEEN '2019-11-18 06:00:00' AND '2019-11-18 08:00:00'
    ''', 
    conn)

SQL_VEH1 = pd.read_sql(
    '''
    SELECT DISTINCT idvehiculo 
    FROM eventosmodelom 
    WHERE idruta = 0 AND fecharegistro BETWEEN '2019-11-18 08:00:00' AND '2019-11-18 10:00:00'
    ''', 
    conn)

SQL_VEH2 = pd.read_sql(
    '''
    SELECT DISTINCT idvehiculo 
    FROM eventosmodelom 
    WHERE idruta = 0 AND fecharegistro BETWEEN '2019-11-18 10:00:00' AND '2019-11-18 12:00:00'
    ''', 
    conn)

SQL_VEHt = pd.concat([SQL_VEH, SQL_VEH1, SQL_VEH2], axis=0)
SQL_VEHn = len(SQL_VEHt.idvehiculo.unique())


## Append 2 Dataframes  -----RICARDO
#SQL_Query = SQL_Query.append(SQL_Query1)
SQL_QueryNA = pd.concat([SQL_Query, SQL_Query1, SQL_Query2], axis=0)
SQL_QueryNAN = len(SQL_QueryNA)

## Identificacion de rutas NA -----RICARDO

#idruta_0 = (SQL_Query['idruta'] == 0) 
#SQL_QueryNA = SQL_Query[idruta_0]
#SQL_QueryNA = SQL_QueryNA.sort_values(by=['idvehiculo','secuenciarecorrido']).reset_index(drop=True)
SQL_QueryNA = SQL_QueryNA.sort_values(by=['idvehiculo','fecharegistro']).reset_index(drop=True)

#SQL_QueryNA['pasajerossuben'] = SQL_QueryNA['pasajerossuben'].astype(int)
#SQL_QueryNA['pasajerosbajan'] = SQL_QueryNA['pasajerosbajan'].astype(int)

fechamin = SQL_QueryNA.fecharegistro.min()
fechamax = SQL_QueryNA.fecharegistro.max()
pasajeros = SQL_QueryNA.pasajerossuben.sum()


# charts

scatter = px.scatter(SQL_QueryNA, x='longitud', y='latitud')

pasajerosx = (SQL_QueryNA['pasajerossuben'] >= 15)
SQL_QueryNA1 = SQL_QueryNA[pasajerosx]
scatter2 = px.scatter(SQL_QueryNA1, x='fecharegistro', y='pasajerossuben', color='idvehiculo')

velocidadx = (SQL_QueryNA['velocidad'] >= 50)
SQL_QueryNA2 = SQL_QueryNA[velocidadx]
scatter3 = px.scatter(SQL_QueryNA2, x='fecharegistro', y='velocidad', color='idvehiculo')


SQL_QueryNA['hora'] = SQL_QueryNA.fecharegistro
SQL_QueryNA.set_index('hora',inplace=True, drop=True)
SQL_QueryNAhora = SQL_QueryNA.groupby(pd.Grouper(freq='30min')).agg({'pasajerossuben':'sum'})

bar1 = px.bar(SQL_QueryNAhora, x=SQL_QueryNAhora.index, y='pasajerossuben', text='pasajerossuben')


#### ------------- application

app = dash.Dash(__name__
, external_stylesheets=[dbc.themes.BOOTSTRAP]
)
server = app.server

# CONTROLS:

 # define visual objects and styles
sidebar = html.Div(
    [
        #controls,
        dcc.DatePickerRange(id='date_picker1', min_date_allowed=date(2019,11,1),
                    max_date_allowed=date(2019,11,30),initial_visible_month =date(2019,11,1),
                    minimum_nights = 0),
        dcc.Input(id='input_hour1',type='text', placeholder='Start hour', debounce=True,
          pattern= u'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'),
        dcc.Input(id='output_hour1',type='text', placeholder='End hour', debounce=True,
          pattern= u'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'),
        html.Button(id= 'date_button1', n_clicks=0, children = 'Process')
    ],
    style=CONTENT_STYLE,
)

# banner object
nav = dbc.Navbar(
         [
            html.Div(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        # Change App Name here
                        dbc.Col(html.Img(src=app.get_asset_url('logo5.png'), height="120px",
#                         style=column,
                                )),
                        dbc.Col(html.Img(src=app.get_asset_url('correlation.jpg'), height="120px",
#                        style=column,
                                )),

                        dbc.Col(html.Img(src=app.get_asset_url('amva.jpg'), height="120px",
#                        style=column,
                                )),
                        html.H2(
#                        dbc.NavbarBrand(
                        "DASHBOARD ANÁLISIS Y PLANEACIÓN AMVA",
                            style=column,
#                                )
                                ),
                    ],
#                    style = row1,

#                    align="center",
#                    no_gutters=True,
            ),
          # href="https://plot.ly",
        ),
#        dbc.NavbarToggler(id="navbar-toggler"),
#        dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
    ],
    color="dark",
    dark=True,
)

# intro div
intro = html.Div(
                        [
                            html.Div(
                                [
                                    html.H3("INTRODUCCIÓN", style=CONTENT_STYLE
                                        ),

                                    html.P(
                                        "El transporte público es un servicio vital para una ciudad, ya que permite a sus ciudadanos desplazarse, viajar y desarrollar la economía de la ciudad. Además, se ha trabajado mucho en el diseño de un sistema de transporte inclusivo, eficiente y sostenible. Sin embargo, ha habido una falta de coordinación de las diferentes partes interesadas y hay una falta de datos confiables para los tomadores de decisiones. Las partes interesadas del sistema de transporte pueden incluir: gobierno, autoridades de tránsito, empresas propietarias de autobuses, formuladores de políticas, fabricantes de autobuses, conductores, usuarios, etc. Pueden tener diferentes intereses y percepciones sobre cómo debería ser un sistema de transporte público y una metodología sistemática para la evaluación de los principales factores de servicio no está disponible, más aún cuando los datos están disponibles, pero son diversos, dispersos y no confiables.El Centro de Operaciones de Transporte Público (GTPC) reconoce que hasta el 40% de los datos capturados para el sistema operativo diario tienen problemas de calidad. Los datos de baja calidad no son adecuados para alimentar el sistema operativo ni utilizarse para el modelado de predicciones, la planificación de rutas óptimas o para la toma de decisiones.",
                                        style=CONTENT_STYLE,
                                        className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    )
#id="imagen-intro",
imagen = html.Div([html.A(children=[
                                html.Img(src=app.get_asset_url("banner.jpg"),
                                         style={
                'height': '100%',
                'width': '100%'
            })
                            ],
                         )
], style={'textAlign': 'center'})

#OUR TEAM
# intro div
NOSOTROS = html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("NUESTRO EQUIPO", style=CONTENT_STYLE
                                        ),

                                    html.P(
                                        "Contamos con el mejor talento de Científicos de Datos certificados con Honores por el Ministerio de Tecnologías de la Información y Comunicaciones (MINTIC). Somos Expertos en la generación de soluciones de Negocio, aplicamos alternativas basadas en Inteligencia Artificial, expertos en bases de datos, integración de herramientas y metodologías tecnologicas para un mejor desarrollo y sostenibilidad del país. Somos tu mejor Opción.",
                                        style=CONTENT_STYLE,
                                        className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    )
#id="imagen-intro",
EQUITEAM = html.Div([html.A(children=[
                                html.Img(src=app.get_asset_url("TEAM.png"),
                                         style={
                'height': '100%',
                'width': '100%'
            })
                            ],
                         )
], style={'textAlign': 'center'})



# GRAPHS
graph1 = dcc.Graph(figure=scatter, id='scatter')
graph2 = dash_table.DataTable(id='table',
                     columns =[{'name':i, 'id':i} for i in SQL_QueryNA.columns],
                     data=SQL_QueryNA.head(10).to_dict('records'))

graph5 = dcc.Graph(figure=scatter2, id='scatter2')

graph6 = dcc.Graph(figure=scatter3, id='scatter3')

graph7 = dcc.Graph(figure=bar1, id='bar1')


# GRAPHS
graph11 = dcc.Graph(figure=scatter, id='scatter11')
graph22 = dash_table.DataTable(id='table11',
                     columns =[{'name':i, 'id':i} for i in SQL_QueryNA.columns],
                     data=SQL_QueryNA.head(10).to_dict('records'))
graph3 = dcc.Graph(
        id='example-graph_2',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                },
                'title': 'Dash Data Visualization'
            }
        }
    )


graph4 = dcc.Graph(

        figure = go.Figure([go.Indicator(
                                        mode = "number",
                                        #value = len(SQL_QueryNA['idruta'].unique()),
                                        value = pasajeros,
                                        title = {"text": "# de Pasajeros Suben:"},
                                        domain = {'x': [0, 0.3], 'y': [0.4, 0.7]}
                                        #delta = {'reference': 400, 'relative': True, 'position' : "top"}
                                        ),
                                                
                                        go.Indicator(
                                        #mode = "number+delta",
                                        mode = "number",
                                        #value = len(SQL_QueryNA['idvehiculo'].unique()),
                                        value = SQL_VEHn,
                                        title = {"text": "Vehiculos NA:"},
                                        #delta = {'reference': 400, 'relative': True},
                                        domain = {'x': [0.3, 0.6], 'y': [0.4, 0.7]}
                                        ),
                                        
                                        go.Indicator(
                                        #mode = "number+delta",
                                        mode = "number",
                                        #value = SQL_QueryNA['idvehiculo'].count(),
                                        value = registrosNAT,
                                        title = {"text": "# de Registros NA:"},
                                        #delta = {'reference': 400, 'relative': True},
                                        domain = {'x': [0.6, 0.9], 'y': [0.4, 0.7]}
                                        ),

                                        go.Indicator(
                                        #mode = "number+delta",
                                        mode = "number",
                                        value = SQL_QueryNA['velocidad'].mean(),
                                        title = {"text": "Velocidad Promedio NA K/hr:"},
                                        #delta = {'reference': 400, 'relative': True},
                                        domain = {'x': [0, 0.3], 'y': [0, 0.3]}
                                        ),

                                        go.Indicator(
                                        #mode = "number+delta",
                                        mode = "number",
                                        #value = (SQL_QueryNA['idvehiculo'].count())/(SQL_QueryNA['idvehiculo'].count())*100,
                                        value = registrosNAT/NregistrosT*100,
                                        number = {'suffix': "%"},
                                        title = {"text": "% Registros NA:"},
                                        #delta = {'reference': 400, 'relative': True},
                                        domain = {'x': [0.3, 0.6], 'y': [0, 0.3]}
                                        ),

                                        go.Indicator(
                                        #mode = "number+delta",
                                        mode = "number",
                                        value = SQL_QueryNAN,
                                        #value = SQL_QueryNAN/registrosNAT,
                                        #number = {'suffix': "%"},
                                        title = {"text": "Registros NA por corregir:"},
                                        #delta = {'reference': 400, 'relative': True},
                                        domain = {'x': [0.6, 0.9], 'y': [0, 0.3]}),

                                        go.Indicator(
                                            #mode = "number+delta",
                                            #mode = "number",
                                            #value = 0,
                                            #number = {'prefix': "$"},
                                            title = {"text": str(fechamin)},
                                            #delta = {'reference': 400, 'relative': True},
                                            domain = {'x': [0, 0.3], 'y': [0.8, 1]}),

                                        go.Indicator(
                                            #mode = "number+delta",
                                            #mode = "number",
                                            #value = 0,
                                            title = {"text": str(fechamax)},
                                            #delta = {'reference': 400, 'relative': True},
                                            domain = {'x': [0.3, 0.6], 'y': [0.8, 1]}),

                                        go.Indicator(
                                            #mode = "number+delta",
                                            mode = "number",
                                            #value = SQL_QueryNA['idvehiculo'].count(),
                                            value = NregistrosT,
                                            title = {"text": "Total Registros:"},
                                            #delta = {'reference': 400, 'relative': True},
                                            domain = {'x': [0.6, 0.9], 'y': [0.8, 1]})

                            ]),

            id='KPI1')



content_first_row = dbc.Row(dbc.Col(''))

content_second_row = dbc.Row(dbc.Col(intro))

content_third_row = dbc.Row(
    [
        dbc.Col(graph4
        )
    ]

)

content_seventh_row = dbc.Row([

    dbc.Col(
    dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4(id='TITL', children=['# RUTAS'], className='card-title'),
                        html.P(id='card_text_1', children=[str(SQL_QueryNA['latitud'].mean())]),
                    ]
                )
            ], color="primary", inverse=True
        ),
        md=2
    ),
    dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H4('# EMPRESAS', className='card-title'),
                        html.P('Sample text.'),
                    ]
                )
            ] ,color="primary", inverse=True

        ),
        md=2
    ),
    dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4('# BACH', className='card-title'),
                        html.P('Sample text.'),
                    ]
                )
            ] ,    color="primary", inverse=True

        ),
        md=2
    ),
    dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4('# LINEA', className='card-title'),
                        html.P('Sample text.'),
                    ]
                )
            ],    color="primary", inverse=True
        ),
        md=2
    )
])


content_fourth_row = dbc.Row(
    [
        html.Br([]),
        dbc.Col(graph7
        )
    ]
)


content_Eigth_row = dbc.Row(
    [

        dbc.Col(
            dcc.Graph(id='graph_1'), md=4
        ),
        dbc.Col(
            dcc.Graph(id='graph_2'), md=4
        ),
        dbc.Col(
            dcc.Graph(id='graph_3'), md=4
        )
    ]
)

content_sixth_row = dbc.Row(
    [
        dbc.Col(graph2
            #dcc.Graph(figure=scatter, id='scatter'), md=12,
        )
    ]
)


content_fifth_row = dbc.Row(
    [
        dbc.Col(
        #    dcc.Graph(id='graph_5'), md=6
            graph5
        ),
        dbc.Col(
        #    dcc.Graph(id='graph_6'), md=6
            graph6
        )
    ]
)

content_tenth_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_7'), md=6
        ),
        dbc.Col(
            dcc.Graph(id='graph_8'), md=6
        )
    ]
)
tabs = dbc.Tabs(
    [
        dbc.Tab([content_second_row], label="QUIENES SOMOS"),

        dbc.Tab([html.Hr(),
                 html.H3('PERIODO A CONSULTAR:', style=CONTENT_STYLE),
                 sidebar,
                 html.Hr(),
                 html.H3('KPI´S RUTAS NA:', style=CONTENT_STYLE),
                 content_third_row,
                 html.Hr(),
                 html.H3('DISTRIBUCIÓN DE PASAJEROS POR HORA:', style=CONTENT_STYLE),
                 content_fourth_row,
                 html.H3('ANOMALIAS EN VARIABLES DE PASAJEROS Y VELOCIDAD EN REGISTROS NA:', style=CONTENT_STYLE),
                 content_fifth_row, #
                 html.Hr(),
                 html.H3('TABLA DETALLADA DE EVENTOS NA:', style=CONTENT_STYLE),
                 content_sixth_row], label="EDA"),

        dbc.Tab([graph11, content_tenth_row ], label="MODELO"),

        dbc.Tab([NOSOTROS, EQUITEAM], label="NUESTRO EQUIPO")
    ],

    style=taab_STYLE,
)

content = html.Div(
    [
        #html.H2('Analytics Dashboard', style=TEXT_STYLE),
        #html.Hr(),
        html.Div(content_first_row), # BANNER
        html.Hr(),
        html.Div(tabs),
        #html.Hr(className="myHr"),
        #html.Div(content_third_row),
        #html.Hr(),
        #html.Div(content_fifth_row),
        #html.Hr(),
        #html.Div(content_sixth_row),
        #html.Hr(),
        #html.Div(content_fourth_row)
    ],
)

#### layout
app.layout = html.Div(children=[
                                nav,
                                html.Hr(),
                                imagen,
                                content,


#html.Br([]),
#html.H5("EXPLORACIÓN DE DATOS"),

#graph1,


#html.Br([]),
#html.H5("RUTAS REPORTADAS"),

#graph2,

#html.Br([]),

#html.H5("MAPEO"),

#graph3,

html.Div(id='output_date')
], id='layout')


#### Interactividad




#### Initiate server where app will work
if __name__ == '__main__':
    app.run_server(debug=True)
