---
title: "URSA – Urbanização e Saúde na Amazônia"
date: 2025-01-06T10:00:00-03:00
draft: false

description: "Repositórios de dados abertos para apoio à vigilância em saúde única na região amazônica, integrando dados ambientais, socioeconômicos e de saúde ao longo do gradiente urbano-rural."
image: ""
tags: ["urbanização", "amazônia", "saúde-única", "análise-espacial", "leishmaniose", "geoespacial"]
status: "active"
funder: "FGV"
start_date: "2025-01-06"
end_date: ""
github_link: ""
website_link: "https://info.dengue.mat.br/geoserver"
toc: true
author: "Flávio Codeço Coelho"
---

## Apresentação

O projeto **URSA** (Urbanização e Saúde na Amazônia) investiga a relação entre transformações populacionais na região amazônica e saúde. A premissa central é que a combinação de adensamentos urbanos com vulnerabilidade social e ambiental, sem políticas públicas adequadas, cria condições para a emergência de patógenos e a manutenção de endemias.

O projeto organiza dados abertos que contemplam as dimensões econômica, ambiental e de saúde no gradiente urbano-rural na Amazônia, utilizando o dataset **Trajetórias**, que compreende indicadores ambientais, socioeconômicos e de incidência de doenças vetoriais entre 2000 e 2017 em 772 municípios de nove estados da Amazônia Legal Brasileira.

## Equipe

| Membro | Função |
|--------|--------|
| Flávio Codeço Coelho | Coordenador (EMAp/FGV) |
| Cláudia Codeço | Coordenadora (Fiocruz) |
| Anielli Souza | Pesquisadora Pós-doutorado (INPE/FGV) |
| Daniel Câmara | Pesquisador Pós-doutorado (FGV) |
| Carlos Fonseca | Mestrando (EMAp) |
| Maria Eduarda Mesquita | Bolsista IC |
| Ana Julia Amaro | Bolsista IC |
| Silvia Maués | Colaboradora (VigiFronteiras/SVS Macapá) |

## Objetivos

- Organizar repositórios de dados abertos cobrindo as dimensões econômica, ambiental e de saúde ao longo do gradiente urbano-rural na Amazônia
- Definir superfícies de risco para doenças transmissíveis como leishmaniose, raiva e dengue
- Desenvolver modelos dinâmicos espaço-temporais de transmissão
- Incorporar os processos de transformação da paisagem nos modelos de risco e transmissão
- Apoiar a vigilância em saúde única através da modelagem prospectiva do risco epidemiológico

## Resultados

### 1. Inventário de dados espaciais

Um inventário sistemático de dados geoespaciais de acesso livre e aberto para a Amazônia e o Brasil foi elaborado. Os dados estão armazenados no **GeoServer** ([info.dengue.mat.br/geoserver](https://info.dengue.mat.br/geoserver)), que atualmente reúne informações ambientais e socioeconômicas/demográficas desde 1987, com resoluções espaciais de 1 km, 100 m e 30 m. Todas as camadas são acessíveis via serviços WFS e WCS, permitindo integração direta com o QGIS.

![layers](/images/ursa_layers.png)

Fontes de dados incluem: **TerraClass**, **MapBiomas** (uso e cobertura do solo, queimadas, desmatamento), **PRODES**, **GHSL** (densidade populacional, superfície construída) e diversos produtos do **IBGE** (malhas municipais, setores censitários, bacias hidrográficas, REGIC, áreas indígenas).


![data](/images/ursa_data.png)

### 2. Classificação de risco de Leishmaniose Tegumentar – Oiapoque (AP)

Sob a perspectiva da saúde única, foram mapeadas áreas potenciais de ocorrência da leishmaniose tegumentar (LT) em 2022, considerando a paisagem como mediadora dos processos saúde-doença. A metodologia classifica o risco em quatro categorias: **risco autóctone alto**, **risco alóctone alto**, **risco moderado** e **risco baixo**.

Dados socioambientais (uso e cobertura da terra, densidade populacional, redes de drenagem e estradas) foram integrados em células de 2×2 km. Um classificador supervisionado baseado em árvores de decisão com método boosting foi treinado, obtendo **94% de acurácia global**. Das 6.062 células mapeadas, 25 foram classificadas como risco autóctone alto, 467 como risco alóctone alto, 4.409 como risco moderado e 1.161 como risco baixo.

![layers](/images/ursa_leish.png)

### 3. População Sintética

Uma população sintética está sendo desenvolvida a partir dos dados do censo brasileiro de 2022 para o município de Oiapoque. A abordagem cria domicílios povoados conforme a distribuição de moradores por domicílio ao nível de setores censitários (97 setores). Indivíduos recebem características demográficas (sexo, faixa etária) correspondentes às distribuições censitárias e são vinculados aos domicílios. O conjunto resultante preserva as propriedades estatísticas da população real, viabilizando a modelagem epidemiológica.

### 4. Automatização do mapeamento de risco

Um pipeline computacional está sendo desenvolvido para automatizar a geração de grades espaciais regulares e o cálculo de métricas de paisagem a partir de dados geoespaciais vetoriais. O sistema suporta células de tamanho configurável (padrão 2×2 km), processamento paralelo para escalabilidade e modo de teste para validação rápida.

### 5. Workshop Internacional

Um workshop internacional foi realizado nos dias 26 e 27 de agosto de 2025, em Oiapoque (AP), na fronteira com São Jorge (Saint-Georges), Guiana Francesa. O evento reuniu profissionais de saúde humana, saúde animal e meio ambiente do Brasil e da França, incluindo representantes de:

- **Brasil**: Ministério da Saúde, Fiocruz, FGV, INPE, SVS-AP, DIAGRO
- **França**: Institut Pasteur de Guyane, ARS Guyane, IRD

As atividades incluíram cartografia participativa, análise FOFA para vigilância em Saúde Única de leishmaniose e raiva, e construção de calendário ecológico.

## Financiamento

Fundação Getulio Vargas (FGV), em colaboração com a Fiocruz.
