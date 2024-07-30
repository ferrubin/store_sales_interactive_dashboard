import pandas as pd
import plotly.express as px


# Función para formatear números grandes
def formatear_numero(num):
    if num >= 1e6:
        return f'{num/1e6:.2f}M'
    elif num >= 1e3:
        return f'{num/1e3:.0f}k'
    else:
        return str(num)

def crear_grafico_snb(df):
    # Calcular el valor total generado
    df['valor_total'] = df['cantidad'] * df['valor_unitario']
    
    # Calcular ventas netas (valor_total - costo_envio)
    df['ventas_netas'] = df['valor_total'] - df['costo_envio']
    
    # Filtrar las 5 marcas principales por ventas netas
    top_marcas = df.groupby('marca')['ventas_netas'].sum().nlargest(5).index
    df_top_marcas = df[df['marca'].isin(top_marcas)]
    
    # Calcular ventas netas por marca
    ventas_netas = df_top_marcas.groupby('marca')['ventas_netas'].sum().reset_index()
    ventas_netas.rename(columns={'ventas_netas': 'ventas_netas_totales'}, inplace=True)
    
    # Formatear ventas netas totales
    ventas_netas['ventas_netas_totales_fmt'] = ventas_netas['ventas_netas_totales'].apply(formatear_numero)
    
    # Encontrar el producto con más ingresos netos para cada marca
    df_producto_mas_rentable = df_top_marcas.loc[df_top_marcas.groupby('marca')['ingresos_netos'].idxmax()]
    
    # Unir los datos de ventas netas con el DataFrame del producto más rentable
    df_producto_mas_rentable = df_producto_mas_rentable.merge(ventas_netas, on='marca')
    
    # Reemplazar nombres de marcas
    df_producto_mas_rentable['marca'] = df_producto_mas_rentable['marca']



    colores_personalizados = {
        'marca'[0]: '#6481EC',
        'marca'[1]: '#3354D0',
        'marca'[2]: '#1F3CAA',
        'marca'[3]: '#081E71',
        'marca'[4]: '#081E71'
    }
    

    
    # Crear el gráfico Sunburst
    fig = px.sunburst(
        df_producto_mas_rentable,
        path=['ventas_netas_totales_fmt', 'marca', 'condicion', 'producto'],
        values='ingresos_netos',
        color='marca',
        color_discrete_map=colores_personalizados,
        title='VENTAS POR MARCA Y PRODUCTO',
    )

    fig.update_traces(insidetextorientation='auto', 
            textfont_size=12,
            marker=dict(colors=df_producto_mas_rentable['marca'].map(colores_personalizados)))
    
    return fig
