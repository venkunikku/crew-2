## Setting up Dataproc cluster

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
