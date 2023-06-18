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
import numpy as np
import base64
import pytz


st.set_page_config(page_title="tʰɛːta Terminal", page_icon="⏳ ", layout="wide", initial_sidebar_state="collapsed", menu_items=None)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            .styles_streamlitAppContainer__2rBcU.styles_embed__2ZU1V  {visibility: hidden;} 
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)


import seaborn as sns
sns.set_palette('Set3')

st.set_option('deprecation.showPyplotGlobalUse', False)

subm = False




#Filter Section => Sidebar

#Index = st.sidebar.selectbox('Index:',['Any','S&P 500', 'DJIA'],key='Index')
#Sector = st.sidebar.selectbox('Sector:',['Any', 'Basic Materials', 'Communication Services', 'Consumer Cyclical', 'Consumer Defensive', 'Energy', 'Financial', 'Healthcare', 'Industrials', 'Real Estate', 'Technology', 'Utilities'],key='Sector')
#Industry = st.sidebar.selectbox('Industry:',['Any', 'Stocks only (ex-Funds)', 'Exchange Traded Fund', 'Advertising Agencies', 'Aerospace & Defense', 'Agricultural Inputs', 'Airlines', 'Airports & Air Services', 'Aluminum', 'Apparel Manufacturing', 'Apparel Retail', 'Asset Management', 'Auto Manufacturers', 'Auto Parts', 'Auto & Truck Dealerships', 'Banks - Diversified', 'Banks - Regional', 'Beverages - Brewers', 'Beverages - Non-Alcoholic', 'Beverages - Wineries & Distilleries', 'Biotechnology', 'Broadcasting', 'Building Materials', 'Building Products & Equipment', 'Business Equipment & Supplies', 'Capital Markets', 'Chemicals', 'Closed-End Fund - Debt', 'Closed-End Fund - Equity', 'Closed-End Fund - Foreign', 'Coking Coal', 'Communication Equipment', 'Computer Hardware', 'Confectioners', 'Conglomerates', 'Consulting Services', 'Consumer Electronics', 'Copper', 'Credit Services', 'Department Stores', 'Diagnostics & Research', 'Discount Stores', 'Drug Manufacturers - General', 'Drug Manufacturers - Specialty & Generic', 'Education & Training Services', 'Electrical Equipment & Parts', 'Electronic Components', 'Electronic Gaming & Multimedia', 'Electronics & Computer Distribution', 'Engineering & Construction', 'Entertainment', 'Farm & Heavy Construction Machinery', 'Farm Products', 'Financial Conglomerates', 'Financial Data & Stock Exchanges', 'Food Distribution', 'Footwear & Accessories', 'Furnishings, Fixtures & Appliances', 'Gambling', 'Gold', 'Grocery Stores', 'Healthcare Plans', 'Health Information Services', 'Home Improvement Retail', 'Household & Personal Products', 'Industrial Distribution', 'Information Technology Services', 'Infrastructure Operations', 'Insurance Brokers', 'Insurance - Diversified', 'Insurance - Life', 'Insurance - Property & Casualty', 'Insurance - Reinsurance', 'Insurance - Specialty', 'Integrated Freight & Logistics', 'Internet Content & Information', 'Internet Retail', 'Leisure', 'Lodging', 'Lumber & Wood Production', 'Luxury Goods', 'Marine Shipping', 'Medical Care Facilities', 'Medical Devices', 'Medical Distribution', 'Medical Instruments & Supplies', 'Metal Fabrication', 'Mortgage Finance', 'Oil & Gas Drilling', 'Oil & Gas E&P', 'Oil & Gas Equipment & Services', 'Oil & Gas Integrated', 'Oil & Gas Midstream', 'Oil & Gas Refining & Marketing', 'Other Industrial Metals & Mining', 'Other Precious Metals & Mining', 'Packaged Foods', 'Packaging & Containers', 'Paper & Paper Products', 'Personal Services', 'Pharmaceutical Retailers', 'Pollution & Treatment Controls', 'Publishing', 'Railroads', 'Real Estate - Development', 'Real Estate - Diversified', 'Real Estate Services', 'Recreational Vehicles', 'REIT - Diversified', 'REIT - Healthcare Facilities', 'REIT - Hotel & Motel', 'REIT - Industrial', 'REIT - Mortgage', 'REIT - Office', 'REIT - Residential', 'REIT - Retail', 'REIT - Specialty', 'Rental & Leasing Services', 'Residential Construction', 'Resorts & Casinos', 'Restaurants', 'Scientific & Technical Instruments', 'Security & Protection Services', 'Semiconductor Equipment & Materials', 'Semiconductors', 'Shell Companies', 'Silver', 'Software - Application', 'Software - Infrastructure', 'Solar', 'Specialty Business Services', 'Specialty Chemicals', 'Specialty Industrial Machinery', 'Specialty Retail', 'Staffing & Employment Services', 'Steel', 'Telecom Services', 'Textile Manufacturing', 'Thermal Coal', 'Tobacco', 'Tools & Accessories', 'Travel Services', 'Trucking', 'Uranium', 'Utilities - Diversified', 'Utilities - Independent Power Producers', 'Utilities - Regulated Electric', 'Utilities - Regulated Gas', 'Utilities - Regulated Water', 'Utilities - Renewable', 'Waste Management'],key='Industry')
#Market_Cap = st.sidebar.selectbox('Market Cap.:',['Any', 'Mega ($200bln and more)', 'Large ($10bln to $200bln)', 'Mid ($2bln to $10bln)', 'Small ($300mln to $2bln)', 'Micro ($50mln to $300mln)', 'Nano (under $50mln)', '+Large (over $10bln)', '+Mid (over $2bln)', '+Small (over $300mln)', '+Micro (over $50mln)', '-Large (under $200bln)', '-Mid (under $10bln)', '-Small (under $2bln)', '-Micro (under $300mln)'],key='Market_Cap')
#Price = st.sidebar.selectbox('Price:',['Any', 'Under $1', 'Under $2', 'Under $3', 'Under $4', 'Under $5', 'Under $7', 'Under $10', 'Under $15', 'Under $20', 'Under $30', 'Under $40', 'Under $50', 'Over $1', 'Over $2', 'Over $3', 'Over $4', 'Over $5', 'Over $7', 'Over $10', 'Over $15', 'Over $20', 'Over $30', 'Over $40', 'Over $50', 'Over $60', 'Over $70', 'Over $80', 'Over $90', 'Over $100', '$1 to $5', '$1 to $10', '$1 to $20', '$5 to $10', '$5 to $20', '$5 to $50', '$10 to $20', '$10 to $50', '$20 to $50', '$50 to $100'],key='Price')
#Performance = st.sidebar.selectbox('Performance:',['Any', 'Today Up', 'Today Down', 'Today -15%', 'Today -10%', 'Today -5%', 'Today +5%', 'Today +10%', 'Today +15%', 'Week -30%', 'Week -20%', 'Week -10%', 'Week Down', 'Week Up', 'Week +10%', 'Week +20%', 'Week +30%', 'Month -50%', 'Month -30%', 'Month -20%', 'Month -10%', 'Month Down', 'Month Up', 'Month +10%', 'Month +20%', 'Month +30%', 'Month +50%', 'Quarter -50%', 'Quarter -30%', 'Quarter -20%', 'Quarter -10%', 'Quarter Down', 'Quarter Up', 'Quarter +10%', 'Quarter +20%', 'Quarter +30%', 'Quarter +50%', 'Half -75%', 'Half -50%', 'Half -30%', 'Half -20%', 'Half -10%', 'Half Down', 'Half Up', 'Half +10%', 'Half +20%', 'Half +30%', 'Half +50%', 'Half +100%', 'Year -75%', 'Year -50%', 'Year -30%', 'Year -20%', 'Year -10%', 'Year Down', 'Year Up', 'Year +10%', 'Year +20%', 'Year +30%', 'Year +50%', 'Year +100%', 'Year +200%', 'Year +300%', 'Year +500%', 'YTD -75%', 'YTD -50%', 'YTD -30%', 'YTD -20%', 'YTD -10%', 'YTD -5%', 'YTD Down', 'YTD Up', 'YTD +5%', 'YTD +10%', 'YTD +20%', 'YTD +30%', 'YTD +50%', 'YTD +100%'],key='Performance')
#Current_Volume = st.sidebar.selectbox('Current Volume:',['Any', 'Under 50K', 'Under 100K', 'Under 500K', 'Under 750K', 'Under 1M', 'Over 0', 'Over 50K', 'Over 100K', 'Over 200K', 'Over 300K', 'Over 400K', 'Over 500K', 'Over 750K', 'Over 1M', 'Over 2M', 'Over 5M', 'Over 10M', 'Over 20M'],key='Current_Volume')
#Average_Volume = st.sidebar.selectbox('Average Volume:',['Any', 'Under 50K', 'Under 100K', 'Under 500K', 'Under 750K', 'Under 1M', 'Over 50K', 'Over 100K', 'Over 200K', 'Over 300K', 'Over 400K', 'Over 500K', 'Over 750K', 'Over 1M', 'Over 2M', '100K to 500K', '100K to 1M', '500K to 1M', '500K to 10M'],key='Average_Volume')
#Earnings_Date = st.sidebar.selectbox('Earnings Date:',['Any', 'Today', 'Today Before Market Open', 'Today After Market Close', 'Tomorrow', 'Tomorrow Before Market Open', 'Tomorrow After Market Close', 'Yesterday', 'Yesterday Before Market Open', 'Yesterday After Market Close', 'Next 5 Days', 'Previous 5 Days', 'This Week', 'Next Week', 'Previous Week', 'This Month'],key='Earnings_Date')
#Pattern = st.sidebar.selectbox('Pattern:',['Any', 'Horizontal S/R', 'Horizontal S/R (Strong)', 'TL Resistance', 'TL Resistance (Strong)', 'TL Support', 'TL Support (Strong)', 'Wedge Up', 'Wedge Up (Strong)', 'Wedge Down', 'Wedge Down (Strong)', 'Triangle Ascending', 'Triangle Ascending (Strong)', 'Triangle Descending', 'Triangle Descending (Strong)', 'Wedge', 'Wedge (Strong)', 'Channel Up', 'Channel Up (Strong)', 'Channel Down', 'Channel Down (Strong)', 'Channel', 'Channel (Strong)', 'Double Top', 'Double Bottom', 'Multiple Top', 'Multiple Bottom', 'Head & Shoulders', 'Head & Shoulders Inverse'],key='Pattern')
#Candlestick = st.sidebar.selectbox('Candlestick:',['Any', 'Long Lower Shadow', 'Long Upper Shadow', 'Hammer', 'Inverted Hammer', 'Spinning Top White', 'Spinning Top Black', 'Doji', 'Dragonfly Doji', 'Gravestone Doji', 'Marubozu White', 'Marubozu Black'],key='Candlestick')
#RSI = st.sidebar.selectbox('RSI (14):',['Any', 'Overbought (90)', 'Overbought (80)', 'Overbought (70)', 'Overbought (60)', 'Oversold (40)', 'Oversold (30)', 'Oversold (20)', 'Oversold (10)', 'Not Overbought (<60)', 'Not Overbought (<50)', 'Not Oversold (>50)', 'Not Oversold (>40)'],key='RSI')
#ATR = st.sidebar.selectbox('Average True Range:',['Any', 'Over 0.25', 'Over 0.5', 'Over 0.75', 'Over 1', 'Over 1.5', 'Over 2', 'Over 2.5', 'Over 3', 'Over 3.5', 'Over 4', 'Over 4.5', 'Over 5', 'Under 0.25', 'Under 0.5', 'Under 0.75', 'Under 1', 'Under 1.5', 'Under 2', 'Under 2.5', 'Under 3', 'Under 3.5', 'Under 4', 'Under 4.5', 'Under 5'],key='ATR')
#SMA20 = st.sidebar.selectbox('20-Day SMA:',['Any', 'Price below SMA20', 'Price 10% below SMA20', 'Price 20% below SMA20', 'Price 30% below SMA20', 'Price 40% below SMA20', 'Price 50% below SMA20', 'Price above SMA20', 'Price 10% above SMA20', 'Price 20% above SMA20', 'Price 30% above SMA20', 'Price 40% above SMA20', 'Price 50% above SMA20', 'Price crossed SMA20', 'Price crossed SMA20 above', 'Price crossed SMA20 below', 'SMA20 crossed SMA50', 'SMA20 crossed SMA50 above', 'SMA20 crossed SMA50 below', 'SMA20 crossed SMA200', 'SMA20 crossed SMA200 above', 'SMA20 crossed SMA200 below', 'SMA20 above SMA50', 'SMA20 below SMA50', 'SMA20 above SMA200', 'SMA20 below SMA200'],key='SMA20')
#SMA50 = st.sidebar.selectbox('50-Day SMA:',['Any', 'Price below SMA50', 'Price 10% below SMA50', 'Price 20% below SMA50', 'Price 30% below SMA50', 'Price 40% below SMA50', 'Price 50% below SMA50', 'Price above SMA50', 'Price 10% above SMA50', 'Price 20% above SMA50', 'Price 30% above SMA50', 'Price 40% above SMA50', 'Price 50% above SMA50', 'Price crossed SMA50', 'Price crossed SMA50 above', 'Price crossed SMA50 below', 'SMA50 crossed SMA20', 'SMA50 crossed SMA20 above', 'SMA50 crossed SMA20 below', 'SMA50 crossed SMA200', 'SMA50 crossed SMA200 above', 'SMA50 crossed SMA200 below', 'SMA50 above SMA20', 'SMA50 below SMA20', 'SMA50 above SMA200', 'SMA50 below SMA200'],key='SMA50')
#SMA200 = st.sidebar.selectbox('200-Day SMA:',['Any', 'Price below SMA200', 'Price 10% below SMA200', 'Price 20% below SMA200', 'Price 30% below SMA200', 'Price 40% below SMA200', 'Price 50% below SMA200', 'Price 60% below SMA200', 'Price 70% below SMA200', 'Price 80% below SMA200', 'Price 90% below SMA200', 'Price above SMA200', 'Price 10% above SMA200', 'Price 20% above SMA200', 'Price 30% above SMA200', 'Price 40% above SMA200', 'Price 50% above SMA200', 'Price 60% above SMA200', 'Price 70% above SMA200', 'Price 80% above SMA200', 'Price 90% above SMA200', 'Price 100% above SMA200', 'Price crossed SMA200', 'Price crossed SMA200 above', 'Price crossed SMA200 below', 'SMA200 crossed SMA20', 'SMA200 crossed SMA20 above', 'SMA200 crossed SMA20 below', 'SMA200 crossed SMA50', 'SMA200 crossed SMA50 above', 'SMA200 crossed SMA50 below', 'SMA200 above SMA20', 'SMA200 below SMA20', 'SMA200 above SMA50', 'SMA200 below SMA50'],key='SMA200')
#Volatility = st.sidebar.selectbox('Volatility:',['Any', 'Week - Over 3%', 'Week - Over 4%', 'Week - Over 5%', 'Week - Over 6%', 'Week - Over 7%', 'Week - Over 8%', 'Week - Over 9%', 'Week - Over 10%', 'Week - Over 12%', 'Week - Over 15%', 'Month - Over 2%', 'Month - Over 3%', 'Month - Over 4%', 'Month - Over 5%', 'Month - Over 6%', 'Month - Over 7%', 'Month - Over 8%', 'Month - Over 9%', 'Month - Over 10%', 'Month - Over 12%', 'Month - Over 15%'],key='Volatility')
#Analyst = st.sidebar.selectbox('Analyst Recom.:',['Any', 'Strong Buy (1)', 'Buy or better', 'Buy', 'Hold or better', 'Hold', 'Hold or worse', 'Sell', 'Sell or worse', 'Strong Sell (5)'],key='Analyst')
#d20_HL = st.sidebar.selectbox('20-Day High/Low:',['Any', 'New High', 'New Low', '5% or more below High', '10% or more below High', '15% or more below High', '20% or more below High', '30% or more below High', '40% or more below High', '50% or more below High', '0-3% below High', '0-5% below High', '0-10% below High', '5% or more above Low', '10% or more above Low', '15% or more above Low', '20% or more above Low', '30% or more above Low', '40% or more above Low', '50% or more above Low', '0-3% above Low', '0-5% above Low', '0-10% above Low'],key='d20_HL')
#W52_HL = st.sidebar.selectbox('52-Day High/Low:',['Any', 'New High', 'New Low', '5% or more below High', '10% or more below High', '15% or more below High', '20% or more below High', '30% or more below High', '40% or more below High', '50% or more below High', '60% or more below High', '70% or more below High', '80% or more below High', '90% or more below High', '0-3% below High', '0-5% below High', '0-10% below High', '5% or more above Low', '10% or more above Low', '15% or more above Low', '20% or more above Low', '30% or more above Low', '40% or more above Low', '50% or more above Low', '60% or more above Low', '70% or more above Low', '80% or more above Low', '90% or more above Low', '100% or more above Low', '120% or more above Low', '150% or more above Low', '200% or more above Low', '300% or more above Low', '500% or more above Low', '0-3% above Low', '0-5% above Low', '0-10% above Low'],key='W52_HL')

