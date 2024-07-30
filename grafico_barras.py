import pandas as pd
import plotly.express as px

def crear_grafico_barras(df):

    revenue_productos = df.groupby('tipo_producto').agg({'valor_total': 'sum'}).reset_index()
    revenue_productos = revenue_productos.sort_values(by='valor_total', ascending=True)
    

    # Gráfico de barras con los 10 productos de mayor valor_total
    grafico_barras = px.bar(
        revenue_productos.tail(10),
        x='tipo_producto',
        y='valor_total',
        text='valor_total', 
        color='valor_total',
        color_continuous_scale='blues_r',
        title='INGRESOS POR TIPO DE PRODUCTO'
    )
    
    # Actualizar los nombres de los ejes
    grafico_barras.update_layout(
        xaxis_title='TIPO DE PRODUCTO',
        yaxis_title='INGRESOS TOTALES   ($)',
        coloraxis_showscale=False
    )
    
    # Formato de texto de las barras
    grafico_barras.update_traces(
        texttemplate='%{text:.3s}', 
        textposition='outside'
    )
    
    # Formato de los ejes
    grafico_barras.update_yaxes(tickformat=",.1s")
    
    return grafico_barras
