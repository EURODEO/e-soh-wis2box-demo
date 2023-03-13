import os
import time

from minio import Minio

minio_path = '/nld/knmi_esoh_demo/data/core/weather/surface-based-observations/synop/'

endpoint = 'localhost:9000'
WIS2BOX_STORAGE_USERNAME = 'minio'
WIS2BOX_STORAGE_PASSWORD = 'minio123'

client = Minio(
    endpoint=endpoint,
    access_key=WIS2BOX_STORAGE_USERNAME,
    secret_key=WIS2BOX_STORAGE_PASSWORD,
    secure=False)


directory = '/Users/phaf/src/rodeo/wis2box-sample-input'

# iterate over files in
# that directory
for filename in sorted(os.listdir(directory)):
    filepath = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(filepath) and filename.endswith('.bufr'):
        print(f"Uploading {filename}")
        client.fput_object('wis2box-incoming', minio_path+filename, filepath)
        time.sleep(10)


# filename = filepath.split('/')[-1]
# client.fput_object('wis2box-incoming', minio_path+filename, filepath)
