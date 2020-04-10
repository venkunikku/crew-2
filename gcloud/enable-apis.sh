# Note: Billing must we enabled prior

gcloud config set project $PROJECT_ID
gcloud services enable dataproc.googleapis.com --project $PROJECT_ID
gcloud services enable cloudbilling.googleapis.com --project $PROJECT_ID
gcloud services enable compute.googleapis.com --project $PROJECT_ID
gcloud services enable cloudapis.googleapis.com --project $PROJECT_ID
gcloud services enable cloudresourcemanager.googleapis.com --project $PROJECT_ID
gcloud services enable dns.googleapis.com --project $PROJECT_ID
gcloud services enable iam.googleapis.com --project $PROJECT_ID
gcloud services enable iamcredentials.googleapis.com --project $PROJECT_ID
gcloud services enable servicemanagement.googleapis.com --project $PROJECT_ID
gcloud services enable serviceusage.googleapis.com --project $PROJECT_ID
gcloud services enable storage-api.googleapis.com --project $PROJECT_ID
gcloud services enable storage-component.googleapis.com --project $PROJECT_ID
