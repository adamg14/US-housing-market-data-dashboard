from data_visualisation import sale_price_data, house_price_data, sale_count_data, date_filter, string_to_date
from shiny import App, render, ui
from US_STATES import US_STATES
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Read CSVs for display in the data frames
string_sale_price_df = pd.read_csv("./Metro_invt_fs_uc_sfrcondo_sm_month.csv")
string_house_price_df = pd.read_csv("./Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv")
string_state_count_df = pd.read_csv("./Metro_sales_count_now_uc_sfrcondo_month.csv")

# Define the user interface
app_ui = ui.page_fluid(
    ui.h1("United States of America Housing Market Analysis", style="text-align: center;"),
    ui.input_select(
        id="us_state", 
        label="Filter By State", 
        choices=US_STATES
    ),
    ui.input_slider(
        id="date_range", 
        label="Filter By Date Range",
        min=string_to_date("2000-01-31"),
        max=string_to_date("2024-12-31"),
        value=[string_to_date("2000-01-01"), string_to_date("2024-12-31")]
    ),
    ui.output_plot("list_price"),
    ui.output_data_frame("table"),
    ui.output_plot("house_price"),
    ui.output_data_frame("house_price_data_frame"),
    ui.output_plot("sale_count"),
    ui.output_data_frame("sale_count_data_frame")
)

# Define the server logic
def server(input, output, session):
    @render.plot
    def list_price():
        # Compute average by State
        state_price = sale_price_data.groupby("StateName").mean(numeric_only=True)
        data_columns = sale_price_data.columns[6:]
        state_price_data_avg = state_price[data_columns].reset_index()

        # Melt the data for plotting
        price_data = state_price_data_avg.melt(
            id_vars=["StateName"], 
            var_name="Date", 
            value_name="Value"
        )
        
        # Filter by date
        price_data = date_filter(price_data, input.date_range())

        # Filter by state (or entire US)
        if input.us_state() == "United States":
            # Show all states (already melted)
            pass
        else:
            price_data = price_data[price_data["StateName"] == input.us_state()]

        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=12))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        sns.lineplot(data=price_data, x="Date", y="Value", hue="StateName", ax=ax)
        plt.legend(ncol=3, bbox_to_anchor=(1.05, 1), loc="upper left", fontsize="small")
        plt.tight_layout()
        plt.title("Average Monthly Rent by State")
        plt.ylabel("Average Monthly Rent")
        return fig

    @render.data_frame
    def table():
        # Show entire US or filtered by state
        if input.us_state() == "United States":
            df = string_sale_price_df
        else:
            df = string_sale_price_df[string_sale_price_df["StateName"] == input.us_state()]
        # Return a DataGrid with the filtered dataframe
        return render.DataGrid(df)

    @render.plot
    def house_price():
        # Compute average by State
        state_price = house_price_data.groupby("StateName").mean(numeric_only=True)
        data_columns = house_price_data.columns[6:]
        state_price_data_avg = state_price[data_columns].reset_index()

        # Filter by user-selected state (unless user wants entire US)
        if input.us_state() != "United States":
            state_price_data_avg = state_price_data_avg[
                state_price_data_avg["StateName"] == input.us_state()
            ]

        # Melt the data for plotting
        price_data = state_price_data_avg.melt(
            id_vars=["StateName"], 
            var_name="Date", 
            value_name="Value"
        )
        price_data["Date"] = pd.to_datetime(price_data["Date"])
        price_data = date_filter(price_data, input.date_range())
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=30))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        sns.lineplot(data=price_data, x="Date", y="Value", hue="StateName", ax=ax)
        plt.legend(ncol=3, bbox_to_anchor=(1.05, 1), loc="upper left", fontsize="small")
        plt.tight_layout()
        plt.title("Average House Price by State")
        plt.ylabel("Average House Price")
        return fig

    @render.data_frame
    def house_price_data_frame():
        # Show entire US or filtered by state
        if input.us_state() == "United States":
            df = string_house_price_df
        else:
            df = string_house_price_df[string_house_price_df["StateName"] == input.us_state()]
        return df

    @render.plot
    def sale_count():
        # Compute average by State
        state_sales = sale_count_data.groupby("StateName").mean(numeric_only=True)
        data_columns = state_sales.columns[6:]
        state_sales_data_avg = state_sales[data_columns].reset_index()

        # Filter by user-selected state (unless user wants entire US)
        if input.us_state() != "United States":
            state_sales_data_avg = state_sales_data_avg[
                state_sales_data_avg["StateName"] == input.us_state()
            ]

        # Melt the data for plotting
        state_count = state_sales_data_avg.melt(
            id_vars=["StateName"], 
            var_name="Date", 
            value_name="Value"
        )
        
        # date filter
        state_count["Date"] = pd.to_datetime(state_count["Date"])
        state_count = date_filter(state_count, input.date_range())
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=30))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        sns.lineplot(data=state_count, x="Date", y="Value", hue="StateName", ax=ax)
        plt.legend(ncol=3, bbox_to_anchor=(1.05, 1), loc="upper left", fontsize="small")
        plt.tight_layout()
        plt.title("Average Monthly House Sales by State")
        plt.ylabel("Average House Sales")
        return fig

    @render.data_frame
    def sale_count_data_frame():
        # Show entire US or filtered by state
        if input.us_state() == "United States":
            df = string_state_count_df
            df = date_filter(df, input.date_range())
        else:
            df = string_state_count_df[string_state_count_df["StateName"] == input.us_state()]
            
            
        # filter by date user input
        df = date_filter(df, input.date_range())
        
        return df

# Create and run the Shiny app
app = App(app_ui, server)
