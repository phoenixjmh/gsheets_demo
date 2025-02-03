import json

def write_data(out_data, filename):
    with open(filename, 'w') as file:
        json.dump(out_data, file,indent=4)

def write_meta_data(out_data):
    write_data(out_data,"metadata.json")


#this will be much faster than performing operations over the API access
def sheet_to_json(sheet):
    json_rows=sheet.get_all_records()
    write_data(json_rows, "sheet-raw.json")

def read_sheet_data():
    return read_data("sheet-raw.json")

def read_meta_data():
    return read_data("metadata.json")

def read_data(filename):
    with open(filename,'r') as file:
        data=json.load(file)
    return data