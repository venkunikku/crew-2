## Start up a vm with a GPU accelerator:

```
sh start-gpu-vm.sh
```

## Once the vm is live

On one shell, ssh into the vm. This will log you in as root:

```
sh ssh.sh
```

You will need to set up all of the dependencies defined in gpu-vm-setup.sh. Move back to the root directory and:

```
sh gpu-vm-setup.sh
```

Note that this might take around 10-15 minutes. Note also that this is where you might pre-define a Github repo to clone.

If you want to use jupyter, in the root directory:

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
