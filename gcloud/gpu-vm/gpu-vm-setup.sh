# Prophylactically update all the packages, optional.
sudo apt -y update && sudo apt -y upgrade

sudo apt-get install -yq python3 python3-pip libsndfile1-dev
pip3 install wrapt --upgrade --ignore-installed
pip3 install pandas
pip3 install scipy 
pip3 install tensorflow-gpu
pip3 install keras
pip3 install tensorflow_hub
pip3 install pomegranate==0.10
pip3 install cupy
pip3 install gcsfs
pip3 install jupyter
pip3 install librosa
pip3 install soundfile
pip3 install python_speech_features
pip3 install pydub
pip3 install --upgrade google-cloud-storage
pip3 install wave
pip3 install hmmlearn

# cloning repo of interest
git clone https://github.com/venkunikku/crew-2.git

# jupyter starting script
gsutil cp gs://ad-bucket-15730/start-jupyter.sh /start-jupyter.sh

### Set up for Cuda 10.1, cuDNN 7.6.5 ###

# Add NVIDIA package repositories
sudo wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-repo-ubuntu1804_10.1.243-1_amd64.deb
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
sudo dpkg -i cuda-repo-ubuntu1804_10.1.243-1_amd64.deb
sudo apt-get update
sudo wget http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb
sudo apt install -y ./nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb
sudo apt-get update

# Install NVIDIA driver
sudo apt-get install -y --no-install-recommends nvidia-driver-430
# Doesn't hurt to reboot here and check to see if GPUs are visible via `nvidia-smi`

# Install development and runtime libraries (~4GB)
sudo apt-get install -y --no-install-recommends \
    cuda-10-1 \
    libcudnn7=7.6.4.38-1+cuda10.1  \
    libcudnn7-dev=7.6.4.38-1+cuda10.1


# Install TensorRT. Requires that libcudnn7 is installed above.
sudo apt-get install -y --no-install-recommends libnvinfer6=6.0.1-1+cuda10.1 \
    libnvinfer-dev=6.0.1-1+cuda10.1 \
    libnvinfer-plugin6=6.0.1-1+cuda10.1                                       

# changing ownership for write access to repo
sudo chown -R chrisolen:chrisolen /crew-2

# initializing gh account
#cd ../../crew-2 && git config --global user.name "chrisolen1"
