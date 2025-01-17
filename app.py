from data_visualisation import sale_price_data, house_price_data, sale_count_data, date_filter, string_to_date
from shiny.express import input
from shiny import App, render, ui
from US_STATES import US_STATES
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

string_sale_price_df = pd.read_csv("./Metro_invt_fs_uc_sfrcondo_sm_month.csv")
string_house_price_df = pd.read_csv("./Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv")
string_state_count_df = sale_count_data = pd.read_csv("./Metro_sales_count_now_uc_sfrcondo_month.csv")

app_ui = ui.page_fluid(
    ui.h1("United States of America Housing Market Analysis", style="text-align: center;"),
    ui.input_select("us_state", "Filter By State", choices=US_STATES),
    ui.input_slider("date_range", "Filter By Date Range",
    min=string_to_date('2000-01-31'),
    max=string_to_date('2024-12-31'),
    value=[string_to_date(x) for x in ["2018-3-31", "2024-4-30"]]
    ),
    
    ui.output_plot("list_price"),
    ui.output_data_frame("table"),
    ui.output_plot("house_price"),
    ui.output_data_frame("house_price_data_frame"),
    ui.output_plot("sale_count"),
    ui.output_data_frame("sale_count_data_frame")
    
    
)

def server(input, output, session):
    @render.plot
    def list_price():
        state_price = sale_price_data.groupby("StateName").mean(numeric_only=True)
        data_columns = sale_price_data.columns[6:]
        state_price_data = state_price[data_columns].reset_index()
        price_data = state_price_data.melt(id_vars=["StateName"], var_name="Date", value_name="Value")
        price_data = state_price_data.melt(id_vars=["StateName"], var_name="Date", value_name="Value")
        
        if input.us_state() == "United States":
            price_data = state_price_data.melt(id_vars=["StateName"], var_name="Date", value_name="Value")
        else:
            price_data = price_data[price_data["StateName"] == input.us_state()]
            
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=12))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        sns.lineplot(data=price_data, x="Date", y="Value", hue="StateName", ax=ax)
        plt.legend(ncol=3, bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
        plt.tight_layout()
        plt.title("Average Monthly Rent by State")
        plt.ylabel("Average Monthly Rent")
        return fig
    
    @render.data_frame
    def table():
        if input.us_state() == "United States":
            df = string_sale_price_df
        else:
            df = string_sale_price_df[string_sale_price_df["StateName"] == input.us_state()]
        
        return render.DataGrid(df)
    
    
    @render.plot
    def house_price():
        state_price = house_price_data.groupby("StateName").mean(numeric_only=True)
        data_columns = house_price_data.columns[6:]
        state_price_data = state_price[data_columns].reset_index()

        # Filter first
        if input.us_state() != "United States":
            state_price_data = state_price_data[state_price_data["StateName"] == input.us_state()]

        # Now melt the filtered data
        price_data = state_price_data.melt(id_vars=["StateName"], var_name="Date", value_name="Value")

        price_data["Date"] = pd.to_datetime(price_data["Date"])

        # Plot
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=30))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        sns.lineplot(data=price_data, x="Date", y="Value", hue="StateName", ax=ax)
        plt.legend(ncol=3, bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
        plt.tight_layout()
        plt.title("Average House Price by State")
        plt.ylabel("Average House Price")
        return fig
    
    
    @render.data_frame
    def house_price_data_frame():
        if input.us_state() == "United States":
            df = string_sale_price_df
        else:
            df = string_sale_price_df[string_sale_price_df["StateName"] == input.us_state()]
    
        return df
    
    
    @render.plot
    def sale_count():
        state_sales = sale_count_data.groupby("StateName").mean(numeric_only=True)
        data_columns = state_sales.columns[6:]
        state_count_data = state_sales[data_columns].reset_index()

        if input.us_state() != "United States":
            state_count_data = state_count_data[state_count_data["StateName"] == input.us_state()]

        state_count = state_count_data.melt(id_vars=["StateName"], var_name="Date", value_name="Value")
        
        state_count["Date"] = pd.to_datetime(state_count["Date"])
        
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=30))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        sns.lineplot(data=state_count, x="Date", y="Value", hue="StateName", ax=ax)
        plt.legend(ncol=3, bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
        plt.tight_layout()
        plt.title("Average Monthly House Sales by State")
        plt.ylabel("Average House Price")
        return fig
    
    
    @render.data_frame
    def sale_count_data_frame():
        if input.us_state() == "United States":
            df = string_state_count_df
        else:
            df = string_sale_price_df[string_sale_price_df["StateName"] == input.us_state()]
        
        return df


app = App(app_ui, server)
