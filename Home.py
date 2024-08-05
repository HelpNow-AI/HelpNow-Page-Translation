import streamlit as st
import pandas as pd
import json
import uuid
import os
import zipfile
import tempfile

from convert_exceltojson import split_lang_jsonfile
from convert_json_file_check import target_file_write, result_file_write, compare_file

APP_ROOT = os.getcwd()
print('APP ROOT: ',APP_ROOT)

st.set_page_config(
   page_title="HelpNow Page Translation",
)


def save_uploaded_file(upload_id, uploaded_file):
    # 파일을 서버의 지정된 경로에 저장
    status = False
    save_path = f"./uploaded_files/{upload_id}"
    if os.path.exists(save_path) == False:
        os.makedirs(save_path, exist_ok=True)

    file_path = os.path.join(save_path, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        status = True

    return file_path, status


def zip_files_in_directory(directory_path):
    # Temporary file to store the zip
    temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
    with zipfile.ZipFile(temp_zip.name, 'w') as zipf:
        for foldername, subfolders, filenames in os.walk(directory_path):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                zipf.write(file_path, os.path.relpath(file_path, directory_path))
    return temp_zip.name



def main():
    st.title('HelpNow Page Translation')


    uploaded_file = st.file_uploader("Choose a ONLY Excel file", type='xlsx')
    if uploaded_file is not None:
        upload_id = uuid.uuid4()
        file_path, status = save_uploaded_file(upload_id, uploaded_file)

        # #######################################################################################

        if status:
            st.success(f"File saved to ./uploaded_files/{upload_id}/{uploaded_file.name}")
            runpath = APP_ROOT

            ####### Step 1 ####### 
            langlist = ['EN', 'JP', 'KO']
            ascii_json = f"{runpath}/uploaded_files/{upload_id}/ascii_json_file.json"

            ## excel to pandas dataframe  
            df = pd.read_excel(file_path, usecols= ['Path', 'EN', 'JP', 'KO', 'json_CHECK'], engine='openpyxl')
            df = df[df['json_CHECK'] == 'Y']
            df_no_duplicates = df.drop_duplicates(subset=['Path']).sort_values(by='Path')

            json_data = df_no_duplicates.to_json(orient='records', indent=4)

            # Write JSON data to file (us-ascii)
            with open(ascii_json, 'w', encoding='utf-8') as json_file:
                json_file.write(json_data)

            with open(ascii_json, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # Convert the JSON data to a pandas DataFrame
            dt = pd.DataFrame(data)

            for lan in langlist : 
                _runpath = f"{runpath}/uploaded_files/{upload_id}"
                # print (f"start : {lan}")
                split_lang_jsonfile(_runpath, dt, lan)    
                print (f"outputfile : {_runpath}/{str(lan).lower()}_convert.json")
            
            st.success("STEP 1. Convert Excel to Json is Done.")



            ####### Step 2 ####### 
            ## target data frame import  ``
            _runpath = f"{runpath}/uploaded_files/{upload_id}"
            src_ascii_json = f"{_runpath}/ascii_json_file.json"
            ascii_json = f"{_runpath}/ascii_json_file_check.json"

            # Read the ASCII JSON file
            with open(src_ascii_json, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # Convert the JSON data to a pandas DataFrame
            dfasc = pd.DataFrame(data)
            fin_data = dfasc[['Path', 'EN', 'JP', 'KO']].to_json(orient='records', indent=4, force_ascii=False)

            for lan in langlist :
                target_file_write(_runpath, dfasc, lan)
                result_file_write(_runpath, lan)
                compare_file(_runpath, lan)    
            st.success("STEP 2. Json File Check is Done.")


            ## to .zip
            zip_file_path = zip_files_in_directory(_runpath)
            if zip_file_path:
                with open(zip_file_path, 'rb') as f:
                    bytes_data = f.read()
                    st.subheader("📥 Download Translation json file.")
                    st.download_button(label=f"{uploaded_file.name.replace('.xlsx','')}.zip", data=bytes_data, file_name=f"{uploaded_file.name.replace('.xlsx','')}.zip", mime='application/zip')

        else:
            st.error(f"File not saved to ./uploaded_files/{uploaded_file.name}")



if __name__ == '__main__':
 main()