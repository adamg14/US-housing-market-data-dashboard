from data_visualisation import sale_price_data, house_price_data, sale_count_data, date_filter, string_to_date
from shiny import App, render, ui
from US_STATES import US_STATES
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from faicons import icon_svg

# Read CSVs for display in the data frames
string_sale_price_df = pd.read_csv("./Metro_invt_fs_uc_sfrcondo_sm_month.csv")
string_house_price_df = pd.read_csv("./Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv")
string_state_count_df = pd.read_csv("./Metro_sales_count_now_uc_sfrcondo_month.csv")

# Define the user interface
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_select(
            id="us_state", 
            label="Filter By State", 
                choices=US_STATES,
                selected="United States"  # Optional: set default selection
            ),
        ui.input_slider(
            id="date_range", 
            label="Filter By Date Range",
            min=string_to_date("2000-01-31"),
            max=string_to_date("2024-12-31"),
            value=[string_to_date("2000-01-01"), string_to_date("2024-12-31")],
            step=30  # Optional: define step size (in days)
        ),
    ),
    
    ui.page_fluid(
        ui.h1("United States of America Housing Market Analysis", style="text-align: center;"),
    
    ui.h2("List House Price Data by State (Monthly Price)", style="text-align: center;"),
    
    ui.navset_card_tab(
        ui.nav_panel("Graph",
                    ui.output_plot("list_price"),
                    icon=icon_svg("chart-line"),
                    ),
        
        ui.nav_panel("Table",
                    ui.output_data_frame("table"),
                    icon=icon_svg("table")
                    ),
        title="Mean Rent Price"
    ),
    
    ui.h2("House Price Data by State", style="text-align: center;"),
    
    ui.navset_card_tab(
        ui.nav_panel("Graph",
                     ui.output_plot("house_price"),
                     icon=icon_svg("chart-line"),
                     ),
        
        ui.nav_panel("Table",
                     ui.output_data_frame("house_price_data_frame"),
                     icon=icon_svg("table")
                     ),
        title="Mean House Price"
    ),   
    
    ui.h2("House Sales Data by State", style="text-align: center;"),
    
    ui.navset_card_tab(
        ui.nav_panel("Graph",
                     ui.output_plot("sale_count"),
                     icon=icon_svg("chart-line"),
                     ),
        
        ui.nav_panel("Table",
                     ui.output_data_frame("sale_count_data_frame"),
                     icon=icon_svg("table")
                     ),
        title="Meane Sale Count"
    ),
    
    ui.layout_column_wrap(
        ui.value_box(
                "This month's average rent",
                ui.output_text("current_rent"),
                ui.output_text("rent_percent_change"),
                showcase=icon_svg("dollar-sign"),
                showcase_layout="bottom",
                theme="text-green"
            ),
        
        ui.value_box(
            "This month's average house value",
            ui.output_text("current_value"),
            ui.output_text("house_value_percent_change"),
            showcase=icon_svg("house"),
            showcase_layout="bottom",
            theme="text-green"
        ),
        
        ui.value_box(
            "Average amount of houses listed (per state)",
            ui.output_text("current_count"),  
            ui.output_text("sale_count_percent_change"),
            showcase=icon_svg("coins"),
            theme="text-green"
        ),
    )
    )
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
        else:
            df = string_state_count_df[string_state_count_df["StateName"] == input.us_state()]
        
        return df
    
    @render.text
    def current_rent():
        if input.us_state() == "United States":
            last_column = string_sale_price_df.columns[-1]
            return "$" + str(string_sale_price_df[last_column].mean())
        else:
            filter_state = string_sale_price_df[string_sale_price_df["StateName"] == input.us_state()]
            last_column = filter_state.columns[-1]
            return "$" + str(filter_state[last_column].mean().round(2))
        
    @render.text
    def current_value():
        if input.us_state() == "United States":
            last_column = string_house_price_df.columns[-1]
            return "$" + str(string_house_price_df[last_column].mean())
        else:
            filter_state = string_house_price_df[string_house_price_df["StateName"] == input.us_state()]
            last_column = filter_state.columns[-1]
            return "$" + str(filter_state[last_column].mean().round(2))
    
    @render.text
    def current_count():
        if input.us_state() == "United States":
            last_column = string_state_count_df.columns[-1]
            return "$" + str(string_state_count_df[last_column].mean())
        else:
            filter_state = string_state_count_df[string_state_count_df["StateName"] == input.us_state()]
            last_column = filter_state.columns[-1]
            return f"{filter_state[last_column].mean().round(2)}"
        
    @render.text
    def rent_percent_change():
        if input.us_state() == "United States":
            last_element = string_sale_price_df.iloc[-1, -1]
            penultimate_element = string_sale_price_df.iloc[-2, -1]
            print(last_element, penultimate_element)
            return str(((last_element - penultimate_element) / penultimate_element).round(3))+ "%"
        else:
            filter_state = string_state_count_df[string_sale_price_df["StateName"] == input.us_state()]
            last_element = filter_state.iloc[-1, -1]
            penultimate_element = filter_state.iloc[-1, -2]
            
            return "Percent change in the last month: " + str(((last_element - penultimate_element) / penultimate_element).round(3))+ "%"
        
    
    @render.text
    def house_value_percent_change():
        if input.us_state() == "United States":
            last_element = string_house_price_df.iloc[-1, -1]
            penultimate_element = string_house_price_df.iloc[-2, -1]
            print(last_element, penultimate_element)
            return " Percent change in the last month: " + str(((last_element - penultimate_element) / penultimate_element).round(3))+ "%"
        else:
            filter_state = string_house_price_df[string_house_price_df["StateName"] == input.us_state()]
            last_element = filter_state.iloc[-1, -1]
            penultimate_element = filter_state.iloc[-1, -2]
            
            return "Percent change in the last month: " + str(((last_element - penultimate_element) / penultimate_element).round(3))+ "%"
    
    
    @render.text
    def sale_count_percent_change():
        if input.us_state() == "United States":
            last_element = string_state_count_df.iloc[-1, -1]
            penultimate_element = string_state_count_df.iloc[-2, -1]
            print(last_element, penultimate_element)
            return str(((last_element - penultimate_element) / penultimate_element).round(3))+ "%"
        else:
            last_element = string_state_count_df.iloc[-1, -1]
            penultimate_element = string_state_count_df.iloc[-2, -1]
            print(last_element, penultimate_element)
            return "Percent change in the last month: " + str(((last_element - penultimate_element) / penultimate_element).round(3))+ "%"
        
        
# Create and run the Shiny app
app = App(app_ui, server)
