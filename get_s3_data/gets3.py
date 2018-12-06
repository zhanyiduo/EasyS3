##get_s3_data/gets3.py
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import boto3
import io
import pandas as pd
import os, sys

class easys3(object):
    '''Provides a simpler wrapper for boto3 to access s3'''
    def __init__(self, aws_access_key_id=None, 
                    aws_secret_access_key=None,
                    s3_bucket=None,
                    s3_filepath=None,
					dir = 'Data'):

        assert not aws_access_key_id, 'AWS ID empty!'
        assert not aws_secret_access_key, 'AWS secret empty!'
        assert not s3_bucket, 'Bucket empty!'
        assert not s3_filepath, 'Filepath empty!'

        self.conn = boto3.resource('s3',
                                   aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key)
        self.client = boto3.client('s3',
                                   aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key)

        self.bucket = s3_bucket
        if s3_filepath.endswith('/'):
            self.s3_prefix = s3_filepath
            s3_file_list = self.list_objects(Bucket =self.bucket, prefix=self.s3_prefix)
            print('List of files in the folder:')
            print(s3_file_list)
        else:
            self.s3_filepath, self.s3_prefix, self.filename = self.clean_s3_path(s3_filepath)
            self.download(dir)

    def list_buckets(self):
        '''lists bucket names visiable via provided credentials'''
        buckets = self.client.list_buckets()
        return [i['Name'] for i in buckets['Buckets']]

    def list_objects(self, Bucket, prefix=None, full_key=False):
        '''lists top level object names given bucket and prefix
        When prefix is None, it will list first level objects in
        the bucket but takes longer time.
        
        Args:
            prefix: in the format of 'path1/path2/'
            full_key: showing the full key with prefix
        '''
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

        return dir_list + obj_list

    def download(self,local_dir='Data'):
        '''download object to destination
        Args:
            local_directory: local path
        '''
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        FILE_dir = os.path.join(local_dir,self.filename)
        print('Start to download from ' + self.s3_filepath)
        self.client.download_file(Bucket = self.bucket,
                                  Key = self.s3_filepath,
                                  Filename = FILE_dir)
        print('Download Complete. File is saved at: ' + FILE_dir)

    @staticmethod
    def clean_s3_path(s3_filepath):
        '''
            From the provided filepath to do:
            1. clean the path
            2. extract the prefix
            3. extract the filename
        '''
        assert not s3_filepath.endswith('/'), 'Incorrect path format!'
        s3_filepath = s3_filepath.replace(r'\\','/')#replace backslash to forward slash
        if s3_filepath.startswith('/'):
            s3_filepath = s3_filepath[1:]
        filename = s3_filepath.split('/')[-1]
        s3_prefix = os.path.split(s3_filepath)[0]
        s3_prefix = s3_prefix+'/'
        return s3_filepath, s3_prefix, filename 
