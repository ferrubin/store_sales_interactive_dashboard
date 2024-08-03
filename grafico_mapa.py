import pandas as pd
import plotly.express as px
import requests
import json

def crear_grafico_mapa(df):

    df_ingresos_ciudad = df.groupby(['abbrev_state','state_name']).agg(
    ingresos_netos=('ingresos_netos', 'sum')).reset_index()
    df_ingresos_ciudad


    file_id = '161Y6BbBVNAnKhSosPetTBSWx-cmP4FYs'
    url = f'https://drive.google.com/uc?export=download&id={file_id}'
    response = requests.get(url)
    brazil_states_geojson = response.json()


    fig_mapa = px.choropleth(
        df_ingresos_ciudad,
        geojson=brazil_states_geojson,
        locations='abbrev_state',
        color='ingresos_netos',
        color_continuous_scale='blues',
        featureidkey='properties.sigla',
        title='GANANCIA NETA POR ESTADO',
        range_color=[df_ingresos_ciudad['ingresos_netos'].min(), df_ingresos_ciudad['ingresos_netos'].max()],
        hover_data={'abbrev_state': False, 'state_name': True}
    )
    fig_mapa.update_geos(
        visible=False,
        scope="south america",
        center={"lat": -14.2350, "lon": -51.9253},
        projection_scale=1.6,
        showland=False,
        showcountries=False,
        showcoastlines=False,
        showframe=False,
        showsubunits=False
    )
    fig_mapa.update_layout(
        height=420,
        margin=dict(l=0, r=10, t=100, b=0),
        coloraxis_showscale=True,
        paper_bgcolor='rgba(0,0,0,0)',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            bgcolor='rgba(0,0,0,0)',
            projection_type='mercator',
        )
    )
    fig_mapa.update_traces(
        marker_line_width=0,
        hovertemplate='<b>%{customdata[1]}</b><br>Ventas Totales: %{z}<extra></extra>'
    )
    
    return fig_mapa