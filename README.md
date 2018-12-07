# EasyS3
* This module can be used to download AWS S3 files conveniently using python.

## Install
```python
pip install git+https://github.com/zhanyiduo/EasyS3
```
## Input
* aws_access_key_id: your AWS access ID
* aws_secret_access_key: your AWS secret key
* s3_bucket: the S3 bucket name.
* s3_filepath: the filepath of the desired file to be downloaded.
* dir: the local directory that you wish to save the data.


## Example 
```python
	from get_s3_data.gets3 import easys3
	import argparse

	print("Please Enter your AWS Access Key ID, AWS Secrect Access Key, S3 Bucket, and S3 filepath in the format of:\
		 '--aws_id xxx --aws_secret xxx --s3_bucket xxx --s3_filepath xxx/xxx/xxx'")
	parser = argparse.ArgumentParser(description='S3_info')
	parser.add_argument('--aws_id', type=str)
	parser.add_argument('--aws_secret', type=str)
	parser.add_argument('--s3_bucket', type=str)
	parser.add_argument('--s3_filepath', type=str)
	argv = parser.parse_args()

	AWS_ACCESS_KEY_ID = argv.aws_id
	AWS_SECRET_ACCESS_KEY = argv.aws_secret
	s3_bucket = argv.s3_bucket
	s3_filepath = argv.s3_filepath


	S3 = easys3(aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            s3_bucket=s3_bucket,
            s3_filepath=s3_filepath,
            download_list=True,
            dir='Data')
```