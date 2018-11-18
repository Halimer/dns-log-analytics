import boto3
import datetime

#Connection for S3 and Athena
s3 = boto3.client('s3')
athena = boto3.client('athena')

#Get Year, Month, Day for partition (this will get tomorrow date's value)
date = datetime.datetime.now()
athena_year = str(date.year)
athena_month = str(date.month).rjust(2, '0')
athena_day = str(date.day - 1).rjust(2, '0')



#Parameters for S3 log location and Athena table
#Fill this carefully (Read the commented section on top to help)
s3_buckcet = 'halimer-dns-analytics'
s3_input = 's3://' + s3_buckcet + '/'
database = 'DNS_analytics'
table_name = 'logs'


#Executing the athena query:
def run_query(query, database, s3_output):
        query_response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': database
            },
        ResultConfiguration={
            'OutputLocation': s3_output,
            }
        )
        print('Execution ID: ' + query_response['QueryExecutionId'])
        return query_response
    
#Main function for get regions and run the query on the captured regions
def lambda_handler(event, context):
    # Get Account ID and region from lambda function arn in the context
    account_id = context.invoked_function_arn.split(":")[4]
    my_region = context.invoked_function_arn.split(":")[3]
    
    # Set Athena Output
    s3_ouput = 's3://aws-athena-query-results-' + account_id + '-' + my_region

    
    partition_string = athena_year + "-"+ athena_month + "-" + athena_day
    query = str("ALTER TABLE "+ table_name +" ADD PARTITION (d='" + partition_string + "');")
    print(query)

    run_query(query, database, s3_ouput) 