#st.sidebar.write("### Ticker Options")

heute = dt.datetime.now()
heute_uhrzeit = heute.strftime("%d/%m/%Y, %H:%M:%S")

with st.container():
    col1, col2 =  st.columns([10,10],gap= "large")

with col1:
    st.write('')
    #st.markdown("![Alt Text](https://drive.google.com/uc?export=download&id=1QgEx2DGkzt_v-s2a_g9IEi80jRQ7oZl6)")

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

with col2:
    with st.form(key='Form1'):
        with st.sidebar:
            st.write("### Ticker Options")
            Index = st.selectbox('Index:', ['Any', 'S&P 500', 'DJIA'], key='Index')
            Sector = st.selectbox('Sector:',
                                  ['Any', 'Basic Materials', 'Communication Services', 'Consumer Cyclical',
                                   'Consumer Defensive', 'Energy', 'Financial', 'Healthcare', 'Industrials',
                                   'Real Estate', 'Technology', 'Utilities'], key='Sector')
            Industry = st.selectbox('Industry:',
                                    ['Any', 'Stocks only (ex-Funds)', 'Exchange Traded Fund',
                                     'Advertising Agencies',
                                     'Aerospace & Defense', 'Agricultural Inputs', 'Airlines',
                                     'Airports & Air Services', 'Aluminum', 'Apparel Manufacturing',
                                     'Apparel Retail',
                                     'Asset Management', 'Auto Manufacturers', 'Auto Parts',
                                     'Auto & Truck Dealerships',
                                     'Banks - Diversified', 'Banks - Regional', 'Beverages - Brewers',
                                     'Beverages - Non-Alcoholic', 'Beverages - Wineries & Distilleries',
                                     'Biotechnology', 'Broadcasting', 'Building Materials',
                                     'Building Products & Equipment', 'Business Equipment & Supplies',
                                     'Capital Markets', 'Chemicals', 'Closed-End Fund - Debt',
                                     'Closed-End Fund - Equity', 'Closed-End Fund - Foreign', 'Coking Coal',
                                     'Communication Equipment', 'Computer Hardware', 'Confectioners',
                                     'Conglomerates',
                                     'Consulting Services', 'Consumer Electronics', 'Copper', 'Credit Services',
                                     'Department Stores', 'Diagnostics & Research', 'Discount Stores',
                                     'Drug Manufacturers - General', 'Drug Manufacturers - Specialty & Generic',
                                     'Education & Training Services', 'Electrical Equipment & Parts',
                                     'Electronic Components', 'Electronic Gaming & Multimedia',
                                     'Electronics & Computer Distribution', 'Engineering & Construction',
                                     'Entertainment', 'Farm & Heavy Construction Machinery', 'Farm Products',
                                     'Financial Conglomerates', 'Financial Data & Stock Exchanges',
                                     'Food Distribution',
                                     'Footwear & Accessories', 'Furnishings, Fixtures & Appliances', 'Gambling',
                                     'Gold',
                                     'Grocery Stores', 'Healthcare Plans', 'Health Information Services',
                                     'Home Improvement Retail', 'Household & Personal Products',
                                     'Industrial Distribution', 'Information Technology Services',
                                     'Infrastructure Operations', 'Insurance Brokers', 'Insurance - Diversified',
                                     'Insurance - Life', 'Insurance - Property & Casualty',
                                     'Insurance - Reinsurance',
                                     'Insurance - Specialty', 'Integrated Freight & Logistics',
                                     'Internet Content & Information', 'Internet Retail', 'Leisure', 'Lodging',
                                     'Lumber & Wood Production', 'Luxury Goods', 'Marine Shipping',
                                     'Medical Care Facilities', 'Medical Devices', 'Medical Distribution',
                                     'Medical Instruments & Supplies', 'Metal Fabrication', 'Mortgage Finance',
                                     'Oil & Gas Drilling', 'Oil & Gas E&P', 'Oil & Gas Equipment & Services',
                                     'Oil & Gas Integrated', 'Oil & Gas Midstream',
                                     'Oil & Gas Refining & Marketing',
                                     'Other Industrial Metals & Mining', 'Other Precious Metals & Mining',
                                     'Packaged Foods', 'Packaging & Containers', 'Paper & Paper Products',
                                     'Personal Services', 'Pharmaceutical Retailers',
                                     'Pollution & Treatment Controls',
                                     'Publishing', 'Railroads', 'Real Estate - Development',
                                     'Real Estate - Diversified', 'Real Estate Services', 'Recreational Vehicles',
                                     'REIT - Diversified', 'REIT - Healthcare Facilities', 'REIT - Hotel & Motel',
                                     'REIT - Industrial', 'REIT - Mortgage', 'REIT - Office', 'REIT - Residential',
                                     'REIT - Retail', 'REIT - Specialty', 'Rental & Leasing Services',
                                     'Residential Construction', 'Resorts & Casinos', 'Restaurants',
                                     'Scientific & Technical Instruments', 'Security & Protection Services',
                                     'Semiconductor Equipment & Materials', 'Semiconductors', 'Shell Companies',
                                     'Silver', 'Software - Application', 'Software - Infrastructure', 'Solar',
                                     'Specialty Business Services', 'Specialty Chemicals',
                                     'Specialty Industrial Machinery', 'Specialty Retail',
                                     'Staffing & Employment Services', 'Steel', 'Telecom Services',
                                     'Textile Manufacturing', 'Thermal Coal', 'Tobacco', 'Tools & Accessories',
                                     'Travel Services', 'Trucking', 'Uranium', 'Utilities - Diversified',
                                     'Utilities - Independent Power Producers', 'Utilities - Regulated Electric',
                                     'Utilities - Regulated Gas', 'Utilities - Regulated Water',
                                     'Utilities - Renewable', 'Waste Management'], key='Industry')
            Market_Cap = st.selectbox('Market Cap.:',
                                      ['Any', 'Mega ($200bln and more)', 'Large ($10bln to $200bln)',
                                       'Mid ($2bln to $10bln)', 'Small ($300mln to $2bln)',
                                       'Micro ($50mln to $300mln)', 'Nano (under $50mln)',
                                       '+Large (over $10bln)', '+Mid (over $2bln)',
                                       '+Small (over $300mln)', '+Micro (over $50mln)',
                                       '-Large (under $200bln)', '-Mid (under $10bln)',
                                       '-Small (under $2bln)', '-Micro (under $300mln)'],
                                      key='Market_Cap')
            Price = st.selectbox('Price:',
                                 ['Any', 'Under $1', 'Under $2', 'Under $3', 'Under $4', 'Under $5', 'Under $7',
                                  'Under $10', 'Under $15', 'Under $20', 'Under $30', 'Under $40', 'Under $50',
                                  'Over $1', 'Over $2', 'Over $3', 'Over $4', 'Over $5', 'Over $7', 'Over $10',
                                  'Over $15', 'Over $20', 'Over $30', 'Over $40', 'Over $50', 'Over $60',
                                  'Over $70',
                                  'Over $80', 'Over $90', 'Over $100', '$1 to $5', '$1 to $10', '$1 to $20',
                                  '$5 to $10', '$5 to $20', '$5 to $50', '$10 to $20', '$10 to $50', '$20 to $50',
                                  '$50 to $100'], key='Price')
            Performance = st.selectbox('Performance:',
                                       ['Any', 'Today Up', 'Today Down', 'Today -15%', 'Today -10%', 'Today -5%',
                                        'Today +5%', 'Today +10%', 'Today +15%', 'Week -30%', 'Week -20%',
                                        'Week -10%',
                                        'Week Down', 'Week Up', 'Week +10%', 'Week +20%', 'Week +30%', 'Month -50%',
                                        'Month -30%', 'Month -20%', 'Month -10%', 'Month Down', 'Month Up',
                                        'Month +10%', 'Month +20%', 'Month +30%', 'Month +50%', 'Quarter -50%',
                                        'Quarter -30%', 'Quarter -20%', 'Quarter -10%', 'Quarter Down',
                                        'Quarter Up',
                                        'Quarter +10%', 'Quarter +20%', 'Quarter +30%', 'Quarter +50%', 'Half -75%',
                                        'Half -50%', 'Half -30%', 'Half -20%', 'Half -10%', 'Half Down', 'Half Up',
                                        'Half +10%', 'Half +20%', 'Half +30%', 'Half +50%', 'Half +100%',
                                        'Year -75%',
                                        'Year -50%', 'Year -30%', 'Year -20%', 'Year -10%', 'Year Down', 'Year Up',
                                        'Year +10%', 'Year +20%', 'Year +30%', 'Year +50%', 'Year +100%',
                                        'Year +200%',
                                        'Year +300%', 'Year +500%', 'YTD -75%', 'YTD -50%', 'YTD -30%', 'YTD -20%',
                                        'YTD -10%', 'YTD -5%', 'YTD Down', 'YTD Up', 'YTD +5%', 'YTD +10%',
                                        'YTD +20%',
                                        'YTD +30%', 'YTD +50%', 'YTD +100%'], key='Performance')
            Current_Volume = st.selectbox('Current Volume:',
                                          ['Any', 'Under 50K', 'Under 100K', 'Under 500K', 'Under 750K', 'Under 1M',
                                           'Over 0', 'Over 50K', 'Over 100K', 'Over 200K', 'Over 300K', 'Over 400K',
                                           'Over 500K', 'Over 750K', 'Over 1M', 'Over 2M', 'Over 5M', 'Over 10M',
                                           'Over 20M'], key='Current_Volume')
            Average_Volume = st.selectbox('Average Volume:',
                                          ['Any', 'Under 50K', 'Under 100K', 'Under 500K', 'Under 750K', 'Under 1M',
                                           'Over 50K', 'Over 100K', 'Over 200K', 'Over 300K', 'Over 400K',
                                           'Over 500K',
                                           'Over 750K', 'Over 1M', 'Over 2M', '100K to 500K', '100K to 1M',
                                           '500K to 1M', '500K to 10M'], key='Average_Volume')
            Earnings_Date = st.selectbox('Earnings Date:',
                                         ['Any', 'Today', 'Today Before Market Open', 'Today After Market Close',
                                          'Tomorrow', 'Tomorrow Before Market Open', 'Tomorrow After Market Close',
                                          'Yesterday', 'Yesterday Before Market Open',
                                          'Yesterday After Market Close',
                                          'Next 5 Days', 'Previous 5 Days', 'This Week', 'Next Week',
                                          'Previous Week',
                                          'This Month'], key='Earnings_Date')
            Pattern = st.selectbox('Pattern:', ['Any', 'Horizontal S/R', 'Horizontal S/R (Strong)', 'TL Resistance',
                                                'TL Resistance (Strong)', 'TL Support', 'TL Support (Strong)',
                                                'Wedge Up', 'Wedge Up (Strong)', 'Wedge Down',
                                                'Wedge Down (Strong)',
                                                'Triangle Ascending', 'Triangle Ascending (Strong)',
                                                'Triangle Descending', 'Triangle Descending (Strong)', 'Wedge',
                                                'Wedge (Strong)', 'Channel Up', 'Channel Up (Strong)',
                                                'Channel Down',
                                                'Channel Down (Strong)', 'Channel', 'Channel (Strong)',
                                                'Double Top',
                                                'Double Bottom', 'Multiple Top', 'Multiple Bottom',
                                                'Head & Shoulders',
                                                'Head & Shoulders Inverse'], key='Pattern')
            Candlestick = st.selectbox('Candlestick:',
                                       ['Any', 'Long Lower Shadow', 'Long Upper Shadow', 'Hammer',
                                        'Inverted Hammer',
                                        'Spinning Top White', 'Spinning Top Black', 'Doji', 'Dragonfly Doji',
                                        'Gravestone Doji', 'Marubozu White', 'Marubozu Black'], key='Candlestick')
            RSI = st.selectbox('RSI (14):',
                               ['Any', 'Overbought (90)', 'Overbought (80)', 'Overbought (70)', 'Overbought (60)',
                                'Oversold (40)', 'Oversold (30)', 'Oversold (20)', 'Oversold (10)',
                                'Not Overbought (<60)', 'Not Overbought (<50)', 'Not Oversold (>50)',
                                'Not Oversold (>40)'], key='RSI')
            ATR = st.selectbox('Average True Range:',
                               ['Any', 'Over 0.25', 'Over 0.5', 'Over 0.75', 'Over 1', 'Over 1.5', 'Over 2',
                                'Over 2.5',
                                'Over 3', 'Over 3.5', 'Over 4', 'Over 4.5', 'Over 5', 'Under 0.25', 'Under 0.5',
                                'Under 0.75', 'Under 1', 'Under 1.5', 'Under 2', 'Under 2.5', 'Under 3',
                                'Under 3.5',
                                'Under 4', 'Under 4.5', 'Under 5'], key='ATR')
            SMA20 = st.selectbox('20-Day SMA:',
                                 ['Any', 'Price below SMA20', 'Price 10% below SMA20', 'Price 20% below SMA20',
                                  'Price 30% below SMA20', 'Price 40% below SMA20', 'Price 50% below SMA20',
                                  'Price above SMA20', 'Price 10% above SMA20', 'Price 20% above SMA20',
                                  'Price 30% above SMA20', 'Price 40% above SMA20', 'Price 50% above SMA20',
                                  'Price crossed SMA20', 'Price crossed SMA20 above', 'Price crossed SMA20 below',
                                  'SMA20 crossed SMA50', 'SMA20 crossed SMA50 above', 'SMA20 crossed SMA50 below',
                                  'SMA20 crossed SMA200', 'SMA20 crossed SMA200 above',
                                  'SMA20 crossed SMA200 below',
                                  'SMA20 above SMA50', 'SMA20 below SMA50', 'SMA20 above SMA200',
                                  'SMA20 below SMA200'],
                                 key='SMA20')
            SMA50 = st.selectbox('50-Day SMA:',
                                 ['Any', 'Price below SMA50', 'Price 10% below SMA50', 'Price 20% below SMA50',
                                  'Price 30% below SMA50', 'Price 40% below SMA50', 'Price 50% below SMA50',
                                  'Price above SMA50', 'Price 10% above SMA50', 'Price 20% above SMA50',
                                  'Price 30% above SMA50', 'Price 40% above SMA50', 'Price 50% above SMA50',
                                  'Price crossed SMA50', 'Price crossed SMA50 above', 'Price crossed SMA50 below',
                                  'SMA50 crossed SMA20', 'SMA50 crossed SMA20 above', 'SMA50 crossed SMA20 below',
                                  'SMA50 crossed SMA200', 'SMA50 crossed SMA200 above',
                                  'SMA50 crossed SMA200 below',
                                  'SMA50 above SMA20', 'SMA50 below SMA20', 'SMA50 above SMA200',
                                  'SMA50 below SMA200'],
                                 key='SMA50')
            SMA200 = st.selectbox('200-Day SMA:',
                                  ['Any', 'Price below SMA200', 'Price 10% below SMA200', 'Price 20% below SMA200',
                                   'Price 30% below SMA200', 'Price 40% below SMA200', 'Price 50% below SMA200',
                                   'Price 60% below SMA200', 'Price 70% below SMA200', 'Price 80% below SMA200',
                                   'Price 90% below SMA200', 'Price above SMA200', 'Price 10% above SMA200',
                                   'Price 20% above SMA200', 'Price 30% above SMA200', 'Price 40% above SMA200',
                                   'Price 50% above SMA200', 'Price 60% above SMA200', 'Price 70% above SMA200',
                                   'Price 80% above SMA200', 'Price 90% above SMA200', 'Price 100% above SMA200',
                                   'Price crossed SMA200', 'Price crossed SMA200 above',
                                   'Price crossed SMA200 below',
                                   'SMA200 crossed SMA20', 'SMA200 crossed SMA20 above',
                                   'SMA200 crossed SMA20 below',
                                   'SMA200 crossed SMA50', 'SMA200 crossed SMA50 above',
                                   'SMA200 crossed SMA50 below',
                                   'SMA200 above SMA20', 'SMA200 below SMA20', 'SMA200 above SMA50',
                                   'SMA200 below SMA50'], key='SMA200')
            Volatility = st.selectbox('Volatility:',
                                      ['Any', 'Week - Over 3%', 'Week - Over 4%', 'Week - Over 5%',
                                       'Week - Over 6%',
                                       'Week - Over 7%', 'Week - Over 8%', 'Week - Over 9%', 'Week - Over 10%',
                                       'Week - Over 12%', 'Week - Over 15%', 'Month - Over 2%', 'Month - Over 3%',
                                       'Month - Over 4%', 'Month - Over 5%', 'Month - Over 6%', 'Month - Over 7%',
                                       'Month - Over 8%', 'Month - Over 9%', 'Month - Over 10%', 'Month - Over 12%',
                                       'Month - Over 15%'], key='Volatility')
            Analyst = st.selectbox('Analyst Recom.:',
                                   ['Any', 'Strong Buy (1)', 'Buy or better', 'Buy', 'Hold or better', 'Hold',
                                    'Hold or worse', 'Sell', 'Sell or worse', 'Strong Sell (5)'], key='Analyst')
            d20_HL = st.selectbox('20-Day High/Low:',
                                  ['Any', 'New High', 'New Low', '5% or more below High', '10% or more below High',
                                   '15% or more below High', '20% or more below High', '30% or more below High',
                                   '40% or more below High', '50% or more below High', '0-3% below High',
                                   '0-5% below High', '0-10% below High', '5% or more above Low',
                                   '10% or more above Low', '15% or more above Low', '20% or more above Low',
                                   '30% or more above Low', '40% or more above Low', '50% or more above Low',
                                   '0-3% above Low', '0-5% above Low', '0-10% above Low'], key='d20_HL')
            W52_HL = st.selectbox('52-Day High/Low:',
                                  ['Any', 'New High', 'New Low', '5% or more below High', '10% or more below High',
                                   '15% or more below High', '20% or more below High', '30% or more below High',
                                   '40% or more below High', '50% or more below High', '60% or more below High',
                                   '70% or more below High', '80% or more below High', '90% or more below High',
                                   '0-3% below High', '0-5% below High', '0-10% below High', '5% or more above Low',
                                   '10% or more above Low', '15% or more above Low', '20% or more above Low',
                                   '30% or more above Low', '40% or more above Low', '50% or more above Low',
                                   '60% or more above Low', '70% or more above Low', '80% or more above Low',
                                   '90% or more above Low', '100% or more above Low', '120% or more above Low',
                                   '150% or more above Low', '200% or more above Low', '300% or more above Low',
                                   '500% or more above Low', '0-3% above Low', '0-5% above Low', '0-10% above Low'],
                                  key='W52_HL')
            submitted = st.form_submit_button(label='Search 🔎')
            if submitted:
                subm = True


            def reset():
                st.session_state.Index = 'Any'
                st.session_state.Sector = 'Any'
                st.session_state.Industry = 'Any'
                st.session_state.Market_Cap = 'Any'
                st.session_state.Price = 'Any'
                st.session_state.Current_Volume = 'Any'
                st.session_state.Average_Volume = 'Any'
                st.session_state.Earnings_Date = 'Any'
                st.session_state.Pattern = 'Any'
                st.session_state.Candlestick = 'Any'
                st.session_state.RSI = 'Any'
                st.session_state.ATR = 'Any'
                st.session_state.Volatility = 'Any'
                st.session_state.Analyst = 'Any'
                st.session_state.Performance = 'Any'
                st.session_state.d20_HL = 'Any'
                st.session_state.W52_HL = 'Any'
                st.session_state.SMA20 = 'Any'
                st.session_state.SMA50 = 'Any'
                st.session_state.SMA200 = 'Any'


            st.sidebar.button('Reset Filters', on_click=reset)
            st.sidebar.write(' ____________________________________')


