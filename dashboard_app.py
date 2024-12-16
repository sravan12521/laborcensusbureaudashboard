import pandas as pd
import os
import streamlit as st
import numpy as np
import plotly.express as px
from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests
import json

# folder location 

storage_folder = "labor_census_bureau"


# api items pulled 

api_items = [ "LNS11000000" ,"PRS85006092","CES0000000001",
                "LNS12000000","CES0500000008","PRS85006112"]


# class object handling api data pull

class DataPullUSLaborBureau():


    def HistoricalData(self):    

        # start range of pulling data

        prev_year = (datetime.now() - relativedelta(months=12)).year


        # api call        
        
        headers = {'Content-type': 'application/json'}


        data = json.dumps({"seriesid": api_items,"startyear":str(prev_year),"endyear":datetime.now().year,
        "registrationkey":"34cf2452001040f3ba96a89e33a46db8"})
        
        
        p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)

        # creating dataframe

        api_data = json.loads(p.text)

        for _id in api_items:

            data_obj = [x for x in api_data['Results']['series'] if x['seriesID'] ==_id]

            api_table = pd.DataFrame.from_dict(data_obj[0]['data'],orient='columns')

            api_table.to_csv(storage_folder+'/'+_id+'.csv',index=False)
    

        return {'status':"Success"}
    

    def IncrementalData(self):

        # api call        
        headers = {'Content-type': 'application/json'}

        # pull data
        data = json.dumps({"seriesid": api_items,'latest':True,
                            "registrationkey":"34cf2452001040f3ba96a89e33a46db8"})

        # making api call
        p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', 
                            data=data, headers=headers)

        api_data = json.loads(p.text)

        for _id in api_items:

            data_obj = [x for x in api_data['Results']['series'] if x['seriesID'] ==_id]

            orig_table = pd.read_csv(storage_folder+'/'+_id+'.csv')

            increm_table = pd.DataFrame.from_dict(data_obj[0]['data'],orient='columns')

            # Append df2 to df1
            append_df = pd.concat([orig_table, increm_table], ignore_index=True)

            append_df.loc[:,'year']=append_df['year'].astype(str)

            # Remove duplicates 
            unique_df = append_df.drop_duplicates(subset=['year','periodName'])

            # writing data back to storage

            unique_df.to_csv(storage_folder+'/'+_id+'.csv',index=False)

            print('loading incremental data ....')

        
        return 'successfully loaded'

api_data_pull = DataPullUSLaborBureau()

if os.path.exists(storage_folder) == False:

    os.makedirs(storage_folder)

    api_data_pull.HistoricalData()

#                                                            Part 2 : Dashboard Layer

def CalculateYearMonthColumn(df):

    # mappings for month and quarters

    month_q_map = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
        'July': '07', 'August': '08', 'September': '09', 'October': '10', 
        'November': '11', 'December': '12',
        "1st Quarter":'03','2nd Quarter':"06","3rd Quarter":"09","4th Quarter":"12"
    }

    df['yearMonth'] = df['year'].astype(str) + '-' + df['periodName'].map(month_q_map)

    df['date']=pd.to_datetime(df['yearMonth'])

    return df

# Title
# Configure the page layout to 'wide'
st.set_page_config(page_title="Dashboard", layout="wide")

st.title("U.S Bureau Of Labor Statistics - Dashboard")

# Sidebar To Load Incremental Data & Filter The Charts Scope

st.sidebar.header('Dashboard Date Range')

start_date = st.sidebar.date_input("Start Date", 
            value=datetime.now() - relativedelta(months=15), 
            min_value=datetime.now() - relativedelta(months=15), 
            max_value=datetime.now())

end_date = st.sidebar.date_input("End Date", 
            value=datetime.now(), 
            min_value=datetime.now() - relativedelta(months=15), 
            max_value=datetime.now())

# Incremental Load Button

# if st.sidebar.button('Load Latest Data'):    

#     api_data_pull.IncrementalData()

#     st.rerun()


# Reading the tables

civilian_labor_force = pd.read_csv(storage_folder+'/'+'LNS11000000.csv')

non_farm_productivity_df = pd.read_csv(storage_folder+'/'+'PRS85006092.csv')

non_farm_employment_df = pd.read_csv(storage_folder+'/'+'CES0000000001.csv')

non_farm_bu_cost_df = pd.read_csv(storage_folder+'/'+'PRS85006112.csv')

civ_employment_df = pd.read_csv(storage_folder+'/'+'LNS12000000.csv')

hourly_earnings_prod_emp_df = pd.read_csv(storage_folder+'/'+'CES0500000008.csv')

# filtering by timestamp from sidebar

civ_labor_force = CalculateYearMonthColumn(civilian_labor_force)

