import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='StartUp Analysis',)
df = pd.read_csv('startup_cleaned1.csv')

# to insert 'Select One' in investor list
investor_list=sorted(set(df['investors'].str.split(',').sum()))
investor_list[0]='Seletc One'


#creating new columns for our requirments
df['date']=pd.to_datetime(df['date'],errors='coerce')



#creating function for Overall Analysis---------------------------------------------------------------------------------------------------------
def load_overall_analysis():
    st.title('OVERALL ANALYSIS')

    #calculating total investment 
    total=round(df['amount'].sum())

    #calculating max investment
    max=df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]   

    #calculating average investment
    avg=round(df.groupby('startup')['amount'].sum().mean())

    #calculating number of  funded startups
    num_startups=df['startup'].nunique()

   
    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric('Total Investment',str(total) + ' Cr')
    with col2:
        st.metric('Max Investment',str(max) + ' Cr')

    with col3:
        st.metric('Average Investment',str(avg) + ' Cr')
        
    with col4:
        st.metric('Total Startups',str(num_startups) + ' Cr')

    #creating YoY Graph-------------------------------------------------------------------------
    st.header('MoM Graph')

    selected_option=st.selectbox('Select One',['Total','Count'])

    if selected_option == 'Total':
        st.subheader('MoM Investment Graph')
        temp_df=df.groupby(['year','month'])['amount'].sum().reset_index()
    else:
        st.subheader('MoM Investment Count Graph')
        temp_df=df.groupby(['year','month'])['amount'].count().reset_index()


    temp_df['x_axis']=temp_df['month'].astype(str)+ '-' +temp_df['year'].astype(str)

    fig5, ax5 = plt.subplots(figsize=(20,20))
    ax5.plot(temp_df['x_axis'],temp_df['amount'])
    plt.xticks(rotation=90)
    st.pyplot(fig5)
        
    # ❖	Sector Analysis Pie -> top sectors(Count + Sum)---------------------------------------- 
    st.subheader('Sector Analysis')
    top_sectors_btn=st.selectbox('Select type of Analysis',['Count','Sum'])

    if top_sectors_btn== 'Count':
        st.subheader('Top Sectors Count')
        top_sectors=df.groupby('vertical')['subvertical'].count().sort_values(ascending=False).head()
    else:
        st.subheader('Top Sectors Sum')
        top_sectors=df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head()


    fig6, ax6= plt.subplots()
    ax6.pie(top_sectors,labels=top_sectors.index,autopct='%0.01f%%')
    st.pyplot(fig6)
    
    #❖	City wise funding----------------------------------------------------------------
    city_funding=df[~(df['amount']==0)].groupby('city')['amount'].sum().sort_values(ascending=False)

    st.header('City Wise Funding')

    city_wise_funding_btn=st.selectbox('Type of Data',['DataFrame','Bar Graph'])
    if city_wise_funding_btn=='DataFrame':
        st.dataframe(city_funding)

    else:
        fig7, ax7 = plt.subplots(figsize=(20,20))
        ax7.bar(city_funding.index,city_funding.values,log= True)
        ax7.set_xlabel('Citys')
        ax7.set_ylabel('Crore Rupees')
        plt.xticks(rotation=90)
        st.pyplot(fig7)

    #❖	Top Startups -> year wise -> Overall---------------------------------------------------------
    st.title('Top Startups ')

    selected_option = st.selectbox('Select Type',['select_one','yearly','Overall'])
    if selected_option == 'yearly':

        st.header('Top startups from year 2015-2020')
        col1, col2 = st.columns(2)
        with col1:
            temp_df=df[df['year'] == 2015].groupby('startup')['amount'].sum().sort_values(ascending=False).head(5)

            fig9, ax10 = plt.subplots(figsize=(8,8))
            ax10.pie(temp_df, labels=temp_df.index, autopct='%0.1f%%')
            plt.title('year - 2015')
            st.pyplot(fig9)

        with col2:
            temp_df=df[df['year'] == 2016].groupby('startup')['amount'].sum().sort_values(ascending=False).head(5)

            fig9, ax10 = plt.subplots(figsize=(8,8))
            ax10.pie(temp_df, labels=temp_df.index, autopct='%0.1f%%')
            plt.title('year - 2016')
            st.pyplot(fig9)



        col3, col4 = st.columns(2)
        with col3:
            temp_df=df[df['year'] == 2017].groupby('startup')['amount'].sum().sort_values(ascending=False).head(5)

            fig9, ax10 = plt.subplots(figsize=(8,8))
            ax10.pie(temp_df, labels=temp_df.index, autopct='%0.1f%%')
            plt.title('year - 2017')
            st.pyplot(fig9)

        with col4:
            temp_df=df[df['year'] == 2018].groupby('startup')['amount'].sum().sort_values(ascending=False).head(5)

            fig9, ax10 = plt.subplots(figsize=(8,8))
            ax10.pie(temp_df, labels=temp_df.index, autopct='%0.1f%%')
            plt.title('year - 2018')
            st.pyplot(fig9)


        col5, col6 = st.columns(2)
        with col5:
            temp_df=df[df['year'] == 2019].groupby('startup')['amount'].sum().sort_values(ascending=False).head(5)

            fig9, ax10 = plt.subplots(figsize=(8,8))
            ax10.pie(temp_df, labels=temp_df.index, autopct='%0.1f%%')
            plt.title('year - 2019')
            st.pyplot(fig9)


        with col6:
            temp_df=df[df['year'] == 2020].groupby('startup')['amount'].sum().sort_values(ascending=False).head(5)

            fig9, ax10 = plt.subplots(figsize=(8,8))
            ax10.pie(temp_df, labels=temp_df.index, autopct='%0.1f%%')
            plt.title('year - 2020')
            st.pyplot(fig9)

    elif selected_option =='Overall':
        temp_df=df.groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        fig10, ax11 = plt.subplots(figsize=(10,10))
        ax11.pie(temp_df, labels=temp_df.index, autopct='%0.1f%%')
        st.pyplot(fig10)

    #❖	Top investors--------------------------------------------------------------------------------
    top_investors=df.groupby('investors')['amount'].sum().head()
    st.header('Top Investors')

    st.table(top_investors)

    #❖	Funding Heatmap----------------------------------------------------------------------------

    


