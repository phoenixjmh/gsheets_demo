import gspread
import pandas as pd
import dataio as IO
from employee import Employee
from google.oauth2.service_account import Credentials
from difflib import get_close_matches




# Apparently, changing the column names will destroy the program's ability to function.
# Potential Solutions
#   - Use fuzzy search get_close_matches from difflib ***THIS SHOULD WORK***
#   - Use indices



scopes = ["https://www.googleapis.com/auth/spreadsheets"]


def get_workbook():
    creds = Credentials.from_service_account_file("res/creds.json", scopes=scopes)
    client = gspread.authorize(creds)
    sheet_id = "1yCA-LKtvmyDJVi1Tnxeo-uLVUoYSwKidJgUYntsPNls"
    workbook = client.open_by_key(sheet_id)
    return workbook


def get_adjacent_cells_for(dataFrame, col_string):
    # Step 1: Find rows that contain "Mobile"
    mobile_rows = dataFrame.isin([col_string]).any(axis=1)

    # Step 2: Filter the DataFrame to only those rows
    filtered_df = dataFrame[mobile_rows]

    # Step 3: Count non-null cells in each column
    column_counts = filtered_df.count()

    # Step 4: Sum up all the counts to get the total number of cells
    return column_counts.sum()
def get_empty_locations(df):
    empty_locations = []
    for row in range(df.shape[0]):  # Iterate through rows
        for col in range(df.shape[1]):  # Iterate through columns
            if df.iat[row, col] == "" or pd.isna(
                df.iat[row, col]
            ):  # Check for empty or NaN
                empty_locations.append((row, col))  #
    return empty_locations

def get_matching_column(query,df):
    matches=get_close_matches(query,df.columns,n=1,cutoff=0.6)
    return matches[0] if matches else None


def do_data_sort():

    workbook = get_workbook()
    sheet = workbook.sheet1
    data = sheet.get_all_values()
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)
    metadata = IO.read_meta_data()
    y_total_cells = metadata["TotalCells"]
    y_filled_cells = metadata["FilledCells"]
    y_empty_cells = metadata["EmptyCells"]
    in_industries = metadata["Industries"]
   
    

    #Fuzzy searching close column matches in case columns change name or location
    ind_query_match=get_matching_column("Indu",df)
   
    if ind_query_match:
       df_ind=df[ind_query_match]
       print(f"found {df_ind.value_counts().count()} total industries")
    else:
        print("Could not find matching column for Ind! ABORT!")

    out_industries = df["Industry"].value_counts().to_dict()
    t_empty_cells = (df == "").sum().sum()

    empty_locations=get_empty_locations(df)
    t_total_cells = df.notna().sum().sum()
    t_filled_cells = t_total_cells - t_empty_cells

    IO.save_hl_sheet("hl_file.xlsx", df, empty_locations)

    delta = t_total_cells - y_total_cells
    delta = delta + y_empty_cells - t_empty_cells
    print(f"There are {t_total_cells} total cells," f"{t_empty_cells} are empty")
    print(f"Yesterday there were" f"{y_total_cells} total cells")
    print(f"There are {delta} new entries")

    out_head = {k: out_industries[k] for k in list(out_industries)[:5]}
    employees = []
    for ind in out_head:
        e = Employee(
            ind,
            0,
            [
                0,
            ],
        )
        op = get_adjacent_cells_for(df, ind)
        e.update_output(op)
        employees.append(e)

    for e in employees:
        e.print_output()

    # sums return default numpy numbers, which does not agree with our reads
    metadata["TotalCells"] = int(t_total_cells)
    metadata["FilledCells"] = int(t_filled_cells)
    metadata["EmptyCells"] = int(t_empty_cells)
    metadata["Industries"] = out_industries

    IO.write_meta_data(metadata)

    all_employee_data = []

    for e in employees:
        all_employee_data.append(e.obj_to_dict())

    print(all_employee_data)

    loaded_employees = []
    for ed in all_employee_data:
        e = Employee(**ed)
        loaded_employees.append(e)

    print(loaded_employees)

    for le in loaded_employees:
        le.print_output()


do_data_sort()
