import pandas as pd

string_sale_price_df = pd.read_csv("./Metro_invt_fs_uc_sfrcondo_sm_month.csv")

def current_average(df):
    if input.us_state() == "United States":
        last_column = df.columns[-1]
        return df[last_column].mean()
    else:
        filter_state = df[df["StateName"] == input.us_state()]
        last_column = filter_state.columns[-1]
        return filter_state[last_column].mean()
    
def change_average(df):
    if True:
        last_element = df.iloc[-1, -1]
        penultimate_element = df.loc[-2, -1]
        
        return str((last_element - penultimate_element) / penultimate_element)+ "%"
    else:
        filter_state = df[df["StateName"] == input.us_state()]
        last_element = filter_state.iloc[-1, -1]
        penultimate_element = filter_state.loc[-2, -1]
        
        return str((last_element - penultimate_element) / penultimate_element)+ "%"
    
print(change_average(string_sale_price_df))