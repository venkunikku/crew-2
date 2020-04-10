# tensorflow dependency
pip install wrapt --upgrade --ignore-installed

# cloning repo of interest
git clone https://github.com/venkunikku/crew-2.git

# jupyter starting script
gsutil cp gs://ad-bucket-1/start-jupyter.sh /start-jupyter.sh

# changing ownership for write access to repo
sudo chown -R chrisolen:chrisolen /crew-2

# initializing gh account
#cd ../../crew-2 && git config --global user.name "chrisolen1"
