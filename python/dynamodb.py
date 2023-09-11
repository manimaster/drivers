import os
import boto3

class DynamoDB:
    def __init__(self):
        # Get DynamoDB connection details from ENV variables
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY", None)
        self.aws_secret_key = os.getenv("AWS_SECRET_KEY", None)
        self.region_name = os.getenv("AWS_REGION", "us-west-2")
        
        self.client = self._connect()
        
    def _connect(self):
        # Establish a connection to the DynamoDB
        session = boto3.Session(
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=self.region_name
        )
        return session.resource('dynamodb')
    
    def list_tables(self):
        # List all the tables
        return list(self.client.tables.all())
    
    def create_table(self, table_name, attribute_definitions, key_schema, provisioned_throughput):
        # Create a new table
        table = self.client.create_table(
            TableName=table_name,
            AttributeDefinitions=attribute_definitions,
            KeySchema=key_schema,
            ProvisionedThroughput=provisioned_throughput
        )
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    
    def delete_table(self, table_name):
        # Delete the specified table
        table = self.client.Table(table_name)
        table.delete()
    
    def insert_item(self, table_name, item):
        # Insert a new item into the table
        table = self.client.Table(table_name)
        table.put_item(Item=item)
    
    def get_item(self, table_name, key):
        # Retrieve an item from the table
        table = self.client.Table(table_name)
        response = table.get_item(Key=key)
        return response.get('Item')
    
    def update_item(self, table_name, key, update_expression, expression_attribute_values):
        # Update an item in the table
        table = self.client.Table(table_name)
        table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
    
    def delete_item(self, table_name, key):
        # Delete an item from the table
        table = self.client.Table(table_name)
        table.delete_item(Key=key)
    
    def query_items(self, table_name, **kwargs):
        # Query items from the table based on certain conditions
        table = self.client.Table(table_name)
        return table.query(**kwargs)


# import os

# os.environ["AWS_ACCESS_KEY"] = "YOUR_AWS_ACCESS_KEY"
# os.environ["AWS_SECRET_KEY"] = "YOUR_AWS_SECRET_KEY"
# os.environ["AWS_REGION"] = "us-west-2"


# db = DynamoDB()

# # Create a sample table
# db.create_table(
#     table_name='users',
#     attribute_definitions=[
#         {'AttributeName': 'username', 'AttributeType': 'S'},
#         {'AttributeName': 'last_name', 'AttributeType': 'S'}
#     ],
#     key_schema=[
#         {'AttributeName': 'username', 'KeyType': 'HASH'},
#         {'AttributeName': 'last_name', 'KeyType': 'RANGE'}
#     ],
#     provisioned_throughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
# )

# # Insert a sample item
# db.insert_item('users', {'username': 'john', 'last_name': 'doe', 'age': 30})

# # Query the item
# print(db.get_item('users', {'username': 'john', 'last_name': 'doe'}))
