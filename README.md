Fome Zero - Dashboard Estratégico 

Este repositório contém o código de um dashboard interativo desenvolvido com Streamlit. O painel é uma ferramenta de Business Intelligence projetada para fornecer insights estratégicos a partir dos dados da plataforma Fome Zero, auxiliando na tomada de decisão baseada em dados.

1. Problema de Negócio
A Fome Zero é uma plataforma de marketplace de restaurantes. Seus gestores e o CEO precisam de uma visão clara e consolidada do negócio para tomar decisões estratégicas. As principais questões que precisam de respostas são:

Qual o panorama geral da empresa em números (restaurantes, países, cidades)?

Onde a empresa está mais presente e onde há potencial para expansão?

Quais cidades e países possuem os restaurantes mais bem avaliados? E os piores?

Quais tipos de culinária são os mais populares e bem avaliados pelos clientes?

Como a empresa pode identificar seus melhores restaurantes parceiros e aqueles que precisam de mais atenção?

A ausência de uma ferramenta centralizada para responder a essas perguntas dificulta a definição de metas, a alocação de recursos e a identificação de oportunidades de crescimento.

2. Premissas do Negócio
Para a construção deste dashboard, foram consideradas as seguintes premissas:

O conjunto de dados zomato.csv é uma representação fiel e atualizada da operação da empresa.

As métricas de sucesso incluem a quantidade de restaurantes, a diversidade geográfica e culinária, e a média das avaliações dos clientes.

O público-alvo principal da ferramenta são os times de negócio, marketing e o corpo executivo (C-Level).

Os insights gerados pelo dashboard serão utilizados para guiar decisões estratégicas, como expansão de mercado, campanhas de marketing e programas de qualidade para restaurantes parceiros.

3. Estratégia da Solução
Para resolver o problema de negócio, a estratégia adotada foi o desenvolvimento de um dashboard interativo, que permite a exploração dos dados de forma intuitiva. A solução foi implementada com as seguintes etapas:

Coleta e Limpeza de Dados: Tratamento do dataset para garantir a qualidade e a precisão das informações, incluindo renomeação de colunas, tratamento de valores nulos, remoção de duplicatas e outliers.

Engenharia de Features: Criação de novas colunas a partir das existentes (ex: nome do país a partir do código, categoria de preço) para enriquecer a análise.

Desenvolvimento do Dashboard: Utilização de Python com a biblioteca Streamlit para criar a interface web. As visualizações foram construídas com Altair (gráficos) e Folium (mapas).

Organização em Abas: O painel foi dividido em quatro visões estratégicas para facilitar a análise:

Página Principal: Visão geral com métricas-chave e um mapa geográfico interativo.

Visão por Países: Análise comparativa do desempenho entre os países.

Visão por Cidades: Detalhamento do desempenho em nível de cidade.

Visão por Culinárias: Insights sobre a popularidade e qualidade dos diferentes tipos de comida.

Filtros Interativos: Implementação de filtros dinâmicos que permitem ao usuário segmentar os dados por país, cidade ou culinária, personalizando a análise conforme a necessidade.

4. Top 3 Insights de Dados
A análise dos dados através do dashboard revelou os seguintes insights estratégicos:

Concentração de Mercado e Oportunidade de Expansão: A grande maioria dos restaurantes (mais de 60%) está concentrada na Índia. Embora isso demonstre um forte domínio de mercado, também representa um risco de dependência. Países como Austrália, Brasil e Canadá têm uma presença muito pequena, indicando um enorme potencial de crescimento e diversificação geográfica.

Qualidade Associada à Culinária: Tipos de culinária como Italiana, Japonesa e Árabe apresentam consistentemente as maiores médias de avaliação. Isso sugere que os clientes associam essas cozinhas a uma maior qualidade ou que os restaurantes desses segmentos são mais bem-sucedidos na plataforma. A empresa pode usar essa informação para criar campanhas de marketing direcionadas ou para buscar novos parceiros nesses segmentos.

Cidades com Alta e Baixa Performance: O dashboard permite identificar rapidamente as cidades com a maior quantidade de restaurantes bem avaliados (nota > 4.0) e mal avaliados (nota < 2.5). Cidades com muitas avaliações baixas, como Ancara (Turquia), podem necessitar de um plano de ação para melhorar a qualidade dos restaurantes parceiros ou revisar a estratégia de captação local.

5. O Produto Final do Projeto
O produto final é um dashboard interativo online, acessível via navegador web. A ferramenta permite que qualquer membro do time Fome Zero, especialmente os tomadores de decisão, possa:

Visualizar as métricas de desempenho da empresa em tempo real (se conectado a um banco de dados).

Aplicar filtros para analisar mercados ou nichos específicos.

Exportar visualizações e dados para relatórios e apresentações.

Obter respostas rápidas para perguntas de negócio complexas sem a necessidade de conhecimento técnico em análise de dados.

6. Conclusão
O projeto atingiu seu objetivo ao transformar um conjunto de dados brutos em uma ferramenta de BI poderosa e intuitiva. O dashboard soluciona o problema de negócio inicial, fornecendo uma visão 360º da operação da Fome Zero e capacitando a liderança a tomar decisões mais inteligentes e baseadas em evidências.

7. Próximos Passos
Para evoluir o projeto, sugere-se os seguintes passos:

