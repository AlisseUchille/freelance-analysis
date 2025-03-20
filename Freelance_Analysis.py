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

# Rimuoviamo eventuali righe con dati mancanti
df = df.dropna()

# Rendiamo i nomi delle colonne case insensitive
df.columns = df.columns.str.lower()

# Formattazione delle colonne numeriche in dollari
df['earnings_usd'] = df['earnings_usd'].apply(lambda x: f"${x:,.2f}")
df['hourly_rate'] = df['hourly_rate'].apply(lambda x: f"${x:,.2f}")

# Debug: mostra informazioni sul dataset
st.write("### Informazioni sul dataset")
st.write(df.info())  # Debug: informazioni sul dataset
st.write("### Prime righe del dataset")
st.dataframe(df.head())

# Mostra i nomi delle colonne
st.write("### Nomi delle colonne nel dataset")
st.write(df.columns.tolist())

# Statistiche descrittive
st.write("### Statistiche descrittive")
st.write(df.describe())

# Debug: verifica la presenza delle colonne chiave
required_columns = ['job_category', 'job_completed', 'earnings_usd', 'hourly_rate']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    st.write(f"⚠️ Attenzione: Le seguenti colonne sono assenti nel dataset: {missing_columns}")

# Grafico Guadagni Medi per Categoria Lavorativa
if 'job_category' in df.columns and 'earnings_usd' in df.columns:
    st.write("### Guadagni Medi per Categoria Lavorativa")
    df['earnings_usd'] = df['earnings_usd'].replace('[\$,]', '', regex=True).astype(float)
    job_avg = df.groupby('job_category')['earnings_usd'].mean().reset_index()
    fig = px.bar(job_avg, x='job_category', y='earnings_usd', title='Guadagni Medi per Categoria Lavorativa')
    st.plotly_chart(fig)

# Grafici a torta per Job Completed > 50 e <= 50
if 'job_completed' in df.columns and 'job_category' in df.columns and 'earnings_usd' in df.columns:
    df_high_jobs = df[df['job_completed'] > 50]
    df_low_jobs = df[df['job_completed'] <= 50]
    
    if not df_high_jobs.empty:
        st.write("### Guadagni Medi per Job Category (Job Completed > 50)")
        job_avg_high = df_high_jobs.groupby('job_category')['earnings_usd'].mean().reset_index()
        fig_high = px.pie(job_avg_high, names='job_category', values='earnings_usd', title='Guadagni Medi per Job Category (Job Completed > 50)', color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_high)
    else:
        st.write("⚠️ Nessun dato disponibile per Job Completed > 50")
    
    if not df_low_jobs.empty:
        st.write("### Guadagni Medi per Job Category (Job Completed ≤ 50)")
        job_avg_low = df_low_jobs.groupby('job_category')['earnings_usd'].mean().reset_index()
        fig_low = px.pie(job_avg_low, names='job_category', values='earnings_usd', title='Guadagni Medi per Job Category (Job Completed ≤ 50)', color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_low)
    else:
        st.write("⚠️ Nessun dato disponibile per Job Completed ≤ 50")

st.write("## Analisi completata!")
