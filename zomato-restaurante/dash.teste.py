# --- Importação das Bibliotecas Necessárias ---
import inflection
import streamlit as st
import pandas as pd
import altair as alt
import folium
from folium.plugins import MarkerCluster
import streamlit.components.v1 as components

# =====================================================================
# FUNÇÕES AUXILIARES DE PRÉ-PROCESSAMENTO E LÓGICA
# =====================================================================


def rename_columns(dataframe):
    """
    Renomeia as colunas do DataFrame para o formato snake_case.
    Exemplo: 'Restaurant ID' -> 'restaurant_id'.
    """
    df = dataframe.copy()

    # Funções auxiliares para transformação dos nomes
    def title(x): return inflection.titleize(x)
    def remove_sp(x): return x.replace(" ", "")
    def undersc(x): return inflection.underscore(x)

    # Aplica as transformações em sequência
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(remove_sp, cols_old))
    cols_new = list(map(undersc, cols_old))

    df.columns = cols_new
    return df


def create_price_type(price_range):
    """
    Cria uma categoria de preço (string) com base no valor numérico de price_range.
    """
    if price_range == 1:
        return 'cheap'
    elif price_range == 2:
        return 'normal'
    elif price_range == 3:
        return 'expensive'
    else:
        return 'gourmet'


def get_rating_color(rating):
    """
    Retorna uma cor com base na nota de avaliação para usar nos marcadores do mapa Folium.
    """
    if rating >= 4.5:
        return 'green'
    elif rating >= 3.5:
        return 'lightgreen'
    elif rating >= 2.5:
        return 'orange'
    else:
        return 'red'

# =====================================================================
# CARREGAMENTO E LIMPEZA PRINCIPAL DOS DADOS
# =====================================================================


@st.cache_data  # Habilita o cache para otimizar o carregamento
def load_and_preprocess_data(file_path):
    """
    Carrega o arquivo CSV e aplica todas as etapas de limpeza e pré-processamento.
    """
    df = pd.read_csv(file_path)

    # 1. Renomear colunas para o padrão snake_case
    df = rename_columns(df)

    # 2. Remover colunas com um único valor (não agregam informação)
    single_val_cols = [col for col in df.columns if df[col].nunique() == 1]
    df.drop(columns=single_val_cols, inplace=True)

    # 3. Tratar dados nulos em 'cuisines' e padronizar para o primeiro tipo
    df['cuisines'] = df['cuisines'].fillna('unknown')
    df['cuisines'] = df['cuisines'].apply(lambda x: x.split(',')[0].strip())

    # 4. Remover registros duplicados
    df.drop_duplicates(inplace=True)

    # 5. Mapear 'country_code' para o nome do país
    COUNTRIES = {
        1: "India", 14: "Australia", 30: "Brazil", 37: "Canada",
        94: "Indonesia", 148: "New Zeland", 162: "Philippines",
        166: "Qatar", 184: "Singapure", 189: "South Africa",
        191: "Sri Lanka", 208: "Turkey", 214: "United Arab Emirates",
        215: "England", 216: "United States of America"
    }
    df['country'] = df['country_code'].map(COUNTRIES)

    # 6. Criar coluna 'price_type' com base na 'price_range'
    df['price_type'] = df['price_range'].apply(create_price_type)

    # 7. Mapear código de cor para nome da cor
    COLORS = {
        "3F7E00": "darkgreen", "5BA829": "green", "9ACD32": "lightgreen",
        "CDD614": "orange", "FFBA00": "red", "CBCBC8": "darkred",
        "FF7800": "darkred"
    }
    df['rating_color_name'] = df['rating_color'].map(COLORS)

    # 8. Filtrar outliers de custo para não distorcer as médias
    custo = df['average_cost_for_two']
    limite = custo.mean() + 2 * custo.std()
    df = df[custo <= limite].copy()

    # 9. Resetar o índice do DataFrame final
    df.reset_index(drop=True, inplace=True)
    return df

