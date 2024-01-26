import yfinance as yf
import streamlit as st
import pandas as pd



st.write("<div style='text-align:center;font-size:45px;font-weight:bold;color:black'>ГРАФИКИ АКЦИЙ КРУПНЕЙШИХ КОМПАНИЙ РОССИИ </div>", unsafe_allow_html=True)



sheets = ['БАНКИ', 'ПРОМЫШЛЕННОСТЬ', 'IT', 'ТОРГОВЛЯ']
dicts = []

for sheet in sheets:
    df = pd.read_excel('RF_COMPS.xlsx', sheet_name=sheet)
    ticker_dict = df.set_index(df.columns[0]).to_dict().get(df.columns[1])
    images_dict = df.set_index(df.columns[0]).to_dict().get(df.columns[2])
    dicts.append({'ticker_dict': ticker_dict, 'images_dict': images_dict})

bank_ticker_dicts, prom_ticker_dicts, it_ticker_dicts, torg_ticker_dicts = [d['ticker_dict'] for d in dicts]
bank_images_dict, prom_images_dict, it_images_dict, torg_images_dict = [d['images_dict'] for d in dicts]




#боковая панель
st.sidebar.write("<div style='text-align:center;font-size:50px;font-weight:bold;color:black'>Функционал</div>", unsafe_allow_html=True)
st.sidebar.info("Сайт показывает ***Цену закрытия***  и ***Объем акций*** ведущих компаний России")
st.sidebar.info("Ниже вы можете выбрать ***тип*** компании и ***период времени***")
company_options = ['Банк', 'Промышленная', 'IT','Розничная торговля']
selected_options = st.sidebar.selectbox('Тип компании', company_options)
start_date = st.sidebar.slider("Выберите начальный год:", 2010, 2022, 2010)
end_date = st.sidebar.slider("Выберите конечный год:", 2010, 2022, 2022)

def show_stock_data(selected_option, company_name, company_ticker_dicts, company_images_dict, start_date, end_date):
    company_name = st.selectbox("**Выберите компанию**:", list(company_ticker_dicts.keys()))
    if company_name not in company_ticker_dicts:
        st.error("Company not found.")
        return
    tickerSymbol = company_ticker_dicts[company_name]
    tickerDf = yf.download(tickerSymbol, start=f'{start_date}-1-1', end=f'{end_date}-12-31')
    st.write("<div style='text-align:center'><img src='{}' style='width:450px; height:auto;' /></div>".format(company_images_dict[company_name]), unsafe_allow_html=True)
    st.write("<div style='text-align:center;font-size:30px;font-weight:bold;color:black'>ЦЕНА ЗАКРЫТИЯ "f"«{company_name}» ({start_date} - {end_date})</div>", unsafe_allow_html=True)
    st.line_chart(tickerDf.Close)
    st.write("<div style='text-align:center;font-size:30px;font-weight:bold;color:black'>ОБЪЕМ АКЦИЙ"f"«{company_name}» ({start_date} - {end_date})</div>", unsafe_allow_html=True)
    st.line_chart(tickerDf.Volume)


if "Банк" in selected_options:
    show_stock_data("Банк", df, bank_ticker_dicts, bank_images_dict, start_date, end_date)

elif "Промышленная" in selected_options:
    show_stock_data("Промышленная", df, prom_ticker_dicts, prom_images_dict, start_date, end_date)

elif "IT" in selected_options:
    show_stock_data("IT", df, it_ticker_dicts, it_images_dict, start_date, end_date)

elif "Розничная торговля" in selected_options:
    show_stock_data("Розничная торговля", df, torg_ticker_dicts, torg_images_dict, start_date, end_date)
