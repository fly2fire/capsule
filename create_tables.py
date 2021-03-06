from __future__ import print_function # Python 2/3 compatibility
import boto3


def create_quotes():
    table = client.create_table(
        TableName='Quotes.EOD',
        KeySchema=[
            {
                'AttributeName': 'Symbol',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'Date',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'Symbol',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Date',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    w = client.get_waiter('table_exists')
    w.wait(TableName='Quotes.EOD')
    print("table Quotes.EOD created")
    print("Table status:", table)


def create_securities():
    table = client.create_table(
        TableName='Securities',
        KeySchema=[
            {
                'AttributeName': 'Symbol',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'Broker',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'Symbol',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Broker',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    w = client.get_waiter('table_exists')
    w.wait(TableName='Securities')
    print("table Securities created")
    print("Table status:", table)


client = boto3.client('dynamodb', region_name='us-east-1')

try:
    if 'Quotes.EOD' in client.list_tables()['TableNames']:
        client.delete_table(TableName='Quotes.EOD')
        waiter = client.get_waiter('table_not_exists')
        waiter.wait(TableName='Quotes.EOD')
        print("table Quotes.EOD deleted")
    if 'Securities' in client.list_tables()['TableNames']:
        client.delete_table(TableName='Securities')
        waiter = client.get_waiter('table_not_exists')
        waiter.wait(TableName='Securities')
        print("table Securities deleted")

except Exception as e:
    print(e)

create_securities()
create_quotes()