# =====================================================================
# CONFIGURAÇÃO INICIAL DA PÁGINA STREAMLIT
# =====================================================================


st.set_page_config(
    page_title="Fome Zero - Dashboard do CEO",
    page_icon="🍽️",
    layout="wide"
)

# Carrega e processa os dados (usando o cache se disponível)
# ATENÇÃO: O caminho do arquivo está fixo. Modifique se necessário.
file_path = 'zomato-restaurante/database/zomato.csv'
df_raw = load_and_preprocess_data(file_path)

# Injetar CSS para estilizar o menu de navegação na sidebar
st.markdown("""
<style>
    /* Esconde o círculo do radio button */
    .stRadio > label > div[data-testid="stFlexbox"] > div:first-child {
        display: none;
    }
    /* Estilo para o label do radio button (texto/emoji) */
    .stRadio > label {
        padding: 10px 15px;
        margin-bottom: 5px;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.2s, color 0.2s;
    }
    /* Estilo para o item selecionado */
    .stRadio > label[data-baseweb="radio"][aria-checked="true"] {
        background-color: #e0e0e0;
        font-weight: bold;
        color: #1a1a1a;
    }
    /* Estilo de hover para os itens */
    .stRadio > label:hover {
        background-color: rgba(150, 150, 150, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# SIDEBAR (BARRA LATERAL) DE NAVEGAÇÃO E FILTROS
# =====================================================================

st.sidebar.title("Fome Zero")

# Menu de navegação principal
pages_display = ["📊 Main Page", "🌍 Countries", "🏙️ Cities", "🍜 Cuisines"]
selected_page_display = st.sidebar.radio(
    "Navegação",
    pages_display,
    index=0,
    key="sidebar_navigation_radio",
    label_visibility="collapsed"
)

# Mapeia o nome de exibição para um ID interno para a lógica de páginas
page_id_map = {
    "📊 Main Page": "main_page",
    "🌍 Countries": "countries_page",
    "🏙️ Cities": "cities_page",
    "🍜 Cuisines": "cuisines_page"
}
selected_page_id = page_id_map[selected_page_display]

# =====================================================================
# LÓGICA DE EXIBIÇÃO DAS PÁGINAS
# =====================================================================

# --- PÁGINA 1: MAIN PAGE (VISÃO GERAL) ---
if selected_page_id == "main_page":
    st.title("🍽️ Fome Zero - Dashboard")
    st.markdown(
        "O Melhor lugar para encontrar seu mais novo restaurante favorito!")

    st.sidebar.markdown("---")
    st.sidebar.markdown("## Filtros")
    st.sidebar.markdown(
        "Escolha o(s) País(es) que Deseja visualizar os Restaurantes")

    # Filtro de país para a Main Page
    unique_countries = sorted(df_raw['country'].unique().tolist())
    selected_countries = st.sidebar.multiselect(
        "País(es)",
        unique_countries,
        default=unique_countries
    )

    # Aplica o filtro de país ao DataFrame
    if selected_countries:
        df_filtered = df_raw[df_raw['country'].isin(selected_countries)]
    else:
        df_filtered = pd.DataFrame()  # DataFrame vazio se nada for selecionado

    st.header("📊 Métricas Gerais")

    # Exibe as métricas em colunas
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Restaurantes",
                  f"{df_filtered['restaurant_id'].nunique():.0f}")
    with col2:
        st.metric("Países", f"{df_filtered['country'].nunique()}")
    with col3:
        st.metric("Cidades", f"{df_filtered['city'].nunique()}")
    with col4:
        st.metric("Avaliações", f"{df_filtered['votes'].sum():,}")
    with col5:
        st.metric("Culinárias", f"{df_filtered['cuisines'].nunique()}")

    st.markdown("---")

    # Mapa de Restaurantes com Folium
    st.header("📍 Mapa de Restaurantes")
    df_map_data = df_filtered.dropna(subset=['latitude', 'longitude']).copy()

    if not df_map_data.empty:
        map_center = [df_map_data['latitude'].mean(
        ), df_map_data['longitude'].mean()]
        zomato_map = folium.Map(location=map_center, zoom_start=2)
        marker_cluster = MarkerCluster().add_to(zomato_map)

        # Adiciona marcadores ao cluster
        for _, row in df_map_data.iterrows():
            popup_html = f"""
            <b>{row['restaurant_name']}</b><br>
            Culinária: {row['cuisines']}<br>
            Avaliação: {row['aggregate_rating']}/5.0 ({row['votes']:.0f} votos)<br>
            Custo p/ dois: {row['currency']} {row['average_cost_for_two']:.2f}
            """
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color=get_rating_color(
                    row['aggregate_rating']), icon='cutlery', prefix='fa')
            ).add_to(marker_cluster)

        # Renderiza o mapa no Streamlit
        components.html(zomato_map._repr_html_(), height=500, scrolling=True)
    else:
        st.info("Não há dados para exibir no mapa com os filtros selecionados.")

# --- PÁGINA 2: COUNTRIES (VISÃO PAÍSES) ---
elif selected_page_id == "countries_page":
    st.title("🌍 Visão por Países")

    # Filtros específicos para esta página
    st.sidebar.markdown("---")
    st.sidebar.markdown("## Filtros")
    unique_countries = sorted(df_raw['country'].unique().tolist())
    selected_countries = st.sidebar.multiselect(
        "País(es)",
        unique_countries,
        default=unique_countries,
        key="countries_filter"
    )

    if selected_countries:
        df_filtered = df_raw[df_raw['country'].isin(selected_countries)]
    else:
        df_filtered = pd.DataFrame()

    if not df_filtered.empty:
        # Gráfico 1: Restaurantes por País
        df_paises = df_filtered.groupby("country")["restaurant_id"].nunique().reset_index().rename(
            columns={"restaurant_id": "quantidade"}).sort_values(by="quantidade", ascending=False)
        grafico_paises = alt.Chart(df_paises).mark_bar().encode(
            x=alt.X("country:N", title="País", sort="-y"),
            y=alt.Y("quantidade:Q", title="Quantidade de Restaurantes"),
            tooltip=["country", "quantidade"]
        ).properties(title="Quantidade de Restaurantes por País")
        st.altair_chart(grafico_paises, use_container_width=True)

        st.markdown("---")

        # Gráfico 2: Cidades por País
        df_cidades_por_pais = df_filtered.groupby("country")["city"].nunique().reset_index(
        ).rename(columns={"city": "quantidade"}).sort_values(by="quantidade", ascending=False)
        grafico_cidades = alt.Chart(df_cidades_por_pais).mark_bar().encode(
            x=alt.X("country:N", title="País", sort="-y"),
            y=alt.Y("quantidade:Q", title="Quantidade de Cidades"),
            tooltip=["country", "quantidade"]
        ).properties(title="Quantidade de Cidades Registradas por País")
        st.altair_chart(grafico_cidades, use_container_width=True)

        st.markdown("---")

        # Gráficos de Média
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Média de Avaliações por País")
            df_avg_votes = df_filtered.groupby('country')['votes'].mean().round(
                2).sort_values(ascending=False).reset_index()
            grafico_media_avaliacoes = alt.Chart(df_avg_votes).mark_bar().encode(
                x=alt.X("country:N", title="País", sort='-y'),
                y=alt.Y("votes:Q", title="Média de Avaliações"),
                tooltip=["country", alt.Tooltip("votes:Q", format=".2f")]
            )
            st.altair_chart(grafico_media_avaliacoes, use_container_width=True)

        with col2:
            st.markdown("##### Média de Custo (Prato p/ 2) por País")
            df_avg_cost = df_filtered.groupby('country')['average_cost_for_two'].mean(
            ).round(2).sort_values(ascending=False).reset_index()
            grafico_media_preco = alt.Chart(df_avg_cost).mark_bar(color='#ff7f0e').encode(
                x=alt.X("country:N", title="País", sort='-y'),
                y=alt.Y("average_cost_for_two:Q",
                        title="Preço Médio (Prato para Dois)"),
                tooltip=["country", alt.Tooltip(
                    "average_cost_for_two:Q", format=".2f")]
            )
            st.altair_chart(grafico_media_preco, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")

# --- PÁGINA 3: CITIES (VISÃO CIDADES) ---
elif selected_page_id == "cities_page":
    st.title("🏙️ Visão por Cidades")

    # Filtros específicos para esta página
    st.sidebar.markdown("---")
    st.sidebar.markdown("## Filtros")
    unique_countries = sorted(df_raw['country'].unique().tolist())
    selected_countries = st.sidebar.multiselect(
        "País(es)",
        unique_countries,
        default=unique_countries,
        key="cities_filter"
    )

    if selected_countries:
        df_filtered = df_raw[df_raw['country'].isin(selected_countries)]
    else:
        df_filtered = pd.DataFrame()

    if not df_filtered.empty:
        # Gráfico 1: Top 10 Cidades com mais restaurantes
        st.header("Top 10 Cidades com Mais Restaurantes")
        df_top_cities = df_filtered.groupby(["city", "country"])["restaurant_id"].nunique().reset_index().rename(
            columns={"restaurant_id": "quantidade"}).sort_values(by="quantidade", ascending=False).head(10)
        grafico_cidades_restaurantes = alt.Chart(df_top_cities).mark_bar().encode(
            x=alt.X("city:N", title="Cidade", sort='-y'),
            y=alt.Y("quantidade:Q", title="Quantidade de Restaurantes"),
            color=alt.Color("country:N", title="País"),
            tooltip=["city", "country", "quantidade"]
        )
        st.altair_chart(grafico_cidades_restaurantes, use_container_width=True)

        st.markdown("---")

        # Gráficos de Avaliação por Cidade
        st.header("Análise de Avaliação por Cidade")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Top 7 Cidades (Avaliação > 4.0)")
            df_acima_4 = df_filtered[df_filtered["aggregate_rating"] > 4.0].groupby(["city", "country"])["restaurant_id"].nunique(
            ).reset_index().rename(columns={"restaurant_id": "quantidade"}).sort_values(by="quantidade", ascending=False).head(7)
            grafico_acima_4 = alt.Chart(df_acima_4).mark_bar().encode(
                x=alt.X("city:N", title="Cidade", sort='-y'),
                y=alt.Y("quantidade:Q", title="Qtd. Restaurantes"),
                color=alt.Color("country:N", title="País"),
                tooltip=["city", "country", "quantidade"]
            )
            st.altair_chart(grafico_acima_4, use_container_width=True)

        with col2:
            st.subheader("Top 7 Cidades (Avaliação < 2.5)")
            df_abaixo_2_5 = df_filtered[df_filtered["aggregate_rating"] < 2.5].groupby(["city", "country"])["restaurant_id"].nunique(
            ).reset_index().rename(columns={"restaurant_id": "quantidade"}).sort_values(by="quantidade", ascending=False).head(7)
            grafico_abaixo_2_5 = alt.Chart(df_abaixo_2_5).mark_bar(color='#d62728').encode(
                x=alt.X("city:N", title="Cidade", sort='-y'),
                y=alt.Y("quantidade:Q", title="Qtd. Restaurantes"),
                color=alt.Color("country:N", title="País"),
                tooltip=["city", "country", "quantidade"]
            )
            st.altair_chart(grafico_abaixo_2_5, use_container_width=True)

        st.markdown("---")

        # Gráfico 3: Cidades com mais tipos de culinária
        st.header("Top 10 Cidades com Maior Diversidade Culinária")
        df_cities_cuisine_count = df_filtered.groupby(["city", "country"])["cuisines"].nunique().reset_index(
        ).rename(columns={"cuisines": "quantidade"}).sort_values(by="quantidade", ascending=False).head(10)
        chart_cities_cuisine_count = alt.Chart(df_cities_cuisine_count).mark_bar().encode(
            x=alt.X("city:N", title="Cidade", sort='-y'),
            y=alt.Y("quantidade:Q", title="Tipos de Culinária Distintos"),
            color=alt.Color("country:N", title="País"),
            tooltip=["city", "country", "quantidade"]
        )
        st.altair_chart(chart_cities_cuisine_count, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")

# --- PÁGINA 4: CUISINES (VISÃO CULINÁRIAS) ---
elif selected_page_id == "cuisines_page":
    st.title("🍜 Visão por Culinárias")

    # Filtros na sidebar
    with st.sidebar:
        st.markdown("---")
        st.markdown("## Filtros")
        country_list = sorted(df_raw['country'].dropna().unique())
        selected_countries = st.multiselect(
            "Países", country_list, default=country_list)

        qtd_restaurantes = st.slider(
            "Qtd. de Restaurantes para exibir", 1, 20, 10)

        cuisine_list = sorted(df_raw['cuisines'].dropna().unique())
        selected_cuisines = st.multiselect(
            "Tipos de Culinária", cuisine_list, default=cuisine_list)

    # Aplica filtros
    df_filtered = df_raw[
        (df_raw["country"].isin(selected_countries)) &
        (df_raw["cuisines"].isin(selected_cuisines))
    ]

    if not df_filtered.empty:
        # Métricas: Melhores restaurantes por tipo de culinária principal
        st.header(f"Top {qtd_restaurantes} Restaurantes Mais Bem Avaliados")
        df_top_n_restaurantes = df_filtered.sort_values(
            by="aggregate_rating", ascending=False).head(qtd_restaurantes)
        st.dataframe(df_top_n_restaurantes[[
            "restaurant_name", "country", "city", "cuisines",
            "aggregate_rating", "average_cost_for_two", "votes"
        ]], use_container_width=True)

        st.markdown("---")

        # Gráficos de melhores e piores culinárias
        st.header("Análise da Avaliação Média por Culinária")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### Top 10 Melhores Culinárias")
            df_melhores_cuisines = df_filtered.groupby("cuisines")["aggregate_rating"].mean().reset_index().rename(
                columns={"aggregate_rating": "nota_media"}).sort_values(by="nota_media", ascending=False).head(10)
            chart_melhores = alt.Chart(df_melhores_cuisines).mark_bar().encode(
                y=alt.Y("cuisines:N", sort='-x', title="Tipo de Culinária"),
                x=alt.X("nota_media:Q", scale=alt.Scale(
                    domain=[0, 5]), title="Média da Avaliação"),
                tooltip=[alt.Tooltip("cuisines"), alt.Tooltip(
                    "nota_media", format=".2f")]
            )
            st.altair_chart(chart_melhores, use_container_width=True)

        with col2:
            st.markdown("##### Top 10 Piores Culinárias")
            # Filtra culinárias com nota > 0 para não pegar 'unknown' ou erros
            df_piores_cuisines = df_filtered[df_filtered['aggregate_rating'] > 0].groupby("cuisines")["aggregate_rating"].mean(
            ).reset_index().rename(columns={"aggregate_rating": "nota_media"}).sort_values(by="nota_media", ascending=True).head(10)
            chart_piores = alt.Chart(df_piores_cuisines).mark_bar(color='#d62728').encode(
                y=alt.Y("cuisines:N", sort='x', title="Tipo de Culinária"),
                x=alt.X("nota_media:Q", scale=alt.Scale(
                    domain=[0, 5]), title="Média da Avaliação"),
                tooltip=[alt.Tooltip("cuisines"), alt.Tooltip(
                    "nota_media", format=".2f")]
            )
            st.altair_chart(chart_piores, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")
