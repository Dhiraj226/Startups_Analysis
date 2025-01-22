import pandas as pd
import streamlit as st  
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='Startup Analysis')
df=pd.read_csv('database\startup_cleaned.csv')

df.rename(columns={'amount':'amount(cr)'},inplace=True)
df['date']=df['date'].astype('datetime64[ns]')
df['year']=df['date'].dt.year
df['month']=df['date'].dt.month


def investors(investor):
    st.subheader(investor)
    st.write('Recent Investment')
    st.dataframe(df[df['investor'].str.contains(selected)].sort_values('date',ascending=False)[['date','startup','city','amount(cr)']].head(1))
    
def ma(investor):
    big=df[df['investor'].str.contains(selected)].groupby('startup')['amount(cr)'].sum().sort_values(ascending=False).head(3)
    st.write('Biggest Investments')
    fig,ax=plt.subplots()
    ax.bar(big.index,big.values)
    st.pyplot(fig)


def ver(investor):
    vertical=df[df['investor'].str.contains(selected)].groupby('vertical')['amount(cr)'].sum()
    st.write('sector Invested')
    fig,ax1=plt.subplots()
    ax1.pie(vertical.values,labels=vertical.index,autopct='%0.01f')
    st.pyplot(fig)


def city(investor):
    city=df[df['investor'].str.contains(selected)].groupby('city')['amount(cr)'].sum().sort_values(ascending=False).head(3)
    st.write('Most Invested Cities')
    fig,ax1=plt.subplots()
    ax1.pie(city.values,labels=city.index,autopct='%0.01f')
    st.pyplot(fig)

def yearly(investor):
    plt.clf()
    yearr=df[df['investor'].str.contains(selected)].groupby(df['date'].dt.year)['amount(cr)'].sum()
    st.write('Yearly Analysis')
    x=yearr.index
    y=yearr.values
    plt.plot(x,y, marker='o')
    plt.xlabel('year')
    plt.ylabel('Investment')
    plt.title('Yearly Investment')
    plt.legend()
    plt.show()
    st.pyplot(plt)

def over():
    total=round(df['amount(cr)'].sum())
    st.metric('Total Investment',str(total)+'cr')


def high():
    amount=df.groupby('startup')['amount(cr)'].sum().sort_values(ascending=False).head(1)
    st.write('Highest Investment')
    st.dataframe(amount)


def avg():
    average=round(df['amount(cr)'].mean())
    st.metric('Average Investment',str(average)+'cr')

def num():
    number=df['startup'].nunique()
    st.metric('Total Startup',str(number))    

st.sidebar.title('Startup Funding Analysis')
option=st.sidebar.selectbox('Select One',['Overall Analysis','Investor'])



if option=='Overall Analysis':
    st.title('Overall Analysis') 
    col5,col6,col7,col8=st.columns(4)
    with col5:
        over()
    with col6:
        high()
    with col7:
        avg()    
    with col8:    
        num()
    col9,col10 = st.columns(2)
    with col9:
        st.subheader('MoM')
        select_option=st.selectbox('Select Type',['Total','Count'])
        if select_option=='Count':
            temp_df=df.groupby(['year','month'])['startup'].count().reset_index()
            temp_df['x-axix']=temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')    
            st.write('Monthly invested v/s no.of startup ')
            fig3,ax3=plt.subplots()
            ax3.plot(temp_df['x-axix'],temp_df['startup'])
            st.pyplot(fig3)
        else:
            temp_df=df.groupby(['year','month'])['amount(cr)'].sum().reset_index()
            temp_df['x-axix']=temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')    
            st.write('Monthly invested v/s Total Amount ')
            fig4,ax4=plt.subplots()
            ax4.plot(temp_df['x-axix'],temp_df['amount(cr)'])
            st.pyplot(fig4)
        
    with col10:
        st.subheader('Top Investing Sector')
        tem=df['vertical'].value_counts().head(10)
        st.write('sector Invested')
        fig7,ax7=plt.subplots()
        ax7.pie(tem.values,labels=tem.index,autopct='%0.01f')
        st.pyplot(fig7)
        

else :
    st.title('Investor Analysis')
    selected=st.sidebar.selectbox('select investor',sorted(set(df['investor'].str.split(',').sum())))
    btn2=st.sidebar.button('Find investor Details')
    if btn2:
        investors(selected)
        col1,col2 =st.columns(2)
        with col1:
            ma(selected)
        with col2:
            ver(selected)    
        col3,col4=st.columns(2)
        with col3:
            city(selected)
        with col4:
            yearly(selected)
            



        



   
    


