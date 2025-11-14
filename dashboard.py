import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="SCPL!!!", page_icon=":bar_chart:",layout="wide")

st.title(" :bar_chart: SCPL DASHBOARD BUSINESS OVERVIEW")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

uploaded_files = st.file_uploader(":file_folder: Upload up to 4 CSV files", type=["csv"], accept_multiple_files=True)

dfs = []


if uploaded_files:
    for fl in uploaded_files[:4]:
        st.write(f"Loaded: {fl.name}")
        df = pd.read_csv(fl, encoding="ISO-8859-1")
        dfs.append(df)
else:
    os.chdir(r"C:\Users\Hello\OneDrive\Desktop\streamlit")
    filenames = [
        "OSLAN_Report_with_District.csv",
        "Collection_Report_with_District.csv",
        "CB_Report_with_District.csv",
        "Income_vs_Expenses_Report_with_District.csv"
    ]
    for file in filenames:
        df = pd.read_csv(file, encoding="ISO-8859-1")
        dfs.append(df)

# ✅ Move this OUTSIDE the if-else block so it's always defined
main_df = pd.concat(dfs, ignore_index=True)
main_df['Date'] = pd.to_datetime(main_df['Date'], errors='coerce')
 
col1, col2 = st.columns((2))
df["Date"] = pd.to_datetime(df["Date"])

# Getting the min and max date 
startDate = main_df["Date"].min()
endDate = main_df["Date"].max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = main_df[(main_df["Date"] >= date1) & (main_df["Date"] <= date2)].copy()

st.sidebar.header("Choose your filter: ")
     
# Filter the data based on Branch Name, DM Name and District
branch_name = st.sidebar.multiselect("Pick your Branch Name", df["Branch Name"].unique())
dm_name = st.sidebar.multiselect("Pick your DM Name", df["DM Name"].unique())
district = st.sidebar.multiselect("Pick your District", df["District"].unique())
month = st.sidebar.multiselect("Pick your Month", df["Month Name"].unique())

# Filter the data
df2 = main_df.copy()

if branch_name:
    df2 = df2[df2["Branch Name"].isin(branch_name)]

if dm_name:
    df2 = df2[df2["DM Name"].isin(dm_name)]

if district:
    df2 = df2[df2["District"].isin(district)]

if month:
    df2 = df2[df2["Month Name"].isin(month)]
    
    
# Show filtered data
st.write(df2)

fy_df = df2.groupby("FY", as_index=False)["Disbursement In Value"].sum()

with col1:
    st.subheader("FY wise Disbursement")

    fig = px.bar(
        fy_df,
        x="FY",
        y="Disbursement In Value",
        color="FY",  # ✅ This enables dynamic colors
        text=['₹{:,.2f}'.format(x) for x in fy_df["Disbursement In Value"]],
        template="seaborn",
        height=350
    )

    fig.update_traces(textposition="inside")
    fig.update_layout(xaxis_tickangle=-45, showlegend=False)  # Hide legend if not needed

    st.plotly_chart(fig, use_container_width=True)
    
df2["New client "] = pd.to_numeric(df2["New client "], errors="coerce")

newclient_df = df2.groupby("FY", as_index=False)["New client "].sum()

with col2:
    st.subheader("FY wise New client")

    fig = px.bar(
        newclient_df,
        x="FY",
        y="New client ",
        color="FY",
        text=[f'{x:,.0f}' for x in newclient_df["New client "]],
        template="seaborn",
        height=350
    )

    fig.update_traces(textposition="inside")
    fig.update_layout(xaxis_tickangle=-45, showlegend=False)

    st.plotly_chart(fig, use_container_width=True)
    
cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("fy_df"):
        st.write(fy_df.style.background_gradient(cmap="Blues"))
        csv = fy_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "fy.csv", mime = "text/csv",
                           help = 'Click here to download the data as a CSV file')

with cl2:
    with st.expander("newclient_df"):
        region = newclient_df.groupby(by = "FY", as_index = False)["New client "].sum()
        st.write(newclient_df.style.background_gradient(cmap="Oranges"))
        csv = newclient_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "newclient.csv", mime = "text/csv",
                           help = 'Click here to download the data as a CSV file')
        
