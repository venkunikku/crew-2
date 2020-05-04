sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get install -y python3-dev python3-pip \
     build-essential libssl-dev libffi-dev \
     libxml2-dev libxslt1-dev zlib1g-dev libsndfile1-dev

# generate python
pip3 install pandas
pip3 install numpy

# general audio dependencies
sudo apt-get install python3-pyaudio
pip3 install PyAudio
pip3 install python_speech_features
pip3 install scipy
pip3 install scikit-learn

# hmm dependencies
pip3 install hmmlearn
pip3 install pomegranate==0.10


# NN dependencies
pip3 install tensorflow
pip3 install keras
pip3 install sklearn


# Streaming audio
pip3 install librosa
#pip3 install pyaudio
pip3 install wave
pip3 install time
pip3 install sys


