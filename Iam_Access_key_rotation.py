#importing required modules
import boto3
from datetime import datetime, timezone

#using client instead of resource as because it doesn't have update access key functionality
client = boto3.client("iam")
paginator = client.get_paginator('list_users')

#gives current date
current_date = datetime.now(timezone.utc)
#set the maximum age of the access key
max_key_age = 5

# printing users first in-order to list access keys next
for response in paginator.paginate():
    # iterate through each user in the response
    for user in response["Users"]:
        # extract the username of the user
        username = user["UserName"]
        
        # print access keys for the users by passing username
        list_keys = client.list_access_keys(UserName=username)
        print(list_keys)
        
        # iterate through each access key for the user
        for accesskey in list_keys['AccessKeyMetadata']:
            # extract access key details
            access_key_id = accesskey['AccessKeyId']
            key_creation_date = accesskey['CreateDate']

            # calculating the age of the access key
            age = (current_date - key_creation_date).days

            # Deactivating access keys based on the condition if age exceeds maximum key age
            if age > max_key_age:
                print("Deactivating the Access Key for the following user:", username)
                client.update_access_key(
                    UserName=username,
                    AccessKeyId=access_key_id,
                    Status='Inactive'
                )
                
                # Generating a new access key for the user after deactivating the old key
                print("Generating a new access key for the following user:", username)
                new_key = client.create_access_key(UserName=username)
                print("New Access Key:", new_key['AccessKey'])
