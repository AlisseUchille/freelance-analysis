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

# Debug: verifica la presenza delle colonne chiave
required_columns = ['industry', 'skill', 'earnings', 'job_category', 'job_completed']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    st.write(f"⚠️ Attenzione: Le seguenti colonne sono assenti nel dataset: {missing_columns}")

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

# Grafici a torta per Job Completed > 50 e <= 50
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

st.write("## Analisi completata!")