with st.container():
    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1],gap= "small")
with col1:
    st.write("### Option Screener")
if st.button("Refresh/ Reload Data"):
            streamlit_js_eval(js_expressions="parent.window.location.reload()")
st.text('Last Updated:' + " " + str(heute_uhrzeit))
            
            
    #if st.button("Refresh/ Reload Data"):
        #pyautogui.hotkey("ctrl", "F5")
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

    #st.table(data_sp500.style.applymap(color_negative_red, subset=['Chg', '%Chg']))
    st.metric(label="S&P 500", value=data_sp500['Price'].iloc[0], delta=str(data_sp500['%Chg'].iloc[0])+ '%')

with col3:
    #st.table(data_nq.style.applymap(color_negative_red, subset=['Chg', '%Chg']))
    st.metric(label="Nasdaq", value=data_nq['Price'].iloc[0], delta=str(data_nq['%Chg'].iloc[0])+ '%')
with col4:
    #st.table(data_iwm.style.applymap(color_negative_red, subset=['Chg', '%Chg']))
    st.metric(label="Russell 2000", value=data_iwm['Price'].iloc[0], delta=str(data_iwm['%Chg'].iloc[0])+ '%')
with col5:
    #st.table(data_vix.style.applymap(color_negative_red, subset=['Chg', '%Chg']))
    st.metric(label="VIX", value=data_vix['Price'].iloc[0], delta=str(data_vix['%Chg'].iloc[0])+ '%')

