#!/usr/bin/env python
# coding: utf-8

# <h3 style="color:#1f6feb;">COVID-19 Global Analysis</h3>
# 
# This notebook explores global COVID-19 trends using data from Our World in Data.  
# We focus on:
# 
# - When each country reported its first confirmed case  
# - When each country hit its peak daily number of new cases  
# - How Case Fatality Ratio (CFR) evolved over time
# 
# Python (Pandas, Matplotlib) is used for data cleaning, analysis, and visualization.

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt

import matplotlib.dates as mdates


# In[2]:


#We define a helper function to compute the peak wave per country to avoid repeating code.
def compute_country_peaks(df):
    #Peak date per country
    peaks=(df.sort_values("date").groupby("country",as_index=False)
           .apply(lambda x: x.loc[x["new_cases"].idxmax(),["date"]])
           .reset_index(drop=True).rename(columns={"date":"peak_date"}))   
    
    #Converting peak dates to month for clearer visualization
    peaks["peak_month"]=peaks["peak_date"].dt.to_period("M").astype(str)
    return peaks


# In[3]:


#Same with the plot
def plot_peak_barchart(df,title="COVID-19 Peak Month per Country"):
    #Counting how many countries peaked each month
    month_counts=(df.groupby("peak_month")["country"].count().reset_index(name="num_countries").sort_values("peak_month"))
    
    #The plot
    plt.figure(figsize=(14,6))
    plt.bar(month_counts["peak_month"],month_counts["num_countries"],width=0.8)
    plt.xticks(rotation=90)
    plt.xlabel("Peak Month")
    plt.ylabel("Number of Countries")
    plt.title(title)
    plt.tight_layout()
    plt.show()


# In[4]:


#Loading Covid-19 dataset
url="https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv"
df=pd.read_csv(url)


# In[5]:


#Let's use .sample() to display random rows from our dataset
df.sample(10)


# In[6]:


df.info()


# By using info(), we can quickly check the structure of the dataset and confirm that some columns contain missing values. Dtype also helps us verify that numerical fields are stored correctly as float64, which means we can safely perform analysis on them without additional type conversion.

# In[7]:


#Sum of missing values in each column
missing=df.isna().sum()

#We sort it and add a filter ([missing>0]) to display all the rows of our results
missing=missing[missing>0].sort_values(ascending=False)

print(missing)


# Since some columns contain a large number of missing values, we calculate the percentage of missing entries relative to the total dataset size to understand how severe the gaps are.

# In[8]:


missing_percent=(missing/len(df))*100

missing_sum=pd.DataFrame({'Missing Count':missing,'Missing %':missing_percent}).sort_values('Missing %',ascending=False)
print(missing_sum)


# We could set a threshold and remove columns with a high percentage of missing values. However, in healthcare datasets, even sparse fields can be clinically meaningful, so dropping them blindly could lead to losing valuable information. For this project, we focus on a subset of columns that are both relevant and have relatively low levels of missing data.

# In[9]:


covid=df[['continent','country','date','total_cases','new_cases','total_deaths','new_deaths','population']]
covid.sample(10)


# The column with the highest number of missing values in our filtered dataset is `continent`, so let's take a closer look at the entries with no assigned continent to understand what’s going on.
# 

# In[10]:


covid[covid['continent'].isna()]


# In[11]:


#Checking the name of the country for NaN continent entries
set(covid[covid['continent'].isna()]['country'])


# Some rows contain incorrect values in the `country` column, such as “Africa” and “Asia,” which represent continents rather than individual countries. We also find variations like “England,” “England and Wales,” and “Scotland,” despite already having “United Kingdom” as a unified entry. 
# 
# To ensure consistency and avoid double counting, we remove rows with missing values in the `continent` column.
# 
# 

# In[12]:


covid=covid.dropna(subset=['continent'])


# In[13]:


set(covid["country"]) #and we make sure there are no 'double' countries anymore


# Next, we move into exploring information from the dataset by finding the date of the first confirmed case for each country. Since the `date` column was stored as a string (`object` type), we first convert it to a proper datetime format. We also drop rows with missing values in `total_cases` to ensure that our results only include valid case records.

# In[14]:


#Time format
covid["date"]=pd.to_datetime(covid["date"])
covid["date"].dtype


# In[15]:


#Drop NaN for "total_cases"
covid_valid=covid.dropna(subset="total_cases")


# In[16]:


#First case for each country
first_cases=(covid_valid[covid_valid["total_cases"]>0].groupby("country")["date"].min().reset_index())

first_cases.columns= ["country","first_case_date"]


# In[17]:


#Sorting the dates
first_cases=first_cases.sort_values("first_case_date")
first_cases


# In[18]:


#Plot
plt.figure(figsize=(14,34))

plt.scatter(first_cases["first_case_date"],first_cases["country"],s=12)

plt.yticks(fontsize=9)  #smaller font for more spacing
plt.gca().set_ylim(-1,len(first_cases)+1)  #expand y-axis range

plt.xlabel("Date of First Confirmed Case")
plt.ylabel("Country")
plt.title("Timeline of First COVID-19 Case by Country")
plt.grid(axis='x',linestyle='--',alpha=0.4)

plt.tight_layout()
plt.show() 


# The timeline shows that the majority of countries recorded their first COVID-19 case by mid-2020, but some remained case-free until 2021 or later. 
# 
# To quantify this trend, we calculate the proportion of countries in each continent that had not reported any cases prior to 2021.

