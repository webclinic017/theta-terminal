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
with st.expander("Top 10 recent financial news", expanded=True):
    st.dataframe(all_news['news'].head(10).set_index('Date'), use_container_width=True, height=200)  # .to_markdown())

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

    select_text = "Nothing Selected"
    multi_css = f'''
    <style>
    .stMultiSelect div div div div div:nth-of-type(2) {{visibility: hidden;}}
    .stMultiSelect div div div div div:nth-of-type(2)::before {{visibility: visible; content:"{select_text}"}}
    </style>
    '''
    st.markdown(multi_css, unsafe_allow_html=True)

with col3:
    ROC = st.number_input('ROC (min)', 0, 100, value=2)
with col4:
    IV = st.number_input('IV (min)', 0, 1000, value=10)

with st.container():
    cpad1, col, pad2 = st.columns((1, 60, 10))

with col:
    path = os.path.dirname(__file__)

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
df = raw.reset_index(drop=True).set_index(['symbol', 'expiration', 'optionType'])
df = df.xs(type, level=2).reset_index()

symbols = ['A', 'AA', 'AAL', 'AAP', 'AAPL', 'ABBV', 'ABNB', 'ABR', 'ABT', 'ADBE', 'ADI', 'ADM', 'AEHR', 'AEM', 'AFRM',
           'AG', 'AGNC', 'AI', 'AIG', 'ALB', 'ALGM', 'AMAT', 'AMC', 'AMD', 'AMT', 'AMZN', 'APA', 'APLD', 'APLS', 'APO',
           'APP', 'APPS', 'AR', 'ARKK', 'ARRY', 'ASAN', 'ASO', 'ATVI', 'AU', 'AUPH', 'AVGO', 'AVTR', 'AXP', 'AYX',
           'AZN',
           'AZUL', 'BA', 'BABA', 'BAC', 'BAX', 'BBIO', 'BBWI', 'BBY', 'BE', 'BEKE', 'BIDU', 'BILI', 'BILL', 'BJ',
           'BLDR',
           'BLNK', 'BLUE', 'BMBL', 'BMEA', 'BMY', 'BN', 'BOH', 'BP', 'BTU', 'BUD', 'BURL', 'BWA', 'BX', 'BXMT', 'BXP',
           'BYND',
           'C', 'CAKE', 'CAT', 'CC', 'CCI', 'CCJ', 'CCL', 'CDAY', 'CELH', 'CF', 'CFG', 'CFLT', 'CHGG', 'CHPT', 'CHWY',
           'CLF',
           'CM', 'CMA', 'CMCSA', 'COF', 'COHR', 'COIN', 'COP', 'CPE', 'CPNG', 'CPRI', 'CPRX', 'CRM', 'CROX', 'CRSP',
           'CRWD',
           'CSIQ', 'CTLT', 'CVNA', 'CVS', 'CVX', 'CZR', 'DAL', 'DASH', 'DBX', 'DD', 'DDD', 'DDOG', 'DFS', 'DHI', 'DIS',
           'DISH',
           'DKNG', 'DLO', 'DLR', 'DLTR', 'DNA', 'DOCN', 'DOCS', 'DOCU', 'DOW', 'DQ', 'DT', 'DV', 'DVN', 'DXCM', 'EDR',
           'EGO',
           'ELAN', 'ELF', 'ENPH', 'ENVX', 'EOG', 'EQT', 'ETSY', 'EW', 'EWBC', 'EXAS', 'EXPE', 'EXPI', 'F', 'FANG',
           'FCEL',
           'FCX', 'FDX', 'FGEN', 'FHN', 'FIS', 'FITB', 'FL', 'FSLR', 'FSLY', 'FSR', 'FTCH', 'FTI', 'FTNT', 'FUBO',
           'FUTU',
           'FYBR', 'GDRX', 'GE', 'GFS', 'GILD', 'GLD', 'GLW', 'GM', 'GME', 'GNRC', 'GOLD', 'GOOG', 'GOOGL', 'GOOS',
           'GOTU',
           'GPN', 'GPS', 'GS', 'GSK', 'GT', 'GTLB', 'HAL', 'HAS', 'HCA', 'HES', 'HOG', 'HOOD', 'HPQ', 'HUT', 'IBM',
           'IEP',
           'IFF', 'IGT', 'IMGN', 'INDI', 'INMD', 'INTC', 'IOT', 'IRM', 'IWM', 'JBL', 'JD', 'JMIA', 'JOBY', 'JPM', 'KBH',
           'KD',
           'KEY', 'KMI', 'KMX', 'KNX', 'KR', 'KSS', 'LAC', 'LAZR', 'LCID', 'LEN', 'LI', 'LLY', 'LNC', 'LULU', 'LUMN',
           'LUV',
           'LVS', 'LYB', 'LYFT', 'LYV', 'M', 'MANU', 'MARA', 'MBLY', 'MDB', 'MET', 'META', 'MKC', 'MLCO', 'MMM', 'MODG',
           'MOS',
           'MP', 'MPC', 'MPW', 'MQ', 'MRNA', 'MRO', 'MRVL', 'MS', 'MSFT', 'MTCH', 'MU', 'MVIS', 'NCLH', 'NEM', 'NEP',
           'NET',
           'NFE', 'NFLX', 'NIO', 'NKE', 'NKLA', 'NLY', 'NNOX', 'NOVA', 'NRG', 'NTLA', 'NU', 'NUE', 'NVAX', 'NVDA',
           'NVO', 'NWL',
           'NXT', 'OKTA', 'OMC', 'ON', 'ONON', 'OPCH', 'OPEN', 'ORCL', 'OVV', 'OXY', 'OZK', 'PACW', 'PAGS', 'PANW',
           'PARA',
           'PATH', 'PAYO', 'PBR', 'PCG', 'PD', 'PDD', 'PENN', 'PFG', 'PGY', 'PINS', 'PLAY', 'PLD', 'PLNT', 'PLTK',
           'PLTR',
           'PLUG', 'PM', 'PNC', 'PRU', 'PSTG', 'PSX', 'PTON', 'PXD', 'PYPL', 'QCOM', 'QQQ', 'QRVO', 'QS', 'RBLX', 'RC',
           'RCL',
           'RDFN', 'RF', 'RIG', 'RIOT', 'RIVN', 'RKLB', 'RKT', 'RMBS', 'RNG', 'ROKU', 'ROST', 'RPD', 'RRC', 'RUN',
           'RVLV', 'S',
           'SABR', 'SBLK', 'SCHW', 'SDGR', 'SE', 'SFIX', 'SG', 'SGEN', 'SHEL', 'SHLS', 'SHOP', 'SLB', 'SLG', 'SLV',
           'SMAR',
           'SMCI', 'SNAP', 'SNDL', 'SNOW', 'SOFI', 'SOUN', 'SOXL', 'SPCE', 'SPLK', 'SPOT', 'SPR', 'SPWR', 'SPY', 'SQ',
           'SQM',
           'SRPT', 'STLD', 'STNG', 'STWD', 'STX', 'STZ', 'SU', 'SWKS', 'SWN', 'T', 'TAL', 'TDOC', 'TEAM', 'TECK', 'TFC',
           'TGT',
           'TGTX', 'TMC', 'TME', 'TMO', 'TMUS', 'TPR', 'TPX', 'TQQQ', 'TRGP', 'TRIP', 'TRUP', 'TSLA', 'TSM', 'TTD',
           'TTWO',
           'TWLO', 'U', 'UAL', 'UBER', 'UEC', 'UNIT', 'UNP', 'UPS', 'UPST', 'USB', 'V', 'VALE', 'VFC', 'VIPS', 'VLO',
           'VLY',
           'VNO', 'VTNR', 'VZ', 'W', 'WAL', 'WBA', 'WBD', 'WDC', 'WFC', 'WOLF', 'WPM', 'WW', 'WYNN', 'X', 'XLE', 'XOM',
           'XPEV',
           'YEXT', 'Z', 'ZI', 'ZION', 'ZM', 'ZS', 'ZTO', 'ACWI', 'ACWX', 'AGG', 'AMLP', 'ANGL', 'ARKG', 'ARKK', 'ASHR',
           'BIL',
           'BOIL', 'BOTZ', 'BSV', 'COWZ', 'CWB', 'DBC', 'DFAC', 'DGRO', 'DIA', 'DPST', 'DRIP', 'DUST', 'EEM', 'EFA',
           'EFV',
           'EMB', 'EMLC', 'EWA', 'EWC', 'EWG', 'EWH', 'EWJ', 'EWT', 'EWU', 'EWW', 'EWY', 'EWZ', 'EZU', 'FAS', 'FAZ',
           'FDL',
           'FEZ', 'FLOT', 'FLRN', 'FNDF', 'FPE', 'FTSM', 'FVD', 'FXI', 'FXN', 'GDX', 'GDXJ', 'GLD', 'GOVT', 'HIBS',
           'HYG',
           'HYLB', 'IAU', 'IBB', 'ICLN', 'ICSH', 'IEF', 'IEFA', 'IEI', 'IEMG', 'IGIB', 'IGSB', 'IJH', 'IJR', 'INDA',
           'IQLT',
           'ITB', 'ITOT', 'IUSB', 'IVV', 'IVW', 'IWD', 'IWF', 'IWM', 'IWN', 'IWR', 'IXUS', 'IYR', 'JDST', 'JEPI',
           'JEPQ',
           'JETS', 'JNK', 'JNUG', 'JPST', 'KBE', 'KBWB', 'KOLD', 'KRE', 'KWEB', 'LABD', 'LABU', 'LQD', 'MBB', 'MCHI',
           'MJ',
           'MSOS', 'MUB', 'NUGT', 'NVDS', 'OUNZ', 'PDBC', 'PFF', 'PGX', 'PSQ', 'QID', 'QLD', 'QQQ', 'QQQM', 'QUAL',
           'QYLD',
           'RSP', 'RWM', 'RYLD', 'SARK', 'SCHD', 'SCHE', 'SCHF', 'SCHG', 'SCHH', 'SCHO', 'SCHP', 'SCHR', 'SCHX', 'SCO',
           'SDOW',
           'SDS', 'SGOL', 'SH', 'SHV', 'SHY', 'SHYG', 'SILJ', 'SJNK', 'SLV', 'SMH', 'SOXL', 'SOXS', 'SOXX', 'SPAB',
           'SPDN',
           'SPDW', 'SPEM', 'SPIB', 'SPLG', 'SPLV', 'SPSB', 'SPTI', 'SPTL', 'SPTS', 'SPXL', 'SPXS', 'SPXU', 'SPY',
           'SPYD',
           'SPYG', 'SPYV', 'SQQQ', 'SRLN', 'SSO', 'SVIX', 'SVXY', 'TBT', 'TECL', 'TECS', 'TFLO', 'TIP', 'TLT', 'TMF',
           'TNA',
           'TQQQ', 'TSLL', 'TSLQ', 'TWM', 'TZA', 'UCO', 'UDOW', 'UNG', 'UPRO', 'URA', 'USFR', 'USHY', 'USMV', 'USO',
           'UUP',
           'UVIX', 'UVXY', 'VCIT', 'VCLT', 'VCSH', 'VEA', 'VEU', 'VGIT', 'VGK', 'VGLT', 'VGSH', 'VIXY', 'VMBS', 'VNQ',
           'VOO',
           'VT', 'VTEB', 'VTI', 'VTIP', 'VTV', 'VTWO', 'VWO', 'VXUS', 'VXX', 'VYM', 'WEBL', 'XBI', 'XHB', 'XLB', 'XLC',
           'XLE',
           'XLF', 'XLI', 'XLK', 'XLP', 'XLRE', 'XLU', 'XLV', 'XLY', 'XME', 'XOP', 'XRT', 'YANG', 'YINN', 'BITI', 'BITO',
           'BIV',
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
request_params2 = StockLatestQuoteRequest(symbol_or_symbols=symbols)
quotes = data_client.get_stock_latest_bar(request_params2)

close = pd.DataFrame.from_dict({k: dict(v) for k, v in quotes.items()}, orient='index').reset_index(drop=True)
close = close[['symbol', 'close']]
close = close.rename(columns={'close': 'Last Price'})
close = close.set_index('symbol')
x = df.join(close)

today_start = datetime.date.today()
nyse = mcal.get_calendar('NYSE')
date = pd.to_datetime(today_start) - pd.tseries.offsets.CustomBusinessDay(1, holidays=nyse.holidays().holidays)
start_date = date.strftime('%Y-%m-%d %H:%M:%S')

today_str = date.today().strftime("%Y-%m-%d")
start_date = date.today() - timedelta(days=3)
end_date = date.today() + timedelta(days=5)
nyse_schedule = nyse.schedule(start_date=start_date, end_date=end_date)

if today_str in nyse_schedule.index:
    start_date = datetime.date.today().strftime('%Y-%m-%d %H:%M:%S')

else:
    start_date = date

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


else:
    x['% OTM'] = round((x['Last Price'] * 100 / x['strike'])) - 100
    x['BE'] = x['strike'] + x['lastPrice']



x = x.rename(columns={'lastPrice': 'Mark', 'Change': '% Day Change', 'impliedVolatility': 'IV', '% OTM': 'Moneyness',
                    'lastTradeDate': 'Last Trade Date', 'bid': 'Bid', 'ask': 'Ask', 'openInterest': 'Open Int'})
columnsTitles = ['strike', 'expiration', 'DTE', 'Last Price', '% Day Change', 'Bid', 'Ask', 'Mark', 'BE', 'ROC',
                     'Annual Yield',
                     'Open Int', 'Moneyness', 'IV', 'Sector', 'Contract Time', 'Last Trade Date']
x = x.reindex(columns=columnsTitles)

if today_str in nyse_schedule.index:
    x = x.loc[(x['Last Trade Date'] >= pd.Timestamp(today_start))]
else:
    x = x.loc[(x['Last Trade Date'] >= pd.Timestamp(date))]

x = x[x['DTE'] <= DTE]
x = x.loc[x['Moneyness'].between(-200, OTM)]
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
filtered_df.insert(12, 'Delta', [mb.BS([i,j,1,k], volatility=l).putDelta if type=='puts' else mb.BS([i,j,1,k], volatility=l).callDelta for i,j,k,l in zip(filtered_df["Last Price"], filtered_df["strike"], filtered_df["DTE"], filtered_df["IV"])])
filtered_df.insert(13, 'Theta', [mb.BS([i,j,1,k], volatility=l).putTheta if type=='puts' else mb.BS([i,j,1,k], volatility=l).callTheta for i,j,k,l in zip(filtered_df["Last Price"], filtered_df["strike"], filtered_df["DTE"], filtered_df["IV"])])
filtered_df['expiration'] = pd.to_datetime(filtered_df['expiration']).dt.strftime('%Y-%m-%d')
st.dataframe(filtered_df.style.applymap(color_negative_red, subset=['% Day Change', 'Moneyness']).format(d),
             height=1000, use_container_width=True)


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
  | BE                 | Break Even (Net Debit) as for a naked put or call. (strike price at which the position breaks even at expiry)                       |
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


st.markdown(
    "[![Foo](https://em-content.zobj.net/thumbs/120/sony/336/envelope_2709-fe0f.png)](https://twitter.com/mvnchi0)")


