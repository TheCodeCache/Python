# Example – 1 (Customizing Python Scripts)

### 1. Original upload python script (copy from Local to S3) –  
`up_aws_s3.py` – 
```python

import sys, os, botocore, boto3, socket

def upload (profile,endpoint_url,bucket_name,orig_file_name,Tgt_file_name):
    try:
        print('Started Uploading file [' + Tgt_file_name + '] for the Bucket:' + '(' + str(bucket_name) + ')')
        session = boto3.session.Session(profile_name=profile)
        s3 = session.resource('s3',
        region_name='us-east-1',
        endpoint_url=endpoint_url,
        config=boto3.session.Config(signature_version='s3v4'))
        s3.Bucket(bucket_name).upload_file(orig_file_name,Tgt_file_name,ExtraArgs={'ServerSideEncryption':'aws:kms','SSEKMSKeyId':'alias/S3/MarshDev-MBDL'})
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

```

### 2. Original download python script (copy from S3 to Local) –  
`down_aws_s3.py` – 
```python


import sys, os, botocore, boto3, socket

def download(profile,endpoint_url,bucket_name,orig_file_name,Tgt_file_name):
    try:
        print('Started downloading file [' + Tgt_file_name + '] for the Bucket:' + '(' + str(bucket_name) + ')')
        session = boto3.session.Session(profile_name=profile)
        s3 = session.resource('s3',region_name='us-east-1',endpoint_url=endpoint_url,config=boto3.session.Config(signature_version='s3v4'))
        s3.Bucket(bucket_name).download_file(Tgt_file_name,orig_file_name)

        print('File download Successfully:' + str(Tgt_file_name) + ' in bucket [' + bucket_name +']')

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
        download(profile,endpoint_url,bucket_name,orig_file_name,Tgt_file_name)
    else:
        print("Invalid Arguments passed")
        sys.exit(0)
except botocore.exceptions.ClientError as e:
    print(e.response)

```

To invoke the above script, we had to use below commands –  

```
python down_aws_s3.py <full_s3_path> <full local path>
python up_aws_s3.py <full local path> <full_s3_path>
```

# Customized Scripts – 

**it is built on top of above original scripts**  

