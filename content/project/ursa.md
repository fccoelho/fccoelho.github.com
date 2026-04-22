---
title: "URSA – Urbanization and Health in the Amazon"
date: 2025-01-06T10:00:00-03:00
draft: false

description: "Open data repositories to support One Health surveillance in the Amazon region, integrating environmental, socioeconomic, and health data along the urban-rural gradient."
image: ""
tags: ["urbanization", "amazon", "one-health", "spatial-analysis", "leishmaniasis", "geospatial"]
status: "active"
funder: "FGV"
start_date: "2025-01-06"
end_date: ""
github_link: ""
website_link: "https://info.dengue.mat.br/geoserver"
toc: true
author: "Flávio Codeço Coelho"
---

## Overview

**URSA** (Urbanização e Saúde na Amazônia) investigates the relationship between urbanization trends in the Amazon region and public health outcomes. The project is premised on the understanding that the combination of urban densification with social and environmental vulnerability, without adequate public policies, creates conditions for pathogen emergence and the persistence of endemic diseases.

The project organizes open data covering economic, environmental, and health dimensions along the urban-rural gradient in the Amazon, using the **Trajetórias** dataset which includes environmental, socioeconomic, and vector-borne disease incidence indicators across 772 municipalities in nine states of the Brazilian Legal Amazon (2000–2017).

## Team

| Member | Role |
|--------|------|
| Flávio Codeço Coelho | Coordinator (EMAp/FGV) |
| Cláudia Codeço | Coordinator (Fiocruz) |
| Anielli Souza | Postdoctoral Researcher (INPE/FGV) |
| Daniel Câmara | Postdoctoral Researcher (FGV) |
| Carlos Fonseca | MSc Student (EMAp) |
| Maria Eduarda Mesquita | Research Assistant (IC) |
| Ana Julia Amaro | Research Assistant (IC) |
| Silvia Maués | Collaborator (VigiFronteiras/SVS Macapá) |

## Objectives

- Organize open data repositories covering the economic, environmental, and health dimensions along the urban-rural gradient in the Amazon
- Define risk surfaces for infectious diseases such as leishmaniasis, rabies, and dengue
- Develop spatial-temporal dynamic transmission models
- Incorporate landscape transformation processes into risk and transmission models
- Support One Health surveillance through prospective epidemiological risk modeling

## Results

### 1. Spatial Data Inventory

A systematic inventory of free and open geospatial data for the Amazon and Brazil has been compiled. The data is stored on a **GeoServer** ([info.dengue.mat.br/geoserver](https://info.dengue.mat.br/geoserver)), which currently hosts environmental and socioeconomic/demographic information from 1987 onwards, with spatial resolutions ranging from 1 km to 30 m. All layers are accessible via WFS and WCS services, enabling direct integration with QGIS.

![layers](/images/ursa_layers.png)

Data sources include: **TerraClass**, **MapBiomas** (land use/cover, fires, deforestation), **PRODES**, **GHSL** (population density, built-up surface), and various **IBGE** products (municipal boundaries, census sectors, hydrographic basins, REGIC, indigenous areas).

![data](/images/ursa_data.png)

### 2. Cutaneous Leishmaniasis Risk Classification – Oiapoque (AP)

Under a One Health perspective, potential occurrence areas for cutaneous leishmaniasis (CL) were mapped for 2022, considering the landscape as a mediator of health-disease processes. The methodology classifies risk into four categories: **high autochthonous risk**, **high allochthonous risk**, **moderate risk**, and **low risk**.

Socio-environmental data (land use/cover, population density, drainage networks, roads) were integrated into 2×2 km cells. A supervised classifier based on decision trees with boosting was trained, achieving **94% overall accuracy**. Of the 6,062 cells mapped, 25 were classified as high autochthonous risk, 467 as high allochthonous risk, 4,409 as moderate risk, and 1,161 as low risk.

![layers](/images/ursa_leish.png)

### 3. Synthetic Population

A synthetic population is being developed from the 2022 Brazilian census data for the municipality of Oiapoque. The approach creates households populated according to the distribution of residents per household at the census tract level (97 tracts). Individuals are assigned demographic characteristics (sex, age group) matching census distributions and then linked to households. The resulting dataset preserves the statistical properties of the real population while enabling epidemiological modeling.

### 4. Automated Risk Mapping

A computational pipeline is being developed to automate the generation of regular spatial grids and the calculation of landscape metrics from vector geospatial data. The system supports configurable cell sizes (default 2×2 km), parallel processing for scalability, and a test mode for rapid validation on grid subsets.

### 5. International Workshop

An international workshop was held on August 26–27, 2025, in Oiapoque (AP), on the border with Saint-Georges, French Guiana. The event brought together professionals from human health, animal health, and environmental sectors from both Brazil and France, including representatives from:

- **Brazil**: Ministry of Health, Fiocruz, FGV, INPE, SVS-AP, DIAGRO
- **France**: Institut Pasteur de Guyane, ARS Guyane, IRD

Activities included participatory cartography, a SWOT (FOFA) analysis for One Health surveillance of leishmaniasis and rabies, and ecological calendar construction.

## Funding

Fundação Getulio Vargas (FGV), in collaboration with Fiocruz.