with st.container():
    col1, col2 = st.columns([10,2])

with col1:
    st.write("### News")
    fnews = News()
    all_news = fnews.get_news()
    st.dataframe(all_news['news'].head(10).set_index('Date'),use_container_width=True,height =200)

with st.container():
    col1, col2, col3, col4,col5 = st.columns([5,5,5,5,5],gap= "small")

with col1:
    DTE = st.number_input('DTE (less than)',value=60)
    type = st.radio(
        "Option Type",
        ('puts', 'calls'))
with col2:
    OTM = st.number_input('%OTM (min)', value=5)
    #st.write("Ticker Presets:")

    #agree = st.checkbox('Stock List (S&P 500 CV >2M Price >$1)',help ='Settings: Index: S&P500, Current Volume: >2M, Price: >$1')
    #agree2 = st.checkbox('Stock List (S&P 500 CV >5M Price <$50)', help='Settings: Index: S&P500, Current Volume: >5M, Price: <$50')
    #agree3 = st.checkbox('Stock List (Any CV >10M Price <$50)', help='Settings: Index: Any, Current Volume: >10M, Price: <$50, Ex Funds')

with col3:
    ROC = st.number_input('ROC (min)',0,100, value=2)
with col4:
    IV = st.number_input('IV (min)', 0, 1000, value=10)
    list =['VTWO', 'SPHD', 'QQQJ', 'SPLG', 'TUR', 'EWJ', 'EWZ', 'FXI', 'URA', 'EWG', 'EWU', 'FEZ', 'SPTI', 'SIL',
             'SPLB', 'EEM', 'CIBR', 'DBA',
             'KBE', 'USO', 'KRE', 'UGA', 'URNM', 'WCLD', 'UNG', 'DBC', 'XLRE', 'KWEB', 'X', 'COPX', 'SLV', 'XLF',
             'XME', 'GDX', 'JETS', 'KIE', 'IGF',
             'FCX', 'NEM']

    foverview = Overview()

    filters_dict = {'Index': Index, 'Option/Short': 'Optionable', 'Sector': Sector, 'Industry': Industry,
                    'Market Cap.': Market_Cap, 'Price': Price, 'Performance': Performance,
                    'Current Volume': Current_Volume, 'Average Volume': Average_Volume,
                    'Earnings Date': Earnings_Date, 'Pattern': Pattern, 'Candlestick': Candlestick, 'RSI (14)': RSI,
                    'Average True Range': ATR, '20-Day Simple Moving Average': SMA20,
                    '50-Day Simple Moving Average': SMA50, '200-Day Simple Moving Average': SMA200,
                    'Volatility': Volatility, 'Analyst Recom.': Analyst, '20-Day High/Low': d20_HL,
                    '52-Week High/Low': W52_HL}


    @st.cache_data(show_spinner=False)
    def filter_data():
        df = foverview.screener_view(sleep_sec=0)[['Ticker\n\n']]
        return df


    #if Index or Sector or Industry or Market_Cap or Price or Performance or Current_Volume or Average_Volume or Earnings_Date or Pattern or Candlestick or RSI or ATR or SMA20 or SMA50 or SMA200 or Volatility or Analyst or d20_HL or W52_HL:
    if subm:
        foverview.set_filter(filters_dict=filters_dict)
        #df = foverview.screener_view(sleep_sec=0)[['Ticker\n\n']]
        df = filter_data()
        #df = foverview.screener_view()
        #list = df['Ticker\n\n'].values.tolist()
        symbols = st.sidebar.multiselect('Selected Tickers',df['Ticker\n\n'].values.tolist() ,df['Ticker\n\n'].values.tolist())

    else:
        symbols = st.sidebar.multiselect(
            'Selected Tickers', list,
            ['VTWO', 'SPHD', 'QQQJ', 'SPLG', 'TUR', 'EWJ', 'EWZ', 'FXI', 'URA', 'EWG', 'EWU', 'FEZ', 'SPTI', 'SIL',
             'SPLB', 'EEM', 'CIBR', 'DBA',
             'KBE', 'USO', 'KRE', 'UGA', 'URNM', 'WCLD', 'UNG', 'DBC', 'XLRE', 'KWEB', 'X', 'COPX', 'SLV', 'XLF',
             'XME', 'GDX', 'JETS', 'KIE', 'IGF',
             'FCX', 'NEM'])

