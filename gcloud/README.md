# spark-on-gcp

Simple way to spin up cluster for ML/DL tasks on GCP without Docker/Kubernetes.

Note you will need a valid GCP account and the gcloud_sdk installed on your local device.

## Initial Setup

Begin by initializing environmental variables in the var directory. Choose the .rc script that works best for your purposes, depending on your memory, processing, and GPU requirements. You will also need to rename some of the environmental variables for your own purposes:

```
source var/high-mem-gpu.rc
```

Create a new GCP project:

```
sh create-gcp-project.sh
```

Enable the relevant APIs. Note that you may have to manually enable billing:

```
sh enable-apis.sh
```

Create new storage bucket:

```
sh create-gcs.sh
```

Sends initialization scripts to GCS. This will copy cuda-setup.sh, cluster-init-actions.sh, start-jupyter.sh, and vm-init-actions to GCS:

```
sh scripts-to-gcs.sh
```



































