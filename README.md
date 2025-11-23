COVID-19 Global Analysis

This project explores how COVID-19 spread across the world using data from Our World
in Data. I focused on three simple but interesting questions:
1. When did each country report its first confirmed case?
2. When did each country hit its peak in daily new cases?
3. How did the Case Fatality Ratio (CFR) change over time?

The analysis is done in Python using Pandas and Matplotlib, inside a Jupyter Notebook.


Dataset

Source: Our World in Data / COVID-19 dataset - 
Format: CSV - 
Scope: Daily records for each country, including cases, deaths, testing, vaccination, and
demographic information.

After exploring the dataset, the following columns were selected for the core analysis:
• continent
• country
• date
• total_cases
• new_cases
• total_deaths
• new_deaths
• population


Data Cleaning

Like most real-world healthcare data, this dataset came with:
• missing values
• inconsistent country names
• entries with zero cases but included in totals

The notebook emphasizes that data cleaning is not a one-time step
but an ongoing process throughout the analysis.


Key Analyses

First Confirmed Case Timeline - 
For each country:
• The first date with total_cases > 0 was extracted.
• A timeline scatter plot shows how the virus spread globally.
• Most countries reported cases within the first half of 2020, while many in Oceania did
not report cases until 2021 due to geographical isolation.

Peak Wave Detection - 
For each country:
• The date of maximum daily new cases (new_cases) was calculated.
• A bar chart shows how many countries peaked per month.
• After cleaning, the majority of peaks clustered around Dec 2021 – Mar 2022.

Case Fatality Ratio (CFR) Trends - 
CFR was calculated as: CFR = total_deaths / total_cases

Example comparisons were made between:
• Greece
• Italy
• United States
A clear pattern emerged:
• Italy experienced a much higher CFR in early 2020, especially during the first wave.
• CFR declined significantly from 2021 onward as pandemics responses improved
worldwide.


Visualizations

The notebook includes:
• First-case timeline scatter plot
• Bar chart of monthly peak waves
• CFR trend comparison line plot

All visualizations are generated in Python.


Conclusions

The analysis highlights:
• The rapid spread of COVID-19 in early 2020
• How isolated island nations (especially in Oceania) remained COVID-free the longest
• How peak outbreaks aligned globally around late 2021 – early 2022
• CFR trends demonstrate the dramatic improvement of medical response and detection
as the pandemic progressed

The project also reinforces the importance of:
• Constant data validation
• Cleaning throughout the workflow
• Not blindly trusting raw datasets


Tools Used

• Python
• Pandas
• Matplotlib
• Jupyter Notebook
• Our World in Data (COVID-19 dataset)


Contents

• Jupyter Notebook with full code and plots
• Exported PDF with results and commentary
• This README


Next Steps

• Try a SQL version of the same analysis
• Add forecasting models
• Explore vaccination or mobility trends


Contributions

Suggestions, improvements, or pull requests are welcome
