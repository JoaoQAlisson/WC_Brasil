import pandas as pd
import numpy as np
import plotly_express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import streamlit as st
from datetime import date, timedelta

st.set_page_config(
    page_title="Dashboard | World Cup",
    page_icon=":brazil:",
    layout="wide",
)

#carregar dados
df = pd.read_csv('data/results.csv')
df = df[df['tournament'] == 'FIFA World Cup']
df = df[df['date'] < '2026-01-01']
df = df.replace('Brazil', 'Brasil')# Prepração de dados

#Separas as edições 
df["year"] = pd.to_datetime(df["date"]).dt.year.astype(str)

map_copas = {
    "1930": "1930 - Uruguay",
    "1934": "1934 - Italy",
    "1938": "1938 - France",
    "1950": "1950 - Brasil",
    "1954": "1954 - Switzerland",
    "1958": "1958 - Sweden",
    "1962": "1962 - Chile",
    "1966": "1966 - England",
    "1970": "1970 - Mexico",
    "1974": "1974 - Germany",
    "1978": "1978 - Argentina",
    "1982": "1982 - Spain",
    "1986": "1986 - Mexico",
    "1990": "1990 - Italy",
    "1994": "1994 - USA",
    "1998": "1998 - France",
    "2002": "2002 - Korea/Japan",
    "2006": "2006 - Germany",
    "2010": "2010 - South Africa",
    "2014": "2014 - Brasil",
    "2018": "2018 - Russia",
    "2022": "2022 - Qatar"
}

df["edicao"] = df["year"].map(map_copas)

# #Campeões do Mundo
champs = [
    "Uruguay",
    "Italy",
    "Germany",
    "Brasil",
    "England",
    "Argentina",
    "France",
    "Spain",
]

title = pd.DataFrame([
    ["Brasil", 5, [1958,1962,1970,1994,2002]],
    ["Italy", 4,[1938,1934,1982,2006]],
    ["Germany", 4,[1954,1974,1990,2014]],
    ["Argentina", 3,[1978,1986,2022]],
    ["Uruguay" ,2,[1930,1950]],
    ["France", 2,[1998,2018]],
    ["England", 1,[1966]],
    ["Spain", 1,[2010]]
], columns=['Seleção', 'Títulos', 'Anos'])

#quantidade de jogos 
home_match = df["home_team"].value_counts()
away_match = df["away_team"].value_counts()

matches = home_match.add(away_match, fill_value=0).astype(int)
#quantidade de gols
home_score = df.groupby('home_team')['home_score'].sum()
away_score = df.groupby('away_team')['away_score'].sum()
goals_team = home_score.add(away_score, fill_value=0)
goals_team = goals_team.sort_values(ascending=False)
#sofridos
home_conced = df.groupby('home_team')['away_score'].sum()
away_conced = df.groupby('away_team')['home_score'].sum()
goals_conced = home_conced.add(away_conced, fill_value=0)
goals_conced = goals_conced.sort_values(ascending=False)

stats = pd.DataFrame({
    "Jogos": matches,
    'Gols Feitos': goals_team,
    'Gols Sofridos': goals_conced,
    'Média de Gols Feitos': (goals_team/matches).round(2),
    'Média de Gols Sofridos': (goals_conced/matches).round(2)
})
# Nomeia a coluna do índice
stats.index.name = 'team'  

## Gols do brasil por copa
df_Brasil = df[(df['home_team'] == 'Brasil') | (df['away_team'] == 'Brasil')].copy()
scored_hbr = df_Brasil[df_Brasil['home_team'] == 'Brasil'].groupby('edicao')['home_score'].sum()
scored_abr = df_Brasil[df_Brasil['away_team'] == 'Brasil'].groupby('edicao')['away_score'].sum()
conced_hbr = df_Brasil[df_Brasil['home_team'] == 'Brasil'].groupby('edicao')['away_score'].sum()
conced_abr = df_Brasil[df_Brasil['away_team'] == 'Brasil'].groupby('edicao')['home_score'].sum()
scored_Brasil = scored_hbr.add(scored_abr, fill_value=0)
conced_Brasil = conced_hbr.add(conced_abr, fill_value=0)
goals_Brasil_cup = pd.DataFrame({
    'Gols Feitos': scored_Brasil,
    'Gols Sofridos': conced_Brasil
}).reset_index()
goals_Brasil_cup = goals_Brasil_cup.sort_values(by='edicao',ascending=True)
goals_Brasil_cup.rename(columns={'edicao': 'Edição'})

