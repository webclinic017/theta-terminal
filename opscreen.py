from openbb_terminal.sdk import openbb
import matplotlib.pyplot as plt
import streamlit as st
import streamlit.components.v1 as components
import datetime as dt
import pandas as pd
from yahooquery import Ticker
import datetime
import pandas as pd
from datetime import timedelta, date
import pandas_market_calendars as mcal
from finvizfinance.quote import finvizfinance
from finvizfinance.news import News
from finvizfinance.screener.overview import Overview
from streamlit_js_eval import streamlit_js_eval
from pathlib import Path
from deta import Deta
import os
from streamlit_extras.dataframe_explorer import dataframe_explorer
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import StockBarsRequest
import numpy as np
import base64
import pytz
import mibian as mb

st.set_page_config(page_title="tʰɛːta Terminal", page_icon="⏳ ", layout="wide", initial_sidebar_state="collapsed",
                   menu_items=None)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            .viewerBadge_container__1QSob {visibility: hidden;} 
            .embeddedAppMetaInfoBar_container__LZA_B  {visibility: hidden;} 
            .viewerBadge_container__1QSob styles_viewerBadge__1yB5_ {visibility: hidden;} 
            .viewerBadge_link__1S137 {visibility: hidden;} 
            .styles_terminalButton__3xUnY {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)

import seaborn as sns
sns.set_palette('Set3')

