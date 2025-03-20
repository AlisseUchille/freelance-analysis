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
st.write("### Informazioni sul dataset")
st.write(df.info())  # Debug: informazioni sul dataset
st.write("### Prime righe del dataset")
st.dataframe(df.head())

# Mostra i nomi delle colonne
st.write("### Nomi delle colonne nel dataset")
st.write(df.columns.tolist())

# Analisi preliminare
st.write("### Statistiche descrittive")
st.write(df.describe())

# Rimuoviamo eventuali righe con dati mancanti
df = df.dropna()

# Debug: verifica la presenza delle colonne chiave
required_columns = ['industry', 'skill', 'earnings', 'job_category', 'job_completed']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    st.write(f"⚠️ Attenzione: Le seguenti colonne sono assenti nel dataset: {missing_columns}")

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

# Debug: verifica il numero di lavori completati > 50 e ≤ 50
if 'job_completed' in df.columns:
    st.write(f"Numero di lavori completati > 50: {df[df['job_completed'] > 50].shape[0]}")
    st.write(f"Numero di lavori completati ≤ 50: {df[df['job_completed'] <= 50].shape[0]}")

# Grafico a torta dei guadagni medi per Job Category
if 'job_category' in df.columns and 'earnings' in df.columns:
    st.write("### Distribuzione Guadagni Medi per Job Category")
    job_avg = df.groupby('job_category')['earnings'].mean().reset_index()
    if not job_avg.empty:
        fig = px.pie(job_avg, names='job_category', values='earnings', title='Guadagni Medi per Job Category', color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig)
    else:
        st.write("⚠️ Nessun dato disponibile per il grafico a torta Job Category!")

# Grafici a torta per Job Completed > 50 e < 50
if 'job_completed' in df.columns and 'job_category' in df.columns and 'earnings' in df.columns:
    df_high_jobs = df[df['job_completed'] > 50]
    df_low_jobs = df[df['job_completed'] <= 50]
    
    if not df_high_jobs.empty:
        st.write("### Guadagni Medi per Job Category (Job Completed > 50)")
        job_avg_high = df_high_jobs.groupby('job_category')['earnings'].mean().reset_index()
        fig_high = px.pie(job_avg_high, names='job_category', values='earnings', title='Guadagni Medi per Job Category (Job Completed > 50)', color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_high)
    else:
        st.write("⚠️ Nessun dato disponibile per Job Completed > 50")
    
    if not df_low_jobs.empty:
        st.write("### Guadagni Medi per Job Category (Job Completed ≤ 50)")
        job_avg_low = df_low_jobs.groupby('job_category')['earnings'].mean().reset_index()
        fig_low = px.pie(job_avg_low, names='job_category', values='earnings', title='Guadagni Medi per Job Category (Job Completed ≤ 50)', color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_low)
    else:
        st.write("⚠️ Nessun dato disponibile per Job Completed ≤ 50")

# Trend dei guadagni nel tempo
if 'date' in df.columns and 'earnings' in df.columns:
    st.write("### Trend dei Guadagni nel Tempo")
    df['date'] = pd.to_datetime(df['date'])
    df_time = df.groupby(df['date'].dt.to_period("M")).mean().reset_index()
    df_time['date'] = df_time['date'].astype(str)
    fig = px.line(df_time, x='date', y='earnings', title='Trend dei Guadagni nel Tempo')
    st.plotly_chart(fig)

st.write("## Analisi completata!")
