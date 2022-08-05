
import sys, os, botocore, boto3, socket

def upload (profile,endpoint_url,bucket_name,orig_file_name,Tgt_file_name):
	try:
		print('Started Uploading file [' + Tgt_file_name + '] for the Bucket:' + '(' + str(bucket_name) + ')')
		session = boto3.session.Session(profile_name=profile)
		s3 = session.resource('s3',
		region_name='us-east-1',
		endpoint_url=endpoint_url,
		config=boto3.session.Config(signature_version='s3v4'))
		s3.Bucket(bucket_name).upload_file(orig_file_name,Tgt_file_name,ExtraArgs={'ServerSideEncryption':'aws:kms','SSEKMSKeyId':'alias/S3/Dev'})
		print('File Uploaded Successfully:' + str(Tgt_file_name) + ' in bucket [' + bucket_name +']')
	except botocore.exceptions.ClientError as e:
		print(e.response)


try:
	total_arg = len(sys.argv) -1
	if total_arg >= 4 and total_arg <=6:
		profile = sys.argv[1]
		elb_host = sys.argv[2]
		bucket_name = sys.argv[3]
		endpoint_url = 'http://' + socket.gethostbyname(elb_host)
		orig_file_name = sys.argv[4]
		Tgt_file_name = sys.argv[5]
		upload(profile,endpoint_url,bucket_name,orig_file_name,Tgt_file_name)
	else:
		print("Invalid Arguments passed")
		sys.exit(0)
except botocore.exceptions.ClientError as e:
    print(e.response)