#jogos por copas
matches_br = pd.DataFrame(df_Brasil.groupby('edicao')['edicao'].count().reset_index(name='Partidas'))

st.title(":soccer: Brasil na Copa do Mundo")
st.caption("Dados históricos • 1930 – 2022 • 22 edições")
st.divider()
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    with st.container(border=True):
        st.metric(label="TÍTULOS", value=title.iat[0, 1])
        st.caption("Maior vencedor da história")

with col2:
    with st.container(border=True):
        st.metric(label="PARTICIPAÇÕES", value=len(map_copas))
        st.caption("100% das edições")

with col3:
    with st.container(border=True):
        st.metric(label="PARTIDAS JOGADAS", value=stats.loc['Brasil','Jogos'])
        st.caption("Mais que qualquer seleção")

with col4:
    with st.container(border=True):
        st.metric(label="GOLS MARCADOS", value=int(stats.loc['Brasil','Gols Feitos']))
        st.caption("Seleção que mais marcou")

with col5:
    with st.container(border=True):
        st.metric(label="MÉDIA DE GOLS", value=stats.loc['Brasil', 'Média de Gols Feitos'])
        st.caption("Por partida (geral)")

with col6:
    with st.container(border=True):
        st.metric(label="ÚLTIMO TÍTULO", value="2002")
        st.caption("Korea/Japão • há 24 anos")

'''
A seleção é Brasileira é incontestávelmente a maior seleção da história das copas, muitos dizem ser apenas por conta do das cinco conquistas e do histórico passado, mas será que isso se resume apenas
aos títulos? Análisamos todos os jogos 964 Jogos desde a abertura em 1930 até a final em 2022 e assim pudemos verificar. A seleção Brasileira é realmente a melhor?

**Navegue pelas abas abaixo e descubra por que, nesta Copa, você tem todos os motivos matemáticos e históricos para acreditar.**
'''

st.divider()

options_tab = ['Histórico por Copa', 'Volume de Gols', 'Títulos', 'Comparação entre Campeãs', 'Todos os Jogos de Copa do Mundo']
tab = st.pills("Selecione uma Aba:", options_tab, selection_mode="single")

# with tab1:
if tab == 'Histórico por Copa':
    st.markdown("#### A Constância")
    st.write("Em mais de 90 anos de torneio, o Brasil é o único país a nunca ter ficado de fora de uma edição. Os gráficos abaixo ilustram não apenas a regularidade, mas a tradição de sempre marcar presença ofensiva, edição após edição.")
    with st.container(border=True):
        fig1 = px.bar(goals_Brasil_cup,
            x=goals_Brasil_cup['edicao'],
            y=[goals_Brasil_cup['Gols Feitos'],goals_Brasil_cup['Gols Sofridos']],
            barmode='group',
            title='Gols Marcados e Sofridos em cada Copa',
            color_discrete_sequence = ['#4F0009', '#03A256'],
        )
        anos = goals_Brasil_cup['edicao'].str[:4]
        fig1.update_xaxes(
        tickvals=goals_Brasil_cup['edicao'], 
        ticktext=anos,                
        tickmode='array',
        tickangle=-45                       
        )
        
        fig1.update_layout(
        legend_title_text='',
        xaxis_title='Edição',
        yaxis_title='Gols'
        )

        st.plotly_chart(fig1)

    with st.container(border=True):
        fig2 = go.Figure()
        fig2.add_trace(
            go.Scatter(
            x=matches_br['edicao'],
            y=matches_br['Partidas'],
            mode='lines+markers',     
            line=dict(color='#FFCC00', width=3),
            marker=dict(size=8, color='#FFCC00') 
            )
        )
        fig2.update_layout(title="Quantidade de Partidas do Brasil por Edição")
        fig2.update_xaxes(
        tickvals=matches_br['edicao'], 
        ticktext=anos,                
        tickmode='array',
        tickangle=-45                       
        )
        
        st.plotly_chart(fig2)


