from datetime import datetime
import os
import wget

def get_timespan(datetime_str:str) -> int:
    datetime_str = datetime_str.replace('T',' ').split('.')[0]
    datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    timespan_flo = datetime.timestamp(datetime_obj)
    return int(str(timespan_flo).split('.')[0])

# print(get_timespan('2022-01-07T16:01:55.000Z'))

def download_photos(username:str,file_name:str,urls:list)->list:
    
    path = os.getcwd()
    path = os.path.join(path,'photo',username)
    os.makedirs(path)
    
    counter = 0
    paths = []
    for url in urls:
        counter += 1
        save_as = os.path.join(path,file_name+'-'+str(counter)+'.png')
        wget.download(url, save_as)
        paths.append(save_as)

    return paths
    