col3, col4 = st.columns(2)
        
df2["NO of Loan"] = pd.to_numeric(df2["NO of Loan"], errors="coerce")

noofloan_df = df2.groupby("FY", as_index=False)["NO of Loan"].sum()

with col3:
    st.subheader("FY wise NO of Loan")

    fig = px.bar(
        noofloan_df,
        x="FY",
        y="NO of Loan",
        color="FY",
        text=[f'{x:,.0f}' for x in noofloan_df["NO of Loan"]],
        template="seaborn",
        height=350
    )

    fig.update_traces(textposition="inside")
    fig.update_layout(xaxis_tickangle=-45, showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

df2["NO of Loan_1"] = pd.to_numeric(df2["NO of Loan_1"], errors="coerce")

activeloan_df = df2.groupby("FY", as_index=False)["NO of Loan_1"].sum()

with col4:
    st.subheader("FY wise Active Loan")

    fig = px.bar(
        activeloan_df,
        x="FY",
        y="NO of Loan_1",
        color="FY",
        text=[f'{x:,.0f}' for x in activeloan_df["NO of Loan_1"]],
        template="seaborn",
        height=350
    )

    fig.update_traces(textposition="inside")
    fig.update_layout(xaxis_tickangle=-45, showlegend=False)

    st.plotly_chart(fig, use_container_width=True)
    
cl3, cl4 = st.columns((2))
with cl3:
    with st.expander("noofloan_df"):
        region = noofloan_df.groupby(by = "FY", as_index = False)["NO of Loan"].sum()
        st.write(noofloan_df.style.background_gradient(cmap="Blues"))
        csv = noofloan_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "noofloan.csv", mime = "text/csv",
                           help = 'Click here to download the data as a CSV file')

with cl4:
    with st.expander("activeloan_df"):
        region = activeloan_df.groupby(by = "FY", as_index = False)["NO of Loan_1"].sum()
        st.write(activeloan_df.style.background_gradient(cmap="Oranges"))
        csv = activeloan_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "activeloan.csv", mime = "text/csv",
                           help = 'Click here to download the data as a CSV file')
        
col5, col6 = st.columns(2)
        
df2["AUM In Value"] = pd.to_numeric(df2["AUM In Value"], errors="coerce")

aum_df = df2.groupby("FY", as_index=False)["AUM In Value"].sum()

with col5:
    st.subheader("FY wise AUM")

    fig = px.bar(
        aum_df,
        x="FY",
        y="AUM In Value",
        color="FY",
        text=[f'{x:,.0f}' for x in aum_df["AUM In Value"]],
        template="seaborn",
        height=350
    )

    fig.update_traces(textposition="inside")
    fig.update_layout(xaxis_tickangle=-45, showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

df2["PAR COUNT"] = pd.to_numeric(df2["PAR COUNT"], errors="coerce")

parcount_df = df2.groupby("FY", as_index=False)["PAR COUNT"].sum()

with col6:
    st.subheader("FY wise PAR COUNT")

    fig = px.bar(
        parcount_df,
        x="FY",
        y="PAR COUNT",
        color="FY",
        text=[f'{x:,.0f}' for x in parcount_df["PAR COUNT"]],
        template="seaborn",
        height=350
    )

    fig.update_traces(textposition="inside")
    fig.update_layout(xaxis_tickangle=-45, showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

cl5, cl6 = st.columns((2))
with cl5:
    with st.expander("aum_df"):
        region = aum_df.groupby(by = "FY", as_index = False)["AUM In Value"].sum()
        st.write(aum_df.style.background_gradient(cmap="Blues"))
        csv = aum_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "aum.csv", mime = "text/csv",
                           help = 'Click here to download the data as a CSV file')

with cl6:
    with st.expander("parcount_df"):
        region = parcount_df.groupby(by = "FY", as_index = False)["PAR COUNT"].sum()
        st.write(parcount_df.style.background_gradient(cmap="Oranges"))
        csv = parcount_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "parcount.csv", mime = "text/csv",
                           help = 'Click here to download the data as a CSV file')

col7, col8 = st.columns(2)
        
df2["Total PAR In Value"] = pd.to_numeric(df2["Total PAR In Value"], errors="coerce")

