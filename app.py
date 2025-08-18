import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# Configuração da página
# -------------------------------
st.set_page_config(page_title="💎 VisageScore", layout="wide")

# -------------------------------
# Tema claro/escuro (simples)
# -------------------------------
theme = st.sidebar.radio("Tema", ["Claro", "Escuro"])
if theme == "Escuro":
    plt.style.use("dark_background")
else:
    plt.style.use("default")

# -------------------------------
# Abas principais
# -------------------------------
aba = st.sidebar.radio("Navegação", ["🏠 Principal", "💎 Premium", "✉️ Feedback"])

# -------------------------------
# Aba Principal
# -------------------------------
if aba == "🏠 Principal":
    st.title("💎 VisageScore - Versão Gratuita")
    st.write("Faça upload de uma foto para receber uma análise simples.")

    uploaded_file = st.file_uploader("Envie sua foto", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Sua foto", use_column_width=True)
        st.success("✅ Foto recebida! (Na versão gratuita a análise é limitada.)")

# -------------------------------
# Aba Premium
# -------------------------------
elif aba == "💎 Premium":
    st.title("💎 VisageScore - Versão Premium")
    st.write("Aqui estão métricas avançadas baseadas em estética facial:")

    # Exemplo de valores fictícios (0 a 10)
    metricas = {
        "Canthal Tilt": 7,
        "Jawline": 8,
        "Cheekbones": 6,
        "Eye Spacing": 7,
        "Facial Symmetry": 9,
        "Skin Quality": 8
    }

    categorias = list(metricas.keys())
    valores = list(metricas.values())

    # Fechar o gráfico no círculo
    valores += valores[:1]
    categorias += categorias[:1]

    # Radar chart
    angulos = np.linspace(0, 2 * np.pi, len(categorias), endpoint=False).tolist()
    angulos += angulos[:1]

    fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
    ax.plot(angulos, valores, linewidth=2, linestyle='solid')
    ax.fill(angulos, valores, alpha=0.25)

    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(categorias)

    st.pyplot(fig)

    st.info("🔒 Para usar a versão Premium real, será necessário pagamento futuro.")

# -------------------------------
# Aba Feedback
# -------------------------------
elif aba == "✉️ Feedback":
    st.title("✉️ Feedback")
    st.write("Deixe sua opinião sobre o aplicativo!")

    st.write("📧 Contato: **seuemail@exemplo.com**")

    comentario = st.text_area("Escreva seu feedback:")
    if st.button("Enviar"):
        st.success("✅ Obrigado pelo feedback!")

    st.subheader("⭐ Reviews de Usuários")
    st.write("👉 Aqui você poderá adicionar manualmente feedbacks positivos no futuro.")
