import pandas as pd
import numpy as np
import json
import jsondiff
import os

# rundir = os.getcwd()
# print (rundir)
# runpath = os.path.join(rundir, '20240805')

# ## target data frame import  
# src_ascii_json = f"{runpath}/ascii_json_file.json"
# ascii_json = f"{runpath}/ascii_json_file_check.json"
# langlist = ['EN', 'JP', 'KO']

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '.')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '.')
                i += 1
        else:
            out[name[:-1]] = x
    flatten(y)
    
    return out

# 비교대상 파일 작성 
def target_file_write (runpath, dfasc, lan) :
    # 비교 대상 DataFrame  생성 
    fin_data = dfasc[['Path', lan]].to_json(orient='records', indent=4, force_ascii=False)

    _src_asc_json = f"{runpath}/target_{str(lan).lower()}_check_file.json"
    # 원본 비교대상 파일 작성 
    with open(_src_asc_json, 'w', encoding='utf-8') as file:
        file.write(fin_data)  

def result_file_write (runpath, lan) :
    ## Result json file read 
    inputfile = f"{runpath}/{str(lan).lower()}_convert.json"
    with open(inputfile, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    # Flatten the JSON
    flattened_data = flatten_json(json_data)

    srcList = []
    for _key, _val in flattened_data.items() :
        _cbsrcList = [_key, _val]
        srcList.append(_cbsrcList)

    _srcdata = pd.DataFrame(srcList, columns=['Path', lan])

    json_data = _srcdata.to_json(orient='records', indent=4)
    # print (f"----------------------------------")
    # print (f"{type(json_data)}")
    # print (f"----------------------------------")

    # Write JSON data to file (us-ascii)
    outputfile = f"{runpath}/_tmp_{str(lan).lower()}_convert.json"
    with open(outputfile, 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)

    # Read JSON data to file (us-ascii)
    with open(outputfile, 'r', encoding='utf-8') as ascfile:
        data = json.load(ascfile)

    # Write JSON data to file (utf-8)
    finfile =f"{runpath}/fin_{str(lan).lower()}_convert.json"
    with open(finfile, "w", encoding='utf-8') as fin_file:
        # Use json.dump() to write the dictionary to the file
        json.dump(data, fin_file, ensure_ascii=False, indent=4)

    if os.path.isfile(outputfile):
        # If the file exists, delete it
        os.remove(outputfile)
        # print("File removed successfully")

def compare_file (runpath, lan) :
    print (f"{lan}")
    srcfile =f"{runpath}/fin_{str(lan).lower()}_convert.json"
    tarfile = f"{runpath}/target_{str(lan).lower()}_check_file.json"

    with open(srcfile, 'r', encoding='utf-8') as srcdata:
        findata = json.load(srcdata)

    with open(tarfile, 'r', encoding='utf-8') as tgdata:
        orgdata = json.load(tgdata)

    if len(findata) == len(orgdata):
        # Compare dictionaries
        if findata == orgdata:
            print(f"The JSON objects are equal. : {runpath}/{str(lan).lower()}_convert.json")
            if os.path.isfile(srcfile):
                # If the file exists, delete it
                os.remove(srcfile)

            if os.path.isfile(tarfile):
                # If the file exists, delete it
                os.remove(tarfile)

        else:
            print(f"The JSON objects are not equal. : {runpath}/{str(lan).lower()}_convert.json")
            for _num in range(len(orgdata)) :
                _srcrow =  findata[_num]
                _orgrow =  orgdata[_num]
                diff = jsondiff.diff(_srcrow, _orgrow, syntax='symmetric')

                if diff :
                    print (f"componet    : {_srcrow}")
                    print (f"diff result : {diff}")
    else :
        print (f"{runpath}/{str(lan).lower()}_convert.json file row count wrong ! ")
        dataframe_diff (lan)

def dataframe_diff (runpath, lan) :
    # print (f"dataframe_diff run !! lang > {lan}")
    srcfile =f"{runpath}/fin_{str(lan).lower()}_convert.json"
    tarfile = f"{runpath}/target_{str(lan).lower()}_check_file.json"

    with open(srcfile, 'r', encoding='utf-8') as srcdata:
        findata = json.load(srcdata)

    with open(tarfile, 'r', encoding='utf-8') as tgdata:
        orgdata = json.load(tgdata)

    frdata = pd.DataFrame(findata)
    todata = pd.DataFrame(orgdata)

    combined = pd.concat([frdata, todata], ignore_index=True)
    dp = combined.drop_duplicates(subset=['Path'], keep=False).sort_values(by='Path')
    # print (f"differant row-------------------------")
    # print (f"{dp.values[0]}")
    print (f"Path NAME------------------------")
    print (f"{dp.values[0][0]}")
    print (f"--------------------------------------")

# ### MAIN 
# # Read the ASCII JSON file
# with open(src_ascii_json, 'r', encoding='utf-8') as file:
#     data = json.load(file)

# # Convert the JSON data to a pandas DataFrame
# dfasc = pd.DataFrame(data)
# fin_data = dfasc[['Path', 'EN', 'JP', 'KO']].to_json(orient='records', indent=4, force_ascii=False)
# # print (f"----------------------------------")
# # print (f"{fin_data}")
# # print (f"----------------------------------")

# for lan in langlist :
#     target_file_write (lan)
#     result_file_write (lan)
#     compare_file (lan)    

