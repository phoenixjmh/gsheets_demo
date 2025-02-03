import gspread
import pandas as pd
import dataio as IO
from employee import Employee
from google.oauth2.service_account import Credentials


scopes=[
    "https://www.googleapis.com/auth/spreadsheets"
]
def get_workbook():
    creds=Credentials.from_service_account_file("creds.json",scopes=scopes)
    client=gspread.authorize(creds)
    sheet_id="1yCA-LKtvmyDJVi1Tnxeo-uLVUoYSwKidJgUYntsPNls"
    workbook=client.open_by_key(sheet_id)
    return workbook

workbook=get_workbook()
sheet=workbook.sheet1

def get_adjacent_cells_for(dataFrame,col_string):
   # Step 1: Find rows that contain "Mobile"
    mobile_rows = dataFrame.isin([col_string]).any(axis=1)

    # Step 2: Filter the DataFrame to only those rows
    filtered_df = dataFrame[mobile_rows]

    # Step 3: Count non-null cells in each column
    column_counts = filtered_df.count()

    # Step 4: Sum up all the counts to get the total number of cells
    return column_counts.sum()

def do_data_sort():
    data=sheet.get_all_values()
    headers=data.pop(0)
    df=pd.DataFrame(data,columns=headers)
    metadata=IO.read_meta_data()
    y_total_cells=metadata["TotalCells"]
    y_filled_cells=metadata["FilledCells"]
    y_empty_cells=metadata["EmptyCells"]
    in_industries=metadata["Industries"]
    out_industries=df["Industry"].value_counts().to_dict()
    t_empty_cells=(df=='').sum().sum()
    

    t_total_cells=df.notna().sum().sum()
    t_filled_cells=t_total_cells-t_empty_cells


    delta=t_total_cells-y_total_cells
    delta=delta+y_empty_cells-t_empty_cells
    print(f"There are {t_total_cells} total cells,"
          f"{t_empty_cells} are empty")
    print(f"Yesterday there were" 
          f"{y_total_cells} total cells")
    print(f"There are {delta} new entries")


    out_head = {k: out_industries[k] for k in list(out_industries)[:5]}
    employees=[]
    for ind in out_head:
        e=Employee(ind)
        op=get_adjacent_cells_for(df,ind)
        e.update_output(op)
        employees.append(e)
        

    for e in employees:
        e.print_output()

    metadata["TotalCells"]=int(t_total_cells) #sums return default numpy numbers, which does not agree with our reads
    metadata["FilledCells"]=int(t_filled_cells)
    metadata["EmptyCells"]=int(t_empty_cells)
    metadata["Industries"]=out_industries
    IO.write_meta_data(metadata)




do_data_sort()


