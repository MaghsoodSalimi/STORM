<p align="center"><img src = "material/thunder_.png"> </p>
<p align="center"><strong>STORM</strong></p>
<p align="center"><strong>Smart Train Observation & Reporting Model</strong></p>

---


[View the interactive report](https://app.powerbi.com/reportEmbed?reportId=48a3bf00-09a3-4843-83c2-d6381d5168a4&autoAuth=true&ctid=a1795b64-dabd-4758-b988-b309292316cf)



## Introduction

  
This repository showcases a comprehensive project that demonstrates technical competencies across data engineering, cloud platforms, automation, data visualization, and applied machine learning. It highlights the development of an end-to-end data pipeline integrated with an AI model, emphasizing real-time data processing and predictive analytics.



---
## Project Overview

This project focuses on extracting, storing, and visualizing **Train Announcement** data from the Swedish Transport Administration’s public API. It demonstrates working with live data feeds, automating data ingestion, and creating meaningful reports.

Key objectives include:

- Extracting real-time train announcement data from Trafikverket’s API  
- Storing the data in a cloud database (Azure SQL)  
- Automating the data collection and ingestion process  
- Building a Power BI report to visualize train announcements effectively
- Developing an AI model to forecast train delay, using historical data  
- Deploying a Streamlit app to predict the train delay based on user entries

---

## Step 1: Data Extraction with Jupyter Notebook

The initial phase involves exploring and extracting train announcement data using a Jupyter Notebook (located in the `notebook` folder):

- Connection established with Trafikverket’s API ([https://data.trafikverket.se/](https://data.trafikverket.se/))  
- Queried and retrieved train announcement data in JSON/XML format  
- Parsed and transformed the data into structured tables  
- Exported the processed data as CSV files into the `data` folder for validation and further use
- Visualizing data using python libraries  

This step helps in understanding the API structure and the details of train schedules, delays, and statuses.

---

## Step 2: Cloud Storage with Azure SQL Database

To ensure scalable and efficient storage, an **Azure SQL Database** is provisioned:

- A relational database schema is designed for train announcement data  
- Tables optimized for querying time-series and event data are created  
- Secure connections for data insertion and retrieval are established  
- Indexing is configured to improve query performance  

This serves as the central repository for train announcement records.

---

## Step 3: Automated Data Pipeline Using Azure Functions and Power Automate

To maintain continuously updated data, the ingestion process is fully automated:

- An **Azure Function** periodically calls the Trafikverket API to fetch new data  
- The function processes and writes the data directly into the Azure SQL Database  
- **Microsoft Power Automate** is used to schedule and orchestrate the execution of the Azure Function on a recurring basis  

This setup ensures the database reflects the most recent train announcements without manual effort.

---

## Step 4: Data Visualization with Power BI

A Power BI report is created to provide insights into the train announcement data:

- Connected directly to the Azure SQL Database  
- Dashboards highlight train schedules, delays, and announcements  
- Filters and visual elements enable dynamic exploration  
- The report is shared to facilitate easy access and stakeholder engagement  

This visualization supports effective monitoring and analysis of train operations based on live data.

---

## Step 5: AI-Powered Train Delay Forecasting  

To forecast train delays based on historical data, a machine learning model has been developed and integrated into a user-facing application:

- Historical train departure data is read from CSV files and preprocessed for training  
- An XGBoost model is trained to predict train delays based on features like scheduled departure time and actual departure  
- The model's performance is evaluated using metrics such as Mean Absolute Error (MAE) on a test set  
- A Streamlit app is built to allow users to input relevant trip details and receive delay predictions interactively  

This component provides actionable insights to improve scheduling and operational efficiency.


---  
## Project Structure


   
```

/
├── notebook/ # Jupyter Notebook for API data extraction and processing  
├── data/ # CSV files exported from the notebook  
├── azure-function/ # Azure Function code for automated data ingestion  
├── power-bi-report/ # Power BI report files and resources  
├── README.md # This file  

my-project/  
├── src/  
│   ├── main.py  
│   └── utils.py  
├── tests/  
│   └── test_main.py  
└── README.md  

```





```
ProjectRoot/
├── data/
│   ├── input.csv
│   └── output.csv
├── scripts/
│   ├── preprocess.py
│   └── train_model.py
├── models/
│   └── model.pkl
├── notebooks/
│   └── analysis.ipynb
├── README.md
└── requirements.txt
```

---

---

## Technologies Used

- **Python** & **Jupyter Notebook** for data extraction and transformation  
- **Azure SQL Database** for cloud-based storage  
- **Azure Functions** (PowerShell) for serverless automation  
- **Microsoft Power Automate** for task scheduling and orchestration  
- **Power BI** for interactive data visualization and reporting
- **XGBoost** for training a predictive model based on historical data
- **Streamlit** to quickly building a data app that recieves user input and predicts train delays in minutes  

---

## Conclusion

This project demonstrates the ability to design and automate a complete data engineering workflow — encompassing live data acquisition, cloud storage, serverless automation, and insightful reporting. It reflects proficiency in tools and platforms commonly used in enterprise data solutions.

Explore the code and resources provided. For further information or collaboration opportunities, feel free to connect.

---

**Thank you for visiting this portfolio!**

---

*Max*  
PhD Student & Data Engineer
