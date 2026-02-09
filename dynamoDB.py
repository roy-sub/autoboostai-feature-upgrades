import boto3
from typing import List
from botocore.exceptions import ClientError
from config import settings

class DomainUrlManager:
    
    def __init__(self):
        self.dynamodb = boto3.client(
            'dynamodb',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.table_name = settings.DYNAMODB_TABLE_NAME
    
    def _normalize_keyword(self, keyword: str) -> str:
        return keyword.lower().strip().replace(" ", "+")

    def get_domain_urls(self, keyword: str) -> List[str]:
        try:
            response = self.dynamodb.get_item(
                TableName=self.table_name,
                Key={'keyword_search': {'S': self._normalize_keyword(keyword)}}
            )
            
            if 'Item' in response and 'domain_urls' in response['Item']:
                return list(response['Item']['domain_urls']['SS'])
            return []
            
        except ClientError:
            return []

    def add_domain_urls(self, keyword: str, new_urls: List[str]) -> bool:
        if not new_urls:
            return True
            
        try:
            normalized = self._normalize_keyword(keyword)
            existing = set(self.get_domain_urls(keyword))
            all_urls = list(existing | set(new_urls))
            
            if not all_urls:
                return True
            
            self.dynamodb.update_item(
                TableName=self.table_name,
                Key={'keyword_search': {'S': normalized}},
                UpdateExpression='SET domain_urls = :urls',
                ExpressionAttributeValues={':urls': {'SS': all_urls}}
            )
            return True
            
        except ClientError:
            return False

    def get_all_keywords(self) -> List[str]:
        try:
            keywords = []
            scan_kwargs = {
                'TableName': self.table_name,
                'ProjectionExpression': 'keyword_search'
            }
            
            while True:
                response = self.dynamodb.scan(**scan_kwargs)
                keywords.extend([item['keyword_search']['S'] for item in response.get('Items', [])])
                
                if 'LastEvaluatedKey' not in response:
                    break
                scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
            
            return keywords
            
        except ClientError:
            return []
