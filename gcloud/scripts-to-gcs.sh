gsutil cp ./cluster/cluster-init-actions.sh gs://$BUCKET_NAME

gsutil cp ./start-jupyter.sh gs://$BUCKET_NAME

gsutil cp ./cluster/cuda-setup.sh gs://$BUCKET_NAME

gsutil cp ./gpu-vm/gpu-vm-setup.sh gs://$BUCKET_NAME
