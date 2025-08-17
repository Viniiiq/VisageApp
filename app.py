# app.py
import streamlit as st
from PIL import Image
import numpy as np
import mediapipe as mp

# ====== Configurações do Streamlit ======
st.set_page_config(page_title="💎 VisageScore", layout="centered")

# ====== Funções de análise facial ======
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)

def analisar_beleza(img):
    img_rgb = np.array(img.convert('RGB'))
    h, w, _ = img_rgb.shape

    resultados = face_mesh.process(img_rgb)
    if not resultados.multi_face_landmarks:
        return None, ["❌ Nenhum rosto detectado."]

    rosto = resultados.multi_face_landmarks[0]
    pontos = [(int(lm.x*w), int(lm.y*h)) for lm in rosto.landmark]

    # Pontos principais
    olho_esq, olho_dir = pontos[33], pontos[263]
    sobrancelha_esq, sobrancelha_dir = pontos[105], pontos[334]
    nariz_top, nariz_base = pontos[1], pontos[168]
    queixo_esq, queixo_dir = pontos[152], pontos[234]
    boca_sup, boca_inf = pontos[13], pontos[14]

    # Medidas e proporções
    distancia_olhos = np.linalg.norm(np.array(olho_esq) - np.array(olho_dir))
    altura_nariz = np.linalg.norm(np.array(nariz_top) - np.array(nariz_base))
    largura_queixo = np.linalg.norm(np.array(queixo_esq) - np.array(queixo_dir))
    altura_labios = np.linalg.norm(np.array(boca_sup) - np.array(boca_inf))

    inclin_sobrancelha_esq = np.degrees(np.arctan2(sobrancelha_esq[1]-olho_esq[1], sobrancelha_esq[0]-olho_esq[0]))
    inclin_sobrancelha_dir = np.degrees(np.arctan2(sobrancelha_dir[1]-olho_dir[1], sobrancelha_dir[0]-olho_dir[0]))
    sim_sobrancelha = max(0, 1 - abs(inclin_sobrancelha_esq - inclin_sobrancelha_dir)/30)

    inclinacao_rosto = np.degrees(np.arctan2(queixo_dir[1]-queixo_esq[1], queixo_dir[0]-queixo_esq[0]))

    # Valores de referência (pode ajustar)
    ref_distancia_olhos = w*0.3
    ref_altura_nariz = w*0.15
    ref_largura_queixo = distancia_olhos
    ref_sim_sobrancelha = 0.8
    ref_inclinacao_rosto = 0

    alertas = []

    if distancia_olhos < ref_distancia_olhos:
        alertas.append(f"Distância olhos abaixo da média: {distancia_olhos:.1f}px")
    if altura_nariz < ref_altura_nariz:
        alertas.append(f"Altura do nariz abaixo da média: {altura_nariz:.1f}px")
    if largura_queixo < ref_largura_queixo:
        alertas.append(f"Largura do queixo abaixo da média: {largura_queixo:.1f}px")
    if sim_sobrancelha < ref_sim_sobrancelha:
        alertas.append(f"Sobrancelhas desiguais (simetria: {sim_sobrancelha:.2f})")
    if abs(inclinacao_rosto) > ref_inclinacao_rosto+10:
        alertas.append(f"Inclinação geral do rosto fora da média: {inclinacao_rosto:.1f}°")

    if not alertas:
        alertas.append("✅ Todos os valores estão na média ou acima dela!")

    # Nota de beleza (0-10)
    nota = 10 - len([a for a in alertas if "abaixo" in a or "fora" in a])
    nota = max(0, min(10, nota))

    return nota, alertas

# ====== Interface ======
st.title("💎 VisageScore")

# Abas
abas = st.tabs(["Grátis", "Versão Paga", "Feedback"])

with abas[0]:
    st.header("Versão Gratuita")
    st.write("Faça upload da sua foto para análise básica.")
    uploaded_file = st.file_uploader("Escolha uma imagem", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Sua foto", use_column_width=True)
        nota, alertas = analisar_beleza(img)
        if nota is None:
            st.warning(alertas[0])
        else:
            st.subheader(f"Nota de Beleza: {nota}/10")
            for a in alertas:
                st.write(a)

with abas[1]:
    st.header("Versão Paga")
    st.write("Receba análise completa, com relatórios detalhados e feedback avançado.")
    st.info("💳 Pagamento futuro aqui (simulação)")
    uploaded_file = st.file_uploader("Escolha uma imagem para análise completa", key="paga")
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Sua foto", use_column_width=True)
        nota, alertas = analisar_beleza(img)
        if nota is None:
            st.warning(alertas[0])
        else:
            st.subheader(f"Nota de Beleza Completa: {nota}/10")
            for a in alertas:
                st.write(a)
            st.success("Relatório completo disponível!")

with abas[2]:
    st.header("Feedback")
    st.write("Envie seu feedback ou reviews.")
    st.text("Email para contato: seuemail@exemplo.com")
    st.text_area("Deixe seu comentário ou review aqui:")