civ_labor_force_filtered = civ_labor_force.loc[(civ_labor_force['date']>=pd.Timestamp(start_date))&
                                                (civ_labor_force['date']<=pd.Timestamp(end_date))]

civ_labor_force_filtered.reset_index(inplace=True,drop=True)

non_farm_prod_df = CalculateYearMonthColumn(non_farm_productivity_df)

non_farm_prod_filtered_df = non_farm_prod_df.loc[(non_farm_prod_df['date']>=pd.Timestamp(start_date))&
                                                (non_farm_prod_df['date']<=pd.Timestamp(end_date))]

non_farm_prod_filtered_df.reset_index(inplace=True,drop=True)

non_farm_employment_df = CalculateYearMonthColumn(non_farm_employment_df)

non_farm_employment_filtered_df = non_farm_employment_df.loc[(non_farm_employment_df['date']>=pd.Timestamp(start_date))&
                                                (non_farm_employment_df['date']<=pd.Timestamp(end_date))]

civ_employment_df = CalculateYearMonthColumn(civ_employment_df)

civ_employment_filtered_df = civ_employment_df.loc[(civ_employment_df['date']>=pd.Timestamp(start_date))&
                                                (civ_employment_df['date']<=pd.Timestamp(end_date))]

non_farm_bu_cost_df = CalculateYearMonthColumn(non_farm_bu_cost_df)

non_farm_bu_cost_filtered_df = non_farm_bu_cost_df.loc[(non_farm_bu_cost_df['date']>=pd.Timestamp(start_date))&
                                                (non_farm_bu_cost_df['date']<=pd.Timestamp(end_date))]

hourly_earnings_prod_emp_df = CalculateYearMonthColumn(hourly_earnings_prod_emp_df)

hourly_earnings_prod_emp_filtered_df = hourly_earnings_prod_emp_df.loc[(hourly_earnings_prod_emp_df['date']>=pd.Timestamp(start_date))&
                                                (hourly_earnings_prod_emp_df['date']<=pd.Timestamp(end_date))]


# plotting the charts - section 1

col1, col2 =st.columns(2)

with col1:

    st.text('Number Of Civilian Employees Over A Period')

    st.bar_chart(civ_labor_force_filtered[['yearMonth','value']], 
                    x="yearMonth", 
                    y="value",x_label='Month',
                    y_label='Number Of Laborers',
                    use_container_width=True)

with col2:

    fig = px.pie(non_farm_prod_filtered_df, names='periodName', 
    values='value', title='Quarterwise Non-Farm Productivity')

    st.plotly_chart(fig,use_container_width=True)


col3,col4 =st.columns(2)

with col3:

    st.text('Total Nonfarm Employment - Seasonally Adjusted')

    st.bar_chart(non_farm_employment_filtered_df, 
                x="yearMonth", y="value", color="year",use_container_width=True)

with col4:

    st.text('Civilian Employement - Seasonally Adjusted')

    st.bar_chart(civ_employment_filtered_df, 
                x="yearMonth", y="value",color='year',use_container_width=True)


col5,col6 = st.columns(2)

with col5:
    
    st.text('Total Private Average Hourly Earnings - Seasonally Adjusted')

    st.bar_chart(hourly_earnings_prod_emp_filtered_df, 
             x="yearMonth", y="value",color='year',use_container_width=True,horizontal=True,)

with col6:

    fig_6 = px.pie(non_farm_bu_cost_filtered_df[['periodName','value']], names='periodName', 
    values='value', title='Total Private Average Hourly Earnings')

    st.plotly_chart(fig_6)




# plotting the tables - section 2


st.subheader('Civilian Labor Force - Raw Data')

st.dataframe(civ_labor_force_filtered[["year","period","periodName","latest","value","footnotes"]],use_container_width=True)

st.subheader('Non-farm Business Productivity')

st.dataframe(non_farm_prod_filtered_df[["year","period","periodName","latest","value","footnotes"]],use_container_width=True)

st.subheader('Total Nonfarm Employment')

st.dataframe(non_farm_employment_filtered_df[["year","period","periodName","latest","value","footnotes"]],use_container_width=True)

st.subheader('Civilian Employment')

st.dataframe(civ_employment_filtered_df[["year","period","periodName","latest","value","footnotes"]],use_container_width=True)

st.subheader('Total Private Average Hourly Earnings')

st.dataframe(non_farm_bu_cost_filtered_df[["year","period","periodName","latest","value","footnotes"]],use_container_width=True)

st.subheader('Nonfarm Business Unit Labor Costs')

st.dataframe(hourly_earnings_prod_emp_filtered_df[["year","period","periodName","latest","value","footnotes"]],use_container_width=True)

