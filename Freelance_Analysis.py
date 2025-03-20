import pandas as pd
import streamlit as st
import plotly.express as px

# Titolo della web app
st.title("Analisi Freelance Earnings")

# Descrizione dell'analisi
st.markdown(
    """
    ### Obiettivo dell'analisi
    Questo dataset fornisce informazioni dettagliate sui guadagni dei freelancer e sulle tendenze del mercato del lavoro
    in vari settori e categorie di competenze. L'obiettivo è aiutare i professionisti, i ricercatori e chi cerca lavoro
    a comprendere meglio le dinamiche salariali e la domanda nell'economia del lavoro autonomo.
    """
)

# Caricamento automatico del dataset dalla repository
DATA_PATH = "freelancer_earnings_bd.csv"  # Modifica con il nome corretto del file

df = pd.read_csv(DATA_PATH)
st.write("### Anteprima del dataset")
st.dataframe(df.head())

# Mostra i nomi delle colonne
st.write("### Nomi delle colonne nel dataset")
st.write(df.columns.tolist())

# Analisi preliminare
st.write("### Statistiche descrittive")
st.write(df.describe())

# Controllo valori mancanti
st.write("### Valori mancanti")
st.write(df.isnull().sum())

# Rimuoviamo eventuali righe con dati mancanti
df = df.dropna()

# Selezione interattiva dei filtri
industry_filter = st.selectbox("Seleziona un settore", df['industry'].unique()) if 'industry' in df.columns else None
skill_filter = st.selectbox("Seleziona una skill", df['skill'].unique()) if 'skill' in df.columns else None

# Filtriamo il dataset in base alla selezione
if industry_filter:
    df = df[df['industry'] == industry_filter]
if skill_filter:
    df = df[df['skill'] == skill_filter]

# Grafico Guadagni Medi per Settore
if 'industry' in df.columns and 'earnings' in df.columns:
    st.write("### Guadagni Medi per Settore")
    industry_avg = df.groupby('industry')['earnings'].mean().reset_index()
    fig = px.bar(industry_avg, x='industry', y='earnings', title='Guadagni Medi per Settore')
    st.plotly_chart(fig)

# Grafico delle Skill più richieste
if 'skill' in df.columns:
    st.write("### Le Skill più Richieste")
    skill_count = df['skill'].value_counts().reset_index()
    skill_count.columns = ['skill', 'count']
    fig = px.bar(skill_count[:10], x='skill', y='count', title='Le Skill più Richieste')
    st.plotly_chart(fig)

# Trend dei guadagni nel tempo
if 'date' in df.columns and 'earnings' in df.columns:
    st.write("### Trend dei Guadagni nel Tempo")
    df['date'] = pd.to_datetime(df['date'])
    df_time = df.groupby(df['date'].dt.to_period("M")).mean().reset_index()
    df_time['date'] = df_time['date'].astype(str)
    fig = px.line(df_time, x='date', y='earnings', title='Trend dei Guadagni nel Tempo')
    st.plotly_chart(fig)

st.write("## Analisi completata!")
