import pandas as pd
import plotly.express as px

def custom_format(value):
    return f'{value:,.0f}'.replace(',', '.')

def crear_grafico(df):
    # Convertir la columna 'fecha_compra' a tipo datetime
    df['fecha_compra'] = pd.to_datetime(df['fecha_compra'])
    
    # Crear columnas 'Year' y 'Month'
    df['Year'] = df['fecha_compra'].dt.year
    df['Month'] = df['fecha_compra'].dt.strftime('%B')
    
    # Agrupar por año y mes y sumar 'valor_total'
    revenues_monthly = df.groupby(['Year', 'Month']).agg({'valor_total': 'sum'}).reset_index()
    
    # Ordenar los meses correctamente
    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    revenues_monthly['Month'] = pd.Categorical(revenues_monthly['Month'], categories=month_order, ordered=True)
    revenues_monthly = revenues_monthly.sort_values(['Year', 'Month'])
    
    # Aplicar la función de formateo a la columna 'valor_total'
    revenues_monthly['valor_total_formatted'] = revenues_monthly['valor_total'].apply(custom_format)

    # Crear el gráfico de líneas
    grafico_lineas = px.line(
        revenues_monthly,
        x='Month',
        y='valor_total',
        markers=True,
        range_y=(0, revenues_monthly['valor_total'].max()),
        color='Year',
        title='INGRESOS MENSUALES'
    )

    # Formatear las etiquetas emergentes
    grafico_lineas.update_traces(
        hovertemplate='<b>%{x}</b><br>Valor Total: %{customdata[0]}<extra></extra>',
        customdata=revenues_monthly[['valor_total_formatted']]
    )

    # Actualizar los títulos de los ejes
    grafico_lineas.update_layout(
        xaxis_title='MONTH',
        yaxis_title='INGRESOS ($)',
    )
    
    return grafico_lineas