with open('./files/wave.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


st.set_option('deprecation.showPyplotGlobalUse', False)

subm = False

DETA_KEY = st.secrets["DETA_KEY"]


deta = Deta(DETA_KEY)

drive_name = 'theta-data'
drive = deta.Drive(drive_name)

#large_file = drive.get("options_data.parquet")
#with open("options_data.parquet", "wb+") as f:
    #for chunk in large_file.iter_chunks(4096):
        #f.write(chunk)
    #large_file.close()

#df = pd.read_parquet(r'C:\Users\Markus\Desktop\Jupyter\options_data.parquet')

# Filter Section => Sidebar

# Index = st.sidebar.selectbox('Index:',['Any','S&P 500', 'DJIA'],key='Index')
# Sector = st.sidebar.selectbox('Sector:',['Any', 'Basic Materials', 'Communication Services', 'Consumer Cyclical', 'Consumer Defensive', 'Energy', 'Financial', 'Healthcare', 'Industrials', 'Real Estate', 'Technology', 'Utilities'],key='Sector')
# Industry = st.sidebar.selectbox('Industry:',['Any', 'Stocks only (ex-Funds)', 'Exchange Traded Fund', 'Advertising Agencies', 'Aerospace & Defense', 'Agricultural Inputs', 'Airlines', 'Airports & Air Services', 'Aluminum', 'Apparel Manufacturing', 'Apparel Retail', 'Asset Management', 'Auto Manufacturers', 'Auto Parts', 'Auto & Truck Dealerships', 'Banks - Diversified', 'Banks - Regional', 'Beverages - Brewers', 'Beverages - Non-Alcoholic', 'Beverages - Wineries & Distilleries', 'Biotechnology', 'Broadcasting', 'Building Materials', 'Building Products & Equipment', 'Business Equipment & Supplies', 'Capital Markets', 'Chemicals', 'Closed-End Fund - Debt', 'Closed-End Fund - Equity', 'Closed-End Fund - Foreign', 'Coking Coal', 'Communication Equipment', 'Computer Hardware', 'Confectioners', 'Conglomerates', 'Consulting Services', 'Consumer Electronics', 'Copper', 'Credit Services', 'Department Stores', 'Diagnostics & Research', 'Discount Stores', 'Drug Manufacturers - General', 'Drug Manufacturers - Specialty & Generic', 'Education & Training Services', 'Electrical Equipment & Parts', 'Electronic Components', 'Electronic Gaming & Multimedia', 'Electronics & Computer Distribution', 'Engineering & Construction', 'Entertainment', 'Farm & Heavy Construction Machinery', 'Farm Products', 'Financial Conglomerates', 'Financial Data & Stock Exchanges', 'Food Distribution', 'Footwear & Accessories', 'Furnishings, Fixtures & Appliances', 'Gambling', 'Gold', 'Grocery Stores', 'Healthcare Plans', 'Health Information Services', 'Home Improvement Retail', 'Household & Personal Products', 'Industrial Distribution', 'Information Technology Services', 'Infrastructure Operations', 'Insurance Brokers', 'Insurance - Diversified', 'Insurance - Life', 'Insurance - Property & Casualty', 'Insurance - Reinsurance', 'Insurance - Specialty', 'Integrated Freight & Logistics', 'Internet Content & Information', 'Internet Retail', 'Leisure', 'Lodging', 'Lumber & Wood Production', 'Luxury Goods', 'Marine Shipping', 'Medical Care Facilities', 'Medical Devices', 'Medical Distribution', 'Medical Instruments & Supplies', 'Metal Fabrication', 'Mortgage Finance', 'Oil & Gas Drilling', 'Oil & Gas E&P', 'Oil & Gas Equipment & Services', 'Oil & Gas Integrated', 'Oil & Gas Midstream', 'Oil & Gas Refining & Marketing', 'Other Industrial Metals & Mining', 'Other Precious Metals & Mining', 'Packaged Foods', 'Packaging & Containers', 'Paper & Paper Products', 'Personal Services', 'Pharmaceutical Retailers', 'Pollution & Treatment Controls', 'Publishing', 'Railroads', 'Real Estate - Development', 'Real Estate - Diversified', 'Real Estate Services', 'Recreational Vehicles', 'REIT - Diversified', 'REIT - Healthcare Facilities', 'REIT - Hotel & Motel', 'REIT - Industrial', 'REIT - Mortgage', 'REIT - Office', 'REIT - Residential', 'REIT - Retail', 'REIT - Specialty', 'Rental & Leasing Services', 'Residential Construction', 'Resorts & Casinos', 'Restaurants', 'Scientific & Technical Instruments', 'Security & Protection Services', 'Semiconductor Equipment & Materials', 'Semiconductors', 'Shell Companies', 'Silver', 'Software - Application', 'Software - Infrastructure', 'Solar', 'Specialty Business Services', 'Specialty Chemicals', 'Specialty Industrial Machinery', 'Specialty Retail', 'Staffing & Employment Services', 'Steel', 'Telecom Services', 'Textile Manufacturing', 'Thermal Coal', 'Tobacco', 'Tools & Accessories', 'Travel Services', 'Trucking', 'Uranium', 'Utilities - Diversified', 'Utilities - Independent Power Producers', 'Utilities - Regulated Electric', 'Utilities - Regulated Gas', 'Utilities - Regulated Water', 'Utilities - Renewable', 'Waste Management'],key='Industry')
# Market_Cap = st.sidebar.selectbox('Market Cap.:',['Any', 'Mega ($200bln and more)', 'Large ($10bln to $200bln)', 'Mid ($2bln to $10bln)', 'Small ($300mln to $2bln)', 'Micro ($50mln to $300mln)', 'Nano (under $50mln)', '+Large (over $10bln)', '+Mid (over $2bln)', '+Small (over $300mln)', '+Micro (over $50mln)', '-Large (under $200bln)', '-Mid (under $10bln)', '-Small (under $2bln)', '-Micro (under $300mln)'],key='Market_Cap')
# Price = st.sidebar.selectbox('Price:',['Any', 'Under $1', 'Under $2', 'Under $3', 'Under $4', 'Under $5', 'Under $7', 'Under $10', 'Under $15', 'Under $20', 'Under $30', 'Under $40', 'Under $50', 'Over $1', 'Over $2', 'Over $3', 'Over $4', 'Over $5', 'Over $7', 'Over $10', 'Over $15', 'Over $20', 'Over $30', 'Over $40', 'Over $50', 'Over $60', 'Over $70', 'Over $80', 'Over $90', 'Over $100', '$1 to $5', '$1 to $10', '$1 to $20', '$5 to $10', '$5 to $20', '$5 to $50', '$10 to $20', '$10 to $50', '$20 to $50', '$50 to $100'],key='Price')
# Performance = st.sidebar.selectbox('Performance:',['Any', 'Today Up', 'Today Down', 'Today -15%', 'Today -10%', 'Today -5%', 'Today +5%', 'Today +10%', 'Today +15%', 'Week -30%', 'Week -20%', 'Week -10%', 'Week Down', 'Week Up', 'Week +10%', 'Week +20%', 'Week +30%', 'Month -50%', 'Month -30%', 'Month -20%', 'Month -10%', 'Month Down', 'Month Up', 'Month +10%', 'Month +20%', 'Month +30%', 'Month +50%', 'Quarter -50%', 'Quarter -30%', 'Quarter -20%', 'Quarter -10%', 'Quarter Down', 'Quarter Up', 'Quarter +10%', 'Quarter +20%', 'Quarter +30%', 'Quarter +50%', 'Half -75%', 'Half -50%', 'Half -30%', 'Half -20%', 'Half -10%', 'Half Down', 'Half Up', 'Half +10%', 'Half +20%', 'Half +30%', 'Half +50%', 'Half +100%', 'Year -75%', 'Year -50%', 'Year -30%', 'Year -20%', 'Year -10%', 'Year Down', 'Year Up', 'Year +10%', 'Year +20%', 'Year +30%', 'Year +50%', 'Year +100%', 'Year +200%', 'Year +300%', 'Year +500%', 'YTD -75%', 'YTD -50%', 'YTD -30%', 'YTD -20%', 'YTD -10%', 'YTD -5%', 'YTD Down', 'YTD Up', 'YTD +5%', 'YTD +10%', 'YTD +20%', 'YTD +30%', 'YTD +50%', 'YTD +100%'],key='Performance')
# Current_Volume = st.sidebar.selectbox('Current Volume:',['Any', 'Under 50K', 'Under 100K', 'Under 500K', 'Under 750K', 'Under 1M', 'Over 0', 'Over 50K', 'Over 100K', 'Over 200K', 'Over 300K', 'Over 400K', 'Over 500K', 'Over 750K', 'Over 1M', 'Over 2M', 'Over 5M', 'Over 10M', 'Over 20M'],key='Current_Volume')
# Average_Volume = st.sidebar.selectbox('Average Volume:',['Any', 'Under 50K', 'Under 100K', 'Under 500K', 'Under 750K', 'Under 1M', 'Over 50K', 'Over 100K', 'Over 200K', 'Over 300K', 'Over 400K', 'Over 500K', 'Over 750K', 'Over 1M', 'Over 2M', '100K to 500K', '100K to 1M', '500K to 1M', '500K to 10M'],key='Average_Volume')
# Earnings_Date = st.sidebar.selectbox('Earnings Date:',['Any', 'Today', 'Today Before Market Open', 'Today After Market Close', 'Tomorrow', 'Tomorrow Before Market Open', 'Tomorrow After Market Close', 'Yesterday', 'Yesterday Before Market Open', 'Yesterday After Market Close', 'Next 5 Days', 'Previous 5 Days', 'This Week', 'Next Week', 'Previous Week', 'This Month'],key='Earnings_Date')
# Pattern = st.sidebar.selectbox('Pattern:',['Any', 'Horizontal S/R', 'Horizontal S/R (Strong)', 'TL Resistance', 'TL Resistance (Strong)', 'TL Support', 'TL Support (Strong)', 'Wedge Up', 'Wedge Up (Strong)', 'Wedge Down', 'Wedge Down (Strong)', 'Triangle Ascending', 'Triangle Ascending (Strong)', 'Triangle Descending', 'Triangle Descending (Strong)', 'Wedge', 'Wedge (Strong)', 'Channel Up', 'Channel Up (Strong)', 'Channel Down', 'Channel Down (Strong)', 'Channel', 'Channel (Strong)', 'Double Top', 'Double Bottom', 'Multiple Top', 'Multiple Bottom', 'Head & Shoulders', 'Head & Shoulders Inverse'],key='Pattern')
# Candlestick = st.sidebar.selectbox('Candlestick:',['Any', 'Long Lower Shadow', 'Long Upper Shadow', 'Hammer', 'Inverted Hammer', 'Spinning Top White', 'Spinning Top Black', 'Doji', 'Dragonfly Doji', 'Gravestone Doji', 'Marubozu White', 'Marubozu Black'],key='Candlestick')
# RSI = st.sidebar.selectbox('RSI (14):',['Any', 'Overbought (90)', 'Overbought (80)', 'Overbought (70)', 'Overbought (60)', 'Oversold (40)', 'Oversold (30)', 'Oversold (20)', 'Oversold (10)', 'Not Overbought (<60)', 'Not Overbought (<50)', 'Not Oversold (>50)', 'Not Oversold (>40)'],key='RSI')
# ATR = st.sidebar.selectbox('Average True Range:',['Any', 'Over 0.25', 'Over 0.5', 'Over 0.75', 'Over 1', 'Over 1.5', 'Over 2', 'Over 2.5', 'Over 3', 'Over 3.5', 'Over 4', 'Over 4.5', 'Over 5', 'Under 0.25', 'Under 0.5', 'Under 0.75', 'Under 1', 'Under 1.5', 'Under 2', 'Under 2.5', 'Under 3', 'Under 3.5', 'Under 4', 'Under 4.5', 'Under 5'],key='ATR')
# SMA20 = st.sidebar.selectbox('20-Day SMA:',['Any', 'Price below SMA20', 'Price 10% below SMA20', 'Price 20% below SMA20', 'Price 30% below SMA20', 'Price 40% below SMA20', 'Price 50% below SMA20', 'Price above SMA20', 'Price 10% above SMA20', 'Price 20% above SMA20', 'Price 30% above SMA20', 'Price 40% above SMA20', 'Price 50% above SMA20', 'Price crossed SMA20', 'Price crossed SMA20 above', 'Price crossed SMA20 below', 'SMA20 crossed SMA50', 'SMA20 crossed SMA50 above', 'SMA20 crossed SMA50 below', 'SMA20 crossed SMA200', 'SMA20 crossed SMA200 above', 'SMA20 crossed SMA200 below', 'SMA20 above SMA50', 'SMA20 below SMA50', 'SMA20 above SMA200', 'SMA20 below SMA200'],key='SMA20')
# SMA50 = st.sidebar.selectbox('50-Day SMA:',['Any', 'Price below SMA50', 'Price 10% below SMA50', 'Price 20% below SMA50', 'Price 30% below SMA50', 'Price 40% below SMA50', 'Price 50% below SMA50', 'Price above SMA50', 'Price 10% above SMA50', 'Price 20% above SMA50', 'Price 30% above SMA50', 'Price 40% above SMA50', 'Price 50% above SMA50', 'Price crossed SMA50', 'Price crossed SMA50 above', 'Price crossed SMA50 below', 'SMA50 crossed SMA20', 'SMA50 crossed SMA20 above', 'SMA50 crossed SMA20 below', 'SMA50 crossed SMA200', 'SMA50 crossed SMA200 above', 'SMA50 crossed SMA200 below', 'SMA50 above SMA20', 'SMA50 below SMA20', 'SMA50 above SMA200', 'SMA50 below SMA200'],key='SMA50')
# SMA200 = st.sidebar.selectbox('200-Day SMA:',['Any', 'Price below SMA200', 'Price 10% below SMA200', 'Price 20% below SMA200', 'Price 30% below SMA200', 'Price 40% below SMA200', 'Price 50% below SMA200', 'Price 60% below SMA200', 'Price 70% below SMA200', 'Price 80% below SMA200', 'Price 90% below SMA200', 'Price above SMA200', 'Price 10% above SMA200', 'Price 20% above SMA200', 'Price 30% above SMA200', 'Price 40% above SMA200', 'Price 50% above SMA200', 'Price 60% above SMA200', 'Price 70% above SMA200', 'Price 80% above SMA200', 'Price 90% above SMA200', 'Price 100% above SMA200', 'Price crossed SMA200', 'Price crossed SMA200 above', 'Price crossed SMA200 below', 'SMA200 crossed SMA20', 'SMA200 crossed SMA20 above', 'SMA200 crossed SMA20 below', 'SMA200 crossed SMA50', 'SMA200 crossed SMA50 above', 'SMA200 crossed SMA50 below', 'SMA200 above SMA20', 'SMA200 below SMA20', 'SMA200 above SMA50', 'SMA200 below SMA50'],key='SMA200')
# Volatility = st.sidebar.selectbox('Volatility:',['Any', 'Week - Over 3%', 'Week - Over 4%', 'Week - Over 5%', 'Week - Over 6%', 'Week - Over 7%', 'Week - Over 8%', 'Week - Over 9%', 'Week - Over 10%', 'Week - Over 12%', 'Week - Over 15%', 'Month - Over 2%', 'Month - Over 3%', 'Month - Over 4%', 'Month - Over 5%', 'Month - Over 6%', 'Month - Over 7%', 'Month - Over 8%', 'Month - Over 9%', 'Month - Over 10%', 'Month - Over 12%', 'Month - Over 15%'],key='Volatility')
# Analyst = st.sidebar.selectbox('Analyst Recom.:',['Any', 'Strong Buy (1)', 'Buy or better', 'Buy', 'Hold or better', 'Hold', 'Hold or worse', 'Sell', 'Sell or worse', 'Strong Sell (5)'],key='Analyst')
# d20_HL = st.sidebar.selectbox('20-Day High/Low:',['Any', 'New High', 'New Low', '5% or more below High', '10% or more below High', '15% or more below High', '20% or more below High', '30% or more below High', '40% or more below High', '50% or more below High', '0-3% below High', '0-5% below High', '0-10% below High', '5% or more above Low', '10% or more above Low', '15% or more above Low', '20% or more above Low', '30% or more above Low', '40% or more above Low', '50% or more above Low', '0-3% above Low', '0-5% above Low', '0-10% above Low'],key='d20_HL')
# W52_HL = st.sidebar.selectbox('52-Day High/Low:',['Any', 'New High', 'New Low', '5% or more below High', '10% or more below High', '15% or more below High', '20% or more below High', '30% or more below High', '40% or more below High', '50% or more below High', '60% or more below High', '70% or more below High', '80% or more below High', '90% or more below High', '0-3% below High', '0-5% below High', '0-10% below High', '5% or more above Low', '10% or more above Low', '15% or more above Low', '20% or more above Low', '30% or more above Low', '40% or more above Low', '50% or more above Low', '60% or more above Low', '70% or more above Low', '80% or more above Low', '90% or more above Low', '100% or more above Low', '120% or more above Low', '150% or more above Low', '200% or more above Low', '300% or more above Low', '500% or more above Low', '0-3% above Low', '0-5% above Low', '0-10% above Low'],key='W52_HL')

# st.sidebar.write("### Ticker Options")

heute = dt.datetime.now()
heute_uhrzeit = heute.strftime("%d/%m/%Y, %H:%M:%S")

with st.container():
    col1, col2 = st.columns([10, 10], gap="large")

with col1:
    st.write('')
    # st.markdown("![Alt Text](https://drive.google.com/uc?export=download&id=1QgEx2DGkzt_v-s2a_g9IEi80jRQ7oZl6)")

    components.html("""<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="utf-8">

    <style>

    .main-div h1

    {
     font-size: 21px;
    }
    </style>
      </head>
      <body>
       <div class="main-div">
        <image src ="https://drive.google.com/uc?export=download&id=1c2BvCO-czwcLjArQl8lLy35cNTpuUWio" width="100" height="100" controls controlsList="nodownload"></image>

    <script type="text/javascript">
    //Script for disabling right click on mouse
    var message="'The two most powerful warriors are patience and time. — Leo Tolstoy, War and Peace'";
    function clickdsb(){
    if (event.button==2){
    alert(message);
    return false;

    }

    }

    function clickbsb(e){
    if (document.layers||document.getElementById&&!document.all){
    if (e.which==2||e.which==3){
    return false;
    }
    }
    }
    if (document.layers){
    document.captureEvents(Event.MOUSEDOWN);
    document.onmousedown=clickbsb;
    }
    else if (document.all&&!document.getElementById){
    document.onmousedown=clickdsb;
    }
    document.oncontextmenu=new Function("alert(message);return false")
    </script>
    </div>
    </body>
    </html>""", width=100, height=100)
    st.write('tʰɛːta Terminal')

with st.container():
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1], gap="small")
with col1:
    st.write("### Option Screener")
