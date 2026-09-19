@'
# 🧠 Workplace Mental Health Intelligence in Tech

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://tech-mental-health-sabil.streamlit.app)
[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end People Analytics and Decision Support System evaluating the **Open Sourcing Mental Illness (OSMI)** survey. This repository contains an in-depth 15-chart Exploratory Data Analysis (EDA) in Jupyter Notebook, a live interactive Streamlit dashboard for workforce intelligence, and an automated presentation deck.

---

## 📌 Executive Summary

In engineering organizations, developer bandwidth is the central economic asset. Despite extensive spending on wellness perks, mental distress remains an unmonitored risk factor resulting in hidden presenteeism, attrition, and velocity collapse.

This project assesses whether mental healthcare adoption is driven purely by personal/hereditary predisposition, or if company policies, procedural friction, and psychological safety govern care access.

### Key Empirical Takeaways

| Metric / Dimension | Observation | Strategic Implication |
| :--- | :--- | :--- |
| **Treatment Rate** | **50.5%** of surveyed staff sought care | Mental health impacts half the tech workforce, not an edge cohort. |
| **The Ambiguity Gap** | Care uptake is **63.8%** when benefits are known, dropping to **37.1%** when unsure | Policy ambiguity suppresses care more than having zero coverage (48.2%). |
| **Trust & Confidentiality** | **70.2%** doubt or do not know if anonymity is protected | Privacy concerns directly suppress Employee Assistance Program (EAP) usage. |
| **Leave Friction** | Difficult leave correlates with **61.9%** fearing career fallout | Administrative friction leads directly to toxic presenteeism. |
| **Managerial Trust** | **40.9%** discuss issues with managers vs. **17.8%** with peers | Engineering managers are the critical front-line triage point. |

---

## 🏗️ System Architecture

```text
├── survey.csv                         <- Raw OSMI survey dataset (1,259 rows, 27 cols)
├── cleaned_survey.csv                 <- Standardized, wrangled output dataset
├── Mental_Health_EDA.ipynb            <- 15-chart structured exploratory analysis
├── app.py                             <- Streamlit Cloud decision dashboard
├── requirements.txt                   <- Minimal, cloud-compatible dependencies
├── make_ppt.py                        <- Automated 10-slide PowerPoint generator
├── Mental_Health_Tech_Capstone.pptx   <- Exported 16:9 executive presentation
├── presentation_script.txt            <- 7–10 minute defense/viva speaking script
└── README.md                          <- Project documentation
