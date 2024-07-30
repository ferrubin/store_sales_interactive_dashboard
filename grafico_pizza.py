import pandas as pd
import plotly.express as px

def crear_grafico_pizza(df):

    # Extraer solo el primer nombre de cada vendedor
    df['primer_nombre'] = df['nombre_vendedor'].apply(lambda x: x.split()[0])

    # Agrupar por el nombre del vendedor y sumar la cantidad de items vendidos
    vendedores = df.groupby('primer_nombre').agg({'cantidad': 'sum'}).reset_index()
    
    # Ordenar ascendentemente por 'cantidad'
    vendedores = vendedores.sort_values(by='cantidad', ascending=False)
    
    # Renombrar la columna para el gráfico
    vendedores.rename(columns={'cantidad': 'total_ventas'}, inplace=True)
    
    # Crear el gráfico de pastel con los 5 vendedores de mayores ventas
    pastel = px.pie(
        vendedores.head(5),
        values='total_ventas',
        names='primer_nombre',
        title='VENTAS POR VENDEDORES',
        color_discrete_sequence=px.colors.sequential.tempo_r
    )

    pastel.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hoverinfo='label+percent+value',
        textfont_size=13,
        marker=dict(line=dict(color='#000000', width=2))
    )

    # Ajustar los colores de las porciones del gráfico
    pastel.update_layout(
        showlegend=True,
        legend_title_text='Vendedores',
        uniformtext_minsize=3.5,
        uniformtext_mode='hide',
        annotations=[dict(text='', x=0.5, y=0.5, font_size=20, showarrow=False)],
        plot_bgcolor='black',
    )
    
    return pastel