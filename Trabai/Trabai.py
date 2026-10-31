# %%
import glob
import polars as pl

# %%
ficheiros = glob.glob("*.csv")
dadosRaw = {}
for f in ficheiros:
    dadosRaw[f.replace(".csv", "")] = pl.read_csv(f, separator=";")

# %%
dadosArea = {}
for i in dadosRaw:
    dadosArea[i] = (
        dadosRaw[i]
        .filter(pl.col("Type") == "journal", 
                pl.col("SJR") != "null")
        .with_columns(pl.col("SJR").str.replace(",", ".").cast(pl.Float64))
        .with_columns((pl.col("SJR")/pl.col("SJR").max()).alias("Quantil"))
        .select(["Title", "Issn", "SJR", "SJR Best Quartile", "Quantil"])
        .filter(pl.col("Quantil") >= 0.25)
        .with_columns(pl.lit(i).alias("Area"))
)

# %%
Df = pl.concat(dadosArea.values())

# %%
# Limparemos um caso de cada vez
duplicatos = (
    Df
    .filter(pl.col("Issn").is_duplicated(), pl.col("Title").is_duplicated())
)

DfLimpo = (
    Df
    .sort("Quantil", descending = True)
    .unique(subset=["Issn"], keep = "first")
    .unique(subset=["Title"], keep = "first")
    .sort("Quantil", descending=True)
)






# %%
import streamlit as st

# %%


st.set_page_config(page_title="Busca de Artigos SJR", layout="wide")
st.title("📚 Validação de Score Académico - SJR")

@st.cache_data
def carregar_dados():
    ficheiros = glob.glob("*.csv")
    dadosRaw = {}
    for f in ficheiros:
        dadosRaw[f.replace(".csv", "")] = pl.read_csv(f, separator=";")

    dados = {}
    for i in dadosRaw:
        dados[i] = (
            dadosRaw[i]
            .filter(pl.col("Type") == "journal", 
                    pl.col("SJR") != "null")
            .with_columns(pl.col("SJR").str.replace(",", ".").cast(pl.Float64))
            .with_columns((pl.col("SJR")/pl.col("SJR").max()).alias("Quantil"))
            .select(["Title", "Issn", "SJR", "SJR Best Quartile", "Quantil"])
            .filter(pl.col("Quantil") >= 0.25)
    )
    retrun 

# %%