```python

'''
Use this for debug level logging:
boto3.set_stream_logger(name='botocore', level="DEBUG")
python aws_s3.py up artifacts full_data_refresh.sh spark/data_spark/full_data_refresh.sh
python aws_s3.py dn artifacts feed_profile.json CATALOG/feed_profile.json

@author - TheCodeCache - Manoranjan

'''
import sys, os, json, botocore, boto3, socket, time, pandas as pd
import matplotlib.pyplot as plt
import mplcursors, gzip, shutil
from datetime import datetime, timedelta
from matplotlib import dates as mpl_dates

plt.style.use('seaborn')


def get_s3_resource(profile, endpoint_url, bucket_name):
    try:
        session = boto3.session.Session(profile_name=profile)
        s3_resource = session.resource('s3',
                              region_name='us-east-1',
                              endpoint_url=endpoint_url,
                              use_ssl=True,
                              verify=False,
                              config=boto3.session.Config(signature_version='s3v4'))
        return s3_resource
    except botocore.exceptions.ClientError as e:
        print(e.response)


def get_bucket(profile, endpoint_url, bucket_name):
    try:
        s3 = get_s3_resource(profile, endpoint_url, bucket_name)
        s3_bucket = s3.Bucket(bucket_name)
        return s3_bucket
    except botocore.exceptions.ClientError as e:
        print(e.response)


'''mean median mode std_dev'''


def draw(graph_x_y, plot):
    df = pd.DataFrame(graph_x_y)
    timestr = ' %H:%M:%S' if plot == 'time' else ''
    df['file_time'] = pd.to_datetime(df['file_time'], format=f"%Y-%m-%d{timestr}")
    df['file_size'] = df['file_size'] / (1024 * 1024)
    df.sort_values('file_time', inplace=True)
    print(df.head())
    print("\n")
    print(df)
    plt.gcf().autofmt_xdate()
    date_format = mpl_dates.DateFormatter(f'%d-%m-%Y{timestr}')
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.tight_layout()
    plt.xlabel("Arrival data-time")
    plt.ylabel("File Size (MB)")
    plt.title("Data Volume Graph")
    #plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
    plt.plot(df['file_time'], df['file_size'], linestyle='solid', marker='o', markersize=5)
    mplcursors.cursor(hover=True)
    plt.show()
    time.sleep(0.3)
    df.sort_values('file_size', inplace=True)
    df['file_size'].plot(kind='box')
    plt.show()
    print('\n')
    print(df['file_size'].describe())
    


def metadata(): pass


def quick_summary(s3_bucket, prefix=None):
    list_obj(s3_bucket, prefix, limit=10)


graph_x_y2 = {'2021-03-17 18:08:25': 27556580, '2021-03-17 18:08:32': 27554581, '2021-03-17 18:08:23': 27554355,
              '2021-03-17 18:08:22': 27551893, '2021-03-17 18:08:28': 27547377, '2021-03-17 18:08:27': 27546812,
              '2021-03-17 18:08:30': 27544474, '2021-03-17 18:08:26': 27543202, '2021-03-17 18:08:33': 27541810,
              '2021-03-17 18:08:31': 27540808, '2021-06-23 19:04:27': 3222002, '2021-06-23 19:07:41': 661378,
              '2021-06-23 19:07:42': 262918, '2021-06-23 12:06:53': 735781, '2021-08-16 22:31:54': 349846,
              '2021-08-16 22:31:55': 170555, '2021-06-23 12:22:18': 385842, '2021-08-16 21:54:52': 355540,
              '2021-07-09 19:11:05': 7803, '2021-07-09 19:11:06': 38648, '2021-08-13 09:43:26': 108269,
              '2021-08-13 09:43:27': 181870, '2021-09-24 11:27:51': 168590, '2021-05-10 03:23:30': 153245,
              '2021-05-10 03:23:29': 104972, '2021-09-24 11:27:52': 86130, '2021-05-10 03:35:22': 175751,
              '2021-08-13 09:38:54': 206051, '2021-08-13 09:38:55': 10258, '2021-05-10 03:35:21': 26169,
              '2021-05-10 03:35:23': 15149, '2021-06-23 07:47:49': 177475, '2021-04-02 12:16:19': 90401,
              '2021-04-02 18:26:04': 50807, '2021-09-17 13:40:47': 179973, '2021-04-02 18:26:05': 116269,
              '2021-05-10 03:30:12': 66295, '2021-04-02 18:26:06': 11552, '2021-06-23 07:47:50': 14186,
              '2021-05-10 03:30:11': 13834, '2021-04-02 12:16:18': 32771, '2021-09-17 13:40:48': 11392,
              '2021-05-26 03:48:26': 57623, '2021-08-20 06:57:20': 25438, '2021-06-23 12:32:54': 26601,
              '2021-10-28 11:06:42': 26830, '2021-10-29 15:32:25': 849, '2021-07-20 00:31:21': 64079,
              '2021-07-20 00:31:20': 15989, '2021-06-28 09:58:28': 3259, '2021-06-28 10:09:49': 3258,
              '2021-06-28 09:42:20': 2476, '2021-06-08 14:29:32': 1692, '2021-05-26 03:48:27': 3890,
              '2021-10-30 10:55:32': 0}


def list_obj(s3_bucket, prefix='/', sort_attr=('size', True), limit=20, plot='time'):
    try:
        by, reverse = sort_attr

        sort = {'size': lambda obj: obj.size,
                'last_modified': lambda obj: obj.last_modified,
                'file_name': lambda obj: obj.key}

        # Prefix='bluei_claims_DB/unified_layer_staging_partitioned/coverage_sep=WC/'

        objects = s3_bucket.objects.all() if prefix is None else s3_bucket.objects.filter(Prefix=prefix)

        iterable = list(objects)
        print('\n')
        print(f'length: {len(iterable)}')

        iterable.sort(key=sort[by], reverse=reverse)

        counter = 0
        size_list = []
        time_list = []
        key_list = []

        for s3_object in iterable:
            timestr = ' %H:%M:%S' if plot == 'time' else ''
            datetime = pd.to_datetime(s3_object.last_modified).strftime(f'%Y-%m-%d{timestr}')
            size_list.append(s3_object.size)
            time_list.append(datetime)
            key_list.append(s3_object.key)

            if counter < limit:
                print('object#: ', s3_object, s3_object.size, s3_object.last_modified)
                counter += 1

        graph_x_y = {'file_time': time_list, 'file_size': size_list}

        print('graph_x_y#: ', graph_x_y)
        print('graph attr len#: ', len(graph_x_y))
        print("\n")
        print(key_list)
        
        return graph_x_y, key_list
    except botocore.exceptions.ClientError as e:
        print(e.response)


def download(s3_bucket, orig_file_name, Tgt_file_name):
    try:
        print(f'Started downloading file [{Tgt_file_name}] for the Bucket: [{str(s3_bucket.name)}]')
        print("endpoint_url:", endpoint_url)
        s3_bucket.download_file(Tgt_file_name, orig_file_name)

        print(f'File download Successfully: {str(Tgt_file_name)} in bucket [{s3_bucket.name}]')

    except botocore.exceptions.ClientError as e:
        print(e.response)


def upload(s3_bucket, orig_file_name, Tgt_file_name):
    try:
        # boto3.set_stream_logger(name='botocore', level="DEBUG")
        print(f'Started Uploading file [{Tgt_file_name}] for the Bucket: [{str(s3_bucket.name)}]')
        s3_bucket.upload_file(orig_file_name,
                              Tgt_file_name,
                              ExtraArgs={'ServerSideEncryption': 'aws:kms',
                                         'SSEKMSKeyId': 'alias/S3/Dev',
                                         'ContentEncoding': 'UTF-8',
                                         'ContentType': 'text/plain; charset=utf-8'})

        print(f'File Uploaded Successfully: {str(Tgt_file_name)} in bucket [{s3_bucket.name}]')
    except botocore.exceptions.ClientError as e:
        print(e.response)

def remove(s3_bucket, orig_file_name):
    s3_bucket.Object('your-bucket', 'your-key}').delete()

def extract_logs(file_names):
    for file_name in file_names:
        gz_name = file_name+".gz"
        with gzip.open(gz_name,"rb") as f_in, open(file_name,"wb") as f_out:
            shutil.copyfileobj(f_in, f_out)


if __name__ == "__main__":
    try:
        input = sys.argv
        print(sys.argv)
        total_arg = len(sys.argv)
        print(total_arg)

        opn = input[1]
        print(f"operation: {opn}")

        def get_prefix(s3_url):
            tokens = s3_url.split('/', -1)
            bucket_name = tokens[2]
            env = bucket_name.split('-', -1)[5]
            file_name = tokens[-1]
            prefix = '/'.join(tokens[3:-1]) + '/'
            return (bucket_name, env, prefix, file_name)

        if input[2].startswith('s3://'):
            bucket_name, env, prefix, file_name = get_prefix(input[2])
        else:
            #env = input[4]
            env = 'dev'
            word = '-' if 'wcpa' in input[2] or 'datalake' in input[2] else '-datalake-'
            bucket_name = 'ma-aws-us-ue1-ss3-' + env + word + input[2]
            tokens = input[3].split('/', -1)
            file_name = tokens[-1]
            prefix = '/'.join(tokens[:-1]) + '/'
            if bucket_name.endswith('datalake-logs'):
                print(1111)
                prefix = 'emr_logs/'+input[3]+'/steps/'+input[4]+'/'
        print('env: ', env)
        print('bucket_name: ', bucket_name)
        #print('tokens: ', tokens)
        print('file_name: ', file_name)
        print('prefix: ', prefix)

        file_in_s3 = prefix + file_name
        endpoint_url = 'https://' + socket.gethostbyname('dev.s3bucket.mrshmc.com')

        s3_bucket = get_bucket('dev', endpoint_url, bucket_name)
        
        def download_all(s3_bucket, prefix):
            graph_x_y, key_list = list_obj(s3_bucket, prefix)
            file_names = []
            for key in key_list:
                print('\n\n')
                tokens = key.split('/', -1)
                file_name = tokens[-1]
                file_names.append(file_name)
                file_in_s3 = prefix + file_name
                download(s3_bucket, file_name, file_in_s3)
            return file_names
        
        def upload_all(s3_bucket, prefix, file_names):
            for file_name in file_names:
                print('\n\n')
                local_file = "C:\\Z\\" + file_name
                file_in_s3 = prefix + file_name
                upload(s3_bucket, local_file, file_in_s3)
        
        if opn == "up":
            local_file = "C:\\Z\\" + file_name
            upload(s3_bucket, local_file, file_in_s3)
        elif (opn == "dn"):
            if bucket_name.endswith('datalake-logs') and not input[2].startswith('s3://'):
                print(2222)
                file_name = 'stdout.gz'
                download(s3_bucket, file_name, prefix + file_name)
                file_name = 'stderr.gz'
                download(s3_bucket, file_name, prefix + file_name)
                file_name = 'syslog.gz'
                download(s3_bucket, file_name, prefix + file_name)
                file_name = 'hivemongo_script.log'
                download(s3_bucket, file_name, prefix + file_name)
                file_name = 'hivemongo_script.log.err'
                download(s3_bucket, file_name, prefix + file_name)
                file_name = 'response_for_email.json'
                download(s3_bucket, file_name, prefix + file_name)
                file_name = 'Claims_dashboard_job.err'
                download(s3_bucket, file_name, prefix + file_name)
                file_name = 'Claims_dashboard_job.log'
                download(s3_bucket, file_name, prefix + file_name)
                file_name = 'PymongoPysparklogs.log'
                download(s3_bucket, file_name, prefix + file_name)
                file_name = 'response.json'
                download(s3_bucket, file_name, prefix + file_name)
                file_name = 'response.json.gz'
                download(s3_bucket, file_name, prefix + file_name)
                file_name = 'pgp_decrypt.log'
                download(s3_bucket, file_name, prefix + file_name)
                file_name = 'pgp_decrypt.log.err'
                download(s3_bucket, file_name, prefix + file_name)
                
                file_names = ['stdout', 'stderr', 'syslog', 'response.json']
                extract_logs(file_names)
            else:
                print(3333)
                if file_name == '' and prefix is not None:
                    download_all(s3_bucket, prefix)
                else:
                    download(s3_bucket, file_name, file_in_s3)
        elif (opn == "ls"):
            plot = 'time' if not input[-1] or not input[-1].startswith('plot') else input[-1][5:]
            print('plot: ', plot)
            graph_x_y, key_list = list_obj(s3_bucket, prefix, plot=plot)
            print('key_list: ')
            print(key_list)
            #draw(graph_x_y, plot=plot)
        elif (opn == "rm"):
            s3_resource = get_s3_resource('dev', endpoint_url, bucket_name)
            try:
                print(f'file_in_s3: {file_in_s3}')
                print(f'bucket_name: {bucket_name}')
                
                if file_name == '' and prefix is not None:
                    graph_x_y, key_list = list_obj(s3_bucket, prefix)
                    for key in key_list:
                        print('\n\n')
                        tokens = key.split('/', -1)
                        file_name = tokens[-1]
                        file_in_s3 = prefix + file_name
                        s3_resource.meta.client.delete_object(Bucket=bucket_name, Key=file_in_s3)
                else:
                    s3_resource.meta.client.delete_object(Bucket=bucket_name, Key=file_in_s3)
                print(f'File Deleted Successfully: {input[2]}]')
            except ClientError as e:
                raise Exception( "boto3 client error in delete_object: " + e.__str__())
            except Exception as e:
                raise Exception( "Unexpected error in delete_object: " + e.__str__())
        elif (opn == "cp"):
            ## python aws.py cp s3://folder1/ s3://folder2/
            ## python aws.py cp s3://folder1/txt s3://folder2/def.txt
            ## python aws.py cp wcpa-artifacts key1/ key2/ 
            ## python aws.py cp wcpa-artifacts key1/abc.txt key2/def.txt
            
            if (not input[2].startswith('s3://')) and (not input[3].endswith('/')):
                download(s3_bucket, file_name, file_in_s3)
                local_file = "C:\\Z\\" + file_name
                upload(s3_bucket, local_file, input[4])
            elif (not input[2].startswith('s3://')) and (input[3].endswith('/')):
                file_names = download_all(s3_bucket, input[3])
                upload_all(s3_bucket, input[4], file_names)
            elif (not input[2].endswith('/')) and (not input[3].endswith('/')):
                bucket_name, env, src_prefix, src_file_name = get_prefix(input[2])
                bucket_name, env, tgt_prefix, tgt_file_name = get_prefix(input[3])
                src_file_in_s3 = src_prefix + src_file_name
                tgt_file_in_s3 = tgt_prefix + tgt_file_name
                download(s3_bucket, src_file_name, src_file_in_s3)
                local_file = "C:\\Z\\" + src_file_name
                upload(s3_bucket, local_file, tgt_file_in_s3)
            elif (input[2].endswith('/')) and (input[3].endswith('/')):
                bucket_name, env, src_prefix, src_file_name = get_prefix(input[2])
                bucket_name, env, tgt_prefix, tgt_file_name = get_prefix(input[3])
                file_names = download_all(s3_bucket, src_prefix)
                upload_all(s3_bucket, tgt_prefix, file_names)
            else:
                print("copy operation failed - invalid input parameters detected")
        else:
            print("Invalid Arguments passed..")
            sys.exit(0)
    except botocore.exceptions.ClientError as e:
        print(e.response)

```

