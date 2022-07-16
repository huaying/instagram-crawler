import json
import os

path_dir = './output'
file_list = os.listdir(path_dir)

hot_data = None
data = None
for jsonfile in file_list : 
    if jsonfile[:2] == 'p1':
        with open(jsonfile, 'r') as file:
            data1 = json.load(file)
            hot_data += data1[:9]
            data += data1[9:]
        # 파일 새로 쓰기
        with open(os.path.join(path_dir,"p1_hot.json"), "a") as new_file :
            json.dump(hot_data, new_file, ensure_ascii = False, indent=4)  
        with open(os.path.join(path_dir,"p1_recent.json"), "a") as new_file :
            json.dump(data, new_file, ensure_ascii = False, indent=4)
    
    elif jsonfile[:2] == 'p2':
        with open(jsonfile, 'r') as file:
            data1 = json.load(file)
            hot_data += data1[:9]
            data += data1[9:]
        # 파일 새로 쓰기
        with open(os.path.join(path_dir,"p2_hot.json"), "a") as new_file :
            json.dump(hot_data, new_file, ensure_ascii = False, indent=4)  
        with open(os.path.join(path_dir,"p2_recent.json"), "a") as new_file :
            json.dump(data, new_file, ensure_ascii = False, indent=4)

    elif jsonfile[:2] == 'p3':
        with open(jsonfile, 'r') as file:
            data1 = json.load(file)
            hot_data += data1[:9]
            data += data1[9:]
        # 파일 새로 쓰기
        with open(os.path.join(path_dir,"p3_hot.json"), "a") as new_file :
            json.dump(hot_data, new_file, ensure_ascii = False, indent=4)  
        with open(os.path.join(path_dir,"p3_recent.json"), "a") as new_file :
            json.dump(data, new_file, ensure_ascii = False, indent=4)

    elif jsonfile[:2] == 'p4':
        with open(jsonfile, 'r') as file:
            data1 = json.load(file)
            hot_data += data1[:9]
            data += data1[9:]
        # 파일 새로 쓰기
        with open(os.path.join(path_dir,"p4_hot.json"), "a") as new_file :
            json.dump(hot_data, new_file, ensure_ascii = False, indent=4)  
        with open(os.path.join(path_dir,"p4_recent.json"), "a") as new_file :
            json.dump(data, new_file, ensure_ascii = False, indent=4)

    elif jsonfile[:2] == 'p5':
        with open(jsonfile, 'r') as file:
            data1 = json.load(file)
            hot_data += data1[:9]
            data += data1[9:]
        # 파일 새로 쓰기
        with open(os.path.join(path_dir,"p5_hot.json"), "a") as new_file :
            json.dump(hot_data, new_file, ensure_ascii = False, indent=4)  
        with open(os.path.join(path_dir,"p5_recent.json"), "a") as new_file :
            json.dump(data, new_file, ensure_ascii = False, indent=4)

    elif jsonfile[:2] == 'p6':
        with open(jsonfile, 'r') as file:
            data1 = json.load(file)
            hot_data += data1[:9]
            data += data1[9:]
        # 파일 새로 쓰기
        with open(os.path.join(path_dir,"p6_hot.json"), "a") as new_file :
            json.dump(hot_data, new_file, ensure_ascii = False, indent=4)  
        with open(os.path.join(path_dir,"p6_recent.json"), "a") as new_file :
            json.dump(data, new_file, ensure_ascii = False, indent=4)
