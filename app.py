import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import numpy as np

# Leer datos
car_data = pd.read_csv('vehicles_us.csv')
car_data['brand'] = car_data['model'].str.split().str[0]

# Título
st.header('🚗 AutoInsight US')
st.subheader('Análisis Exploratorio — Mercado de Autos Usados')
st.write('Explora los patrones de precio, kilometraje y tiempo de venta del mercado de autos usados en Estados Unidos.')

# --- GRÁFICA 1: Histograma días listados ---
if st.checkbox('📊 Ver distribución de días en venta'):
    st.write(
        'Distribución del tiempo que los vehículos permanecen publicados antes de venderse.')

    promedio = car_data['days_listed'].mean()
    mediana = car_data['days_listed'].median()

    fig1 = go.Figure(data=[go.Histogram(
        x=car_data['days_listed'],
        marker_color='teal',
        opacity=0.85
    )])
    fig1.add_vline(x=promedio, line_dash='dash', line_color='orange',
                   annotation_text=f'Promedio: {promedio:.1f} días', annotation_position='top right')
    fig1.add_vline(x=mediana, line_dash='dot', line_color='red',
                   annotation_text=f'Mediana: {mediana:.1f} días', annotation_position='top left')
    fig1.update_layout(title_text='¿Cuántos días tardan en venderse los autos?',
                       xaxis_title='Días listados', yaxis_title='Cantidad de autos', plot_bgcolor='white')
    st.plotly_chart(fig1, use_container_width=True)

# --- GRÁFICA 2: Scatter odómetro vs año ---
if st.checkbox('📅 Ver kilometraje según año del modelo'):
    st.write('Relación entre el año del modelo y el kilometraje acumulado.')

    fig2 = go.Figure(data=[go.Scatter(
        x=car_data['model_year'], y=car_data['odometer'],
        mode='markers', marker=dict(color='teal', opacity=0.4, size=4)
    )])
    fig2.update_layout(title_text='Kilometraje según Año del Modelo',
                       xaxis_title='Año del modelo', yaxis_title='Odómetro (millas)', plot_bgcolor='white')
    st.plotly_chart(fig2, use_container_width=True)

# --- GRÁFICA 3: Scatter precio vs odómetro (todos los datos) ---
if st.checkbox('🔍 Ver relación entre precio y kilometraje (datos completos)'):
    st.write('Relación general entre precio y kilometraje incluyendo todos los datos.')

    df_clean = car_data[['odometer', 'price']].dropna()
    z = np.polyfit(df_clean['odometer'], df_clean['price'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(df_clean['odometer'].min(),
                         df_clean['odometer'].max(), 100)

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=df_clean['odometer']/1000, y=df_clean['price']/1000,
                              mode='markers', marker=dict(color='teal', opacity=0.3, size=4), name='Vehículos'))
    fig3.add_trace(go.Scatter(x=x_line/1000, y=p(x_line)/1000,
                              mode='lines', line=dict(color='orange', width=2), name='Tendencia'))
    fig3.update_layout(title_text='Precio según Kilometraje (Datos Completos)',
                       xaxis_title='Odómetro (miles de millas)', yaxis_title='Precio (miles de USD)',
                       plot_bgcolor='white', yaxis=dict(rangemode='tozero'))
    st.plotly_chart(fig3, use_container_width=True)