if st.button("Refresh/ Reload Data"):
    streamlit_js_eval(js_expressions="parent.window.location.reload()")
    st.cache_data.clear()
st.text('Last Updated:' + " " + str(heute_uhrzeit))

# if st.button("Refresh/ Reload Data"):
# pyautogui.hotkey("ctrl", "F5")
st.write(' ____________________________________')

with col2:
    def color_negative_red(val):
        if type(val) != 'str':
            color = 'green' if val > 0 else 'red'
            return f'color: {color}'


    data = openbb.economy.indices()
    data[['Chg', '%Chg']] = data[['Chg', '%Chg']].apply(pd.to_numeric)

    data = data.reset_index()
    data = data.rename(columns={' ': 'Ticker'})
    data = data.set_index('Ticker')
    data2 = data.reset_index()

    data_sp500 = data2[data2["Ticker"].str.contains("S&P 500 Futures") == True].drop(['index'], axis=1).set_index(
        'Ticker')
    data_nq = data2[data2["Ticker"].str.contains("Nasdaq Composite") == True].drop(['index'], axis=1).set_index(
        'Ticker')
    data_iwm = data2[data2["Ticker"].str.contains("Russell 2000") == True].drop(['index'], axis=1).set_index('Ticker')
    data_vix = data2[data2["Ticker"].str.contains("CBOE Volatility") == True].drop(['index'], axis=1).set_index(
        'Ticker')

    # st.table(data_sp500.style.applymap(color_negative_red, subset=['Chg', '%Chg']))
    st.metric(label="S&P 500", value=data_sp500['Price'].iloc[0], delta=str(data_sp500['%Chg'].iloc[0]) + '%')

