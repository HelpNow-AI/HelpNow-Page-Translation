import pandas as pd
import numpy as np
import json
import os

# rundir = os.getcwd()
# print (rundir)
# runpath = os.path.join(rundir, '20240805')

# langlist = ['EN', 'JP', 'KO']
# ascii_json = f"{runpath}/ascii_json_file.json"
# path_excel = f"{runpath}/20240805_json.xlsx"

def list_to_nested_dict(runpath, lst):
    result = {}
    for item in lst:
        keys = item[0].split('.')
        value = item[1]
        temp = result
        for key in keys[:-1]:
            temp = temp.setdefault(key, {})
        temp[keys[-1]] = value

    return result

def split_lang_jsonfile (runpath, dt, lag) :

    outputfile = f"{runpath}/{str(lag).lower()}_convert.json"

    _result_dic = {}
    fin_data = dt[['Path', lag]]
    # print (f"----------------------------------")
    # print (f"{fin_data}")
    # print (f"----------------------------------")

    _col_lst = fin_data.values.tolist()
    _result_dic = list_to_nested_dict(runpath, _col_lst)
    # print (f"$$_result_dic : {_result_dic}")

    with open(outputfile, "w", encoding='utf-8') as file:
        # Use json.dump() to write the dictionary to the file
        json.dump(_result_dic, file, ensure_ascii=False, indent=4)

    return outputfile

# ## excel to pandas dataframe  
# df = pd.read_excel(path_excel, usecols= ['Path', 'EN', 'JP', 'KO', 'json_CHECK'], engine='openpyxl')
# df = df[df['json_CHECK'] == 'Y']
# df_no_duplicates = df.drop_duplicates(subset=['Path']).sort_values(by='Path')

# json_data = df_no_duplicates.to_json(orient='records', indent=4)

# # Write JSON data to file (us-ascii)
# with open(ascii_json, 'w', encoding='utf-8') as json_file:
#     json_file.write(json_data)

# with open(ascii_json, 'r', encoding='utf-8') as file:
#     data = json.load(file)

# # Convert the JSON data to a pandas DataFrame
# dt = pd.DataFrame(data)

# for lan in langlist : 
#     # print (f"start : {lan}")
#     split_lang_jsonfile (lan)    
#     print (f"outputfile : {runpath}/{str(lan).lower()}_convert.json")