parvalue_df = df2.groupby("FY", as_index=False)["Total PAR In Value"].sum()

with col7:
    st.subheader("FY wise PAR VALUE")

    fig = px.bar(
        parvalue_df,
        x="FY",
        y="Total PAR In Value",
        color="FY",
        text=[f'{x:,.0f}' for x in parvalue_df["Total PAR In Value"]],
        template="seaborn",
        height=350
    )

    fig.update_traces(textposition="inside")
    fig.update_layout(xaxis_tickangle=-45, showlegend=False)

    st.plotly_chart(fig, use_container_width=True)
    
df2["Total Collection"] = pd.to_numeric(df2["Total Collection"], errors="coerce")

collection_df = df2.groupby("FY", as_index=False)["Total Collection"].sum()

with col8:
    st.subheader("FY wise COLLECTION VALUE")

    fig = px.bar(
        collection_df,
        x="FY",
        y="Total Collection",
        color="FY",
        text=[f'{x:,.0f}' for x in collection_df["Total Collection"]],
        template="seaborn",
        height=350
    )

    fig.update_traces(textposition="inside")
    fig.update_layout(xaxis_tickangle=-45, showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

cl7, cl8 = st.columns((2))
with cl7:
    with st.expander("parvalue_df"):
        region = parvalue_df.groupby(by = "FY", as_index = False)["Total PAR In Value"].sum()
        st.write(parvalue_df.style.background_gradient(cmap="Blues"))
        csv = parvalue_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "parvalue.csv", mime = "text/csv",
                           help = 'Click here to download the data as a CSV file')

with cl8:
    with st.expander("collection_df"):
        region = collection_df.groupby(by = "FY", as_index = False)["Total Collection"].sum()
        st.write(collection_df.style.background_gradient(cmap="Oranges"))
        csv = collection_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "collection.csv", mime = "text/csv",
                           help = 'Click here to download the data as a CSV file')
    
col9, col10 = st.columns(2)
        
df2["No of center handled"] = pd.to_numeric(df2["No of center handled"], errors="coerce")

center_df = df2.groupby("FY", as_index=False)["No of center handled"].sum()

with col9:
    st.subheader("FY wise TOTAL CENTER HANDLED")

    fig = px.bar(
        center_df,
        x="FY",
        y="No of center handled",
        color="FY",
        text=[f'{x:,.0f}' for x in center_df["No of center handled"]],
        template="seaborn",
        height=350
    )

    fig.update_traces(textposition="inside")
    fig.update_layout(xaxis_tickangle=-45, showlegend=False)

    st.plotly_chart(fig, use_container_width=True)
    
df2["No of client handled"] = pd.to_numeric(df2["No of client handled"], errors="coerce")

client_df = df2.groupby("FY", as_index=False)["No of client handled"].sum()

with col10:
    st.subheader("FY wise CUSTOMER HANDLED")

    fig = px.bar(
        client_df,
        x="FY",
        y="No of client handled",
        color="FY",
        text=[f'{x:,.0f}' for x in client_df["No of client handled"]],
        template="seaborn",
        height=350
    )

    fig.update_traces(textposition="inside")
    fig.update_layout(xaxis_tickangle=-45, showlegend=False)

    st.plotly_chart(fig, use_container_width=True)
    
cl9, cl10 = st.columns((2))
with cl9:
    with st.expander("center_df"):
        region = center_df.groupby(by = "FY", as_index = False)["No of center handled"].sum()
        st.write(center_df.style.background_gradient(cmap="Blues"))
        csv = center_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "center.csv", mime = "text/csv",
                           help = 'Click here to download the data as a CSV file')

with cl10:
    with st.expander("client_df"):
        region = client_df.groupby(by = "FY", as_index = False)["No of client handled"].sum()
        st.write(client_df.style.background_gradient(cmap="Oranges"))
        csv = client_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "client.csv", mime = "text/csv",
                           help = 'Click here to download the data as a CSV file')
        
col11, col12 = st.columns(2)
        
df2["C-TGT LAN"] = pd.to_numeric(df2["C-TGT LAN"], errors="coerce")

