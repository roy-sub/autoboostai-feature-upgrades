import boto3
from typing import List
from botocore.exceptions import ClientError

class DomainUrlManager:
    
    def __init__(self, table_name: str = 'autoboostai_domain_urls_table'):

        # Initialize DynamoDB client with credentials
        self.dynamodb = boto3.client(
            'dynamodb',
            aws_access_key_id= "AKIA3CMCCJCUAEQLYKE6",
            aws_secret_access_key= "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",
            region_name= "eu-north-1"
        )
        self.table_name = table_name
    
    def normalize_keyword_search(self, keyword_search: str) -> str:
        
        return keyword_search.lower().strip().replace(" ", "+")

    def get_domain_urls(self, keyword_search: str) -> List[str]:

        try:

            keyword_search = self.normalize_keyword_search(keyword_search)

            response = self.dynamodb.get_item(
                TableName=self.table_name,
                Key={
                    'keyword_search': {'S': keyword_search}
                }
            )
            
            # If the item exists and has domain_urls
            if 'Item' in response and 'domain_urls' in response['Item']:
                return list(response['Item']['domain_urls']['SS'])
            
            # If the item exists but no domain_urls
            if 'Item' in response:
                return []
                
            raise KeyError(f"No record found for keyword_search: {keyword_search}")
            
        except ClientError as e:
            print(f"Error getting domain URLs: {e.response['Error']['Message']}")
            raise

    def add_domain_urls(self, keyword_search: str, new_urls: List[str]) -> bool:

        try:

            keyword_search = self.normalize_keyword_search(keyword_search)

            # Convert list to set to remove any duplicates within new_urls
            unique_new_urls = set(new_urls)
            
            # First, try to get existing URLs
            try:
                existing_urls = self.get_domain_urls(keyword_search)
            except KeyError:
                existing_urls = []
            
            # Combine existing and new URLs
            all_urls = list(set(existing_urls) | unique_new_urls)
            
            # Update the item with all URLs
            self.dynamodb.update_item(
                TableName=self.table_name,
                Key={
                    'keyword_search': {'S': keyword_search}
                },
                UpdateExpression='SET domain_urls = :urls',
                ExpressionAttributeValues={
                    ':urls': {'SS': list(all_urls)}
                }
            )
            
            return True
            
        except ClientError as e:
            print(f"Error adding domain URLs: {e.response['Error']['Message']}")
            raise

    def get_all_keyword_searches(self) -> List[str]:

        try:
            keyword_searches = []
            # Initialize parameters for pagination
            scan_kwargs = {
                'TableName': self.table_name,
                'ProjectionExpression': 'keyword_search'  # Only retrieve the primary key
            }
            
            done = False
            start_key = None
            
            while not done:
                if start_key:
                    scan_kwargs['ExclusiveStartKey'] = start_key
                
                response = self.dynamodb.scan(**scan_kwargs)
                # Extract keyword_search values from the response
                items = response.get('Items', [])
                keyword_searches.extend([item['keyword_search']['S'] for item in items])
                
                # Check if there are more items to scan
                start_key = response.get('LastEvaluatedKey')
                done = start_key is None
            
            return keyword_searches
            
        except ClientError as e:
            print(f"Error retrieving all keyword searches: {e.response['Error']['Message']}")
            raise

# if __name__ == "__main__":
#     domainUrlManager = DomainUrlManager()
#     keyword_search = "Verputzer in Frohnleiten"
#     result = domainUrlManager.get_domain_urls(keyword_search)
#     print(result)
#     print(len(result))
#     print()
#     result = domainUrlManager.get_all_keyword_searches()
#     print(result)
