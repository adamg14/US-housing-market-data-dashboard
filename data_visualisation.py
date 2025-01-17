import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# data pre-processing - separating column indexes into data types (date and non-date) - then processing them accordingly
sale_price_data = pd.read_csv("./Metro_invt_fs_uc_sfrcondo_sm_month.csv")
house_price_data = pd.read_csv("./Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv")
sale_count_data = pd.read_csv("./Metro_sales_count_now_uc_sfrcondo_month.csv")
print(sale_price_data.head())
print(house_price_data.head())
print(sale_count_data.head())

# separating columns into date and non date
# sale price
sale_price_non_dates = sale_price_data.columns[:5]
sale_price_dates = sale_price_data.columns[5:]

# house price
house_price_non_dates = house_price_data.columns[:5]
house_price_dates = house_price_data.columns[5:]

# sale count
sale_count_non_dates = sale_count_data.columns[:5]
sale_count_dates = sale_count_data.columns[5:]

# converting the date columns from string to date
sale_price_dates = pd.to_datetime(sale_price_dates, errors="ignore")
house_price_dates = pd.to_datetime(house_price_dates, errors="ignore")
sale_count_dates = pd.to_datetime(sale_count_dates, errors="ignore")

# rejoining the non-date and date column indexes together
sale_price_data.columns = list(sale_price_non_dates) + list(sale_price_dates)
house_price_data.columns = list(house_price_non_dates) + list(house_price_dates)
sale_count_data.columns = list(sale_count_non_dates) + list(sale_count_dates)

# the DataFrames after data=-preprocessing
print(sale_price_data.head())
print(house_price_data.head())
print(sale_count_data.head())

def date_filter(data_frame, date_range):
    date_range = sorted(date_range)
    dates = pd.to_datetime(data_frame["Date"], format="%Y-%m-%d").dt.date
    return data_frame[(dates >= date_range[0]) & (dates <= date_range[1])]

def string_to_date(date_string):
    return datetime.strptime(date_string,"%Y-%m-%d").date()

# visualisations
# MEAN PRICE OF LISTED HOUSES GROUPED BY STATE
def list_price():
    state_price = sale_price_data.groupby("StateName").mean(numeric_only=True)
    data_columns = sale_price_data.columns[6:]
    state_price_data = state_price[data_columns].reset_index()
    price_data = state_price_data.melt(id_vars=["StateName"], var_name="Date", value_name="Value")
    
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    sns.lineplot(data=price_data, x="Date", y="Value", hue="StateName", ax=ax)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.xticks(rotation=45)
    plt.title("Average Monthly Rent by State")
    plt.tight_layout()
    return fig
    
# MEAN PRICE VALUE OF HOUSES GROUPED BY STATE
def house_price():
    state_price = house_price_data.groupby("StateName").mean(numeric_only=True)
    data_columns = house_price_data.columns[6:]
    state_price_data = state_price[data_columns].reset_index()
    price_data = state_price_data.melt(id_vars=["StateName"], var_name="Date", value_name="Value")
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    sns.lineplot(data=price_data, x="Date", y="Value", hue="StateName", ax=ax)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.xticks(rotation=45)
    plt.title("Average House Value by State")
    plt.tight_layout()
    return fig
    

# NUMBER OF SALES GROUPED BY STATE
def sales_count():
    state_sales = sale_count_data.groupby("StateName").mean(numeric_only=True)
    data_columns = state_sales.columns[6:]
    state_count_data = state_sales[data_columns].reset_index()
    state_count = state_count_data.melt(id_vars=["StateName"], var_name="Date", value_name="Value")
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    sns.lineplot(data=state_count, x="Date", y="Value", hue="StateName", ax=ax)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig
