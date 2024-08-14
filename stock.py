import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import ta
import yfinance as yf
from datetime import datetime, timedelta

st.title("Stock Dashboard")

def fetch_stock_data(ticker, period, interval):
    end_date = datetime.now()
    if period == '1wk':
        start_date = end_date - timedelta(days=7)
        data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    else:
        data = yf.download(ticker, period=period, interval=interval)
    return data

def process_data(data):
    if data.index.tzinfo is None:
        data.index = data.index.tz_localize('UTC')
    data.index = data.index.tz_convert('US/Eastern')
    data.reset_index(inplace=True)
    data.rename(columns={'Date':'Datetime'}, inplace=True)
    return data

def calculate_metrics(data):
    last_close = data['Close'].iloc[-1]
    prev_close = data['Close'].iloc[0]
    change = last_close - prev_close
    pct_change = (change / prev_close) * 100
    high = data['High'].max()
    low = data['Low'].min()
    volume = data['Volume'].sum()
    return last_close, prev_close, change, pct_change, high, low, volume

def add_technical_indicators(data):
    data['SMA_20'] = ta.trend.sma_indicator(data['Close'], window=20)
    data['EMA_20'] = ta.trend.ema_indicator(data['Close'], window=20)
    return data

# st.set_page_config(layout="wide")
st.sidebar.header('Chart Parameters')
ticker = st.sidebar.selectbox('Ticker', ["AAPL","MSFT","NVDA","GOOG","GOOGL","AMZN","META","AVGO","TSLA","COST","ASML","NFLX","AZN","ADBE","PEP","TMUS","AMD","LIN","PDD","QCOM","CSCO","TXN","INTU","AMGN","AMAT","ISRG","CMCSA","ARM","SNY","HON","REGN","VRTX","BKNG","MU","LRCX","PANW","KLAC","ADI","ADP","SBUX","MELI","MDLZ","GILD","INTC","SNPS","EQIX","CTAS","CDNS","CME","ABNB","PYPL","ORLY","CSX","CRWD","NXPI","MAR","CEG","WDAY","NTES","ROP","FTNT","MRVL","ADSK","DASH","AEP","CHTR","PCAR","TTD","CPRT","COIN","KDP","ROST","MNST","PAYX","MPWR","MCHP","KHC","ODFL","NDAQ","JD","IDXX","EA","DDOG","VRSK","GEHC","FAST","ACGL","TEAM","EXC","CTSH","FANG","BKR","CCEP","ALNY","SMCI","XEL","ARGX","MRNA","ON","LULU","CSGP","BIDU","BIIB","FER","FCNCA","CDW","FCNCO","APP","DXCM","TSCO","WTW","AXON","ANSS","ZS","EBAY","FITB","TCOM","ICLR","NTAP","MSTR","TTWO","VOD","TW","FSLR","GFS","ERIE","KSPI","TROW","SBAC","ERIC","CHKP","TER","PTC","STX","CINF","LI","WDC","BGNE","DLTR","BNTX","ILMN","HBAN","LINE","HOLX","RYAAY","FWONK","COO","FOXA","MDB","FWONA","STLD","PFG","ZM","SSNC","FOX","ZBRA","BMRN","NTRS","VRSN","EXPE","SWKS","WBD","GMAB","HOOD","JBHT","ALGN","ENTG","LPLA","DKNG","NWS","BSY","OKTA","ULTA","NWSA","GEN","MANH","AKAM","ENPH","NBIX","NTRA","LNT","CG","WMG","UTHR","CASY","EVRG","GLPI","NDSN","RIVN","GRAB","PODD","AZPN","LOGI","VTRS","UAL","MORN","POOL","INSM","MNDY","ARCC","TRMB","IBKR","REG","NTNX","SRPT","Z","LAMR","FLEX","TTEK","PAA","JKHY","MEDP","RPRX","ZG","CYBR","INCY","MBLY","TECH","SIRI","CHRW","HST","DOCU","FFIV","TXRH","COKE","WING","EWBC","XP","PPC","APA","LECO","FTAI","LEGN","EXAS","QRVO","MMYT","LKQ","NICE","CHDN","SAIA","SFM","DOX","CHK","CHRD","BRKR","WWD","CELH","RGEN","WBA","MKTX","LNW","LBRDA","HAS","LBRDK","MTCH","WIX","HTHT","HSIC","PCVX","RGLD","VFS","DUOL","SEIC","ROIV","FUTU","PCTY","OLED","ESLT","CART","OTEX","DSGX","AFRM","ROKU","WYNN","ENSG","SMMT","IEP","AMKR","ASND","ITCI","CROX","APPF","AGNC","MKSI","WFRD","CBSH","FSV","ALTR","EXEL","CZR","MTSI","TLN","MIDD","CRUS","DBX","PARAA","SPSC","DRS","UFPI","LCID","AAON","HALO","SOFI","LSXMB","LSXMA","LBTYK","LBTYB","LSXMK","RVMD","FYBR","BPOP","LBTYA","PARA","CFLT","IONS","CIGI","HCP","GTLB","JAZZ","PNFP","ACHC","MASI","GNTX","ZION","CGNX","NVMI","CVLT","CYTK","LNTH","LSTR","GGAL","TEM","WSC","LSCC","FRPT","MAT","AAL","WTFC","CCCS","NSIT","SAIC","VKTX","REYN","NOVT","LFUS","BOKF","VRNS","HQY","ALAB","BZ","ETSY","AUR","CWST","RCM","CHX","BPMC","PEGA","ONB","VERX","COOP","HLNE","GRFS","EXLS","NXT","BILI","TMDX","SRCL","CACC","OLLI","KRYS","LANC","BCPC","OPCH","SIGI","BECN","GLBE","MDGL","FCFS","MMSI","CRVL","FRHC","EXPO","AVAV","ALGM","ACT","NXST","XRAY","DOOO","TENB","ACIW","FFIN","COLB","TPG","AVT","CRDO","CSWI","UBSI","RMBS","RARE","COLM","ESGR","NVEI","SATS","RNA","UMBF","RDNT","OZK","DJT","QLYS","NUVL","SLM","BGC","EEFT","BBIO","QXO","MARA","FELE","APLS","VRRM","DYN","IMVT","PI","TIGO","ITRI","ALKS","TSEM","IAC","OS","VNOM","RUN","PECO","FIZZ","CAMT","CNXC","HWC","STNE","ADMA","LYFT","SHC","WAY","LOPE","BRZE","CRNX","CRSP","VLY","AXSM","RUSHA","IPAR","RUSHB","BLKB","SBRA","AEIS","NCNO","GBDC","FIVE","SGRY","SANM","ASO","URBN","OTTR","FORM","TFSL","GH","PAGP","QFIN","ICUI","ACLS","IBOC","LLYVK","CORT","FTDR","AXNX","NEOG","GLNG","TRMD","STEP","LLYVA","IDCC","WEN","PTEN","POWI","CALM","MRUS","HCM","IESC","FOLD","CCOI","WDFC","STRL","PRCT","UPST","SMPL","FRSH","ZI","JJSF","ALVO","BANF","DNLI","LOT","BL"])
time_period = st.sidebar.selectbox('Time Period', ['1d', '1wk', '1mo', '1y', 'max'])
chart_type = st.sidebar.selectbox('Chart Type', ['Candlestick', 'Line'])
indicators = st.sidebar.multiselect('Technical Indicators', ['SMA 20', 'EMA 20'])

interval_mapping = {'1d': '1m', '1wk': '30m', '1mo': '1d', '1y': '1wk', 'max': '1wk'}

if st.sidebar.button('Update'):
    data = fetch_stock_data(ticker, time_period, interval_mapping[time_period])
    data = process_data(data)
    data = add_technical_indicators(data)
    last_close, prev_close, change, pct_change, high, low, volume = calculate_metrics(data)
    st.metric(label=f"{ticker} Last Price", value=f"{last_close:.2f} USD", delta=f"{change:.2f} ({pct_change:.2f}%)")

    col1, col2, col3 = st.columns(3)
    col1.metric("High", f"{high:.2f} USD")
    col2.metric("Low", f"{low:.2f} USD")
    col3.metric("Volume", f"{volume:,}")

    fig = go.Figure()
    if chart_type == 'Candlestick':
        fig.add_trace(go.Candlestick(x=data['Datetime'], open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']))
    else:
        fig = px.line(data, x="Datetime", y='Close')

    for indicator in indicators:
        if indicator == 'SMA 20':
            fig.add_trace(go.Scatter(x=data['Datetime'], y=data['SMA_20'], name='SMA 20'))
        elif indicator == 'EMA 20':
            fig.add_trace(go.Scatter(x=data['Datetime'], y=data['EMA_20'], name='EMA 20'))

    fig.update_layout(title=f"{ticker} {time_period.upper()} Chart", xaxis_title='Time', yaxis_title='Price (USD)', height=600)
    st.plotly_chart(fig, use_container_width=True)
    st.subheader('Historical Data')
    st.dataframe(data[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']])

    st.subheader('Technical Indicators')
    st.dataframe(data[['Datetime', 'SMA_20', 'EMA_20']])

st.sidebar.header('Real-Time Stock Price')
stock_symbols = ["AAPL","MSFT","NVDA","GOOG"]#"GOOGL","AMZN","META","AVGO","TSLA","COST","ASML","NFLX","AZN","ADBE","PEP","TMUS","AMD","LIN","PDD","QCOM","CSCO","TXN","INTU","AMGN","AMAT","ISRG","CMCSA","ARM","SNY","HON","REGN","VRTX","BKNG","MU","LRCX","PANW","KLAC","ADI","ADP","SBUX","MELI","MDLZ","GILD","INTC","SNPS","EQIX","CTAS","CDNS","CME","ABNB","PYPL","ORLY","CSX","CRWD","NXPI","MAR","CEG","WDAY","NTES","ROP","FTNT","MRVL","ADSK","DASH","AEP","CHTR","PCAR","TTD","CPRT","COIN","KDP","ROST","MNST","PAYX","MPWR","MCHP","KHC","ODFL","NDAQ","JD","IDXX","EA","DDOG","VRSK","GEHC","FAST","ACGL","TEAM","EXC","CTSH","FANG","BKR","CCEP","ALNY","SMCI","XEL","ARGX","MRNA","ON","LULU","CSGP","BIDU","BIIB","FER","FCNCA","CDW","FCNCO","APP","DXCM","TSCO","WTW","AXON","ANSS","ZS","EBAY","FITB","TCOM","ICLR","NTAP","MSTR","TTWO","VOD","TW","FSLR","GFS","ERIE","KSPI","TROW","SBAC","ERIC","CHKP","TER","PTC","STX","CINF","LI","WDC","BGNE","DLTR","BNTX","ILMN","HBAN","LINE","HOLX","RYAAY","FWONK","COO","FOXA","MDB","FWONA","STLD","PFG","ZM","SSNC","FOX","ZBRA","BMRN","NTRS","VRSN","EXPE","SWKS","WBD","GMAB","HOOD","JBHT","ALGN","ENTG","LPLA","DKNG","NWS","BSY","OKTA","ULTA","NWSA","GEN","MANH","AKAM","ENPH","NBIX","NTRA","LNT","CG","WMG","UTHR","CASY","EVRG","GLPI","NDSN","RIVN","GRAB","PODD","AZPN","LOGI","VTRS","UAL","MORN","POOL","INSM","MNDY","ARCC","TRMB","IBKR","REG","NTNX","SRPT","Z","LAMR","FLEX","TTEK","PAA","JKHY","MEDP","RPRX","ZG","CYBR","INCY","MBLY","TECH","SIRI","CHRW","HST","DOCU","FFIV","TXRH","COKE","WING","EWBC","XP","PPC","APA","LECO","FTAI","LEGN","EXAS","QRVO","MMYT","LKQ","NICE","CHDN","SAIA","SFM","DOX","CHK","CHRD","BRKR","WWD","CELH","RGEN","WBA","MKTX","LNW","LBRDA","HAS","LBRDK","MTCH","WIX","HTHT","HSIC","PCVX","RGLD","VFS","DUOL","SEIC","ROIV","FUTU","PCTY","OLED","ESLT","CART","OTEX","DSGX","AFRM","ROKU","WYNN","ENSG","SMMT","IEP","AMKR","ASND","ITCI","CROX","APPF","AGNC","MKSI","WFRD","CBSH","FSV","ALTR","EXEL","CZR","MTSI","TLN","MIDD","CRUS","DBX","PARAA","SPSC","DRS","UFPI","LCID","AAON","HALO","SOFI","LSXMB","LSXMA","LBTYK","LBTYB","LSXMK","RVMD","FYBR","BPOP","LBTYA","PARA","CFLT","IONS","CIGI","HCP","GTLB","JAZZ","PNFP","ACHC","MASI","GNTX","ZION","CGNX","NVMI","CVLT","CYTK","LNTH","LSTR","GGAL","TEM","WSC","LSCC","FRPT","MAT","AAL","WTFC","CCCS","NSIT","SAIC","VKTX","REYN","NOVT","LFUS","BOKF","VRNS","HQY","ALAB","BZ","ETSY","AUR","CWST","RCM","CHX","BPMC","PEGA","ONB","VERX","COOP","HLNE","GRFS","EXLS","NXT","BILI","TMDX","SRCL","CACC","OLLI","KRYS","LANC","BCPC","OPCH","SIGI","BECN","GLBE","MDGL","FCFS","MMSI","CRVL","FRHC","EXPO","AVAV","ALGM","ACT","NXST","XRAY","DOOO","TENB","ACIW","FFIN","COLB","TPG","AVT","CRDO","CSWI","UBSI","RMBS","RARE","COLM","ESGR","NVEI","SATS","RNA","UMBF","RDNT","OZK","DJT","QLYS","NUVL","SLM","BGC","EEFT","BBIO","QXO","MARA","FELE","APLS","VRRM","DYN","IMVT","PI","TIGO","ITRI","ALKS","TSEM","IAC","OS","VNOM","RUN","PECO","FIZZ","CAMT","CNXC","HWC","STNE","ADMA","LYFT","SHC","WAY","LOPE","BRZE","CRNX","CRSP","VLY","AXSM","RUSHA","IPAR","RUSHB","BLKB","SBRA","AEIS","NCNO","GBDC","FIVE","SGRY","SANM","ASO","URBN","OTTR","FORM","TFSL","GH","PAGP","QFIN","ICUI","ACLS","IBOC","LLYVK","CORT","FTDR","AXNX","NEOG","GLNG","TRMD","STEP","LLYVA","IDCC","WEN","PTEN","POWI","CALM","MRUS","HCM","IESC","FOLD","CCOI","WDFC","STRL","PRCT","UPST","SMPL","FRSH","ZI","JJSF","ALVO","BANF","DNLI","LOT","BL"]
for symbol in stock_symbols:
    real_time_data = fetch_stock_data(symbol, '1d', '1m')
    if not real_time_data.empty:
        real_time_data = process_data(real_time_data)
        last_price = real_time_data['Close'].iloc[-1]
        change = last_price - real_time_data['Open'].iloc[0]
        pct_change = (change / real_time_data['Open'].iloc[0]) * 100
        st.sidebar.metric(f"{symbol}", f"{last_price:.2f} USD", f"{change:.2f} ({pct_change:.2f}%)")

st.sidebar.subheader('About')
st.sidebar.info('This dashboard provides stock data and technical indicators for various indicators for various time periods. Use the sidebar to check price charts.')