# with tab2:
if tab == 'Volume de Gols':
    st.markdown("#### O País do Futebol Ofensivo")
    st.write("O futebol Brasileiro é o futebol do espetáculo, como João Saldanha já afirmava desde os anos 60, Retranca e Brasil não combinam. Ao compararmos a Amarelinha com as outras seleções que já levantaram a taça, a disparidade ofensiva impressiona.")
    with st.container(border=True):
        df_champs = stats.loc[champs]
        df_champs=df_champs.sort_values(by='Gols Feitos', ascending=False)
        fig3 = px.bar(df_champs,
            x=df_champs.index,
            y=['Gols Feitos','Gols Sofridos'],
            barmode='group',
            title='Gols Marcados e Sofridos em cada Copa'
        )
        fig3.update_layout(
        showlegend=False,
        xaxis_title='Seleções',
        yaxis_title='Gols',
        clickmode='event+select'
        )
        opacidades = [1.0 if time == 'Brasil' else 0.75 for time in df_champs.index]
        cores = ['#03A256' if time == 'Brasil' else '#fff580' for time in df_champs.index]
        cores_bordas = ['#FFCC00' if time == 'Brasil' else '#000000' for time in df_champs.index]
        fig3.update_traces(marker_opacity=opacidades,
                           marker_color=cores,
                           marker_line_width=1,
                           marker_line_color=cores_bordas)
        
        click = st.plotly_chart(fig3, width="stretch", on_select='rerun')
        if click and click['selection']['points']:
            selecao = click['selection']['points'][0]['x']
            dados_time = df_champs.loc[selecao, ['Jogos', 'Gols Feitos', 'Gols Sofridos', 'Média de Gols Feitos', 'Média de Gols Sofridos']]
            st.markdown(f"###  Estatísticas Detalhadas: {selecao}")
            col1, col2, col3, col4, col5 = st.columns(5)
            
            col1.metric("Jogos", int(dados_time['Jogos']))
            col2.metric("Gols Feitos", int(dados_time['Gols Feitos']))
            col3.metric("Gols Sofridos", int(dados_time['Gols Sofridos']))
            col4.metric("Média Feitos", f"{dados_time['Média de Gols Feitos']:.2f}")
            col5.metric("Média Sofridos", f"{dados_time['Média de Gols Sofridos']:.2f}")            
        else:
            st.info(" Clique em uma seleção no gráfico acima para ver os detalhes!")

