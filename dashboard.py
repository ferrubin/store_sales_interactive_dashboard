import pandas as pd
import streamlit as st
import grafico_mapa as graf1
import grafico_lineas as graf2
import grafico_barras as graf3
import grafico_pizza as graf4
import grafico_snb as graf5
import grafico_arbol as graf6



st.set_page_config(layout="wide")

st.title("Dashboard - Following Sales")

# Funcion para mejorar la visual de los numeros
def formatar_numero(valor, prefijo = " "):
    for unidad in [ " ", "K"]:
        if valor <1000:
            return f"{prefijo} {valor:.2f} {unidad}"
        valor /= 1000
    return f"{prefijo} {valor:.2f} M"



# Cargando la base de datos desde github 
df_final = pd.read_csv("https://raw.githubusercontent.com/agus-fran-1998/store_sales_interactive_dashboard/main/df_final.csv")
df_final["fecha_compra"] = pd.to_datetime(df_final["fecha_compra"])


# Creando y configurando los filtros
st.sidebar.image("logo-bootcamp.png")
st.sidebar.title("Filtros")

# Filtro para el grafico de mapa
estados_brasil = sorted(list(df_final["abbrev_state"].unique()))
ciudades = st.sidebar.multiselect("ESTADOS", estados_brasil)

# Filtro para el grafico de barras
productos_categorias = sorted(list(df_final["tipo_producto"].unique()))
productos_categorias.insert(0, "TODOS")
categorias = st.sidebar.selectbox("PRODUCTOS", productos_categorias)

# Filtro para el grafico de lineas
años = st.sidebar.checkbox("Todo el Periodo", value=True)
if not años:
    var_años = st.sidebar.slider("Año", df_final["fecha_compra"].dt.year.min(), 
                      df_final["fecha_compra"].dt.year.max())


# Filtro para el gráfico de pastel
vendedores = sorted(list(df_final["nombre_vendedor"].unique()))
vendedores.insert(0, "TODOS")
seleccion_vendedores = st.sidebar.multiselect("VENDEDORES", vendedores)

# Filtro para el gráfico Sunburst
marcas = sorted(list(df_final["marca"].unique()))
marcas.insert(0, "TODOS")
seleccion_marcas = st.sidebar.multiselect("SELECCIONAR MARCA", marcas)





# Filtrando los datos
# Mapa
if ciudades:
    df_final = df_final[df_final["abbrev_state"].isin(ciudades)]


# Barras
if categorias != "TODOS":
    df_final = df_final[df_final["tipo_producto"] == categorias]


# Lineas
if not años:
    df_final = df_final[df_final["fecha_compra"].dt.year == var_años]


# Pizza
if seleccion_vendedores and "TODOS" not in seleccion_vendedores:
    df_final = df_final[df_final["nombre_vendedor"].isin(seleccion_vendedores)]

# Sunburst
if seleccion_marcas and "TODOS" not in seleccion_marcas:
    df_final = df_final[df_final["marca"].isin(seleccion_marcas)]

# Verificar si hay datos después de aplicar los filtros
if df_final.empty:
    st.write("No hay datos disponibles para los filtros seleccionados.")
else: " "




# Llamar a las graficas
grafico_mapa = graf1.crear_grafico_mapa(df_final)
grafico_lineas = graf2.crear_grafico(df_final)
grafico_barras = graf3.crear_grafico_barras(df_final)
grafico_pizza = graf4.crear_grafico_pizza(df_final)
grafico_snb = graf5.crear_grafico_snb(df_final)
grafico_arbol = graf6.crear_grafico_arbol(df_final)


# Dividiendo la pantalla del dashboard en 2 columnas
col1, col2 = st.columns(2)
with  col1:
    st.metric("**Total de Revenues**", formatar_numero(df_final["valor_total"].sum(), "$"))
    st.plotly_chart(grafico_mapa, use_container_width=True)
    st.plotly_chart(grafico_pizza, use_container_width=True)
    st.plotly_chart(grafico_snb, use_container_width=True)
    
with col2:
    st.metric("**Total de Ventas**", formatar_numero(df_final["cantidad"].sum()))
    st.plotly_chart(grafico_lineas, use_container_width=True)
    st.plotly_chart(grafico_barras, use_container_width=True)
    st.plotly_chart(grafico_arbol, use_container_width=True)
    


#st.dataframe(df_final)