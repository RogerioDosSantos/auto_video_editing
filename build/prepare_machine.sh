
autoVideo::PrepareDevelopment()
{
  # Usage: PrepareDevelopment

  echo "Installing/Updating programs ... "
  sudo apt-get update \
  && sudo apt-get install -y \
      python3-venv \
      python3-pip \
  && python3 -m pip install --upgrade 
      pip \
      setuptools \
      wheel \
      ez_setup \
  && pip3 install \
      moviepy \
      vosk \
  && echo "Installing/Updating programs - DONE"
}

autoVideo::PrepareDevelop
