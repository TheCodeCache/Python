# Code Coverage in Python – 

## Unit Test Guidelines for Python Maven project

### 1. Naming Conventions and Best Practices
![image](https://user-images.githubusercontent.com/26399543/153480488-d94a9f9a-069a-4e56-9b73-15c867f33c45.png)

### 2. Directory structure 
![image](https://user-images.githubusercontent.com/26399543/153480708-4c65af81-0574-4b79-81ec-041be6fe0671.png)  
![image](https://user-images.githubusercontent.com/26399543/153480788-74a8236f-4565-485e-9777-65b669693983.png)  

### 3. External Module Dependency resolution for source files
![image](https://user-images.githubusercontent.com/26399543/153481003-83ac3b05-83c5-4926-9792-596ff8ba795d.png)  
The target directory used in above command should be same as the working directory for the test case execution. In this case it should be src/test.  
### 4. Mocking External API calls
```python
'''
    File name: test_flow_executor.py
    Author: Megha Jain
    Date created: 08/02/2021
    Python Version: 3.9
    Last updated By :
    Date last modified:
'''
from unittest import mock
from unittest.mock import patch
 
# Mocking environment variable before importing main module
with patch.dict(os.environ,os_env,clear=True):
    # Mocking API call before importing main module
    with patch('com.thecodecache.datalake.util.execute_lambda.executelambdafunction', return_value = '{"username":"wdq3e23sad"}'):
        from com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor import lambda_handler
 
#Mocking environment variables above class so that mocked env variable is available to all the internal functions
@mock.patch.dict(os.environ, os_env, clear=True)
class TestFlowExecutor(unittest.TestCase):
 
    #If we have imported the functions inside source files then we can directly mock them in test function.
    @patch('com.mathecodecachersh.datalake.awslambda.abcdflowexecutor.flow_executor.is_batch_complete')
    def test_lambda_handler_with_is_batch_complete_false(self,is_batch_complete):
        is_batch_complete.return_value = False
        self.assertEqual(lambda_handler(self.event,self.context),self.event)   
    
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.abcdFlowConfigDAO.get_flow_config')
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.is_batch_complete')
    #Argument list in test function should be in reverse order of @patch annotations sequence
    def test_lambda_handler_with_ibc_true_no_records(self,is_batch_complete,get_flow_config):
        is_batch_complete.return_value = True
        get_flow_config.return_value = ""
        self.assertEqual(lambda_handler(self.event,self.context),self.event)
 
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.call_lambda_and_handle_response')
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.random_string')
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.get_payload')
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.get_job_config')
    #If we are importing other class in source file and are calling its functions via its object then we should patch the function with fully qualified name i.e. including classname
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.abcdFlowConfigDAO.get_flow_config')
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.is_batch_complete')  
    def test_lambda_handler_with_ibc_true_records_found_lambda(self,is_batch_complete,get_flow_config,get_job_config,get_payload,random_string,call_lambda_and_handle_response):
        is_batch_complete.return_value = True            
        get_flow_config.return_value = read_json_file("resources/record.json", "r")
        get_job_config.return_value = read_json_file("resources/job_configs.json", "r")
        get_payload.return_value = read_json_file("resources/payload.json", "r")
        random_string.return_value ="1234567890"  
        call_lambda_and_handle_response.return_value=""
        lambda_handler(self.event,self.context) 
```
### 5. Mocking Muliple API calls for same function with different values
Sample test case for setting different return values to multiple API calls of same function  
```python
@patch('com.thecodecache.datalake.awslambda.abcdingestionhandler.ingestion_handler.call_lambda_and_handle_response')
@patch('json.loads')
def test_terminate_transient_cluster_has_sor_name_JobFlowId(self,json_loads,call_lambda_and_handle_response):
    print("*********************Inside function test_terminate_transient_cluster_has_sor_name_JobFlowId********************")
     
    # Setting different return values for each call of call_lambda_and_handle_response function
    call_lambda_responses = [None, None, {'Payload': Mock()}, {'StatusCode' : 204},None]
    call_lambda_and_handle_response.side_effect = call_lambda_responses
     
    payload = {'tracking_id': 98316182, 'batch_id': None, 'sor_name': 'ABCD_Mongo', 'audit_request': 'get', 'audit_status': 'NOTHING_IN_PROGRESS'}
    json_loads.return_value = payload
     
    self.assertEqual(terminate_transient_cluster(self.event,self.feed_id, self.abcd_ingestion_timestamp, self.env_var),self.event)
    print("***********************END OF test_terminate_transient_cluster_has_sor_name_JobFlowId***************************")
```
### 6. Mocking boto3.client
**Mocking boto3 library**:  
```python
@mock.patch("boto3.client")
def test_lambda_handler(self,client):
    print("*********************Inside function test_lambda_handler********************")
    client.return_value = "client"
    client.send_message.return_value = read_json_file(path + "client.json", "r")
    self.assertEqual(lambda_handler(self.event, self.context),"c02563b8-5a9a-844a-b621-9fd1989e5368")
    print("***********************END OF test_lambda_handler***************************")
```
### 6. Exception Testing
```python
@patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.send_email')
@patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.AbcdFlowConfigDAO.get_flow_config')
def test_lambda_handler_exception_func(self,get_flow_config,send_email):  
    print("**********************Inside Function test_lambda_handler_exception_func********************")
    send_email.return_value = {}
    get_flow_config.return_value = read_json_file(path + "records_exc.json", "r")
    self.assertRaises(Exception,lambda_handler,self.event,self.context)
    print("***********************END OF test_lambda_handler_exception_func*******************************")
```
### 7. Unit Test Cases for flow_executor lambda function
```python
'''
    File name: test_flow_executor.py
    Author: Megha Jain
    Date created: 08/03/2021
    Python Version: 3.9
    Last updated By : Megha Jain
    Date last modified: 08/12/2021
'''
 
import unittest
from unittest import mock
from unittest.mock import patch
import os,sys
 
sys.path.append('src/main/python')
 
from com.thecodecache.datalake.util.common_utils import read_json_file
 
path = 'resources/test_flow_executor/'
 
os_env = read_json_file(path + "env_var.json", "r")
 
# Mocking environment variable before importing main module
with patch.dict(os.environ,os_env,clear=True):
    # Mocking API call before importing main module
    with patch('com.thecodecache.datalake.util.execute_lambda.executelambdafunction', return_value = {'svc-dev-mythecodecache-app':'abcdefgh'}):
        from com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor import *
 
             
#Mocking environment variables above class so that mocked env variable is available to all the internal functions
@mock.patch.dict(os.environ, os_env, clear=True)
class TestFlowExecutor(unittest.TestCase):
 
    @classmethod
    def setUpClass(cls):
        cls.event = read_json_file(path + "event.json", "r")
        cls.context= ""
 
#####################################  TEST CASES TO TEST lambda_handler FUNCTIONALITY ################################################### 
 
    ######  Test Case To Test Is Batch Complete = False functionality   #####
    #If we have imported the functions inside source files then we can directly mock them in test function.
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.send_email')
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.is_batch_complete')
    def test_lambda_handler_with_is_batch_complete_false(self,is_batch_complete,send_email):
        print("*********************Inside function test_lambda_handler_with_is_batch_complete_false********************")
        is_batch_complete.return_value = False    
        self.assertEqual(lambda_handler(self.event,self.context),self.event)
        print("***********************END OF test_lambda_handler_with_is_batch_complete_false***************************")
 
    ######  Test Case To Test No Record Found functionality When Is Batch Complete = True   #####
    #Argument list in test function should be in reverse order of @patch annotations sequence.   
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.send_email')
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.AbcdFlowConfigDAO.get_flow_config')
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.is_batch_complete')
    def test_lambda_handler_with_ibc_true_no_records(self,is_batch_complete,get_flow_config,send_email):
        print("**********************Inside Function test_lambda_handler_with_ibc_true_no_records************************")
        is_batch_complete.return_value = True
        get_flow_config.return_value = ""
        self.assertEqual(lambda_handler(self.event,self.context),self.event)
        print("No flow found!!")
        print("**************************END OF test_lambda_handler_with_ibc_true_no_records********************************")
 
    ######  Test Case To Test Lambda Function Flow when Records Found and Is Batch Complete = True   #####
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.send_email')
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.call_lambda_and_handle_response')
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.random_string')
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.get_payload')
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.get_job_config')
    #If we are importing other class in source file and are calling its functions via its object then we should patch the function with fully qualified name  i.e. including classname
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.AbcdFlowConfigDAO.get_flow_config')
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.is_batch_complete')  
    def test_lambda_handler_with_ibc_true_records_found_lambda(self,is_batch_complete,get_flow_config,get_job_config,get_payload,random_string,call_lambda_and_handle_response,send_email):  
        print("**********************Inside Function test_lambda_handler_with_ibc_true_records_found_lambda********************")
        is_batch_complete.return_value = True            
        get_flow_config.return_value = read_json_file(path + "records_lambda.json", "r")
        get_job_config.return_value = read_json_file(path + "job_configs.json", "r")
        get_payload.return_value = read_json_file(path + "payload.json", "r")
        random_string.return_value ="1234567890"  
        call_lambda_and_handle_response.return_value=""
        self.assertEqual(lambda_handler(self.event,self.context),self.event)
        print("***********************END OF test_lambda_handler_with_ibc_true_records_found_lambda*******************************")
 
    ######  Test Case To Test Step Function Flow when Records Found and Is Batch Complete = True   #####
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.send_email')
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.call_stepfn_and_handle_response')
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.random_string')
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.get_payload')
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.get_job_config')
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.AbcdFlowConfigDAO.get_flow_config')
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.is_batch_complete')  
    def test_lambda_handler_with_ibc_true_records_found_stepfunction(self,is_batch_complete,get_flow_config,get_job_config,get_payload,random_string,call_stepfn_and_handle_response,send_email):  
        print("**********************Inside Function test_lambda_handler_with_ibc_true_records_found_stepfunction********************")
        is_batch_complete.return_value = True            
        get_flow_config.return_value = read_json_file(path + "records_step.json", "r")
        get_job_config.return_value = read_json_file(path + "job_configs.json", "r")
        get_payload.return_value = read_json_file(path + "payload.json", "r")
        random_string.return_value ="1234567890" 
        call_stepfn_and_handle_response.return_value = ""          
        self.assertEqual(lambda_handler(self.event,self.context),self.event)
        print("***********************END OF test_lambda_handler_with_ibc_true_records_found_stepfunction*******************************")
     
    ######  Test Case To Test Unsupported Function Flow when Records Found and Is Batch Complete = True   #####
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.send_email')
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.random_string')
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.get_payload')
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.get_job_config')
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.AbcdFlowConfigDAO.get_flow_config')
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.is_batch_complete')  
    def test_lambda_handler_with_ibc_true_records_found_unsupported_func(self,is_batch_complete,get_flow_config,get_job_config,get_payload,random_string,send_email):  
        print("**********************Inside Function test_lambda_handler_with_ibc_true_records_found_unsupported_func********************")
        is_batch_complete.return_value = True            
        get_flow_config.return_value = read_json_file(path + "rec.json", "r")
        get_job_config.return_value = read_json_file(path + "job_configs.json", "r")
        get_payload.return_value = read_json_file(path + "payload.json", "r")
        random_string.return_value ="1234567890"       
        self.assertEqual(lambda_handler(self.event,self.context),self.event)
        print("***********************END OF test_lambda_handler_with_ibc_true_records_found_unsupported_func*******************************") 
 
    ######  Test Case To Test Exception Handling for Lambda Handler Function   #####
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.send_email')
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.AbcdFlowConfigDAO.get_flow_config')
    def test_lambda_handler_exception_func(self,get_flow_config,send_email):  
        print("**********************Inside Function test_lambda_handler_exception_func********************")
        send_email.return_value = {}
        get_flow_config.return_value = read_json_file(path + "records_exc.json", "r")
        self.assertRaises(Exception,lambda_handler,self.event,self.context)
        print("***********************END OF test_lambda_handler_exception_func*******************************")
 
#####################################  TEST CASES TO TEST get_job_config FUNCTIONALITY ###################################################       
 
    ######  Test Case To Test the config collection present Flow   #####
    @patch('com.thecodecache.datalake.dao.abcdingestionmaster.flow_config_master.AbcdFlowConfigDAO.get_job_config')
    def test_get_job_config_with_config_collection(self,get_job_config1):
        print("************************Inside Function test_get_job_config_with_config_collection**********************")       
        get_job_config1.return_value = read_json_file(path + "job_configs.json", "r")
        job_config_list = get_job_config(self.event,read_json_file(path + "record.json", "r"))
        for job_config in job_config_list:
            #check if keys from event are present
            self.assertEqual(job_config['hiveQueryS3Location'],"s3://ma-aws-us-ue1-ss3-dev-datalake-artifacts/HIVE/lpm_script/lpm_data_feed.sql") 
            self.assertEqual(job_config['S3_ENCRYPTION_KEY'],"alias/S3/TheCodeCacheDev-MBDL") 
             
            #check if append updated the common key value with latest dict
            self.assertEqual(job_config['GetCatalogueInfo']['feed_business_name'],"mythecodecache.env_jobs_feed_name")  
            self.assertEqual(job_config['F10_value'],991111)
             
            #check if keys from job_config are present
            self.assertEqual(job_config['spark_job_config']['standard_configs']['deploy-mode'],"client")
            self.assertEqual(job_config['ingestion_type'],"POST_INGESTION")
             
        print("***********************END OF test_get_job_config_with_config_collection*******************************")
 
    ######  Test Case To Test without config collection Flow   #####
    @patch('com.thecodecache.datalake.dao.abcdingestionmaster.flow_config_master.AbcdFlowConfigDAO.get_job_config')
    def test_get_job_config_without_config_collection(self,get_job_configDAO):
        print("************************Inside Function test_get_job_config_without_config_collection**********************")       
        get_job_configDAO.return_value = read_json_file(path + "job_configs.json", "r")
        job_config_list = get_job_config(self.event,read_json_file(path + "record_config.json", "r"))
        for job_config in job_config_list:
            #check if keys from event are present
            self.assertEqual(job_config['hiveQueryS3Location'],"s3://ma-aws-us-ue1-ss3-dev-datalake-artifacts/HIVE/lpm_script/lpm_data_feed.sql") 
            self.assertEqual(job_config['S3_ENCRYPTION_KEY'],"alias/S3/TheCodeCacheDev-MBDL") 
                        
            #check if keys from job_config are present
            self.assertEqual(job_config['spark_job_config']['standard_configs']['deploy-mode'],"client")
            self.assertEqual(job_config['python_script_file'],"pysparkpymongo_generic/pysparkmongo.spark.spark_mongo.py")
             
        print("***********************END OF test_get_job_config_without_config_collection*******************************")
 
    ######  Test Case To Test without config and config collection Flow   #####
    @patch('com.thecodecache.datalake.dao.abcdingestionmaster.flow_config_master.AbcdFlowConfigDAO.get_job_config')
    def test_get_job_config_without_config_config_collection(self,get_job_configDAO):
        print("************************Inside Function test_get_job_config_without_config_config_collection**********************")       
        get_job_configDAO.return_value = read_json_file(path + "job_configs.json", "r")
        self.assertEqual(get_job_config(self.event,read_json_file(path + "record_na.json", "r")),[self.event])       
        print("***********************END OF test_get_job_config_without_config_config_collection*******************************")
 
#####################################  TEST CASE TO TEST get_payload FUNCTIONALITY ###################################################
    @patch('com.thecodecache.datalake.awslambda.abcdflowexecutor.flow_executor.populate_cluster_details')
    def test_get_payload(self,populate_cluster_details):
        print("************************Inside Function test_get_payload**********************")       
        populate_cluster_details.return_value = {}
        payload = get_payload(self.event)
        self.assertEqual(payload['ingestion_id'],self.event['F10_value'])
        self.assertEqual(payload['ingestion_timestamp'],self.event['F2_value'])
        self.assertEqual(payload['shell_script_path'],"s3://%s/%s" % (os.environ["BINARY_S3_BUCKET"], self.event['shell_script_path']))
        self.assertEqual(payload['business_contact'],"Team")  
        self.assertEqual(payload['sor_name'],self.event['sor_name'] if 'sor_name' in self.event else 'ABCD_POST_INGESTION')
        print("***********************END OF test_get_payload*******************************")
            
 
if __name__ == '__main__':
    unittest.main()
```
**Execution Command**:  
```python
python -m unittest python/test_flow_executor.py
```

## Python Unit Test integration with SonarQube

### 1. Executing Python Unit Test Cases through Jenkins Pipeline
To execute all python test cases present under 'src/test/python' directory,  
incorporate below changes in pom.xml file present in project root directory:  
![image](https://user-images.githubusercontent.com/26399543/153482075-6e68ca63-f2ab-4ea8-a19d-99fcd4461783.png)  

### 2. Generating Python Test Code Coverage Report
For generating Python Unit test Coverage report, add below execution step in pom.xml file after test execution step :  
![image](https://user-images.githubusercontent.com/26399543/153482242-ff3a2d2b-ab0d-4c0c-aa7d-77eef98bf02a.png)  

### 3. Publishing Python Unit Test Cases Code Coverage report on SonarQube
![image](https://user-images.githubusercontent.com/26399543/153482359-2575263b-1f8b-4615-a9a8-b2140621919b.png)  

### 4. Coverage report on SonarQube Dashboard
**SonarQube Dashboard - Line Coverage report before executing any Unit Test Case for Python code**  
![image](https://user-images.githubusercontent.com/26399543/153482504-bc715341-521e-4351-9719-da49dac9e355.png)  

**SonarQube Dashboard - Current status of Project Coverage report on SonarQube Dashboard:**  
![image](https://user-images.githubusercontent.com/26399543/153482667-bbd3718a-f880-4285-9388-cd58f14e911a.png)  

### 5. Steps to execute Unit Test Cases from local
![image](https://user-images.githubusercontent.com/26399543/153482900-3a890922-d84a-428c-9419-ab3de0599322.png)  






```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

  <groupId>com.thecodecache</groupId>
  <artifactId>python_code_coverage</artifactId>
  <version>1.0.0-SNAPSHOT</version>
  <packaging>jar</packaging>

  <name>Python Code Coverage</name>
  <url>https://github.com/TheCodeCache/Python/edit/master/Code%20Coverage.md</url>

  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <sonar.python.coverage.reportPaths>${project.basedir}/src/test/coverage.xml</sonar.python.coverage.reportPaths>
  </properties>

  <dependencies>
  
  </dependencies>
  
  <build>
        <sourceDirectory>${project.basedir}/src/main</sourceDirectory>
        <testSourceDirectory>${project.basedir}/src/test</testSourceDirectory>

        <plugins>
            <!-- LAMBDA assembly plugins -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-assembly-plugin</artifactId>
                <version>2.6</version>
                <executions>
                    <execution>
                        <id>pysparkpymongo_generic</id>
                        <configuration>
                            <appendAssemblyId>false</appendAssemblyId>
                            <outputDirectory>target/util/python/pysparkpymongo_generic</outputDirectory>
                            <finalName>pysparkmongo</finalName>
                            <descriptors>
                                <descriptor>scripts/build/assembly/pysparkpymongo_generic.xml</descriptor>
                            </descriptors>
                        </configuration>
                        <phase>package</phase>
                        <goals>
                            <goal>single</goal>
                        </goals>
                    </execution>
                    <execution>
                        <id>abcdpysparkhandler_lambda</id>
                        <configuration>
                            <appendAssemblyId>false</appendAssemblyId>
                            <finalName>abcdpysparkhandler_lambda</finalName>
                            <outputDirectory>target/lambda/abcdpysparkhandler</outputDirectory>
                            <descriptors>
                                <descriptor>scripts/build/assembly/abcdpysparkhandler_lambda_assembly.xml</descriptor>
                            </descriptors>
                        </configuration>
                        <phase>package</phase>
                        <goals>
                            <goal>single</goal>
                        </goals>
                    </execution>
                    <execution>
                        <id>abcdflowexecutor_lambda</id>
                        <configuration>
                            <appendAssemblyId>false</appendAssemblyId>
                            <finalName>abcdflowexecutor_lambda</finalName>
                            <outputDirectory>target/lambda/abcdflowexecutor</outputDirectory>
                            <descriptors>
                                <descriptor>scripts/build/assembly/abcdflowexecutor_lambda_assembly.xml</descriptor>
                            </descriptors>
                        </configuration>
                        <phase>package</phase>
                        <goals>
                            <goal>single</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>

            <!-- copy step function and other resources -->
            <plugin>
                <artifactId>maven-resources-plugin</artifactId>
                <version>3.1.0</version>
                <executions>
                    <execution>
                        <id>copy-abcdpysparkhandler-formation-files</id>
                        <phase>package</phase>
                        <goals>
                            <goal>copy-resources</goal>
                        </goals>
                        <configuration>
                            <outputDirectory>target/lambda/abcdpysparkhandler</outputDirectory>
                            <resources>
                                <resource>
                                    <directory>src/main/resources/abcdpysparkhandler</directory>
                                    <include>*.json</include>
                                </resource>
                            </resources>
                        </configuration>
                    </execution>
                    <execution>
                        <id>copy-abcdflowexecutor-formation-files</id>
                        <phase>package</phase>
                        <goals>
                            <goal>copy-resources</goal>
                        </goals>
                        <configuration>
                            <outputDirectory>target/lambda/abcdflowexecutor</outputDirectory>
                            <resources>
                                <resource>
                                    <directory>src/main/resources/abcdflowexecutor</directory>
                                    <include>*.json</include>
                                </resource>
                            </resources>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
            <plugin>
                <groupId>org.sonarsource.scanner.maven</groupId>
                <artifactId>sonar-maven-plugin</artifactId>
                <version>3.7.0.1746</version>
            </plugin>          

            <!-- installing Python dependencies -->
            <plugin>
                <groupId>org.codehaus.mojo</groupId>
                <artifactId>exec-maven-plugin</artifactId>
                <version>1.6.0</version>
                <executions>
                    <execution>
                        <id>abcdpysparkhandler</id>
                        <phase>process-sources</phase>
                        <goals>
                            <goal>exec</goal>
                        </goals>
                        <configuration>
                            <executable>pip</executable>
                            <arguments>
                                <argument>install</argument>
                                <argument>-t</argument>
                                <argument>target/pylib/abcdpysparkhandler</argument>
                                <argument>-r</argument>
                                <argument>src/main/resources/abcdpysparkhandler/requirements.txt</argument>
                            </arguments>
                        </configuration>
                    </execution>
                    <execution>
                        <id>abcdflowexecutor</id>
                        <phase>process-sources</phase>
                        <goals>
                            <goal>exec</goal>
                        </goals>
                        <configuration>
                            <executable>pip</executable>
                            <arguments>
                                <argument>install</argument>
                                <argument>-t</argument>
                                <argument>target/pylib/abcdflowexecutor</argument>
                                <argument>-r</argument>
                                <argument>src/main/resources/abcdflowexecutor/requirements.txt</argument>
                            </arguments>
                        </configuration>
                    </execution>

                    <execution>
                        <id>python-test</id>
                        <phase>test</phase>
                        <goals>
                            <goal>exec</goal>
                        </goals>
                        <configuration>
                            <executable>python3</executable>
                            <workingDirectory>src/test</workingDirectory>
                            <arguments>
                                <argument>-m</argument>
                                <argument>coverage</argument>
                                <argument>run</argument>
                                <argument>-m</argument>
                                <argument>unittest</argument>
                                <argument>discover</argument>
                                <argument>-s</argument>
                                <argument>python</argument>
                            </arguments>    
                            <environmentVariables>
                              <PYTHONPATH>../main/python</PYTHONPATH>
                            </environmentVariables>
                        </configuration>
                    </execution>
                    
                    <execution>
                        <id>python-coverage-report</id>
                        <phase>test</phase>
                        <goals>
                            <goal>exec</goal>
                        </goals>
                        <configuration>
                            <executable>python3</executable>
                            <workingDirectory>src/test</workingDirectory>
                            <arguments>
                                <argument>-m</argument>
                                <argument>coverage</argument>
                                <argument>xml</argument>
                          </arguments>
                            <environmentVariables>
                              <PYTHONPATH>../main/python</PYTHONPATH>
                            </environmentVariables>                          
                        </configuration>
                    </execution>  
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
```

