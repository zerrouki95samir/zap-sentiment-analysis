from google.oauth2 import service_account
from googleapiclient.discovery import build
from textblob import TextBlob
import re
import json


def analyze_doc_keywords_sentiment(doc_id, keywords):
    # Authenticate and build the Docs service
    creds = service_account.Credentials.from_service_account_file('./service_account.json', scopes=['https://www.googleapis.com/auth/documents.readonly'])
    service = build('docs', 'v1', credentials=creds)

    # Fetch the document content
    doc = service.documents().get(documentId=doc_id).execute()
    text = read_document_text(doc)

    # Initialize results dictionary
    results = {keyword: {'occurrences': 0, 'positive': 0, 'neutral': 0, 'negative': 0} for keyword in keywords}

    # Analyze the text
    for paragraph in text.split('\n'):
        paragraph_lower = paragraph.lower()  # Use lower case for case-insensitive search
        for keyword in keywords:
            keyword_lower = keyword.lower()
            for match in re.finditer(r'\b{}\b'.format(re.escape(keyword_lower)), paragraph_lower):
                # Count keyword occurrence
                results[keyword]['occurrences'] += 1
                
                # Extract and analyze sentiment of text following the keyword
                start_pos = match.end()
                snippet = paragraph[start_pos:].strip()
                if snippet:  # Ensure there is text to analyze
                    sentiment = TextBlob(snippet).sentiment.polarity
                    if sentiment > 0:
                        results[keyword]['positive'] += 1
                    elif sentiment < 0:
                        results[keyword]['negative'] += 1
                    else:
                        results[keyword]['neutral'] += 1

    return results

def read_document_text(document):
    """Extracts and returns the text from a Google Doc document."""
    doc_content = document.get('body').get('content')
    text = ""
    for element in doc_content:
        if 'paragraph' in element:
            for para_element in element.get('paragraph').get('elements'):
                if 'textRun' in para_element:
                    text += para_element.get('textRun').get('content')
    return text


def analyze_doc_keywords_sentiment_http(request):
    # Set CORS headers for the preflight request
    if request.method == "OPTIONS":
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }

        return ("", 204, headers)
    
    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Allow-Origin': '*'
    }

    request_json = request.get_json(silent=True)

    if request_json and 'doc_id' in request_json and 'keywords' in request_json:
        doc_id = request_json['doc_id']
        keywords = [keyword.strip() for keyword in request_json['keywords'].split(',')]
    else:
        return ('Missing "doc_id" or "keywords" in the request', 400, headers)
    
    # Your existing logic here...
    results = analyze_doc_keywords_sentiment(doc_id, keywords)
    return (results, 200, headers)


# # Example usage
# doc_id = '1-3jTHpowWyb5cgH_OoK8DjuzfqWnzFSwA4DV8fXFNyQ'
# keywords = ['Bortezomib', 'Lenalidomide', 'Carfilzomib', 'Daratumumab']
# analysis_results = analyze_doc_keywords_sentiment(doc_id, keywords)
# print(analysis_results)