#creating function for Startup**************************************************************************************************************
def load_startup_analysis(input_startup):
    st.subheader(f'STARTUP NAME:- {input_startup}')

    # industry, subindustry, location---------------------------------------------------------------
    startup_details=df[df['startup'].isin([input_startup])][['startup','vertical','subvertical','city']].set_index('startup')
    st.subheader('Startup Details')
    st.dataframe(startup_details)

    #invertors details--------------------------------------------------------------------------------
    temp_df=df[df['startup'].isin([input_startup])][['investors','round','date']]
    temp_df['investors']=temp_df['investors'].str.split(',')

    data=[]
    index=0
    for i in temp_df['investors']:  # to seperate all investors
        for j in i:
        
            round=temp_df['round'].tolist()
            date=temp_df['date'].tolist()

            data.append([j,round[index],date[index]])
        index+=1
        
    new_df=pd.DataFrame(data,columns=['Investors','Stage','Date'])

    st.subheader('Startup Investors Details')
    st.dataframe(new_df)

    #❖	Similar company-----------------------------------------------------------------------------

    temp_df=df[df['startup']==input_startup]['vertical'].tolist()
    similar_startup=df[df['vertical'].isin(temp_df)][['startup','vertical','subvertical','city','investors','round','amount','date']].set_index('startup').sample(5,replace=True)
    st.subheader('Similar Startups')
    st.dataframe(similar_startup)









#creating function for Investors**************************************************************************************************************
def load_investor_details(investor):
    st.header(f'Investor Name :{investor}')
    #load the recent 5 investment details
    last5_df=df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','city','round','amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)


