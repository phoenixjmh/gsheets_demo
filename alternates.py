
def get_total_cell_delta(last_count,new_count):
   return new_count-last_count 


def get_cell_count(data):
    filled=0
    empty=0
    for record in data:
        for key,value in record.items():
            if isinstance(value,str) and value.strip():
                filled+=1
            else:
                empty+=1

    return (filled,empty)

def method_one():
    IO.sheet_to_json(sheet)
    curr_sheet_data_json=IO.read_sheet_data()
    metadata=IO.read_meta_data()
    (filled,empty)=get_cell_count(curr_sheet_data_json)
    cells_yesterday_count=metadata["TotalCells"]
    today_cells_count=filled
    delta=today_cells_count-cells_yesterday_count
    print(f"There are {filled+empty} total cells, of which {today_cells_count}"
          f"are filled\n Yesterday there were{cells_yesterday_count}\n {delta} total cells added")
def method_two():
    in_data=IO.read_data()
    cell=sheet.find("SaaS")
    #Tally a column
    industry_col_idx=sheet.find("Industry").col
    get_total_cell_delta(in_data["TotalCells"])
    in_data["TotalCells"]=len(sheet.get_all_cells())
    print(in_data)
    IO.write_data(in_data)
    industry_values = sheet.col_values(industry_col_idx)
    industry_data={
        "_name":0
    }

    for i in industry_values:
        industry_data[i]=industry_data.get(i,0)+1

#method_one()