with col3:
    # st.table(data_nq.style.applymap(color_negative_red, subset=['Chg', '%Chg']))
    st.metric(label="Nasdaq", value=data_nq['Price'].iloc[0], delta=str(data_nq['%Chg'].iloc[0]) + '%')
with col4:
    # st.table(data_iwm.style.applymap(color_negative_red, subset=['Chg', '%Chg']))
    st.metric(label="Russell 2000", value=data_iwm['Price'].iloc[0], delta=str(data_iwm['%Chg'].iloc[0]) + '%')
with col5:
    # st.table(data_vix.style.applymap(color_negative_red, subset=['Chg', '%Chg']))
    st.metric(label="VIX", value=data_vix['Price'].iloc[0], delta=str(data_vix['%Chg'].iloc[0]) + '%')

with st.container():
    col1, col2 = st.columns([10, 2])

with col1:
    st.write("### News")
    fnews = News()
    all_news = fnews.get_news()
with st.expander("Top 10 recent financial news",expanded=True):
  st.dataframe(all_news['news'].head(10).set_index('Date'),use_container_width=True, height=200) #.to_markdown())
    #st.dataframe(all_news['news'].head(10).set_index('Date'), use_container_width=True, height=200)


with st.container():
    col1, col2, col3, col4, col5 = st.columns([5, 5, 5, 5, 5], gap="small")

