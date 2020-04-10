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

## Setting up Dataproc cluster

Sends initialization scripts to GCS. This will copy cuda-setup.sh, initialization-actions.sh, and sh start-jupyter.sh to GCS:

```
sh scripts-to-gcs.sh
```

### If you want to start a cluster with a GPU accelerator on the master:

```
sh start-gpu-cluster.sh
```

### If you want to start a cluster with a GPU accelerator on preemptive workers (not tested yet):

```
sh start-dist-gpu-cluster.sh
```

### If you want to start a cluster without GPUs:

```
sh start-cluster.sh
```

## Once the cluster is live

On one shell, ssh into the master:

```
sh ssh.sh
```

If you want to use jupyter, cd ../.. into the root directory and:

```
sh start-jupyter.sh
```

Note: You will need to create a password for access to jupyter:

On another shell, open up an ssh tunnel so that we can access a running jupyter server:

```
sh jupyter-tunnel.sh
```

In your browser, enter the following link and follow the prompt to input your chosen password:

```
localhost:1080/tree
```



































