# Sentiment Analysis Workflow Integration
This guide provides an overview of setting up an automated sentiment analysis workflow using Google Cloud Functions and Zapier. This workflow triggers a sentiment analysis on a specific Google Document whenever it's updated, using predefined keywords.


### Prerequisites
- A Google Cloud Platform (GCP) account.
- A Zapier account.
- Access to Google Drive and Google Docs.
- Basic knowledge of deploying Cloud Functions in GCP.

### Google Cloud Function Setup
The provided Python script is designed to be deployed as a Google Cloud Function. It requires a service_account.json file for authentication, which should be securely stored and referenced within your code.

1. Create a Service Account in GCP:
- Navigate to the IAM & Admin -> Service Accounts in the Google Cloud Console.
- Create a new service account with appropriate permissions to access the Google Docs API.
- Generate and download a JSON key for this service account and place it in the root directory of this code (named: sevice_account.json)

2. Share Target Document:
- Share the Google Document you want to analyze with the service account's email address, providing it with at least viewer access.

3. Deploy Cloud Function:
- Use the GCP console or the gcloud CLI tool to deploy your function. Note the trigger URL upon successful deployment.
   - Follow the guide on [Deploying python functions](https://cloud.google.com/functions/docs/deploy#console)

### Zapier Workflow Setup
1. Google Drive Trigger:
    - Create a new Zap and select Google Drive as the trigger app.
    - Choose the trigger event to be "Update File."
    - Configure the trigger to monitor updates in the specific folder/document.

2. Webhooks by Zapier Action:
- For the action part of the Zap, select "Webhooks by Zapier."
- Choose "POST" as the action event.
- Set up the webhook:
    - **URL**: Use the trigger URL of your deployed Google Cloud Function.
    - **Payload Type**: json
    - **Data**: Configure the data to include doc_id and keywords. 



