import streamlit as st
import numpy as np
from PIL import Image
from skimage import filters, transform

# --------------------------
# Funções de análise
# --------------------------

def calcular_simetria(img_array):
    # Corta ao meio e compara esquerda x direita
    h, w, _ = img_array.shape
    metade = w // 2
    esquerda = img_array[:, :metade]
    direita = np.fliplr(img_array[:, metade:])
    simetria = np.mean(np.abs(esquerda - direita))
    return max(0, 100 - simetria)


def calcular_nitidez(img_array):
    # Usa o gradiente de Sobel como medida de nitidez
    gray = np.mean(img_array, axis=2)
    sobel = filters.sobel(gray)
    return float(np.mean(sobel) * 100)


def calcular_luminosidade(img_array):
    # Brilho médio
    return float(np.mean(img_array) / 2.55)


def calcular_proporcoes(img_array):
    # Aproximação de proporções faciais (sem landmarks)
    h, w, _ = img_array.shape
    proporcao_hw = h / w
    ideal = 1.618  # número áureo
    score = 100 - (abs(proporcao_hw - ideal) * 100)
    return max(0, min(score, 100))


# --------------------------
# App Streamlit
# --------------------------

st.set_page_config(page_title="VisageScore 💎", layout="centered")

st.title("VisageScore 💎")
st.write("Avalie sua foto com análise de estética facial (versão gratuita e premium).")

aba = st.sidebar.radio("Escolha uma seção:", ["Análise", "Premium (paga)", "Feedback"])

# --------------------------
# Aba 1: Gratuita
# --------------------------
if aba == "Análise":
    st.header("Versão Gratuita 🟢")

    uploaded_file = st.file_uploader("Envie uma foto (frontal, boa iluminação)", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        img_array = np.array(img)

        st.image(img, caption="Foto enviada", use_column_width=True)

        # Análises básicas
        sim = calcular_simetria(img_array)
        nit = calcular_nitidez(img_array)
        lum = calcular_luminosidade(img_array)

        st.subheader("Resultados:")
        st.write(f"🔹 **Simetria facial**: {sim:.2f}/100")
        st.write(f"🔹 **Nitidez da imagem**: {nit:.2f}/100")
        st.write(f"🔹 **Luminosidade**: {lum:.2f}/100")

        score = (sim + nit + lum) / 3
        st.success(f"💡 Sua nota estética (versão gratuita): **{score:.2f}/100**")

# --------------------------
# Aba 2: Premium
# --------------------------
elif aba == "Premium (paga)":
    st.header("Versão Premium 🔵")

    st.info("🔒 Área Premium: desbloqueie análises avançadas após pagamento.")

    uploaded_file = st.file_uploader("Envie uma foto para análise avançada", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        img_array = np.array(img)

        st.image(img, caption="Foto enviada", use_column_width=True)

        # Análises premium
        sim = calcular_simetria(img_array)
        nit = calcular_nitidez(img_array)
        lum = calcular_luminosidade(img_array)
        prop = calcular_proporcoes(img_array)

        st.subheader("Resultados Premium:")
        st.write(f"🔹 **Simetria facial**: {sim:.2f}/100")
        st.write(f"🔹 **Nitidez da imagem**: {nit:.2f}/100")
        st.write(f"🔹 **Luminosidade**: {lum:.2f}/100")
        st.write(f"🔹 **Proporções faciais (áurea)**: {prop:.2f}/100")

        score = (sim + nit + lum + prop) / 4
        st.success(f"💎 Sua nota estética premium: **{score:.2f}/100**")

# --------------------------
# Aba 3: Feedback
# --------------------------
elif aba == "Feedback":
    st.header("Feedback 📝")
    st.write("📧 Entre em contato: **seuemail@exemplo.com**")
    st.write("⭐ Deixe aqui sua opinião! (em breve reviews serão exibidas)")