# with tab3:
if tab == 'Títulos':
    st.markdown("#### O Caminho da Glória: Nossas Finais")
    st.write("Chegar à final é para poucos, ganhar 5 delas é apenas para o Brasil")
    st.subheader('Títulos Mundiais por Seleção')
    cols = st.columns([2, 2])
    # Esquerda cima
    top_left_cell = cols[0].container(
    border=True, height="stretch", vertical_alignment="center"
    )
    with top_left_cell:
        fig4 = px.bar(
                title,
                x='Títulos',
                y='Seleção',
                orientation='h',
                title='Títulos',
                text_auto=True,
                color_discrete_sequence= ['#03A256']
            )
        fig4.update_traces(textposition='outside', 
                           cliponaxis=False,
                           textfont_color='#FFCC00',
                           textfont_size=18)
        fig4.update_layout(yaxis={'categoryorder': 'total ascending'})
        click01 = st.plotly_chart(fig4, width="stretch", on_select='rerun')
    
    top_right_cell = cols[1].container(
    border=True, height="stretch", vertical_alignment="center"
    )
    with top_right_cell:


        if click01 and click01['selection']['points']:
            selecao_finals = click01['selection']['points'][0]['y']
            st.subheader(f'Finais ganhas de {selecao_finals}')
            anos_titulos = title[title['Seleção'] == selecao_finals]['Anos'].values[0]
            anos_titulos = [int(ano) for ano in anos_titulos]
            mascara_anos = df['year'].fillna(0).astype(int).isin(anos_titulos)
            mascara_time = (df['home_team'] == selecao_finals) | (df['away_team'] == selecao_finals)
            df_filt = df[mascara_anos & mascara_time]
            df_finais = df_filt.sort_values('date').drop_duplicates(
                subset=['year'],
                keep='last')
            
            if not df_finais.empty:

                for index, row in df_finais.iterrows():
                
                    with st.container(border=True):
                        # Essa seção foi realizada com ajuda do ferramenta de IA Gemini (Criação do design utilizando CSS)
                        st.caption(f"🏆 **Copa do Mundo de {int(row['year'])}** • 📅 {row['date']}")
                        c1, c2, c3 = st.columns([3, 2, 3], vertical_alignment="center")
                        
                        with c1:
                            st.markdown(f"<h4 style='text-align: right; margin:0;'>{row['home_team']}</h4>", unsafe_allow_html=True)
                        
                        with c2:
                            gols_casa = int(row['home_score'])
                            gols_fora = int(row['away_score'])
                            st.markdown(f"<h3 style='text-align: center; color: #03A256; margin:0;'>{gols_casa} x {gols_fora}</h3>", unsafe_allow_html=True)
                        
                        with c3:
                            st.markdown(f"<h4 style='text-align: left; margin:0;'>{row['away_team']}</h4>", unsafe_allow_html=True)
                
            else:
                st.warning(f"Nenhum jogo encontrado para os anos {anos_titulos}.")
                
        else:
            st.info(" Clique em uma seleção no gráfico ao lado para ver os detalhes das finais!")