#creating columns
    col1,col2=st.columns(2)
    with col1:
        #biggest investments---------------------------------------------------------------------------------
        big_series=df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        # st.bar_chart(big_series)
        fig, ax = plt.subplots(figsize=(10,10))
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)
        



    with col2:
        #creating investment in sector --> Pie-------------------------------------------------------------------
        vertical_series=df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors Invested in')

        fig1, ax1 = plt.subplots(figsize=(10,10)) # to change the size of pie chart(figsize=(6->width,5->Hieght))
        ax1.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f%%")
        st.pyplot(fig1)



    col3,col4=st.columns(2)

    with col3:
        #creating investment in stage --> Pie ---------------------------------------------------------------
                        
        stage_series=df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Investment in Stages')

        fig2, ax2 = plt.subplots(figsize=(15,15))
        ax2.pie(stage_series,labels=stage_series.index,autopct="%0.01f%%")
        st.pyplot(fig2)

    with col4:
        #creating investment in city --> Pie-----------------------------------------------------------------

        city_series=df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('Investment in City')

        fig3, ax3 = plt.subplots(figsize=(10,10))
        ax3.pie(city_series,labels=city_series.index,autopct="%0.01f%%")
        st.pyplot(fig3)

    #creating investments year by year --> line chart----------------------------------------------------------
    df['year']=df['date'].dt.year
    year_series=df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('Investments Year by Year')

    fig4, ax4 = plt.subplots()
    ax4.plot(year_series.index,year_series.values)
    st.pyplot(fig4)

     #creating similar investors---------------------------------------------------------------------------------
    similar=list(sorted(set(df[df["investors"].str.contains('1Crowd')].sample(5,replace=True)['investors'].str.split(',').sum())))
    st.title('Similar Investors')
    similar_investors_df=pd.DataFrame(similar,columns=['Investors'])
    st.dataframe(similar_investors_df)



    

   
#start of the project---------------------------------------------------------------------------------------------------------------------------
st.title('INDIAN STARTUPS ANALYSIS')
st.subheader('INTRODUCTION')
st.write("""
This project aims to analyze the growth and trends of Indian startups from 2015 to 2020. Using streamlit, Python, pandas, and data visualization, the project will provide insights into the Indian startup ecosystem and its evolution over the years.

The data for this project will be collected from various sources such as industry reports and databases, and will include information such as the number of startups, funding received, and sector-wise distribution.

With the help of Python's pandas library, the collected data will be cleaned, transformed, and organized into a structured format, making it easier to analyze and visualize. The streamlit library will be used to build an interactive web-based interface to display the results and insights derived from the analysis.

Data visualization techniques, such as line charts, bar graphs, and pie charts, will be used to effectively communicate the results and provide a clear understanding of the trends and patterns in the Indian startup ecosystem.

This project will provide valuable insights into the Indian startup landscape, its growth and evolution, and the key players and trends that are shaping the future of startups in India. The insights derived from this project can be used by entrepreneurs, investors, and policy makers to make informed decisions and drive the growth of the Indian startup ecosystem.
""")
st.sidebar.title('START FUNDING ANALYSIS')

option = st.sidebar.selectbox('TYPE OF ANALYSIS',['Select One','Overall Analysis','StartUp','Investors'])

if option == 'Overall Analysis':

    load_overall_analysis()


elif option == 'StartUp':
    st.title('STARTUP ANALYSIS')
    input_startup=st.sidebar.selectbox("STARTUP'S",sorted(df['startup'].unique().tolist()))
    btn2=st.sidebar.button('Find StartUp Details')
    if btn2:
        load_startup_analysis(input_startup)
        
elif option == 'Investors':
    st.title('INVESTORS ANALYSIS')
    select_investor=st.sidebar.selectbox('INVESTORS',investor_list)
    btn3=st.sidebar.button('Find Investors Details')
    if btn3:
        load_investor_details(select_investor)
