<p align="center">STORM – Smart Train Observation & Reporting Model</p>






[View the interactive report](https://app.powerbi.com/reportEmbed?reportId=48a3bf00-09a3-4843-83c2-d6381d5168a4&autoAuth=true&ctid=a1795b64-dabd-4758-b988-b309292316cf)



## Introduction

Welcome to my GitHub portfolio!  
This portfolio is designed to showcase my technical skills and project experience in data engineering, cloud services, automation, and data visualization. The goal is to present the capabilities you are looking for by demonstrating a real-world end-to-end data pipeline.

<img src="material/storm.jpg"  width="100%"/>


---

## Project Overview

In this project, I focus on extracting, storing, and visualizing **Train Announcement** data from the Swedish Transport Administration’s public API. The project demonstrates how to work with live data feeds, automate data ingestion, and create meaningful reports.

The key objectives were:

- Extract real-time train announcement data from Trafikverket’s API  
- Store the data in a cloud database (Azure SQL)  
- Automate the data collection and ingestion process  
- Build a Power BI report to visualize train announcements effectively

---

## Step 1: Data Extraction with Jupyter Notebook

In the initial phase, I explored and extracted train announcement data using a Jupyter Notebook (located in the `notebook` folder):

- Connected to Trafikverket’s API ([https://data.trafikverket.se/](https://data.trafikverket.se/))  
- Queried and retrieved train announcement data in JSON/XML format  
- Parsed and transformed the data into structured tables  
- Exported the processed data as CSV files into the `data` folder for validation and further use  

This step was essential to understand the API structure and data details about train schedules, delays, and statuses.

---

## Step 2: Cloud Storage with Azure SQL Database

To enable scalable and efficient storage, I provisioned an **Azure SQL Database**:

- Designed a relational database schema tailored for train announcement data  
- Created tables optimized for querying time-series and event data  
- Established secure connections for data insertion and retrieval  
- Set up indexing to enhance query performance  

This database serves as the core data repository for all train announcement records.

---

## Step 3: Automated Data Pipeline Using Azure Functions and Power Automate

To keep the data fresh and updated continuously, I automated the data ingestion process:

- Developed an **Azure Function** (implemented with PowerShell) that periodically calls the Trafikverket API to fetch new train announcement data  
- The function processes and writes this data directly into the Azure SQL Database  
- Leveraged **Microsoft Power Automate** to schedule and orchestrate the execution of the Azure Function on a regular basis, ensuring seamless automation  

This setup eliminates manual intervention and guarantees the database always reflects the latest train announcements.

---

## Step 4: Data Visualization with Power BI

Finally, I created a Power BI report to showcase insights from the train announcement data:

- Connected Power BI directly to the Azure SQL Database  
- Designed interactive dashboards highlighting train schedules, delays, and announcements  
- Implemented filters and visual elements for dynamic user exploration  
- Shared the report for easy access by stakeholders  

This visualization enables efficient monitoring and analysis of train operations based on live data.

---

## Project Structure


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



---

## Technologies Used

- Python & Jupyter Notebook for data extraction and processing  
- Azure SQL Database for cloud data storage  
- Azure Functions (PowerShell) for serverless automation  
- Microsoft Power Automate for scheduling and workflow automation  
- Power BI for data visualization and reporting  

---

## Conclusion

This project highlights my ability to build and automate a complete data engineering workflow — from live data acquisition through cloud storage and automation to insightful visualization. It demonstrates proficiency with modern tools and platforms widely used in enterprise data projects.

Feel free to explore the code and resources here, and reach out if you have any questions or collaboration ideas!

---

**Thank you for visiting my portfolio!**

---

*Max*  
PhD Student & Data Engineer  

