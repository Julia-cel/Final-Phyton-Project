import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(
    page_title="Data Careers & Salary Overview ",
    page_icon="📊",
    layout="wide",
)
df_clean=pd.read_csv("https://raw.githubusercontent.com/Julia-cel/Final-Phyton-Project/refs/heads/main/Final_Phyton_Project.csv")
# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filters")

# Filtro de Ano
Years = sorted(df_clean['work_year'].unique())
SelectedYears = st.sidebar.multiselect("Year", Years, default=Years)

# Filtro de Senioridade
WorkExperience = sorted(df_clean['experience_level'].unique())
SelectedWorkExperience = st.sidebar.multiselect("Work Experience", WorkExperience, default=WorkExperience)

# Filtro por Tipo de Contrato
employment_type = sorted(df_clean['employment_type'].unique())
SelectedEmploymentType = st.sidebar.multiselect("Employment Type", employment_type, default=employment_type)

# Filtro por Tamanho da Empresa
company_size = sorted(df_clean['company_size'].unique())
SelectedCompanySize = st.sidebar.multiselect("Company Size", company_size, default=company_size)
df_clean_filtrado = df_clean[
    (df_clean['work_year'].isin(SelectedYears)) &
    (df_clean['experience_level'].isin(SelectedWorkExperience)) &
    (df_clean['employment_type'].isin(SelectedEmploymentType)) &
    (df_clean['company_size'].isin(SelectedCompanySize))
]
st.title("🎲 Data Careers & Salaries Dashboard ")
st.markdown("Explore the salaries data for data professionals worldwide in the last few years. Use the filters on the left to customize your view.")
# --- Métricas Principais (KPIs) ---
st.subheader("Key Metrics (Annual salary in USD)") 
if not df_clean_filtrado.empty:
    salary_mid = df_clean_filtrado['salary_in_usd'].mean()
    salary_max = df_clean_filtrado['salary_in_usd'].max()
    total_records = df_clean_filtrado.shape[0]
    most_frequent_job = df_clean_filtrado["job_title"].mode()[0]
else:
    salary_mid, salary_max, total_records, most_frequent_job = 0, 0, 0, ""

col1, col2, col3, col4 = st.columns(4)
col1.metric("Average Salary", f"${salary_mid:,.0f}")
col2.metric("Maximum Salary", f"${salary_max:,.0f}")
col3.metric("Total Records", f"{total_records:,}")
col4.metric("Most Common Data Role", most_frequent_job)
# --- Análises Visuais com Plotly ---
st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_clean_filtrado.empty:
        top_roles = df_clean_filtrado.groupby('job_title')['salary_in_usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_cargos = px.bar(
            top_roles,
            x='salary_in_usd',
            y='job_title',
            orientation='h',
            title="Top 10 jobs by Average Salary",
            labels={'salary_in_usd': 'Average Annual Salary (USD)', 'job_title': ''}
        )
        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_cargos, use_container_width=True) ##Code to display the chart
    else:
        st.warning("No data available to display job chart.")

with col_graf2:
    if not df_clean_filtrado.empty:
        grafico_hist = px.histogram(
            df_clean_filtrado,
            x='salary_in_usd',
            nbins=30,
            title="Annual Salary Distribution",
            labels={'salary_in_usd': 'Salary Range (USD)', 'count': ''}
        )
        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("No data available to display salary distribution chart.")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_clean_filtrado.empty:
        remote_count = df_clean_filtrado['remote_ratio'].value_counts().reset_index()
        remote_count.columns = ['Work_Mode', 'Quantity']
        grafico_remoto = px.pie(
            remote_count,
            names='Work_Mode',
            values='Quantity',
            title='Proportion of work modes',
            hole=0.5
        )
        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
            st.warning("No data available to display work mode chart.")
    
with col_graf4:
    if not df_clean_filtrado.empty: import pycountry def iso2_to_iso3(code):
            try:
                return pycountry.countries.get(alpha_2=code).alpha_3
            except:
                return None

        df_clean['Country_iso3'] = df_clean['employee_residence'].apply(iso2_to_iso3)
        df_ds = df_clean[df_clean['job_title'] == 'Data Scientist']
        AverageDS = df_ds.groupby('Country_iso3')['salary_in_usd'].mean().reset_index()

        fig = px.choropleth(
            AverageDS,
            locations='Country_iso3',
            color='salary_in_usd',
            hover_name='Country_iso3',
            color_continuous_scale='rdylgn'
        )

        fig.update_layout(title_x=0.1)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available to display country chart.")

st.subheader("Detailed Data")

st.dataframe(df_clean_filtrado)



