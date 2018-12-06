##Example/example.py
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


S3 = easys3(aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY,s3_bucket=s3_bucket,s3_filepath=s3_filepath)