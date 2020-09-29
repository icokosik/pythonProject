
import boto3

dynamodb = boto3.resource('dynamodb')
properties = dynamodb.Table('properties')


def insertIntoProperties(items):
    with properties.batch_writer() as batch:
        for r in items:
            batch.put_item(Item=r)
