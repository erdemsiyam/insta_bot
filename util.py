from datetime import datetime
import os
import wget
import logging

def get_timespan(datetime_str:str) -> int:
    datetime_str = datetime_str.replace('T',' ').split('.')[0]
    datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    timespan_flo = datetime.timestamp(datetime_obj)
    return int(str(timespan_flo).split('.')[0])

def get_timespan_now() -> int:
    time = datetime.now()
    timespan_flo = datetime.timestamp(time)
    return int(str(timespan_flo).split('.')[0])
# print(get_timespan('2022-01-07T16:01:55.000Z'))

def download_photos(username:str,file_name:str,urls:list)->list:
    
    # Klasör Dizini Oluşturulur : photo/username/
    path = os.getcwd()
    path = os.path.join(path,'photo',username)
    os.makedirs(path, exist_ok=True)
    
    # Verilen Foto Urlleri İndirilir
    counter = 0
    paths = []
    for url in urls:
        counter += 1
        save_as = os.path.join(path,file_name+'-'+str(counter)+'.png')
        if url is None:
            logging.info('HATA!!! foto url None : '+save_as)
        else:
            wget.download(url, save_as)
            paths.append(save_as)
            logging.info(str(counter)+'. Foto indirildi : '+save_as)

    return paths

def delete_file(file_path:str):
    os.remove(file_path)