with st.container():
    cpad1, col, pad2 = st.columns((1, 60, 10))

with col:
    tickers = Ticker(symbols)
    #@st.cache_data(show_spinner=False)  # 👈 Add the caching decorator
    #def load_tickers():
        #tickers = Ticker(symbols)
        #return tickers

    @st.cache_data(show_spinner=True)
    def cached_optData():
        df = tickers.option_chain
        return df

    #if Index or Sector or Industry or Market_Cap or Price or Performance or Current_Volume or Average_Volume or Earnings_Date or Pattern or Candlestick or RSI or ATR or SMA20 or SMA50 or SMA200 or Volatility or Analyst or d20_HL or W52_HL:
    if subm:
        st.cache_data.clear()


    #df = tickers.option_chain
    df = cached_optData()

    df = df.xs(type, level=2).reset_index()

    close = tickers.history(period='2d', interval='1m')

    columnsTitles = ['symbol', 'expiration', 'strike', 'lastPrice', 'percentChange', 'impliedVolatility',
                     'lastTradeDate']
    df = df.reindex(columns=columnsTitles)
    df['ROC'] = round((df['lastPrice'] / df['strike'] * 100),2)
    df['expiration'] = pd.to_datetime(df.expiration)
    df['lastTradeDate'] = pd.to_datetime(df.lastTradeDate)


    # df = df[df['lastTradeDate'] >= datetime.today().strftime("%Y-%m-%d")]

    def calculate_days(expiration):
        today = pd.Timestamp('today')
        return (today - expiration).days * -1


    df['DTE'] = df['expiration'].apply(lambda x: calculate_days(x))

    df.style.set_properties(**{'background-color': 'black',
                               'color': 'green'})


    def percentage_change(col1, col2):
        return ((col2 - col1) / col1) * 100


    df = df.set_index('symbol')

    df2 = close['close']
    l = df2.reset_index()
    l['Last Price'] = l.groupby('symbol')['close'].transform('last')
    l['Yesterday'] = l.groupby('symbol')['close'].transform('first')
    l['Change'] = round(percentage_change(l['Yesterday'], l['Last Price']))
    l = l.set_index('symbol')
    l_ = l.drop_duplicates(subset=['Last Price'])
    s = l_.reset_index().drop(['date', 'close', 'Yesterday'], axis=1)
    s = s.set_index('symbol')
    x = df.join(s)

    if type == 'puts':
        x['% OTM'] = round(percentage_change(x['strike'], x['Last Price']))
    if type == 'calls':
        x['% OTM'] = round((x['strike']*100/x['Last Price']))-100

    x['impliedVolatility'] = round(x['impliedVolatility']*100,2)




    x['Annual Yield'] = round((x['lastPrice'] / x['strike']) * (365 / x['DTE']) * 100,2)

    x = x.rename(columns={'lastPrice': 'Mark', 'Change': '%Change', 'impliedVolatility': 'IV',
                          'lastTradeDate': 'Last Trade Date'})
    columnsTitles = ['strike', 'expiration', 'Mark', 'Last Price', '%Change', 'ROC', 'Annual Yield', 'IV', 'DTE',
                     '% OTM', 'Last Trade Date']
    x = x.reindex(columns=columnsTitles)

    #x['Last Trade Date'] = pd.to_datetime(x['Last Trade Date'], format="%Y-%m-%d")


    today_str = date.today().strftime("%Y-%m-%d")
    start_date = date.today() - timedelta(days=3)
    end_date = date.today() + timedelta(days=5)
    nyse = mcal.get_calendar('NYSE')
    nyse_schedule = nyse.schedule(start_date=start_date, end_date=end_date)
    #display(nyse_schedule)
    if today_str in nyse_schedule.index:
        x = x.loc[(x['Last Trade Date'] == pd.Timestamp(date.today()))]
    else:
        x = x.loc[(x['Last Trade Date'] >= pd.Timestamp(date.today() - timedelta(days=3)))]
        #x = x[x['Last Trade Date']] >= pd.to_datetime(today_str) - timedelta(days=3)

    #x = x[x['Last Trade Date'] >= datetime.today().strftime("%Y-%m-%d")]
    x = x[x['DTE'] <= DTE]
    x = x.loc[x['% OTM'].between(OTM, 100)]
    x = x.loc[x['ROC'].between(ROC, 100)]
    x = x.loc[x['IV'].between(IV,1000)]
    x= x.sort_values('ROC', ascending=False)

    x['expiration']= pd.to_datetime(x['expiration']).dt.strftime('%Y-%m-%d')

    #def color_negative_red(val):
        #color = 'green' if val > 0 else 'red'
        #return f'background-color: {color}'

    def color_negative_red(value):
        if isinstance(value,str):
            color ='black'
            return 'color: %s' % color
        if isinstance(value,float):
            if value > 0:
                color = "green"
                return 'color: %s' % color
            if value < 0:
                color = "red"
                return 'color: %s' % color

    x = x.reset_index()
    d = dict.fromkeys(x.select_dtypes('float').columns, "{:.2f}")
    st.dataframe(x.style.applymap(color_negative_red, subset=['%Change']).format(d),height=1000, use_container_width=True)



    @st.cache_data
    def convert_df(x):
        return x.to_csv(index=False).encode('utf-8')


    csv = convert_df(x)

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





