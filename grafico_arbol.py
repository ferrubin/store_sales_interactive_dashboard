import pandas as pd
import plotly.express as px

def crear_grafico_arbol(df):
    # Visualizar la cantidad de productos por marca y tipo. 
    # Columnas relevantes
    df = df[["marca", "tipo_producto", "condicion"]]
    
    # Agrupar datos por marca y tipo de producto
    data = df.groupby(["marca", "tipo_producto"]).size().reset_index(name="count")
    
    # Filtrar las 12 marcas con más productos
    top_marcas = data.groupby("marca")["count"].sum().nlargest(12).index
    data = data[data["marca"].isin(top_marcas)]
    
    # Crear gráfico de mapa de árbol
    arbol_mapa = px.treemap(data, path=["marca", "tipo_producto"], values="count",
                            color_continuous_scale="Blues",  # Escala de colores de azul oscuro a claro
                            labels={"count": "Cantidad de productos"},
                            custom_data=["marca"])  # Agregar datos personalizados (nombre de la marca)
    
    # Personalizar etiquetas
    arbol_mapa.update_traces(texttemplate="%{label}: %{value} productos", textinfo="label+value")
    
    # Título y leyenda
    arbol_mapa.update_layout(title={"text": "DISTRIBUCION DE PRODUCTOS", "font": {"size": 18}},
                             coloraxis_colorbar=dict(title="Cantidad de productos"),
                             margin=dict(l=0, r=0, t=100, b=0))
    
    return arbol_mapa
