"""
Vercel Serverless Function
Simple and clean version
"""
import json


def handler(event, context):
    """Simple handler for testing"""
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": "Hello from Vercel!",
            "status": "success"
        })
    }
