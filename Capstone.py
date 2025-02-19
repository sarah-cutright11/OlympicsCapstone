#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#had to download preprocessor and helper libraries
pip install preprocessor
pip install helper


# In[98]:


#Import necessary libraries

import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime, timedelta
from datetime import date

import statistics as stat #statistics library
from scipy import stats as scstats #statistics within library
import matplotlib.pyplot as plt #Library for charting data, most common
import seaborn as sns #Library for extra datasets, charting data
import plotly as plot #Library for interactive charts 
import plotly.express as px

import streamlit as st
import preprocessor,helper
import plotly.figure_factory as ff


# In[2]:


#import the athlete information Data Frame
df = pd.read_csv('athlete_events.csv')

df.head()


# In[3]:


#Shows information on the Athlete DF
df.info()


# In[4]:


#Shows shape and description of Athletes DF

print('Shape: \n',df.shape)
print('\n')
print('Description: \n', df.describe())


# In[5]:


#uses my data quality check to gain information on the data
import dataquality as dq
dq.data_check(df)


# In[217]:


df.info()


# In[6]:


#looks at the duplicates
duplicates = df[df.duplicated()]
print(duplicates)


# In[7]:


#drops duplicates, shows no duplicates remain
df = df.drop_duplicates(keep = 'last')
df.duplicated().sum()


# In[8]:


#Fills missing Medal with "None"
df['Medal'] = df['Medal'].fillna('None')
df.head()


# In[9]:


#displays basic statistics
print('Basic Statistics:\n', df.describe(include = 'all'))


# In[10]:


#shows ages of participants above the age of 70
above_75 = df[df['Age'] >75]
above_75


# In[11]:


#shows how many participants are above the age of 70
above_75.count()


# In[12]:


#shows the athletes below the age of 15
below_12 = df[df['Age'] < 12]
below_12


# In[13]:


#shows the count of athletes below the ages of 15
below_12.count()


# In[ ]:





# In[14]:


#Imports the NOC Regions DF

dfn = pd.read_csv('noc_regions.csv')

dfn.head()


# In[15]:


#Shows information on NOC Regions DF
dfn.info()


# In[16]:


import dataquality as dq
dq.data_check(dfn)


# In[17]:


#displays basic statistics
print('Basic Statistics:\n', dfn.describe(include = 'all'))


# In[18]:


#dfn.rename(columns={'NOC':'Country_Code'}, inplace=True)
#dfn.head()


# In[19]:


#filtering only summer Olympics
df_sum = df[df['Season'] == 'Summer']

#merge with region_df
df_sum = df_sum.merge(dfn, on = 'NOC', how = 'left')

#dropping duplicates
df_sum.drop_duplicates(inplace = True)

df_sum.head()


# In[20]:


df_sum


# ### Medal Tally

# In[73]:


#function to get medal count by country and year
def get_medal_count():
    #user input for year and country
    year = int(input('Enter the year: '))
    country = input('Enter the country (ex. USA, CAN): ').upper()

    #filters data for the given year and country
    filtered_data = df_sum[(df_sum['Year'] == year) & (df_sum['NOC'] == country)]

    #counts medal by type
    medal_count = filtered_data['Medal'].value_counts()

    #print results
    print(f"\nMedal count for {country} in {year}:")
    print(f"Gold: {medal_count.get('Gold', 0)}")
    print(f"Silver: {medal_count.get('Silver', 0)}")
    print(f"Bronze: {medal_count.get('Bronze', 0)}")
    print(f"Total: {len(filtered_data[filtered_data['Medal'] != 'None'])}")

get_medal_count()


# In[219]:


df_sum.to_csv('athlete_olympic.csv', index=False)


# In[75]:


#function to create the medal tally chart
def create_medal_tally():
    #filter relevant columns
    rel_data = df_sum[df_sum['Medal'] != 'None']

    #group data by year, NOC, medal type, and count the medals
    medal_tally = rel_data.groupby(['Year', 'NOC', 'Medal']).size().unstack(fill_value = 0)
    
    #renaming columns
    medal_tally.rename(columns={'Gold': 'Gold_Medals', 'Silver': 'Silver_Medals', 'Bronze': 'Bronze_Medals'}, inplace = True)
    
    #adding a Total column
    medal_tally['Total_Medals'] = medal_tally.sum(axis=1)
    
    #reset the index
    medal_tally.reset_index(inplace = True)
    
    return medal_tally

#function to get medal tally for specific country
def get_cntry_medal_tally(medal_tally):
    #get user input for country
    country = input('Enter the country (ex. USA, CAN): ').upper()
    
    #filters medal tally for the chosen country
    cntry_medal_tally = medal_tally[medal_tally['NOC'] == country]
    
    #check to see if there is data for that country
    if cntry_medal_tally.empty:
        print(f"No data found for the country code: {country}")
    else:
        #display the medal tally for the country
        print(f"\nMedal Tally for {country}")
        print(cntry_medal_tally)

