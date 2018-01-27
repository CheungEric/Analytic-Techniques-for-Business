#Assignment 4 - Hypothesis Testing
#This assignment requires more individual learning than previous assignments -
#you are encouraged to check out the pandas documentation to find functions or
#methods you might not have used yet, or ask questions on Stack Overflow and
#tag them as pandas and python related. And of course, the discussion forums
#are open for interaction with your peers and the course staff.

#Definitions:
#A quarter is a specific three month period, Q1 is January through March, Q2 is
#April through June, Q3 is July through September, Q4 is October through Dec.
#A recession is defined as starting with two consecutive quarters of GDP
#decline, and ending with two consecutive quarters of GDP growth.
#A recession bottom is the quarter within a recession which had the lowest GDP.
#A university town is a city which has a high percentage of university students
#compared to the total population of the city.

#Hypothesis: University towns have their mean housing prices less effected by
#recessions. Run a t-test to compare the ratio of the mean price of houses in
#university towns the quarter before the recession starts compared to the
#recession bottom. (price_ratio=quarter_before_recession/recession_bottom)

#The following data files are available for this assignment:
#From the Zillow research data site there is housing data for the United States.
#In particular the datafile for all homes at a city level,
#City_Zhvi_AllHomes.csv, has median home sale prices at a fine grained level.

#From the Wikipedia page on college towns is a list of university towns in the
#United States which has been copy and pasted into the file university_towns.txt

#From Bureau of Economic Analysis, US Department of Commerce, the GDP over time
#of the United States in current dollars (use the chained value in 2009 dollars)
#, in quarterly intervals, in the file gdplev.xls. For this assignment, only
#look at GDP data from the first quarter of 2000 onward.

#Each function in this assignment below is worth 10%, with the exception of
#run_ttest(), which is worth 50%.

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa',
'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama',
'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana',
'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia',
'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine',
'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan',
'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam',
'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas',
'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa',
'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia',
'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York',
'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California',
'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico',
'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands',
'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia',
'ND': 'North Dakota', 'VA': 'Virginia'}

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ],
    columns=["State", "RegionName"]  )

    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from "
       (" to the end.
    3. Depending on how you read the data, you may need to remove newline
       character '\n'. '''
    with open ('university_towns.txt') as file:
        state_town = []
        for line in file:
            actual_line = line[:-1]
            if actual_line[-6:] == '[edit]':
                state = actual_line[:-6]
            elif '(' in line:
                town = actual_line[:(actual_line.index('(')-1)]
                state_town.append([state, town])
            else:
                town = actual_line
                state_town.append([state, town])
    df = pd.DataFrame(state_town, columns = ['State', 'RegionName'])

    return df
get_list_of_university_towns()

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a
    string value in a format such as 2005q3'''
    GDP = pd.ExcelFile('gdplev.xls')
    GDP = GDP.parse('Sheet1', skiprows=219)
    GDP = GDP[['1999q4', 9926.1, 12323.3]]
    GDP.columns = ['Quarter','GDP', 'GDP2009']
    for i in range(2, len(GDP)):
        if (GDP.iloc[i-2][1] > GDP.iloc[i-1][2]) and (GDP.iloc[i-1][2] > GDP.iloc[i][2]):
            return GDP.iloc[i-2][0]
get_recession_start()


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a
    string value in a format such as 2005q3'''
    GDP = pd.ExcelFile('gdplev.xls')
    GDP = GDP.parse("Sheet1", skiprows=219)
    GDP = GDP[['1999q4', 9926.1, 12323.3]]
    GDP.columns = ['Quarter','GDP', 'GDP2009']
    start = get_recession_start()
    start_count = GDP[GDP['Quarter'] == start].index.tolist()[0]
    GDP=GDP.iloc[start_count:]
    for i in range(2, len(GDP)):
        if (GDP.iloc[i-2][2] < GDP.iloc[i-1][2]) and (GDP.iloc[i-1][2] < GDP.iloc[i][2]):
            return GDP.iloc[i][0]
get_recession_end()

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a
    string value in a format such as 2005q3'''
    GDP = pd.ExcelFile('gdplev.xls')
    GDP = GDP.parse('Sheet1', skiprows=219)
    GDP = GDP[['1999q4', 9926.1, 12323.3]]
    GDP.columns = ['Quarter','GDP', 'GDP2009']
    start = get_recession_start()
    start_count = GDP[GDP['Quarter'] == start].index.tolist()[0]
    end = get_recession_end()
    end_count = GDP[GDP['Quarter'] == end].index.tolist()[0]
    GDP=GDP.iloc[start_count:end_count+1]
    bottom = GDP['GDP2009'].min()
    bottom_count = GDP[GDP['GDP2009'] == bottom].index.tolist()[0]-start_count
    return GDP.iloc[bottom_count]['Quarter']
get_recession_bottom()

def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].

    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.

    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    housing = pd.read_csv('City_Zhvi_AllHomes.csv')
    housing = housing.drop(housing.columns[[0] + list(range(3,51))], axis=1)
    housings = pd.DataFrame(housing[['State','RegionName']])

    for year in range(2000, 2017):
        if year != 2016:
            housings[str(year) + 'q1'] = housing[[str(year) + '-01', str(year) + '-02', str(year) + '-03']].mean(axis = 1)
            housings[str(year) + 'q2'] = housing[[str(year) + '-04', str(year) + '-05', str(year) + '-06']].mean(axis = 1)
            housings[str(year) + 'q3'] = housing[[str(year) + '-07', str(year) + '-08', str(year) + '-09']].mean(axis = 1)
            housings[str(year) + 'q4'] = housing[[str(year) + '-10', str(year) + '-11', str(year) + '-12']].mean(axis = 1)
        else:
            housings[str(year) + 'q1'] = housing[[str(year) + '-01', str(year) + '-02', str(year) + '-03']].mean(axis = 1)
            housings[str(year) + 'q2'] = housing[[str(year) + '-04', str(year) + '-05', str(year) + '-06']].mean(axis = 1)
            housings[str(year) + 'q3'] = housing[[str(year) + '-07', str(year) + '-08']].mean(axis = 1)

    housings['State'] = [states[state] for state in housings['State']]
    housings = housings.set_index(['State','RegionName'])

    return housings
convert_housing_data_to_quarters()

def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values,
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence.

    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''

    town = get_list_of_university_towns()
    rec_bottom = get_recession_bottom()
    rec_start = get_recession_start()
    housing = convert_housing_data_to_quarters()
    housing_rec_start = housing.columns[housing.columns.get_loc(rec_start) - 1]

    housing['ratio'] =  housing[housing_rec_start] - housing[rec_bottom]
    housing = housing[[rec_bottom, housing_rec_start, 'ratio']]
    housing = housing.reset_index()

    town_and_housing = pd.merge(housing,town,how='inner',on=['State','RegionName'])
    town_and_housing['uni'] = True
    final_housing = pd.merge(housing, town_and_housing, how='outer', on=['State','RegionName',rec_bottom, housing_rec_start, 'ratio'])
    final_housing['uni'] = final_housing['uni'].fillna(False)

    Uni_Town = final_housing[final_housing['uni'] == True]
    Not_Uni_Town = final_housing[final_housing['uni'] == False]

    t,p = ttest_ind(Uni_Town['ratio'].dropna(), Not_Uni_Town['ratio'].dropna())

    if p<0.01:
        X = True
    else:
        X = False

    if Uni_Town['ratio'].mean() < Not_Uni_Town['ratio'].mean():
        Y = "University Town"
    else:
        Y = "Not University Town"

    return(X, p, Y)

run_ttest()





    return "ANSWER"
