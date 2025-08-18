import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --------------------------
# Configuração inicial
# --------------------------
st.set_page_config(page_title="VisageApp", layout="centered")

# --------------------------
# Tema Claro/Escuro
# --------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

theme_colors = {
    "light": {"bg": "#FFFFFF", "text": "#000000"},
    "dark": {"bg": "#111111", "text": "#FFFFFF"}
}

st.markdown(
    f"""
    <style>
    body {{ background-color: {theme_colors[st.session_state.theme]['bg']}; color: {theme_colors[st.session_state.theme]['text']}; }}
    </style>
    """,
    unsafe_allow_html=True
)

st.button("Mudar Tema", on_click=toggle_theme)

# --------------------------
# Upload da Foto
# --------------------------
st.header("Upload da sua foto")

uploaded_file = st.file_uploader("Escolha uma foto", type=["png","jpg","jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Sua foto", use_column_width=True)
    
    # --------------------------
    # Checar versão
    # --------------------------
    premium_user = st.checkbox("Usuário Premium")

    # Simulação de processamento de foto:
    if premium_user:
        # Valores detalhados para gráfico de teia
        categorias = ['Simetria', 'Proporção', 'Tom de Pele', 'Sorriso', 'Olhos', 'Cabelo']
        valores = np.random.randint(50, 100, size=len(categorias))  # aqui você coloca valores reais do processamento
        st.success("Versão Premium: valores detalhados obtidos!")
    else:
        # Versão gratuita: apenas uma nota simples
        categorias = ['Nota']
        valores = [np.random.randint(60, 90)]  # nota simplificada
        st.info(f"Versão gratuita: sua nota é {valores[0]}")

    # --------------------------
    # Gráfico de Teia Seguro
    # --------------------------
    N = len(categorias)
    angulos = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    valores_circular = valores + [valores[0]]  # fecha o gráfico
    angulos_circular = angulos + [angulos[0]]

    fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
    ax.plot(angulos_circular, valores_circular, linewidth=2, linestyle='solid')
    ax.fill(angulos_circular, valores_circular, alpha=0.25)
    ax.set_xticks(angulos)
    ax.set_xticklabels(categorias)
    ax.set_yticklabels([])
    ax.set_title("Gráfico de Teia", va='bottom')
    st.pyplot(fig)

# --------------------------
# Feedback
# --------------------------
st.header("Feedback")
email = st.text_input("Seu email", value="seuemail@gmail.com")
mensagem = st.text_area("Mensagem")

if st.button("Enviar Feedback"):
    if email and mensagem:
        st.success("Obrigado pelo feedback! ✅")
    else:
        st.error("Preencha seu email e mensagem antes de enviar.")