#create the medal tally chart
medal_tally = create_medal_tally()

#allow the user to choose a country and display its medal tally
get_cntry_medal_tally(medal_tally)


# ### Overall Analysis

# In[77]:


#shows an overall analysis of the data

#finds unique stats about the olympic games
editions = df_sum['Year'].unique().shape[0]-1
cities = df_sum['City'].unique().shape[0]
sports = df_sum['Sport'].unique().shape[0]
events = df_sum['Event'].unique().shape[0]
athletes = df_sum['Name'].unique().shape[0]
nations = df_sum['region'].unique().shape[0]

#shows the stats
print(f"Total Editions: {editions}")
print(f"Total Host Cities: {cities}")
print(f"Total Sports: {sports}")
print(f"Total Events: {events}")
print(f"Total Athletes: {athletes}")
print(f"Total Nations: {nations}")


# In[118]:


#Nations Per Year Line Plot

#data preparation
#counts unique nations per year
nations_p_yr = df_sum.groupby('Year')['NOC'].nunique()

#plots the line plots
plt.figure(figsize=(14,8))

#Nations plot
plt.plot(nations_p_yr.index, nations_p_yr.values, label='Nations', color = 'blue', marker = 'o')

#Add labels, title, and legend
plt.title('Nation Olympic Participation Trend Over the Years')
plt.xlabel('Year', fontsize=14)
plt.ylabel('Count', fontsize=14)
plt.legend(title='Legend', fontsize=12)
plt.grid(alpha=0.4)

#show the plot
plt.show()


# In[120]:


#Events Per Year Line Plot

#Data Preparation
#counts unique events per year
events_p_yr = df_sum.groupby('Year')['Event'].nunique()

#plots the line plots
plt.figure(figsize=(14,8))

#Events plot
plt.plot(events_p_yr.index, events_p_yr.values, label='Events', color = 'green', marker = 's')

#Add labels, title, and legend
plt.title('Event Olympic Trends Over the Years')
plt.xlabel('Year', fontsize=14)
plt.ylabel('Count', fontsize=14)
plt.legend(title='Legend', fontsize=12)
plt.grid(alpha=0.4)

#show the plot
plt.show()


# In[122]:


#Athletes Per Year Line Plot

#remove duplicates for accurate counting
df_unique = df_sum.drop_duplicates(subset = ['Year', 'ID'])

#counts unique athletes per year
athletes_p_yr = df_sum.groupby('Year')['ID'].nunique()

#plots the line plots
plt.figure(figsize=(14,8))

#Athletes plot
plt.plot(athletes_p_yr.index, athletes_p_yr.values, label='Ahtletes', color = 'red', marker = '^')

#Add labels, title, and legend
plt.title('Athlete Olympic Participation Trends Over the Years')
plt.xlabel('Year', fontsize=14)
plt.ylabel('Count', fontsize=14)
plt.legend(title='Legend', fontsize=12)
plt.grid(alpha=0.4)

#show the plot
plt.show()


# In[124]:


#Heatmap for number of events for each sport/event

st.title('Number of Events over Time(Every Sport)')
fig, ax = plt.subplots(figsize = (20,20))
x = df_sum.drop_duplicates(['Year', 'Sport', 'Event'])
ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', 
                               aggfunc='count').fillna(0).astype('int'), annot=True)
st.pyplot(fig)


# In[139]:


#Top 15 most successful athletes of all time

#Filters rows with non-null medal values (includes only rows where there is a medal won)
medal_data = df_sum[df_sum['Medal'] != 'None']

#Groups by athlete and calculates total medals won (by category)
ath_medal=(
    medal_data.groupby(['Name', 'Sport', 'NOC'])
    .agg(
        Golds=('Medal', lambda x: (x == 'Gold').sum()),
        Silvers=('Medal', lambda x: (x == 'Silver').sum()),
        Bronzes=('Medal', lambda x: (x == 'Bronze').sum()),
        Total=('Medal', 'count')
    )
    .sort_values(by='Total', ascending=False)
)

#Resets the index
ath_medal.reset_index(inplace=True)

#selects the top 15 athletes
top_15_ath = ath_medal.head(15)

#Displays the results
print('Top 15 Most Successful Athletes of All Time')
top_15_ath


# ### Country Analysis

# In[152]:


#Plots the chosen country's gold, silver, bronze and total medal count 
#throughout the years 

#filters rows with no Medals won out
medal_data = df_sum[df_sum['Medal'] != 'None']