Conexão com Banco de Dados: Migrar a fonte de dados de um arquivo CSV estático para um banco de dados em produção, permitindo análises com dados em tempo real.

Análise Preditiva: Implementar modelos de Machine Learning para prever a nota de um restaurante com base em suas características, auxiliando na prospecção de novos parceiros.

Sistema de Alertas: Criar um sistema que notifique os gestores quando uma métrica importante (ex: queda na avaliação média de uma cidade) atinge um limiar crítico.

Análise de Sentimento: Adicionar uma funcionalidade que processe os comentários textuais das avaliações para extrair insights qualitativos sobre o que os clientes mais gostam e odeiam.

Deploy em Nuvem: Publicar o dashboard em um serviço de nuvem (como Streamlit Cloud, AWS ou GCP) para garantir alta disponibilidade e fácil acesso para toda a empresa.

📊 Visão Geral
O "Fome Zero - Dashboard do CEO" é uma ferramenta de Business Intelligence (BI) criada para fornecer insights estratégicos a partir de dados de restaurantes. O objetivo é permitir uma análise aprofundada e intuitiva sobre a distribuição e a performance dos restaurantes cadastrados na plataforma, auxiliando na tomada de decisões.

O dashboard é dividido em quatro seções principais, cada uma com uma visão específica dos dados:

Página Principal: Oferece uma visão geral com métricas-chave e um mapa interativo.

Visão por Países: Compara o desempenho e a presença da Fome Zero em diferentes países.

Visão por Cidades: Analisa as cidades com maior concentração e melhores avaliações de restaurantes.

Visão por Culinárias: Explora os tipos de culinária mais populares e bem avaliados.

✨ Funcionalidades
Métricas Gerais: Contagem de restaurantes, países, cidades, avaliações e tipos de culinária únicos.

Mapa Interativo: Visualização geoespacial dos restaurantes, com marcadores coloridos por faixa de avaliação e agrupados por proximidade (clusters).

Gráficos Comparativos: Análises visuais sobre a quantidade de restaurantes, cidades e média de avaliações por país.

Rankings de Cidades: Identificação das cidades com mais restaurantes, melhores e piores avaliações médias.

Análise de Culinária: Rankings dos melhores e piores tipos de culinária com base na nota média e uma tabela com os restaurantes mais bem avaliados.

Filtros Dinâmicos: Controles na barra lateral para filtrar os dados por país, quantidade de restaurantes a exibir e tipos de culinária, permitindo uma análise personalizada.

🛠️ Estrutura do Código
O script Python é estruturado da seguinte forma:

Importação de Bibliotecas: Inclui streamlit para a interface web, pandas para manipulação de dados, altair para gráficos, folium para o mapa e inflection para padronização de nomes de colunas.

Funções de Pré-processamento:

rename_columns: Converte os nomes das colunas para o formato snake_case.

create_price_type: Classifica os restaurantes em categorias de preço ('cheap', 'normal', 'expensive', 'gourmet').

get_rating_color: Define a cor do marcador no mapa com base na nota de avaliação.

load_and_preprocess_data: Função principal que carrega o dataset, aplica todas as etapas de limpeza (remoção de nulos, duplicatas, outliers) e engenharia de features.

Configuração da Página Streamlit: Define o título, ícone e layout da página, além de injetar CSS para estilizar a barra de navegação.

Barra de Navegação e Filtros (Sidebar): Cria o menu de navegação entre as páginas e os filtros interativos.

Lógica das Páginas: O conteúdo de cada página (Main Page, Countries, Cities, Cuisines) é renderizado dentro de um bloco condicional if/elif, mantendo o código organizado e modular.

🚀 Como Executar o Projeto
Para executar o dashboard localmente, siga os passos abaixo:

1. Pré-requisitos:
Certifique-se de ter o Python instalado e instale as bibliotecas necessárias:

pip install streamlit pandas altair folium inflection

2. Estrutura de Arquivos:
Mantenha a seguinte estrutura de diretórios:

.
├── database/
│   └── zomato.csv
└── dash.teste.py

Atenção: O caminho para o arquivo zomato.csv está fixo no código. Certifique-se de que o caminho r'C:\Users\carol\Downloads\repos\portifolio_projetos\zomato-restaurante\database\zomato.csv' corresponde à localização no seu sistema ou ajuste-o conforme necessário.

3. Comando de Execução:
Abra o terminal na pasta raiz do projeto e execute o seguinte comando:

streamlit run app.py

O dashboard será aberto automaticamente no seu navegador.

🧹 Análise e Pré-processamento de Dados
A qualidade dos dados é fundamental para a análise. A função load_and_preprocess_data realiza as seguintes etapas:

Renomeação de Colunas: Padroniza os nomes das colunas para facilitar o acesso.

Remoção de Colunas Irrelevantes: Exclui colunas que contêm apenas um valor único.

Tratamento de Dados Ausentes: Preenche valores nulos na coluna cuisines e extrai apenas o primeiro tipo de culinária.

Remoção de Duplicatas: Garante que cada registro seja único.

Engenharia de Features:

country: Mapeia o código do país para seu respectivo nome.

price_type: Cria uma categoria de preço com base na coluna price_range.

rating_color_name: Mapeia códigos de cores hexadecimais para nomes de cores.

Filtro de Outliers: Remove registros com custo para duas pessoas (average_cost_for_two) muito discrepantes (acima de 2 desvios padrão da média) para não distorcer as análises.
