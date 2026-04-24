import os
import streamlit as st


def renderizar_pagina_listas():
    st.title("📚 Materiais de Apoio e Listas")
    st.write("Baixe nossos PDFs com exercícios resolvidos e propostos para praticar o que você aprendeu.")
    st.markdown("<br>", unsafe_allow_html=True)

    # 1. Encontra a pasta onde este código está (pasta utils)
    diretorio_utils = os.path.dirname(os.path.abspath(__file__))

    # 2. Dá um passo para trás para voltar para a pasta principal (limite_inteligente)
    diretorio_raiz = os.path.dirname(diretorio_utils)

    # 3. Entra na pasta de PDFs
    pasta_pdfs = os.path.join(diretorio_raiz, "listas_pdf")

    if os.path.exists(pasta_pdfs):
        arquivos_pdf = [f for f in os.listdir(pasta_pdfs) if f.endswith('.pdf')]

        if arquivos_pdf:
            for arquivo in arquivos_pdf:
                caminho_arquivo = os.path.join(pasta_pdfs, arquivo)

                with open(caminho_arquivo, "rb") as f:
                    pdf_bytes = f.read()

                col_texto, col_botao = st.columns([4, 1])
                with col_texto:
                    nome_exibicao = arquivo.replace('.pdf', '').replace('_', ' ').title()
                    st.subheader(f"📄 {nome_exibicao}")
                with col_botao:
                    st.download_button(
                        label="⬇️ Baixar",
                        data=pdf_bytes,
                        file_name=arquivo,
                        mime="application/pdf",
                        key=f"download_{arquivo}"
                    )
                st.markdown("---")
        else:
            st.info("Nenhuma lista foi encontrada na pasta. Estamos preparando novos materiais!")
    else:
        st.warning("Pasta de arquivos não encontrada.")