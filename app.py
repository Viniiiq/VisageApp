import streamlit as st
from PIL import Image
import numpy as np
import plotly.graph_objects as go
import os

# --- CONFIGURAÇÕES INICIAIS ---
st.set_page_config(page_title="BeautyScore", layout="wide")

# --- DIRETÓRIO PARA HISTÓRICO ---
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# --- ESTILOS DE TEMA ---
theme = st.radio("Escolha o tema:", ["Claro", "Escuro"])
if theme == "Claro":
    st.markdown("""
        <style>
        body {background-color: #f9f9f9; color: #000000;}
        </style>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        body {background-color: #121212; color: #ffffff;}
        </style>
        """, unsafe_allow_html=True)

# --- SELEÇÃO DE VERSÃO ---
st.sidebar.title("Versão do App")
version = st.sidebar.radio("Escolha sua versão:", ["Gratuita", "Premium"])

# --- ABAS ---
tabs = st.tabs(["Upload", "Análise", "Histórico"])

# --- MÉTRICAS PREMIUM ---
premium_metrics = [
    "Deep-set eyes", "Eye spacing", "Eye size", "Eye symmetry",
    "Thick eyebrows", "Arch shape", "Eyebrow symmetry",
    "Nose width", "Nose length", "Nose tip shape", "Nose symmetry",
    "Lip fullness", "Lip symmetry", "Lip shape",
    "Jawline definition", "Chin shape", "Jaw symmetry",
    "Cheekbone prominence", "Cheek symmetry",
    "Face shape"
]

# --- ABA UPLOAD ---
with tabs[0]:
    st.header("Upload de Foto")
    uploaded_file = st.file_uploader("Envie sua foto", type=["png","jpg","jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Sua foto", use_column_width=True)
        # Salva permanentemente na pasta uploads
        file_path = os.path.join("uploads", uploaded_file.name)
        image.save(file_path)
        st.success("Foto carregada com sucesso!")

# --- ABA ANÁLISE ---
with tabs[1]:
    st.header("Análise Facial")
    if uploaded_file:
        st.subheader(f"Versão: {version}")
        if version == "Gratuita":
            st.write("Análise básica: simetria e formato do rosto.")
            st.progress(80)
        else:
            st.write("Análise Premium: métricas detalhadas")
            # Pontuações simuladas
            values = [np.random.randint(60,100) for _ in premium_metrics]

            # Feedback visual com cores: >85 verde, 70-85 amarelo, <70 vermelho
            st.markdown("### Métricas analisadas:")
            for metric, val in zip(premium_metrics, values):
                if val > 85:
                    color = "green"
                elif val > 70:
                    color = "orange"
                else:
                    color = "red"
                st.markdown(f"- {metric}: <span style='color:{color}'>{val}/100</span>", unsafe_allow_html=True)

            # --- GRÁFICO DE TEIA ---
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=premium_metrics,
                fill='toself',
                name='Pontuação'
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0,100])
                ),
                showlegend=False,
                margin=dict(l=30, r=30, t=30, b=30)
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Envie uma foto para visualizar a análise.")

# --- ABA HISTÓRICO ---
with tabs[2]:
    st.header("Histórico de Uploads")
    uploaded_images = os.listdir("uploads")
    if uploaded_images:
        st.write("Fotos anteriores:")
        for i, file_name in enumerate(uploaded_images):
            path = os.path.join("uploads", file_name)
            st.image(Image.open(path), caption=f"Foto {i+1}: {file_name}", width=150)
    else:
        st.info("Nenhuma foto no histórico ainda.")
