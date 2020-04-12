# GPUs are distributed amongst preemptible workers

gcloud dataproc clusters create $CLUSTER_NAME \
--project $PROJECT_ID --region $REGION --zone=$ZONE \
--master-machine-type $MASTER_MCHN_TYPE --master-boot-disk-size $MASTER_SD_SIZE \
--num-preemptible-workers $NUM_WORKERS --worker-machine-type $WORKER_MCHN_TYPE \
--worker-boot-disk-size $WORKER_SD_SIZE \
--preemptible-worker-accelerator type=$WORKER_ACCELERATOR_TYPE,count=$WORKER_ACCELERATOR_COUNT \
--image-version $IMAGE_VERSION --optional-components ANACONDA \
--metadata 'PIP_PACKAGES=pandas==0.23.0 scipy==1.1.0 tensorflow==2.1.0 keras matplotlib sentencepiece tensorflow_hub bert-for-tf2' \
--metadata install-gpu-agent=true \
--initialization-actions gs://$BUCKET_NAME/initialization-actions.sh,gs://goog-dataproc-initialization-actions-${REGION}/python/pip-install.sh,gs://goog-dataproc-initialization-actions-${REGION}/gpu/install_gpu_driver.sh,gs://$BUCKET_NAME/cuda-setup.sh


