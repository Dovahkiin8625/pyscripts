import os
import time
import uuid
import sys
import requests
from minio import Minio
from minio.error import InvalidResponseError
import warnings

ip = "47.105.133.117"
port = "9001"
accessKey = "admin"
secretKey = "liu8625.F"
isSSl = False
bucket = "typora"

warnings.filterwarnings('ignore')
images = sys.argv[1:]
minioClient = Minio(ip+":"+port,
                    access_key=accessKey, secret_key=secretKey, secure=isSSl)
result = "Upload Success:\n"
date = time.strftime("%Y%m%d%H%M%S", time.localtime())

for image in images:
    file_type = os.path.splitext(image)[-1]
    new_file_name = date + file_type
    if image.endswith(".png") or image.endswith(".jpg") or image.endswith(".gif"):
         content_type ="image/"+file_type.replace(".", "");
    else:
        content_type ="image/jpg"
        continue
    try:
        minioClient.fput_object(bucket_name=bucket, object_name= new_file_name, file_path=image,content_type=content_type)
        if image.endswith("temp"):
            os.remove(image)
        result = result +"http://"+ip+":"+port+ "/"+bucket+"/"  + new_file_name + "\n"
    except InvalidResponseError as err:
        result = result + "error:" + err.message + "\n"
print(result)
