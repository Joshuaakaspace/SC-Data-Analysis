import streamlit as st

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

import altair as alt

from io import BytesIO

from pyxlsb import open_workbook as open_xlsb

from streamlit_pandas_profiling import st_profile_report

from pandas_profiling import ProfileReport

 

#matplotlib.rcParmas[figure.figsize] == (20,10)

def main():

    st.title("Service Cloud Data Cleaner and Analyser")

    menu = ['Clean', 'Analysis']

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == 'Clean':

        st.subheader("SC Cleaner")

        file_upload = st.file_uploader("Upload file", type = ['csv'])

        if st.button('Submit'):

            df = pd.read_csv(file_upload)

            #df.drop(columns = ['Alert Id','Hot Topic: Case Number','Description','Template ID','Outage Start.1','Alert Log'], inplace = True)

            df.drop(columns = ['Alert Id','Hot Topic: Case Number','Description','Template ID','Alert Log'], inplace = True)

            df.dropna( inplace = True)

            df["Outage Start"] = pd.to_datetime(df["Outage Start"])

            df["Notified Time"] = pd.to_datetime(df["Notified Time"])

            df["First Reported"] = pd.to_datetime(df["First Reported"])

            df["Actual Resolution"] = pd.to_datetime(df["Actual Resolution"])

            df["Last Updated"] = pd.to_datetime(df["Last Updated"])

            df['B1'] = df["First Reported"] -df["Outage Start"]

            df['B2'] = df["First Reported"] -df["Notified Time"]

            df['B3'] = df["Last Updated"] -df["Actual Resolution"]

            df.drop(columns = ['Outage Start','First Reported','Actual Resolution','Last Updated','Notified Time'], inplace = True)

            #sorting

            time = df['B1']

            timex = []

            for x in time:

                z = x.total_seconds()

                timex.append(z)

            df.insert(2,'Time to Communicate', timex, True)

            #adding 1

            cap = df['Time to Communicate']

            list = ["<5 mins" if x <= 300 else "5 to 15 mins" if 300 <= x <=900 else "15 to 30 mins" if 900 <= x <=1800 else "> 30 mins" for x in cap]

            df.insert(3,'Time to Communicate Bucket', list, True)

            #sorting 2

            time = df['B2']

            timexp = []

            for x in time:

                z = x.total_seconds()

                timexp.append(z)

            df.insert(3,'Time to Issue', timexp, True)

            #adding 2

            cap1 = df['Time to Issue']

            list = ["< 2 mins" if x <= 120 else "2 to 5 mins" if 120 <= x <=300 else "> 5 mins" for x in cap1]

            df.insert(3,'Time to Issue Bucket', list, True)

            #sorting 3

            time = df['B3']

            timexp2 = []

            for x in time:

                z = x.total_seconds()

                timexp2.append(z)

            df.insert(4,'Time to Resolve', timexp2, True)

            #adding 3

            cap2 = df['Time to Resolve']

            list = ["< 15 mins" if x < 900 else "15 to 30 mins" if 900 <= x <=1800 else " 30 to 60 mins" if 1800 <= x <= 3600 else "> 60 mins" for x in cap2]

            df.insert(5,'Time to resolve Bucket', list, True)

            df.drop(['B1','B2', 'B3'], axis = 1, inplace = True)

            st.dataframe(df)

            #plots1

            st.header('Visual Representation')

            st.subheader('Time taken to Communicate')

            labels = ['< 5mins', ' 5 - 15 mins', '15-30 mins', '> 30 mins']

            sizes = df['Time to Communicate Bucket'].value_counts()

            colors = ['gold','green', 'lightcoral','lightskyblue']

            explode = [0.1,0.1,0.1,0.1]

            fig1, ax1 = plt.subplots()

            ax1.pie(sizes, labels =labels, colors=colors, startangle=90, shadow=True, explode= explode, autopct='%1.2f')

            ax1.axis('equal')

            st.pyplot(fig1)

            #plots2

            st.subheader('Time taken to Issue')

            labels = ['< 2 mins', ' 2 - 5 mins','> 5 mins']

            sizes = df['Time to Issue Bucket'].value_counts()

            colors = ['gold','green', 'lightcoral']

            explode = [0.1,0.1,0.1]

            fig1, ax1 = plt.subplots()

            ax1.pie(sizes, labels =labels, colors=colors, startangle=90, shadow=True, explode= explode, autopct='%1.2f')

            ax1.axis('equal')

            st.pyplot(fig1)

            #plot3

            st.subheader('Time taken to resolve')

            labels = ['< 15 mins', ' 15 - 30 mins', '30-60 mins', '> 60 mins']

            sizes = df['Time to resolve Bucket'].value_counts()

            colors = ['gold','green', 'lightcoral','lightskyblue']

            explode = [0.1,0.1,0.1,0.1]

            fig1, ax1 = plt.subplots()

            ax1.pie(sizes, labels =labels, colors=colors, startangle=90, shadow=True, explode= explode, autopct='%1.2f')

            ax1.axis('equal')

            st.pyplot(fig1)

            #csv download

            output = BytesIO()

            writer = pd.ExcelWriter(output, engine='xlsxwriter')

            df.to_excel(writer, index=False, sheet_name='Sheet1')

            workbook = writer.book

            worksheet = writer.sheets['Sheet1']

            format1 = workbook.add_format({'num_format': '0.00'})

            worksheet.set_column('A:A', None, format1) 

            writer.save()

            processed_data = output.getvalue()

            st.download_button(label='Download Current Result', data=processed_data ,file_name= 'df_test.xlsx')

    elif choice == 'Analysis':

        file_upload = st.file_uploader("Upload file", type = ['csv'])

        if st.button('Submit'):

            if file_upload is not None:

                def load_csv():

                    csv = pd.read_csv(file_upload)

                    return csv

            df = load_csv()

            pr = ProfileReport(df, explorative = True)

            st.header("Input DataFrame")

            st_profile_report(pr)

if __name__ == '__main__':

    main()