# --- GRÁFICA 3 FILTRADA: Scatter precio vs odómetro filtrado ---
if st.checkbox('🔍 Ver relación entre precio y kilometraje (mercado principal)'):
    st.write(
        'Análisis filtrado: vehículos con menos de 300,000 millas y precio menor a $100,000 USD.')

    df_filtrada = car_data[
        (car_data['odometer'] < 300000) & (car_data['price'] < 100000)
    ][['odometer', 'price']].dropna()

    mediana_odometer = df_filtrada['odometer'].median() / 1000
    mediana_price = df_filtrada['price'].median() / 1000
    z = np.polyfit(df_filtrada['odometer'], df_filtrada['price'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(
        df_filtrada['odometer'].min(), df_filtrada['odometer'].max(), 100)

    fig3f = go.Figure()
    fig3f.add_trace(go.Scatter(x=df_filtrada['odometer']/1000, y=df_filtrada['price']/1000,
                               mode='markers', marker=dict(color='teal', opacity=0.3, size=4), name='Vehículos'))
    fig3f.add_trace(go.Scatter(x=x_line/1000, y=p(x_line)/1000,
                               mode='lines', line=dict(color='orange', width=2), name='Tendencia'))
    fig3f.add_vline(x=mediana_odometer, line_dash='dash', line_color='deeppink',
                    annotation_text=f'Mediana odómetro: {mediana_odometer:.0f}k millas', annotation_position='top right')
    fig3f.add_hline(y=mediana_price, line_dash='dash', line_color='purple',
                    annotation_text=f'Mediana precio: ${mediana_price:.1f}k USD', annotation_position='bottom right')
    fig3f.update_layout(title_text='Precio según Kilometraje (Mercado Principal)',
                        xaxis_title='Odómetro (miles de millas)', yaxis_title='Precio (miles de USD)',
                        plot_bgcolor='white', yaxis=dict(rangemode='tozero'))
    st.plotly_chart(fig3f, use_container_width=True)

# --- GRÁFICA 4: Box plot precio por marca ---
if st.checkbox('🏷️ Ver distribución de precios por marca'):
    st.write('Distribución de precios de las 10 marcas más frecuentes.')

    top_marcas = car_data['brand'].value_counts().head(10).index
    df_box = car_data[(car_data['brand'].isin(top_marcas))
                      & (car_data['price'] < 100000)]

    fig4 = go.Figure()
    for marca in top_marcas:
        fig4.add_trace(go.Box(y=df_box[df_box['brand'] == marca]['price'],
                              name=marca, marker_color='teal', showlegend=False))
    fig4.add_hline(y=9000, line_dash='dash',
                   line_color='orange', annotation_text='')
    fig4.add_trace(go.Scatter(x=[None], y=[None], mode='lines',
                              line=dict(color='orange', dash='dash', width=2), name='Mediana general: $9,000 USD'))
    fig4.update_layout(title_text='Distribución de Precios por Marca (Top 10)',
                       yaxis_title='Precio (USD)', xaxis_title='Marca', plot_bgcolor='white', showlegend=True)
    st.plotly_chart(fig4, use_container_width=True)

# --- GRÁFICA 5: Box plot precio por tipo ---
if st.checkbox('🚙 Ver distribución de precios por tipo de vehículo'):
    st.write('Distribución de precios según el tipo de vehículo.')

    tipos = car_data['type'].value_counts().index
    fig5 = go.Figure()
    for tipo in tipos:
        df_tipo = car_data[(car_data['type'] == tipo) &
                           (car_data['price'] < 100000)]
        fig5.add_trace(go.Box(y=df_tipo['price'], name=tipo,
                              marker_color='teal', showlegend=False))
    fig5.add_hline(y=9000, line_dash='dash',
                   line_color='orange', annotation_text='')
    fig5.add_trace(go.Scatter(x=[None], y=[None], mode='lines',
                              line=dict(color='orange', dash='dash', width=2), name='Mediana general: $9,000 USD'))
    fig5.update_layout(title_text='Distribución de Precios por Tipo de Vehículo',
                       yaxis_title='Precio (USD)', xaxis_title='Tipo de vehículo',
                       plot_bgcolor='white', showlegend=True)
    st.plotly_chart(fig5, use_container_width=True)

# --- GRÁFICA 6: Box plot kilometraje por tipo ---
if st.checkbox('🛣️ Ver distribución de kilometraje por tipo de vehículo'):
    st.write('Distribución del kilometraje acumulado según el tipo de vehículo.')

    mediana_odo_general = car_data['odometer'].median()
    tipos = car_data['type'].value_counts().index
    fig6 = go.Figure()
    for tipo in tipos:
        df_tipo = car_data[(car_data['type'] == tipo) &
                           (car_data['odometer'] < 300000)]
        fig6.add_trace(go.Box(y=df_tipo['odometer'], name=tipo,
                              marker_color='teal', showlegend=False))
    fig6.add_hline(y=mediana_odo_general, line_dash='dash',
                   line_color='orange', annotation_text='')
    fig6.add_trace(go.Scatter(x=[None], y=[None], mode='lines',
                              line=dict(color='orange', dash='dash', width=2),
                              name=f'Mediana general: {mediana_odo_general/1000:.0f},000 millas'))
    fig6.update_layout(title_text='Distribución de Kilometraje por Tipo de Vehículo',
                       yaxis_title='Odómetro (millas)', xaxis_title='Tipo de vehículo',
                       plot_bgcolor='white', showlegend=True)
    st.plotly_chart(fig6, use_container_width=True)
