from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import boto3
import os, sys


class gets3(object):
    '''Provides a simpler wrapper for boto3 to access s3'''

    def __init__(self, aws_access_key_id=None,
                 aws_secret_access_key=None):

        assert aws_access_key_id, 'AWS ID empty!'
        assert aws_secret_access_key, 'AWS secret empty!'

        self.conn = boto3.resource('s3',
                                   aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key)
        self.client = boto3.client('s3',
                                   aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key)

    def list_buckets(self):
        '''lists bucket names visiable via provided credentials'''
        buckets = self.client.list_buckets()
        print([i['Name'] for i in buckets['Buckets']])
        return [i['Name'] for i in buckets['Buckets']]

    def list_objects(self, Bucket=None, prefix=None, full_key=False):
        '''lists top level object names given bucket and prefix
        When prefix is None, it will list first level objects in
        the bucket but takes longer time.

        Args:
            prefix: in the format of 'path1/path2/'
            full_key: showing the full key with prefix
        '''
        assert Bucket, 'Invalid Bucket information'
        B = self.conn.Bucket(Bucket)
        if not prefix:
            result = B.meta.client.list_objects(Bucket=B.name, Delimiter='/')
            dir_list = [d.get('Prefix') for d in result.get('CommonPrefixes')]
            obj_list = [o.get('Key') for o in result.get('Contents')]
        else:
            result = B.meta.client.list_objects(Bucket=B.name,
                                                Prefix=prefix,
                                                Delimiter='/')
            # check if a "directory" exists
            if not result.get('CommonPrefixes'):
                dir_list = []
            else:
                if full_key:
                    dir_list = [d.get('Prefix')
                                for d in result.get('CommonPrefixes')]
                else:
                    dir_list = [d.get('Prefix').split(prefix)[1]
                                for d in result.get('CommonPrefixes')]
            # check if a "non-directory" object exists
            if not result.get('Contents'):
                obj_list = []
            else:
                if full_key:
                    obj_list = [o.get('Key')
                                for o in result.get('Contents')]
                else:
                    obj_list = [o.get('Key').split(prefix)[1]
                                for o in result.get('Contents')]
        print(dir_list + obj_list)
        return dir_list + obj_list

    def download(self, Bucket=None, s3_filepath=None, local_dir='Data', download_list='True'):
        if s3_filepath.endswith('/'):
            self.s3_prefix = s3_filepath
            s3_file_list = self.list_objects(Bucket=Bucket, prefix=self.s3_prefix)
            print('List of files in the folder:')
            print(s3_file_list)
            if download_list:
                for file in s3_file_list:  # downloading all the files in the diretory
                    if (file) and (not file.endswith('/')):
                        self.s3_filepath = self.s3_prefix + file
                        self.filename = file
                        self.download_file(Bucket=Bucket, s3_filepath=self.s3_filepath, local_dir=local_dir)
                    else:
                        continue
        else:
            self.s3_filepath, self.s3_prefix, self.filename = self.clean_s3_path(s3_filepath)
            self.download_file(Bucket=Bucket, s3_filepath=self.s3_filepath, local_dir=local_dir)

    def download_file(self, Bucket=None, s3_filepath=None, local_dir='Data'):
        '''download object to destination
        Args:
            local_directory: local path
        '''
        filename = s3_filepath.split('/')[-1]
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        FILE_dir = os.path.join(local_dir, filename)
        print('Start to download from ' + s3_filepath)
        self.client.download_file(Bucket=Bucket,
                                  Key=s3_filepath,
                                  Filename=FILE_dir)
        print('Download Complete. File is saved at: ' + FILE_dir)

    def upload_file(self, Bucket=None, prefix=None, local_dir='Data', filename='None'):
        file = os.path.join(local_dir, filename)
        self.client.upload_file(file, Bucket, prefix + filename, extra_args={'ServerSideEncryption': "AES256"})
        print('Upload file to ' + prefix + filename)

    @staticmethod
    def clean_s3_path(s3_filepath):
        '''
            From the provided filepath to do:
            1. clean the path
            2. extract the prefix
            3. extract the filename
        '''
        assert not s3_filepath.endswith('/'), 'Incorrect path format!'
        s3_filepath = s3_filepath.replace(r'\\', '/')  # replace backslash to forward slash
        if s3_filepath.startswith('/'):
            s3_filepath = s3_filepath[1:]
        filename = s3_filepath.split('/')[-1]
        s3_prefix = os.path.split(s3_filepath)[0]
        s3_prefix = s3_prefix + '/'
        return s3_filepath, s3_prefix, filename 