with col1:
    DTE = st.number_input('DTE (less than)', value=60)
    type = st.radio(
        "Option Type",
        ('puts', 'calls'))

with col2:
    OTM = st.number_input('%OTM (min)', value=-5)
    choice = None

    #sector  = st.multiselect('Sector:',['Basic Materials', 'Consumer Cyclical',
                            #'Consumer Defensive','Communication Services',
                            #'Energy','ETF','Financial','Healthcare','Industrials',
                            #'Real Estate','Technology'],'Basic Materials')


    select_text = "Nothing Selected"
    multi_css = f'''
    <style>
    .stMultiSelect div div div div div:nth-of-type(2) {{visibility: hidden;}}
    .stMultiSelect div div div div div:nth-of-type(2)::before {{visibility: visible; content:"{select_text}"}}
    </style>
    '''
    st.markdown(multi_css, unsafe_allow_html=True)

    # st.write("Ticker Presets:")

    # agree = st.checkbox('Stock List (S&P 500 CV >2M Price >$1)',help ='Settings: Index: S&P500, Current Volume: >2M, Price: >$1')
    # agree2 = st.checkbox('Stock List (S&P 500 CV >5M Price <$50)', help='Settings: Index: S&P500, Current Volume: >5M, Price: <$50')
    # agree3 = st.checkbox('Stock List (Any CV >10M Price <$50)', help='Settings: Index: Any, Current Volume: >10M, Price: <$50, Ex Funds')

with col3:
    ROC = st.number_input('ROC (min)', 0, 100, value=2)
with col4:
    IV = st.number_input('IV (min)', 0, 1000, value=10)
  
with st.container():
    cpad1, col, pad2 = st.columns((1, 60, 10))

with col:
    path = os.path.dirname(__file__)

#df1 = pd.read_parquet(r'C:\Users\Markus\Desktop\Jupyter\options_all.parquet')
#df2 = pd.read_parquet(r'C:\Users\Markus\Desktop\Jupyter\options_all.parquet')
#df = pd.concat([df1,df2])



@st.cache_data(show_spinner=True)
def cached_optData():
    data_sorted = drive.get("options_sorted.parquet")
    with open("options_sorted.parquet", "wb+") as f:
        for chunk in data_sorted.iter_chunks(4096):
            f.write(chunk)
        data_sorted.close()

    df = pd.read_parquet(path + '/options_sorted.parquet')
    return df

raw = cached_optData()
df = raw.reset_index(drop=True).set_index(['symbol','expiration','optionType'])
df = df.xs(type, level=2).reset_index()

