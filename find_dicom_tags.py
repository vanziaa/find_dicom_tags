import tempfile

import pydicom
from pydicom.data import get_testdata_files
import linecache
import pandas as pd
import numpy as np
import os


def get_file(path):
    files = []
    if not os.path.exists(path):
        return -1
    for filepath, dirs, names in os.walk(path):
        for filename in names:
                files.append(os.path.join(filepath, filename))
    return files


def get_folders(path):
    folders = []
    if not os.path.exists(path):
        return -1
    for filepath, dirs, names in os.walk(path):
        for name in names:
            if name.endswith('dcm'):
                #print(filepath)
                folder=os.path.join(filepath,name)
                folders.append(folder)
                #print(folder);
            else:
                portion = os.path.splitext(name);
                newname = portion[0] + '.dcm';
                os.rename(os.path.join(filepath,name),os.path.join(filepath, newname))
                folder = os.path.join(filepath,newname);
                folders.append(folder);
                #print("renamed:",folder);            
    return folders

def get_paths(path):
    paths = []
    if not os.path.exists(path):
        return -1
    for filepath, dirs, names in os.walk(path):
        for name in names:
            if name.endswith('dcm'):
                #print(filepath)
                path=filepath
                paths.append(path)
                #print(folder);
    return paths

def get_metadata(folders):
    df=pd.DataFrame(columns=('img_dir','PatientName','AcquisitionTime',
                             'Manufacturer','Manufacturer2','SliceThickness','SeriesInstanceUID','Rows','Columns','KVP','current','SeriesDescription'
                             ));
    df_error=pd.DataFrame(columns=('error_folder','error_name'));
    for folder in folders:
        #print(folder);
        img_dir = folder;
        dataset = pydicom.dcmread(img_dir);
        print(img_dir,dataset.PatientName);
        PatientName = dataset.PatientName;
        StudyInstanceUID = dataset.StudyInstanceUID;
        PatientBirthDate = dataset.PatientBirthDate;
        SeriesInstanceUID = dataset.SeriesInstanceUID;
        SeriesDescription = dataset.SeriesDescription;
        print(PatientName,PatientBirthDate,SeriesDescription);
        row={'img_dir':img_dir,
		'PatientName':dataset.PatientName,
        #'AcquisitionTime':dataset.AcquisitionTime,
        #'Manufacturer':dataset.Manufacturer,
        #'Manufacturer2':dataset.ManufacturerModelName,
        #'SliceThickness':dataset.SliceThickness,
        'SeriesInstanceUID':dataset.SeriesInstanceUID,
        #'Rows':dataset.Rows,
        #'Columns':dataset.Columns,
        #'KVP':dataset.KVP,
        #'current':dataset.XRayTubeCurrent,
        'SeriesDescription':dataset.SeriesDescription
        };
        df = df.append(row,ignore_index=True);
    return df
#dicom folder
folders = get_folders(r'E:\example');
df = get_metadata(folders);
paths = get_paths(r'E:\example')


print(df.head())
    
#以患者studyID为索引删掉重复项，一个病人有多个序列改成序列号

nonerepeat_df = df.drop_duplicates(subset=['SeriesInstanceUID'], keep='first')
#结果表格的输出路径
# output path
writer = pd.ExcelWriter(r'E:\example\naninani.xlsx')
nonerepeat_df.to_excel(writer)
writer.save()