**The above custom modification is one time change**, and we use this daily to interact with S3 from local  

```
To work with python s3 utility,
the steps are as follows -
create a working folder
with this specific name "Z" under C:\ directory

there're different ways to access s3 bucket,

basic commands -

dn - download
up - upload

python aws.py <dn/up> <full_absolute_s3_path>
sample ex to download unified.sh from s3 to C:\z| fodler -
python aws.py dn s3://<artifacts_bucket>/shell/unified.sh
python aws.py up s3://<artifacts_bucket>/shell/unified.sh

python aws.py up wcpa-artifacts shell/unified.sh
python aws.py up artifacts shell/unified.sh -- here artifacts implies datalake-artifacts
the upload operation takes a file from local i.e. C:\Z\ places on S3 with the same name,

python aws.py dn logs <cluster-id> <step-id>
it downloads most of the files from logs bucket

sample ex:
python aws.py dn logs j-CAST5464DFT s-PU76F5TRDE4

python aws.py dn s3://ma-aws-us-ue1-ss3-dev-datalake-logs/emr_logs/j-CAST5464DFT/steps/s-PU76F5TRDE4/
this downloads all the files present unde this directory

python aws.py dn s3://ma-aws-us-ue1-ss3-dev-datalake-logs/emr_logs/j-CAST5464DFT/steps/s-PU76F5TRDE4/stdout.gz
this cmd is for individual file download in this case it gets just stdout.gz from s3 and puts under C:\Z\ folder

```

