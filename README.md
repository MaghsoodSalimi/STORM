<p align="center"><strong>STORM – Smart Train Observation & Reporting Model</strong></p>



📁 ProjectRoot  
├── 📁 data  
│   ├── 📄 input.csv  
│   └── 📄 output.csv  
├── 📁 scripts  
│   ├── 📄 preprocess.py  
│   └── 📄 train_model.py  
├── 📁 models  
│   └── 📄 model.pkl  
├── 📁 notebooks  
│   └── 📄 analysis.ipynb  
├── 📄 README.md  
└── 📄 requirements.txt  




[View the interactive report](https://app.powerbi.com/reportEmbed?reportId=48a3bf00-09a3-4843-83c2-d6381d5168a4&autoAuth=true&ctid=a1795b64-dabd-4758-b988-b309292316cf)



## Introduction

Welcome to STORM!  
  
The repository highlights technical competencies and project work across data engineering, cloud platforms, automation, and data visualization, illustrating relevant capabilities through an end-to-end data pipeline.  




---
## Project Overview

This project focuses on extracting, storing, and visualizing **Train Announcement** data from the Swedish Transport Administration’s public API. It demonstrates working with live data feeds, automating data ingestion, and creating meaningful reports.

Key objectives include:

- Extracting real-time train announcement data from Trafikverket’s API  
- Storing the data in a cloud database (Azure SQL)  
- Automating the data collection and ingestion process  
- Building a Power BI report to visualize train announcements effectively  

---

## Step 1: Data Extraction with Jupyter Notebook

The initial phase involves exploring and extracting train announcement data using a Jupyter Notebook (located in the `notebook` folder):

- Connection established with Trafikverket’s API ([https://data.trafikverket.se/](https://data.trafikverket.se/))  
- Queried and retrieved train announcement data in JSON/XML format  
- Parsed and transformed the data into structured tables  
- Exported the processed data as CSV files into the `data` folder for validation and further use  

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

- An **Azure Function** (implemented with PowerShell) periodically calls the Trafikverket API to fetch new data  
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

## Project Structure



## Project Structure


   
'''
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

'''

---

---

## Technologies Used

- **Python** & **Jupyter Notebook** for data extraction and transformation  
- **Azure SQL Database** for cloud-based storage  
- **Azure Functions** (PowerShell) for serverless automation  
- **Microsoft Power Automate** for task scheduling and orchestration  
- **Power BI** for interactive data visualization and reporting  

---

## Conclusion

This project demonstrates the ability to design and automate a complete data engineering workflow — encompassing live data acquisition, cloud storage, serverless automation, and insightful reporting. It reflects proficiency in tools and platforms commonly used in enterprise data solutions.

Explore the code and resources provided. For further information or collaboration opportunities, feel free to connect.

---

**Thank you for visiting this portfolio!**

---

*Max*  
PhD Student & Data Engineer