ctgt_df = df2.groupby("FY", as_index=False)["C-TGT LAN"].sum()

with col11:
    st.subheader("FY wise C-BUCKET TGT LAN")

    fig = px.bar(
        ctgt_df,
        x="FY",
        y="C-TGT LAN",
        color="FY",
        text=[f'{x:,.0f}' for x in ctgt_df["C-TGT LAN"]],
        template="seaborn",
        height=350
    )

    fig.update_traces(textposition="inside")
    fig.update_layout(xaxis_tickangle=-45, showlegend=False)

    st.plotly_chart(fig, use_container_width=True)
    
df2["C-ACHMT LAN"] = pd.to_numeric(df2["C-ACHMT LAN"], errors="coerce")

cachmt_df = df2.groupby("FY", as_index=False)["C-ACHMT LAN"].sum()

with col12:
    st.subheader("FY wise C-BUCKET ACHMT LAN")

    fig = px.bar(
        cachmt_df,
        x="FY",
        y="C-ACHMT LAN",
        color="FY",
        text=[f'{x:,.0f}' for x in cachmt_df["C-ACHMT LAN"]],
        template="seaborn",
        height=350
    )

    fig.update_traces(textposition="inside")
    fig.update_layout(xaxis_tickangle=-45, showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

cl11, cl12 = st.columns((2))
with cl11:
    with st.expander("ctgt_df"):
        region = ctgt_df.groupby(by = "FY", as_index = False)["C-TGT LAN"].sum()
        st.write(ctgt_df.style.background_gradient(cmap="Blues"))
        csv = ctgt_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "ctgt.csv", mime = "text/csv",
                           help = 'Click here to download the data as a CSV file')

with cl12:
    with st.expander("cachmt_df"):
        region = cachmt_df.groupby(by = "FY", as_index = False)["C-ACHMT LAN"].sum()
        st.write(cachmt_df.style.background_gradient(cmap="Oranges"))
        csv = cachmt_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "cachmt.csv", mime = "text/csv",
                           help = 'Click here to download the data as a CSV file')

col13, col14 = st.columns(2)
        
df2["cb_count"] = pd.to_numeric(df2["cb_count"], errors="coerce")

cbcheck_df = df2.groupby("FY", as_index=False)["cb_count"].sum()

with col13:
    st.subheader("FY wise Total CB Check")

    fig = px.bar(
        cbcheck_df,
        x="FY",
        y="cb_count",
        color="FY",
        text=[f'{x:,.0f}' for x in cbcheck_df["cb_count"]],
        template="seaborn",
        height=350
    )

    fig.update_traces(textposition="inside")
    fig.update_layout(xaxis_tickangle=-45, showlegend=False)

    st.plotly_chart(fig, use_container_width=True)
       
df2["cb_pass_count"] = pd.to_numeric(df2["cb_pass_count"], errors="coerce")

cbpass_df = df2.groupby("FY", as_index=False)["cb_pass_count"].sum()

with col14:
    st.subheader("FY wise Total CB Pass")

    fig = px.bar(
        cbpass_df,
        x="FY",
        y="cb_pass_count",
        color="FY",
        text=[f'{x:,.0f}' for x in cbpass_df["cb_pass_count"]],
        template="seaborn",
        height=350
    )

    fig.update_traces(textposition="inside")
    fig.update_layout(xaxis_tickangle=-45, showlegend=False)

    st.plotly_chart(fig, use_container_width=True) 

cl13, cl14 = st.columns((2))
with cl13:
    with st.expander("cbcheck_df"):
        region = cbcheck_df.groupby(by = "FY", as_index = False)["cb_count"].sum()
        st.write(cbcheck_df.style.background_gradient(cmap="Blues"))
        csv = cbcheck_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "cbcheck.csv", mime = "text/csv",
                           help = 'Click here to download the data as a CSV file')

with cl14:
    with st.expander("cbpass_df"):
        region = cbpass_df.groupby(by = "FY", as_index = False)["cb_pass_count"].sum()
        st.write(cbpass_df.style.background_gradient(cmap="Oranges"))
        csv = cbpass_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "cbpass.csv", mime = "text/csv",
                           help = 'Click here to download the data as a CSV file')
