import streamlit as st
import pandas as pd
import numpy as np
import pymysql
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

st.title("Bank Details Working")

uploaded_file1 = st.file_uploader("Upload the input file", type=["csv","xlsx"])





def processedFile(uploaded_file1):
    if uploaded_file1: 
        bank_detail_df=pd.read_excel(uploaded_file1)
        bank_detail_df = bank_detail_df.rename(columns = {'Customer ID':'customer_id'})



        con = pymysql.connect(host ='easy-prod-db-replica-new.cpmomzsxd8rm.ap-south-1.rds.amazonaws.com',user = 'YashSharma',passwd = 'Vrv6XukaKb8ECUK',port=3306)
        con.connect()
        refund_details1 = pd.read_sql('''select  distinct a.bank_account_number,a.customer_id,  a.bank_account_holder, 
        a.bank_code, b.ifsc_code 
        from payment_service.autopay_subscriptions a join loan_service.bank_details b
        on a.bank_account_number = b.bank_account_no
        where a.subscription_status = 'ACTIVE'
        and a.customer_id in {}
        '''.format(tuple(bank_detail_df['customer_id'])),con)

        con.close()
        refund_details1.shape
        bank_detail_df['customer_id']=bank_detail_df.customer_id.astype(int)
        refund_details1['customer_id']=refund_details1.customer_id.astype(int)
        final_df = pd.merge(bank_detail_df, refund_details1, on='customer_id', how='left')


        file_path = "Bank_details_result.xlsx"
        final_df.to_excel(file_path, index=False)
        st.write(f"Final File saved in {file_path}")

# Provide a download button in Streamlit
        with open(file_path, "r") as file:
            st.download_button(
            label="Download Accuracy File",
            data=file,
            file_name="Accuracy.csv",
            mime="csv",
            )
    else:
        st.info("Please upload the valid XLSX file")



processedFile(uploaded_file1)
