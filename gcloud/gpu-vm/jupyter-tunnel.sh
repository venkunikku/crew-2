gcloud compute ssh $VM_NAME --project=$PROJECT_ID -- -L 1080:$VM_NAME:8888 -N -n
