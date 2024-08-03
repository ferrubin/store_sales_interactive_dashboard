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

    # Encontrar el índice del vendedor con el mayor porcentaje
    max_index = vendedores.tail(5)['total_ventas'].idxmax()

    pastel.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hoverinfo='label+percent+value',
        textfont_size=13,
        hovertemplate='%{label}: %{value:,.0f}'.replace(',', '.') + '<br>Percent: %{percent:.1%}<extra></extra>',
        marker=dict(line=dict(color='#000000', width=2)),
        pull=[0.1 if i == max_index else 0 for i in range(len(vendedores.head(5)))]
    )

    # Ajustar los colores de las porciones del gráfico
    pastel.update_layout(
        showlegend=True,
        legend_title_text='Vendedores',
        uniformtext_minsize=3.5,
        uniformtext_mode='hide',
        annotations=[dict(text='', x=0.5, y=0.5, font_size=20, showarrow=False)],
        plot_bgcolor='black',
        margin=dict(l=0, r=10, t=155, b=0)
    )
    
    return pastel