symbols = ['A', 'AA', 'AAL', 'AAP', 'AAPL', 'ABBV', 'ABNB', 'ABR', 'ABT', 'ADBE', 'ADI', 'ADM', 'AEHR', 'AEM', 'AFRM',
           'AG', 'AGNC', 'AI', 'AIG', 'ALB', 'ALGM', 'AMAT', 'AMC', 'AMD', 'AMT', 'AMZN', 'APA', 'APLD', 'APLS', 'APO',
           'APP', 'APPS', 'AR', 'ARKK', 'ARRY', 'ASAN', 'ASO', 'ATVI', 'AU', 'AUPH', 'AVGO', 'AVTR', 'AXP', 'AYX', 'AZN',
           'AZUL', 'BA', 'BABA', 'BAC', 'BAX', 'BBIO', 'BBWI', 'BBY', 'BE', 'BEKE', 'BIDU', 'BILI', 'BILL', 'BJ', 'BLDR',
           'BLNK', 'BLUE', 'BMBL', 'BMEA', 'BMY', 'BN', 'BOH', 'BP', 'BTU', 'BUD', 'BURL', 'BWA', 'BX', 'BXMT', 'BXP', 'BYND',
           'C', 'CAKE', 'CAT', 'CC', 'CCI', 'CCJ', 'CCL', 'CDAY', 'CELH', 'CF', 'CFG', 'CFLT', 'CHGG', 'CHPT', 'CHWY', 'CLF',
           'CM', 'CMA', 'CMCSA', 'COF', 'COHR', 'COIN', 'COP', 'CPE', 'CPNG', 'CPRI', 'CPRX', 'CRM', 'CROX', 'CRSP', 'CRWD',
           'CSIQ', 'CTLT', 'CVNA', 'CVS', 'CVX', 'CZR', 'DAL', 'DASH', 'DBX', 'DD', 'DDD', 'DDOG', 'DFS', 'DHI', 'DIS', 'DISH',
           'DKNG', 'DLO', 'DLR', 'DLTR', 'DNA', 'DOCN', 'DOCS', 'DOCU', 'DOW', 'DQ', 'DT', 'DV', 'DVN', 'DXCM', 'EDR', 'EGO',
           'ELAN', 'ELF', 'ENPH', 'ENVX', 'EOG', 'EQT', 'ETSY', 'EW', 'EWBC', 'EXAS', 'EXPE', 'EXPI', 'F', 'FANG', 'FCEL',
           'FCX', 'FDX', 'FGEN', 'FHN', 'FIS', 'FITB', 'FL', 'FSLR', 'FSLY', 'FSR', 'FTCH', 'FTI', 'FTNT', 'FUBO', 'FUTU',
           'FYBR', 'GDRX', 'GE', 'GFS', 'GILD', 'GLD', 'GLW', 'GM', 'GME', 'GNRC', 'GOLD', 'GOOG', 'GOOGL', 'GOOS', 'GOTU',
           'GPN', 'GPS', 'GS', 'GSK', 'GT', 'GTLB', 'HAL', 'HAS', 'HCA', 'HES', 'HOG', 'HOOD', 'HPQ', 'HUT', 'IBM', 'IEP',
           'IFF', 'IGT', 'IMGN', 'INDI', 'INMD', 'INTC', 'IOT', 'IRM', 'IWM', 'JBL', 'JD', 'JMIA', 'JOBY', 'JPM', 'KBH', 'KD',
           'KEY', 'KMI', 'KMX', 'KNX', 'KR', 'KSS', 'LAC', 'LAZR', 'LCID', 'LEN', 'LI', 'LLY', 'LNC', 'LULU', 'LUMN', 'LUV',
           'LVS', 'LYB', 'LYFT', 'LYV', 'M', 'MANU', 'MARA', 'MBLY', 'MDB', 'MET', 'META', 'MKC', 'MLCO', 'MMM', 'MODG', 'MOS',
           'MP', 'MPC', 'MPW', 'MQ', 'MRNA', 'MRO', 'MRVL', 'MS', 'MSFT', 'MTCH', 'MU', 'MVIS', 'NCLH', 'NEM', 'NEP', 'NET',
           'NFE', 'NFLX', 'NIO', 'NKE', 'NKLA', 'NLY', 'NNOX', 'NOVA', 'NRG', 'NTLA', 'NU', 'NUE', 'NVAX', 'NVDA', 'NVO', 'NWL',
           'NXT', 'OKTA', 'OMC', 'ON', 'ONON', 'OPCH', 'OPEN', 'ORCL', 'OVV', 'OXY', 'OZK', 'PACW', 'PAGS', 'PANW', 'PARA',
           'PATH', 'PAYO', 'PBR', 'PCG', 'PD', 'PDD', 'PENN', 'PFG', 'PGY', 'PINS', 'PLAY', 'PLD', 'PLNT', 'PLTK', 'PLTR',
           'PLUG', 'PM', 'PNC', 'PRU', 'PSTG', 'PSX', 'PTON', 'PXD', 'PYPL', 'QCOM', 'QQQ', 'QRVO', 'QS', 'RBLX', 'RC', 'RCL',
           'RDFN', 'RF', 'RIG', 'RIOT', 'RIVN', 'RKLB', 'RKT', 'RMBS', 'RNG', 'ROKU', 'ROST', 'RPD', 'RRC', 'RUN', 'RVLV', 'S',
           'SABR', 'SBLK', 'SCHW', 'SDGR', 'SE', 'SFIX', 'SG', 'SGEN', 'SHEL', 'SHLS', 'SHOP', 'SLB', 'SLG', 'SLV', 'SMAR',
           'SMCI', 'SNAP', 'SNDL', 'SNOW', 'SOFI', 'SOUN', 'SOXL', 'SPCE', 'SPLK', 'SPOT', 'SPR', 'SPWR', 'SPY', 'SQ', 'SQM',
           'SRPT', 'STLD', 'STNG', 'STWD', 'STX', 'STZ', 'SU', 'SWKS', 'SWN', 'T', 'TAL', 'TDOC', 'TEAM', 'TECK', 'TFC', 'TGT',
           'TGTX', 'TMC', 'TME', 'TMO', 'TMUS', 'TPR', 'TPX', 'TQQQ', 'TRGP', 'TRIP', 'TRUP', 'TSLA', 'TSM', 'TTD', 'TTWO',
           'TWLO', 'U', 'UAL', 'UBER', 'UEC', 'UNIT', 'UNP', 'UPS', 'UPST', 'USB', 'V', 'VALE', 'VFC', 'VIPS', 'VLO', 'VLY',
           'VNO', 'VTNR', 'VZ', 'W', 'WAL', 'WBA', 'WBD', 'WDC', 'WFC', 'WOLF', 'WPM', 'WW', 'WYNN', 'X', 'XLE', 'XOM', 'XPEV',
           'YEXT', 'Z', 'ZI', 'ZION', 'ZM', 'ZS', 'ZTO','ACWI', 'ACWX', 'AGG', 'AMLP', 'ANGL', 'ARKG', 'ARKK', 'ASHR', 'BIL',
            'BOIL', 'BOTZ', 'BSV', 'COWZ', 'CWB', 'DBC', 'DFAC', 'DGRO', 'DIA', 'DPST', 'DRIP', 'DUST', 'EEM', 'EFA', 'EFV',
            'EMB', 'EMLC', 'EWA', 'EWC', 'EWG', 'EWH', 'EWJ', 'EWT', 'EWU', 'EWW', 'EWY', 'EWZ', 'EZU', 'FAS', 'FAZ', 'FDL',
            'FEZ', 'FLOT', 'FLRN', 'FNDF', 'FPE', 'FTSM', 'FVD', 'FXI', 'FXN', 'GDX', 'GDXJ', 'GLD', 'GOVT', 'HIBS', 'HYG',
            'HYLB', 'IAU', 'IBB', 'ICLN', 'ICSH', 'IEF', 'IEFA', 'IEI', 'IEMG', 'IGIB', 'IGSB', 'IJH', 'IJR', 'INDA', 'IQLT',
            'ITB', 'ITOT', 'IUSB', 'IVV', 'IVW', 'IWD', 'IWF', 'IWM', 'IWN', 'IWR', 'IXUS', 'IYR', 'JDST', 'JEPI', 'JEPQ',
            'JETS', 'JNK', 'JNUG', 'JPST', 'KBE', 'KBWB', 'KOLD', 'KRE', 'KWEB', 'LABD', 'LABU', 'LQD', 'MBB', 'MCHI', 'MJ',
            'MSOS', 'MUB', 'NUGT', 'NVDS', 'OUNZ', 'PDBC', 'PFF', 'PGX', 'PSQ', 'QID', 'QLD', 'QQQ', 'QQQM', 'QUAL', 'QYLD',
            'RSP', 'RWM', 'RYLD', 'SARK', 'SCHD', 'SCHE', 'SCHF', 'SCHG', 'SCHH', 'SCHO', 'SCHP', 'SCHR', 'SCHX', 'SCO', 'SDOW',
            'SDS', 'SGOL', 'SH', 'SHV', 'SHY', 'SHYG', 'SILJ', 'SJNK', 'SLV', 'SMH', 'SOXL', 'SOXS', 'SOXX', 'SPAB', 'SPDN',
            'SPDW', 'SPEM', 'SPIB', 'SPLG', 'SPLV', 'SPSB', 'SPTI', 'SPTL', 'SPTS', 'SPXL', 'SPXS', 'SPXU', 'SPY', 'SPYD',
            'SPYG', 'SPYV', 'SQQQ', 'SRLN', 'SSO', 'SVIX', 'SVXY', 'TBT', 'TECL', 'TECS', 'TFLO', 'TIP', 'TLT', 'TMF', 'TNA',
            'TQQQ', 'TSLL', 'TSLQ', 'TWM', 'TZA', 'UCO', 'UDOW', 'UNG', 'UPRO', 'URA', 'USFR', 'USHY', 'USMV', 'USO', 'UUP',
            'UVIX', 'UVXY', 'VCIT', 'VCLT', 'VCSH', 'VEA', 'VEU', 'VGIT', 'VGK', 'VGLT', 'VGSH', 'VIXY', 'VMBS', 'VNQ', 'VOO',
            'VT', 'VTEB', 'VTI', 'VTIP', 'VTV', 'VTWO', 'VWO', 'VXUS', 'VXX', 'VYM', 'WEBL', 'XBI', 'XHB', 'XLB', 'XLC', 'XLE',
            'XLF', 'XLI', 'XLK', 'XLP', 'XLRE', 'XLU', 'XLV', 'XLY', 'XME', 'XOP', 'XRT', 'YANG', 'YINN','BITI', 'BITO', 'BIV',
            'BKLN', 'BND', 'BNDX']


