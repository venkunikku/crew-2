gcloud dataproc clusters create sarc-cluster --region $REGION \
--master-machine-type $MASTER_MCHN_TYPE --num-masters $NUM_MASTERS --master-boot-disk-size $MASTER_SD_SIZE \
--worker-machine-type $WORKER_MCHN_TYPE --num-workers $NUM_WORKERS --worker-boot-disk-size $WORKER_SD_SIZE \
--image-version $IMAGE_VERSION --optional-components ANACONDA \
--metadata 'PIP_PACKAGES=pandas==0.23.0 scipy==1.1.0 tensorflow keras matplotlib sentencepiece tensorflow_hub bert-for-tf2' \
--metadata install-gpu-agent=true \
--initialization-actions gs://$BUCKET_NAME/initialization-actions.sh,gs://goog-dataproc-initialization-actions-${REGION}/python/pip-install.sh,gs://goog-dataproc-initialization-actions-${REGION}/gpu/install_gpu_driver.sh 