#grouping by Year, Country/NOC, and medal to count medals
country_medals = (
    medal_data.groupby(['Year', 'NOC', 'Medal'])
    .size()
    .unstack(fill_value = 0)
    .reset_index()
)

#Add a Total column for the sum of all medals
country_medals['Total'] = country_medals['Gold'] + country_medals['Silver'] + country_medals['Bronze']

#function to create a line plot for a specific country
def plot_med_by_country():
    #getting user input
    country = input('Enter the 3-letter NOC code for the country of choice (ex. USA, CAN): ').upper()

    #filter data for the selected country
    country_data = country_medals[country_medals['NOC'] == country]

    #check if the country exists
    if country_data.empty:
        print(f"No data found for the country {country}. Please try again.")
        return

    #plot the data
    plt.figure(figsize=(14,8))
    plt.plot(country_data['Year'], country_data['Gold'], label = 'Gold', color='gold', marker='o')
    plt.plot(country_data['Year'], country_data['Silver'], label = 'Silver', color='silver', marker='s')
    plt.plot(country_data['Year'], country_data['Bronze'], label = 'Bronze', color='darkgoldenrod', marker='^')
    plt.plot(country_data['Year'], country_data['Total'], label = 'Total', color='blue', linestyle='--', marker='*')

    #adding labels, title, legend, and grid
    plt.title(f'Medals won by {country} Over the Years', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Number of Medals', fontsize=14)
    plt.legend(title='Medal Typle', fontsize=12)
    plt.grid(alpha=0.4)

    #show the plot
    plt.show()

plot_med_by_country()


# In[159]:


#plots just the total medal count for the chosen country 

#filters rows with no Medals won out
medal_data = df_sum[df_sum['Medal'] != 'None']

#grouping by Year, Country/NOC, and medal to count medals
country_medals = (
    medal_data.groupby(['Year', 'NOC', 'Medal'])
    .size()
    .unstack(fill_value = 0)
    .reset_index()
)

#Add a Total column for the sum of all medals
country_medals['Total'] = country_medals['Gold'] + country_medals['Silver'] + country_medals['Bronze']

#function to create a line plot for a specific country
def plot_med_by_country():
    #getting user input
    country = input('Enter the 3-letter NOC code for the country of choice (ex. USA, CAN): ').upper()

    #filter data for the selected country
    country_data = country_medals[country_medals['NOC'] == country]

    #check if the country exists
    if country_data.empty:
        print(f"No data found for the country {country}. Please try again.")
        return

    plt.figure(figsize=(14,8))
    plt.plot(country_data['Year'], country_data['Total'], label='Total', color='blue', linestyle='--', marker='*')
    
    #adding labels, title, legend, and grid
    plt.title(f'Medals won by {country} Over the Years', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Number of Medals', fontsize=14)
    plt.legend(title='Medal Typle', fontsize=12)
    plt.grid(alpha=0.4)

    plt.show()

plot_med_by_country()


# In[181]:


#Heatmap for number of events for each sport/event by country

#function to generate a heatmap for a user-selected country
def event_hm_by_country():
    
    #getting user input
    country = input('Enter the 3-letter NOC code for the country of choice (ex. USA, CAN): ').upper()

    #drops rows if medal is none
    medal_data = df_sum[df_sum['Medal'] != 'None']
    
    #filter data for the selected country
    country_data = medal_data[medal_data['NOC'] == country]

    #check if the country exists
    if country_data.empty:
        print(f"No data found for the country {country}. Please try again.")
        return

    #group data by sport and year to count the number of events
    event_count = (
        country_data.groupby(['Year', 'Sport'])
        .size()
        .unstack(fill_value=0)
    )

    #creates the heatmap
    plt.figure(figsize=(16,10))
    sns.heatmap(event_count, annot=True, fmt='d')

    #Add titles and labels
    plt.title(f'{country} Excels in the Following Sports')
    plt.xlabel('Sport', fontsize=14)
    plt.ylabel('Year', fontsize=14)

    #rotate sport names for better readability
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)

    #show the heatmap
    plt.tight_layout()
    plt.show()

#calls the function
event_hm_by_country()


# In[221]:


#top 10 athletes by user chosen country

#function to get the top 10 athletes by country
def top_10_ath_cntry():
    #getting user input
    country = input('Enter the 3-letter NOC code for the country of choice (ex. USA, CAN): ').upper()

    #drops rows if medal is none
    medal_data = df_sum[df_sum['Medal'] != 'None']
    
    #filter data for the selected country
    country_data = medal_data[medal_data['NOC'] == country]

    #check if the country exists
    if country_data.empty:
        print(f"No data found for the country {country}. Please try again.")
        return

    #group by athletes and count their medals
    top_athletes = (
        country_data.groupby(['Name', 'Sport'])['Medal']
        .count()
        .reset_index()
        .sort_values(by='Medal', ascending= False)
    )

    #get top 10 athletes
    top_10 = top_athletes.head(10)

    #Displays the top 10 athletes
    print(f'Top 10 Athletes from {country} by Medals Won: ')
    print(top_10)

#call function
top_10_ath_cntry()


# ### Athlete Analysis

# In[193]:


#Distribution of Age

#Drop duplicates and NaN in the Age column
def age_dist_medal():
    #drop rows with NaN in the Age column
    clean_data = df_sum.dropna(subset=['Age', 'Medal'])

    #Drop duplicate athletes for each medal category
    clean_data = clean_data.drop_duplicates(subset=['Name', 'Medal'])

    #create the distribution plot
    plt.figure(figsize=(12,8))
    sns.kdeplot(data=clean_data, x='Age', hue='Medal', fill=False, common_norm=False, alpha =0.6)

    #Add titles and labels
    plt.title("Age Distribution by Medal Category", fontsize=16)
    plt.xlabel('Age', fontsize=14)
    plt.ylabel('Density', fontsize=14)
    plt.legend(title='Medal Type', fontsize=12)
    plt.grid(alpha=0.4)
    
    #show the plot
    plt.tight_layout()
    plt.show()

#call function
age_dist_medal()


# In[201]:


#Look at the Age Distribution for all sports for Gold medalists
#Drop duplicates and NaN in the Age column
def age_dist_medal_sport():
    #filters data for gold medalists only
    gold_medals = df_sum[(df_sum['Medal'] == 'Gold')]
    
    #drop rows with NaN in the Age column
    gold_medals = gold_medals.dropna(subset=['Age'])

    #Drop duplicate athletes for each medal category
    gold_medals = gold_medals.drop_duplicates(subset=['Name', 'Sport'])

    #create the distribution plot
    plt.figure(figsize=(14,8))
    sns.kdeplot(data=gold_medals, x='Age', hue='Sport', fill=False, common_norm=False, alpha =0.7, linewidth=2)

    #Add titles and labels
    plt.title("Age Distribution for Gold Medalists by Sport", fontsize=16)
    plt.xlabel('Age', fontsize=14)
    plt.ylabel('Density', fontsize=14)
    plt.legend(title='Sport', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(alpha=0.3)
    
    #show the plot
    plt.tight_layout()
    plt.show()

#call function
age_dist_medal_sport()


# In[211]:


#comparing the height vs. weight of user selected sports
#looks at medal won and gender

#function to create scatter plot
def height_v_weight():
    #getting user sport input
    sport = input('Enter the sport to analyze (ex. swimming, basketball, etc): ')

    #filter data based off chosen sport
    sport_data = df_sum[df_sum['Sport'] == sport]

    #handles missing values in height/weight and medal columns
    sport_data = sport_data.dropna(subset=['Height', 'Weight'])

    #fill missing medals with No Medal
    sport_data['Medal'] = sport_data['Medal'].fillna('None')

    plt.figure(figsize=(12,8))
    sns.scatterplot(data=sport_data, x='Weight', y='Height', hue='Medal', style='Sex', palette ='viridis', alpha=0.7, s=100)

    #title and labels
    plt.title(f'Height vs. Weight of athletes in {sport}', fontsize=16)
    plt.xlabel('Weight(kg)', fontsize=14)
    plt.ylabel('Height (cm)', fontsize=14)
    plt.legend(title='Medal / Gender', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(alpha=0.3)

    #show plot
    plt.tight_layout()
    plt.show()

#call function
height_v_weight()


# In[215]:


#comparing the male vs. female participation throughout the years

#function to create the line plot of male v. female over the years
def men_v_women():
    #group data by year and sex, then count the number of participants
    gender_count = df_sum.groupby(['Year', 'Sex'])['ID'].nunique().reset_index()

    #pivot data to have separate columns for male and female
    gender_count_pivot = gender_count.pivot(index='Year', columns='Sex', values='ID').fillna(0)

    #rename columns for clarity
    gender_count_pivot.columns = ['Female', 'Male']

    #plot data
    plt.figure(figsize=(12,8))
    sns.lineplot(data=gender_count_pivot, linewidth=2.5)

    #add titles and labels
    plt.title('Male vs. Female Participants in the Olympics over the Years', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Number of Participants', fontsize=14)
    plt.legend(title='Gender', labels=['Female', 'Male'])
    plt.grid(alpha=0.3)

    #show plot
    plt.tight_layout()
    plt.show()

#call function
men_v_women()