# Example - 2: (Profile update activity on https://naukri.com)


```java
package com.naukri.profile_update;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.edge.EdgeDriver;


/**
 * For better productivity
 * 
 * this code uploads a pdf file, a resume basically, to naukri.com
 * 
 * TODO - To make it resilient from failure, also in case of failure, it must
 * send a response w/o fail
 * 
 * @author TheCodeCache - Manoranjan
 */
public class Resume {

	private static String username = null;
	private static String password = null;
	private static WebDriver driver = null;

	private static boolean enable = false;

	private static Map<String, String> hardcodedURLs = new HashMap<>();

	static {
		System.out.println("Resume class Loading");
	}

	static {
		System.setProperty("webdriver.edge.driver", "D:\\workspace\\drivers\\msedgedriver.exe");
//		EdgeOptions options = new EdgeOptions();
//		options.addArguments("headless");
		if (enable)
			driver = new EdgeDriver();
	}

	static {
		hardcodedURLs.put("login", "https://www.naukri.com/nlogin/login");
		hardcodedURLs.put("profile", "https://www.naukri.com/mnjuser/profile?id=&altresid");
		hardcodedURLs.put("logout", "https://www.naukri.com/nlogin/logout");
	}

	static {
		try (InputStream input = new FileInputStream("src/main/resources/credential.properties")) {

			Properties prop = new Properties();

			// load a properties file
			prop.load(input);

			// get the property value and print it out
			username = CryptoUtil.decrypt(prop.getProperty("username"));
			password = CryptoUtil.decrypt(prop.getProperty("password"));

		} catch (IOException ex) {
			ex.printStackTrace();
		}
	}

	/**
	 * Uploads file to the job portal
	 * 
	 * @param resume - absolute path to the resume file to be uploaded, it can be
	 *               pdf/docx
	 */
	public static void upload(String resume) {
		if (!enable) {
			driver = new EdgeDriver();
			//driver.manage().window().maximize();
		}
		try {
			// Login
			driver.get(hardcodedURLs.get("login"));
			delay(1);

			WebElement username = driver.findElement(By.id("usernameField"));
			WebElement password = driver.findElement(By.id("passwordField"));

			username.sendKeys(Resume.username);
			password.sendKeys(Resume.password);

			WebElement login = driver.findElement(By.xpath("//*[@id=\"loginForm\"]/div[2]/div[3]/div/button[1]"));

			login.click();
			delay(1);

			// Profile
			driver.get(hardcodedURLs.get("profile"));
			delay(2);

			WebElement uploadElement = driver.findElement(By.id("attachCV"));

			uploadElement.sendKeys(resume);
			delay(4);

			// Logout
			driver.get(hardcodedURLs.get("logout"));
			System.out.println("Exit..");
			delay(1);
		} catch (Exception e) {
			e.printStackTrace();
		}

		if (!enable) {
			driver.close();
			driver.quit();
		}
	}

	private static void delay(int k) {
		System.out.println("wait " + k + " secs");
		try {
			Thread.sleep(k * 1000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}

	public static void main(String[] args) {

		String resume = "C:\\Users\\manoranjan.kumar\\Downloads\\vc\\Manoranjan_Resume.pdf";
		upload(resume);
	}
}


package com.naukri.profile_update;

import java.util.Timer;
import java.util.TimerTask;

public class Scheduler {

	public static void main(String[] args) throws InterruptedException {

		Timer timer = new Timer();
		TimerTask task = new MyTask();
		timer.schedule(task, 5000, 12000);
	}
}

class MyTask extends TimerTask {

	private String resume = "C:\\Users\\manoranjan.kumar\\Downloads\\vc\\Manoranjan_Resume.pdf";

	@Override
	public void run() {
		Resume.upload(resume);
	}
}

```
