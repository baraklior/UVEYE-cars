ARG CUDA="10.2"
ARG CUDNN="8"

FROM nvidia/cuda:${CUDA}-cudnn${CUDNN}-devel-ubuntu16.04

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# install basics
RUN apt-get update -y \
 && apt-get install -y apt-utils git curl ca-certificates bzip2 cmake tree htop bmon iotop \
 && apt-get install -y libglib2.0-0 libsm6 libxext6 libxrender-dev libgl1-mesa-glx

# Install Miniconda
RUN curl -so /miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
 && chmod +x /miniconda.sh \
 && /miniconda.sh -b -p /miniconda \
 && rm /miniconda.sh

ENV PATH /miniconda/bin:$PATH:

# Create a Python 3.6 environment
RUN /miniconda/bin/conda install -y conda-build \
 && /miniconda/bin/conda create -y --name py37 python=3.7 \
 && /miniconda/bin/conda clean -ya

ENV CONDA_DEFAULT_ENV=py37
ENV CONDA_PREFIX=/miniconda/envs/$CONDA_DEFAULT_ENV
ENV PATH=$CONDA_PREFIX/bin:$PATH
ENV CONDA_AUTO_UPDATE_CONDA=false

RUN conda install -y ipython pytorch torchvision cudatoolkit=10.2 -c pytorch \
    && pip install ninja yacs cython matplotlib opencv-python flask
    #NOTE: Python 3.9 users will need to add '-c=conda-forge' for installation

# install pycocotools
RUN git clone https://github.com/cocodataset/cocoapi.git \
 && cd cocoapi/PythonAPI \
 && python setup.py build_ext install

# install PyTorch Detection
COPY . .
ENV FORCE_CUDA="1"
# RUN git clone https://github.com/facebookresearch/maskrcnn-benchmark.git \
RUN cd maskrcnn-benchmark \
 && python setup.py build develop

WORKDIR /car_server
CMD ["python", "./server.py"]

