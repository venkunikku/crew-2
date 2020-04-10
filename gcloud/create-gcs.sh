# create bucket
gsutil mb -l $REGION -p $PROJECT_ID gs://${BUCKET_NAME}/ 

#sleep 5

# create service account
#gcloud iam service-accounts create $BUCKET_SA --display-name $BUCKET_SA

#sleep 5

# make service account an admin of storage bucket
#export SA_EMAIL=$(gcloud iam service-accounts list --filter="displayName:$BUCKET_SA" --format='value(email)')
#gcloud projects add-iam-policy-binding $PROJECT_ID --member serviceAccount:$SA_EMAIL --role roles/storage.admin
