import streamlit as st
import pandas as pd
import plotly.express as px
import base64 #Standard python module
from io import StringIO, BytesIO # Standars Python Module
from PIL import Image




def generate_excel_download_link(df):
    towrite= BytesIO()
    fig.write_html(towrite, include_plotlyjs= "cdn")
    df.to_excel(towrite,encoding="utf-8", index=False, header=True) #write to BytesIO
    towrite.seek(0) # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href= "data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,base64,{b64}" download="data_download.xlsx">Download Excel File</a>'
    return st.markgown(href, unsafe_allow_html =True)

def generate_html_download_link(fig):
    towrite = StringIO()
    fig.write_html(towrite, include_plotlyjs="cdn")
    towrite= BytesIO(towrite.getvalue().encode())
    b64 =base64.b64encode(towrite.reade()).decode()
    href = f'<a href="data:text.html;charset=utf-8; base64,{b64}" download= "plot.html">Download html file </a>'
    return st.markgown(href, unsafe_allow_html =True)



st.set_page_config(page_title='Excel Plotter')
st.title('Excel Plotter')
st.subheader('Feed me with your file')
uploaded_file=st.file_uploader('choose a XLSX file', type='xlsx')
if uploaded_file:
    st.markdown('---')
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    st.dataframe(df)
    # number_column_analyze= st.text_input('enter the number')
    # column_name = []
    # for i in number_column_analyze:
    #     column_name = "{}".st.text_input('Enter the exact column name', {i}).extend()
    image = Image.open('data_dash.PNG')
    st.image(image,
         caption= 'Designed by Eltemfus',
         use_column_width =True)

    groupby_column = st.selectbox(
        'please inter the data you would like to analyse', ('Invoice_number','Agent','Customer_name','Price_unit','Payment_due_date','Comments')
        
    )

    # -----Groupe Dadaframe
    output_columns = ['Customer_name','Agent']
    # output_columns=[]
    # for i in column_name:
    #     output_columns = "{}".st.text_input('Enter deux column name', {i}).extend()
   
    df_grouped = df.groupby(by=[groupby_column],as_index=False)[output_columns].sum()
    st.dataframe(df_grouped)

#------('Invoice_number','Agent','Customer_name','Price_unit','Payment_due_date','Comments')

    #---PLOT DATAFRAME
    fig = px.bar(
        df_grouped,
        x= 'Customer_name',
        y= 'Agent',
        color ='Agent',
        color_continuous_scale=['red','yellow','green'],
        template='plotly_white',
        title= f'<b>Customer_name & Payment_due_date by {groupby_column} </b>'

    )
    st.plotly_chart(fig)

    

    pie_chart = px.pie( df_grouped,
        title= 'Customer_name & Payment_due_date',
        values= 'Agent',
        names= 'Customer_name'


    )
    st.plotly_chart(pie_chart)


    #------Download section
    st.subheader('Download')
    generate_excel_download_link(fig)
    generate_html_download_link(fig)