if tab == 'Comparação entre Campeãs':
    st.header('Comparação com as Seleções Campeãs Mundiais')
    st.write("A maior seleção em números! Comparando as estátisticas podemos notar que nenhuma se compara ao Brasil!")
    cols = st.columns([2, 2])
    # Esquerda cima
    top_left_cell = cols[0].container(
    border=True, height="stretch", vertical_alignment="center"
    )
    with top_left_cell:
        stats['Média Feitos (x100)'] = stats['Média de Gols Feitos'] * 100
        stats['Média Sofridos (x100)'] = stats['Média de Gols Sofridos'] * 100
        metricas = [
        'Jogos', 
        'Gols Feitos', 
        'Gols Sofridos', 
        'Média Feitos (x100)', 
        'Média Sofridos (x100)'
    ]
        options = [selecao for selecao in champs if selecao != 'Brasil']
        selecao_rival = st.pills("Escolha uma seleção para comparar com o Brasil:", options, selection_mode="single")
        if selecao_rival:
            valores_brasil=stats.loc['Brasil', metricas].tolist()
            valores_rival=stats.loc[selecao_rival, metricas].tolist()
            valores_brasil.append(valores_brasil[0])
            valores_rival.append(valores_rival[0])
            metricas_radar = metricas + [metricas[0]]
            
            rad_1 = go.Figure()

            rad_1.add_trace(go.Scatterpolar(
                r=valores_brasil,
                theta=metricas_radar,
                fill='toself',
                name='Brasil',
                line_color='#03A256', 
                opacity=0.7,         
                marker=dict(size=8, symbol='circle'),
                hoverinfo='r+name'    
            ))
            rad_1.add_trace(go.Scatterpolar(
                r=valores_rival,
                theta=metricas_radar,
                fill='toself',
                name=selecao_rival,
                line_color='#FF5733', 
                opacity=0.7,
                marker=dict(size=8, symbol='circle'),
                hoverinfo='r+name'
            ))
            rad_1.update_layout(
                polar=dict(
                radialaxis=dict(
                visible=True,
                )),
            showlegend=True
            )
            maior_valor = max(max(valores_brasil), max(valores_rival))

            rad_1.update_layout(
                polar=dict(
                    bgcolor='rgba(0,0,0,0)', # Deixa o fundo do radar transparente
                    radialaxis=dict(
                        visible=True,
                        range=[0, maior_valor * 1.1],
                        showticklabels=True,
                        tickfont=dict(size=10, color='gray'), 
                        gridcolor='rgba(128, 128, 128, 0.3)', 
                        gridwidth=1
                    ),
                    angularaxis=dict(
                        tickfont=dict(size=14, color='white'), 
                        gridcolor='rgba(128, 128, 128, 0.3)',
                        linecolor='rgba(128, 128, 128, 0.3)'
                    )
                ),
                showlegend=True,
                legend=dict(
                    orientation="h", #legenda horizontal
                    yanchor="bottom",
                    y=1.15,          
                    xanchor="center",
                    x=0.5
                ),
                margin=dict(t=80, b=40, l=60, r=60), 
                paper_bgcolor='rgba(0,0,0,0)',       # remove o fundo branco 
                plot_bgcolor='rgba(0,0,0,0)'
            )
        
            st.plotly_chart(rad_1)
            top_right_cell = cols[1].container(
            border=True, height="stretch", vertical_alignment="center"
            )
            with top_right_cell:
                st.markdown(f"###  Comparação Detalhada: {selecao_rival}")
                col1, col2, col3 = st.columns(3)
                
                col1.metric("Jogos", int(valores_rival[0]), (int(valores_rival[0])-int(valores_brasil[0])))
                col2.metric("Gols Feitos", int(valores_rival[1]), (int(valores_rival[1])-int(valores_brasil[1])))
                col3.metric("Gols Sofridos", int(valores_rival[2]), (int(valores_rival[2])-int(valores_brasil[2]))) 
                col4, col5 = st.columns(2)
                col4.metric("Média de Gols Feitos", ((valores_rival[3])/100), (f"{(valores_rival[3])-(valores_brasil[3]):.3}"))
                col5.metric("Média de Gols Sofridos", ((valores_rival[4])/100), (f"{(valores_rival[4])-(valores_brasil[4]):.3}"))
                st.divider()
                st.markdown(f"###  Comparação Detalhada: Brasil")
                col1, col2, col3 = st.columns(3)    
                col1.metric("Jogos", int(valores_brasil[0]), (int(valores_brasil[0])-int(valores_rival[0])))
                col2.metric("Gols Feitos", int(valores_brasil[1]),(int(valores_brasil[1])-int(valores_rival[1])))
                col3.metric("Gols Sofridos", int(valores_brasil[2]),(int(valores_brasil[2])-int(valores_rival[2]))) 
                col4, col5 = st.columns(2)
                col4.metric("Média de Gols Feitos", ((valores_brasil[3])/100),(f"{(valores_brasil[3])-(valores_rival[3]):.3}"))
                col5.metric("Média de Gols Sofridos", ((valores_brasil[4])/100), (f"{(valores_brasil[4])-(valores_rival[4]):.3}"))
        else:
            st.info(" Clique em uma seleção para Comparar com o Brasil")
if tab == 'Todos os Jogos de Copa do Mundo':
    st.header('Copa do Mundo de Futebol')
    st.write("Se aventure pela história e confira todos os 964 Jogos da história da Copa do Mundo")
    edicao = df['edicao'].unique()
    choice = st.selectbox('Escolha a Edição desejada', edicao)
    df_filtered = df[df['edicao'] == choice]
    df_filtered = df_filtered[['date','home_team','home_score','away_score','away_team', 'city', 'country','edicao']]
    df_filtered['home_score'] = df_filtered['home_score'].fillna(0).astype(int)
    df_filtered['away_score'] = df_filtered['away_score'].fillna(0).astype(int) 
    df_filtered = df_filtered.rename(columns={
    'date': 'Data',
    'home_team': 'Time Mandante',
    'home_score': 'Gols mandante',
    'away_score': 'Gols visitante',
    'away_team': 'Time Visitante',
    'city': 'Cidade',
    'country': 'País',
    'edicao': 'Edição'
})
    # st.table(df_filtered, border='horizontal')
    st.dataframe(df_filtered, hide_index=True, width='stretch')

st.markdown("---")
st.caption("Desenvolvido por João Alisson com fim totalmente didático e pessoal | **Dados:** Dataset original disponibilizado por [Mart Jürisoo - Kaggle](https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017). | Alguns componentes visuais (Finais da Aba Títulos) foram criados com auxílio do Gemini, na programação em CSS.")