# In[19]:


#We merge back continent
first_cases=first_cases.merge(covid[["country","continent"]].drop_duplicates(),on="country",how="left")
first_cases.sort_values("first_case_date")


# In[20]:


#Filtering the countries that had their first covid case after 2021
late_countries=first_cases[first_cases["first_case_date"]>"2021-01-01"]
late_countries


# In[21]:


#Counting how many countries per continent
late_counts=late_countries.groupby("continent")["country"].nunique()
late_counts

#Total countries per continent
total_counts=first_cases.groupby("continent")["country"].nunique()
total_counts

#Percentage of countries per continent that remained covid free till 2021
percentage_late=(late_counts/total_counts*100).round(2)
percentage_late=percentage_late.fillna(0)
percentage_late.sort_values(ascending=False)


# Almost half of the countries in Oceania did not report a COVID-19 case until 2021 or later, likely because many of them are remote island nations. Probably the ideal places to be when the next pandemic hits!
# 
# Now that we’ve explored the first reported case, let’s investigate when each country reached its peak number of new daily cases.

# In[22]:


#We drop nan values
covid_c=covid.dropna(subset="new_cases")
covid_c[covid_c["total_cases"].isna()] #checking


# In[23]:


country_peaks=compute_country_peaks(covid_c)


# In[24]:


plot_peak_barchart(country_peaks)


# From the chart, it’s clear that the highest concentration of peak waves occurred between December 2021 and March 2022. However, I’m curious to see which countries reached their peak as late as May 2025, so let’s take a closer look.

# In[25]:


may_2025_peaks=country_peaks[(country_peaks["peak_date"].dt.year==2025)&(country_peaks["peak_date"].dt.month==5)]
print(may_2025_peaks)


# In[26]:


#Let's retrieve the relevant row from our dataset to check the number of the cases
covid_c[(covid_c["country"]=="Thailand")&(covid_c["date"]=="2025-05-27")]


# We also examine the countries that appear to have reached their peak in January 2020 to understand what these early values represent.

# In[27]:


jan_2020_peaks=country_peaks[(country_peaks["peak_date"].dt.year==2020)&(country_peaks["peak_date"].dt.month==1)]
print(jan_2020_peaks)


# In[28]:


covid_c[covid_c["country"].isin(["North Korea","Turkmenistan"])]


# Both countries show zero values throughout the dataset, meaning no real data was ever recorded for them. Keeping them in the analysis creates misleading “peaks” in the bar chart, so it’s better to remove them from the dataset.
# 
# This is a good reminder that data cleaning is not a one-time step. Real-world datasets can contain missing or incorrect entries that only become visible once we start exploring and visualizing them. It’s important to stay attentive throughout the analysis and validate our findings as we go.

# In[29]:


#Removing countries with 0 entries
valid_countries=covid_c.groupby("country")["new_cases"].sum()
valid_countries=valid_countries[valid_countries>0].index

covid_clean=covid_c[covid_c["country"].isin(valid_countries)].copy()


# In[30]:


#Recalculation
country_peaks_clean=compute_country_peaks(covid_clean)


# In[31]:


#Replot
plot_peak_barchart(country_peaks_clean)


# Now that our peak chart is free of misleading entries, we can move on to another metric: the Case Fatality Ratio (CFR) for each country. Before calculating it, we ensure that there are no missing values in `total_deaths`, and then compute and visualize the ratio over time.

# In[32]:


covid_clean[covid_clean["total_deaths"].isna()]


# In[33]:


#Computing CFR per country
covid_clean["CFR"]=covid_clean["total_deaths"]/covid_clean["total_cases"]
covid_clean["CFR"]=covid_clean["CFR"].fillna(0) #replacing NaNs after division by 0

#Getting the percentage
covid_clean["CFR_percent"]=covid_clean["CFR"]*100


# In[34]:


#CFR plot for specific countries, we pick the following
countries=["Greece","Italy","United States"]

plt.figure(figsize=(12,6))

for country in countries:
    subset=covid_clean[covid_clean["country"]==country]
    plt.plot(subset["date"],subset["CFR_percent"],label=country)

plt.xlabel("Date")
plt.ylabel("Case Fatality Ratio (%)")
plt.title("COVID-19 Case Fatality Ratio (CFR) Trends")
plt.legend()
plt.grid(linestyle="--",alpha=0.4)
plt.tight_layout()
plt.show()


# We selected three countries—Italy, Greece, and the United States—to visualize their CFR trends. Italy shows a noticeably higher Case Fatality Ratio during 2020 compared with the other two, likely reflecting the severe impact of the early outbreak. It’s interesting to see how the CFR steadily drops in 2021 and continues declining through 2022, as healthcare systems adapt, testing becomes more widespread, and effective treatments become available.

# CONCLUSION:
# 
# This project examined the timing of first confirmed COVID-19 cases, peak waves, and Case Fatality Ratio trends across countries worldwide. Most countries reported cases by mid-2020, while many island nations in Oceania remained unaffected until 2021. Peaks were concentrated around late 2021 to early 2022, and CFR declined steadily after 2020 as healthcare responses improved. Data issues encountered along the way showed the importance of ongoing cleaning and validation throughout the analysis. Overall, the project demonstrates how global patterns become visible when combining data exploration, visualization, and critical interpretation.
# 

# In[ ]:





# In[ ]:




