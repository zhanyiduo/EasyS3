# Get_S3_data
* This module can be used to download AWS S3 files conveniently using python.

## Install
```python
pip install git+https://github.platforms.engineering/YZHAN6/Get_S3_data
```
## Input
* aws_access_key_id: your AWS access ID
* aws_secret_access_key: your AWS secret key
* s3_bucket: the S3 bucket name.
* s3_filepath: the filepath of the desired file to be downloaded.
* local_dir: the local directory that you wish to save the data.


## Example
```python
	from get_s3_data.gets3 import gets3

    s3 = gets3(aws_access_key_id=AWS_ACCESS_KEY_ID,
	aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    s3.list_buckets()#list of all the buckets

    s3.list_objects(Bucket='breeding-perm-space', prefix='shared/dropbox/')#list of all objects in the folder

    s3.download(Bucket='breeding-perm-space', s3_filepath='aa/bb/')#download a specific file

    s3.download(Bucket='breeding-perm-space', s3_filepath='shared/dropbox/')#if the file path is a directory, will download all files in the directory
```