def calculate_days(expiration):
    today = pd.Timestamp('today')
    return (today - expiration).days * -1

df['DTE'] = df['expiration'].apply(lambda x: calculate_days(x))
df["Contract Time"] = np.where(df["DTE"] >= 21, ">= 21", "< 21")

def percentage_change(col1, col2):
    return ((col2 - col1) / col1) * 100

df = df.set_index('symbol')

api_key = st.secrets["api_key"]
secret = st.secrets["secret"]

data_client = StockHistoricalDataClient(api_key, secret)
request_params = StockLatestQuoteRequest(symbol_or_symbols=symbols)
quotes = data_client.get_stock_latest_bar(request_params)

close = pd.DataFrame.from_dict({k: dict(v) for k,v in quotes.items()}, orient='index').reset_index(drop=True)
close = close[['symbol','close']]
close = close.rename(columns={'close': 'Last Price'})
close = close.set_index('symbol')
x = df.join(close)

today_start = datetime.date.today()
nyse = mcal.get_calendar('NYSE')
date =  pd.to_datetime(today_start) - pd.tseries.offsets.CustomBusinessDay(1, holidays = nyse.holidays().holidays)
start_date = date.strftime('%Y-%m-%d %H:%M:%S')

today_str = date.today().strftime("%Y-%m-%d")
start_date = date.today() - timedelta(days=3)
end_date = date.today() + timedelta(days=5)
nyse_schedule = nyse.schedule(start_date=start_date, end_date=end_date)

if today_str in nyse_schedule.index:
  start_date = datetime.date.today().strftime('%Y-%m-%d %H:%M:%S')
    
else:
  start_date = today_str


