import streamlit as st 
import numpy as np 
import pandas as pd
import seaborn as sns
import datetime
import numpy as np

st.title("HC")
sidebar_radiio = st.sidebar.radio(
    'Chức Năng', 
    ( "Kết quả đầu tư", "Tính lợi nhuận")
)
def plot_pnl(): 
    df = pd.read_excel('pnl_live.xlsx')
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
    df.Date = df.Date.dt.date


    df['gain'] = np.floor(df['return']/df['capital'] * 100000) / 100000
    df['total_gain']=df['gain'].cumsum()
    # print(df['total_gain'])
    arr_gain = df['gain'].values 
    # st.line_chart(x=df.Date, y=df.total_gain, color=None, width=0, height=0, use_container_width=True)
    df = df.drop('gain', axis = 1)
    df.total_gain = 100 * df.total_gain
    total_gain_today = str(np.round((df.total_gain.values[-1]), 2)) + " %"
    gain_today =  str(np.round(arr_gain[-1] * 100, 2)) + " %"
    df['Kết quả đầu tư']=df['total_gain']
    df=df[['Date','Kết quả đầu tư']]
    df_vn30 = pd.read_csv('df_vn30.csv')

    df_vn30.Date = pd.to_datetime(df_vn30.Date)
    df_vn30.Date = df_vn30.Date.dt.date

    # df_vn30 = df_vn30[df_vn30.Date.isin(df.Date)].dropna()

    df_vn30.gain = (df_vn30.gain/df_vn30.Close).values * 100 
    df_vn30.total_gain = df_vn30.gain.cumsum()
    df_vn30['VN30']=df_vn30['total_gain']
    df_vn30=df_vn30[['Date','VN30','gain']]

    chart_data = df.merge(df_vn30, on='Date',how='left')
    chart_data['Date'] = pd.to_datetime(chart_data.Date)
    chart_data['Date']=chart_data['Date'].dt.date
    col1, col2 = st.columns(2)
    with col1: 
        st.metric(label="Kết quả đầu tư của tôi", value= total_gain_today, delta=gain_today)
    with col2: 
        st.metric(label="Tăng trưởng của VN30", value= str(np.round(chart_data.VN30.iloc[-1], 2)) + ' %', delta= str(np.round(df_vn30.gain.iloc[-1], 2)) + ' %')

    st.line_chart(chart_data, x="Date", y=["VN30", "Kết quả đầu tư"])
    st.caption('Kết quả đầu tư so với tăng trưởng của VN30')


login = True 
if login == True: 
    if sidebar_radiio == "Kết quả đầu tư": 
        plot_pnl()
        # st.text('So sánh với tăng trưởng của chỉ số VN30 trong cùng một khoảng thời gian.')
        # plot_pnl_vn30()
    if sidebar_radiio == 'Tính lợi nhuận': 
        st.text('Nếu bạn đầu tư với tôi')
        start_day = st.date_input("Ngày bắt đầu", datetime.date(2024, 1, 1))
        start_end = st.date_input("Ngày tất toán", datetime.date.today())
        start_day = pd.to_datetime(start_day)
        start_end = pd.to_datetime(start_end)
        total_money = st.number_input("Số tiền đầu tư (triệu đ): ", 0)
        df = pd.read_excel('pnl_live.xlsx')
        df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
        df['gain'] = np.floor(df['return']/df['capital'] * 100000) / 100000
        df['total_gain']=df['gain'].cumsum()
        # st.line_chart(x=df.Date, y=df.total_gain, color=None, width=0, height=0, use_container_width=True)
        # df = df.drop('gain', axis = 1)
        filtered_df = df[(df['Date'] >= start_day) & (df['Date'] <= start_end)]
        arr_gain = filtered_df.gain.values 

        total_gain = np.sum(arr_gain)
        Tong_tien = str(np.round((1 + total_gain) * total_money , 2)) + " triệu đ"
        Lai =  str(np.round(total_gain * total_money, 2)) + " triệu đ"
        st.metric(label="Tổng tiền thu về", value= Tong_tien, delta=Lai)

        # start_day = st.date_input("Ngày bắt đầu", datetime.date(2024, 01, 01))
    # st.write('Your birthday is:', d)