request_params = StockBarsRequest(
                        symbol_or_symbols=symbols,
                        timeframe=TimeFrame.Day,
                        start=start_date)

bars = data_client.get_stock_bars(request_params)
bars_df = bars.df.reset_index()

bars_df = bars_df.set_index('symbol')
x['Change'] = round(percentage_change(bars_df['open'], bars_df['close']))

x['impliedVolatility'] = round(x['impliedVolatility'] * 100, 2)
x['Annual Yield'] = round((x['lastPrice'] / x['strike']) * (365 / x['DTE']) * 100, 2)

if type == 'puts':
  x['% OTM'] = round(percentage_change(x['strike'], x['Last Price'])) * -1
  x['BE'] = x['strike'] - x['lastPrice']
  x['Delta'] = [mb.BS([x["Last Price"],x["strike"],1,x["DTE"]], volatility=x["impliedVolatility"]).putDelta 
  x['Theta'] = [mb.BS([x["Last Price"],x["strike"],1,x["DTE"]], volatility=x["impliedVolatility"]).putTheta 

if type == 'calls':
  x['% OTM'] = round((x['Last Price'] * 100 / x['strike'])) -100
  x['BE'] = x['strike'] + x['lastPrice']
  x['Delta'] = [mb.BS([x["Last Price"],x["strike"],1,x["DTE"]], volatility=x["impliedVolatility"]).callDelta 
  x['Theta'] = [mb.BS([x["Last Price"],x["strike"],1,x["DTE"]], volatility=x["impliedVolatility"]).callTheta 

x = x.rename(columns={'lastPrice': 'Mark', 'Change': '% Day Change', 'impliedVolatility': 'IV','% OTM' : 'Moneyness',
                      'lastTradeDate': 'Last Trade Date','bid': 'Bid','ask': 'Ask','openInterest':'Open Int'})
columnsTitles = ['strike', 'expiration','DTE','Last Price','% Day Change','Bid','Ask','Mark','BE','ROC','Annual Yield',
                'Open Int','Moneyness', 'IV','Sector','Contract Time', 'Last Trade Date']
x = x.reindex(columns=columnsTitles)

if today_str in nyse_schedule.index:
    x = x.loc[(x['Last Trade Date'] >= pd.Timestamp(today_start))]
else:
    x = x.loc[(x['Last Trade Date'] >= pd.Timestamp(date))]

x = x[x['DTE'] <= DTE]
x = x.loc[x['Moneyness'].between(-200,OTM)]
x = x.loc[x['ROC'].between(ROC, 100)]
x = x.loc[x['IV'].between(IV, 1000)]


x['expiration'] = pd.to_datetime(x['expiration']).dt.strftime('%Y-%m-%d')


def color_negative_red(value):
    if isinstance(value, str):
        color = 'black'
        return 'color: %s' % color
    if isinstance(value, float):
        if value > 0:
            color = "green"
            return 'color: %s' % color
        if value < 0:
            color = "red"
            return 'color: %s' % color



x = x.sort_values('ROC', ascending=False)
x = x.reset_index()
d = dict.fromkeys(x.select_dtypes('float').columns, "{:.2f}")
x['symbol'] = x['symbol'].astype('category')
x['Sector'] = x['Sector'].astype('category')
filtered_df = dataframe_explorer(x, case=False)
filtered_df['expiration'] = pd.to_datetime(filtered_df['expiration']).dt.strftime('%Y-%m-%d')
st.dataframe(filtered_df.style.applymap(color_negative_red, subset=['% Day Change','Moneyness']).format(d), height=1000, use_container_width=True)


@st.cache_data
def convert_df(filtered_df):
    return filtered_df.to_csv(index=False).encode('utf-8')

csv = convert_df(filtered_df)

with st.expander("Index Description"):
  st.markdown(
      """
| Index              | Description                                                                                                                         |
|--------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| Symbol             | Stock Ticker                                                                                                                        |
| Strike             | Strike price of option contract                                                                                                     |
| Expiration         | Contract expiration date                                                                                                            |
| DTE                | Days to expiration                                                                                                                  |
| Bid                | Contract bid price                                                                                                                  |
| Ask                | Contract ask price                                                                                                                  |
| Mark               | Contract mark price (Midprice between bid and ask prices)                                                                           |
| BE                 | Break Even (Net Debit)                                                                                                              |
| Moneyess           | The relative position of the last (underlying) price to the strike price                                                            |
| IV                 | (Implied Volatility) (captures the market's view of the likelihood of movement in a given security's price)                         |
| Open Int           | (Open Interest) Total number of outstanding option contracts that can provide a more accurate picture of its liquidity and interest |
| ROC                | (Return on Capital) Expected % return of a contract based on capital used if closed at 100% profit                                  |
| Annual Yield       | Annual yield of contract if closed at 100% each time                                                                                |
| Delta              | Measures the sensitivity of an option's theoretical value to an change in price of the underlying asset                             |
| Theta              | Theta is the rate of decline of an option's extrinsic value over time                                                               |
| Sector             | Indentified sector of the company                                                                                                   |
| Contract Timeframe | range to contract expiration (< 21 days / >= 21 days)                                                                               |
"""
)

st.download_button(
    "Download Table",
    csv,
    "file.csv",
    "text/csv",
    key='download-csv'
)
st.write(' ____________________________________')
st.write('Want to get in touch?')

st.markdown(
    "[![Foo](https://em-content.zobj.net/thumbs/120/sony/336/envelope_2709-fe0f.png)](https://twitter.com/mvnchi0)")



