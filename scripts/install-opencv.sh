############################################################################
# Copyright (C) 2024-2025 Nand Compute LLC | All Rights Reserved
############################################################################
#!/bin/sh

GIT_TAG="4.11.0"
WORK_DIR="${HOME}"

# Github repos
OPENCV_GIT_URL="https://github.com/opencv/opencv.git"
CONTRIB_GIT_URL="https://github.com/opencv/opencv_contrib.git"

# Installation directories / files
OPENCV_HEADERS="/usr/local/include/opencv*"
OPENCV_SHARE_1="/usr/local/share/OpenCV"
OPENCV_SHARE_2="/usr/local/share/opencv*"
OPENCV_LIBS="/usr/local/lib/libopencv*"

# Raspberry Pi needs >5.8GB of memory to build OpenCV from source.
#   - 1GB of RAM, need ~5GB of SWAP or 5120
#   - 2GB of RAM, need ~4GB of SWAP or 4096
#   - 4GB of RAM, need ~2GB of SWAP or 2048
#   - 8GB of RAM, need  0GB of SWAP
TEMP_SWAP_SIZE=0

expand_swap(){
  SWAP_SIZE=$1
  sudo sed -i 's/CONF_MAXSWAP=2048/CONF_MAXSWAP=${SWAP_SIZE}/g' /sbin/dphys-swapfile
  sudo sed -i 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=${SWAP_SIZE}/g' /etc/dphys-swapfile
  sudo /etc/init.d/dphys-swapfile stop
  sudo /etc/init.d/dphys-swapfile start 
}

shrink_swap(){
  SWAP_SIZE=$1
  sudo sed -i 's/CONF_MAXSWAP=${SWAP_SIZE}/CONF_MAXSWAP=2048/g' /sbin/dphys-swapfile
  sudo sed -i 's/CONF_SWAPSIZE=${SWAP_SIZE}/CONF_SWAPSIZE=100/g' /etc/dphys-swapfile
  sudo /etc/init.d/dphys-swapfile stop
  sudo /etc/init.d/dphys-swapfile start 
}

case "$1" in
download)
(
  sudo apt-get install -y git
  mkdir -p $WORK_DIR && cd $WORK_DIR
  
  # To prevent downloading entire repo use: --depth 1 --branch ${GIT_TAG}
  git clone --depth 1 --branch ${GIT_TAG} $OPENCV_GIT_URL
  git clone --depth 1 --branch ${GIT_TAG} $CONTRIB_GIT_URL
)
  ;;
build)
(
  # Install dependencies 
  # You may not need all of them if you are building others from source, i.e. Eigen.
  sudo apt-get update
  sudo apt-get -y install cmake build-essential git pkg-config
  sudo apt-get -y install gcc g++
  sudo apt-get -y install gfortran
  sudo apt-get -y  install libatlas-base-dev
  sudo apt-get -y install libtbb2 libtbb-dev libdc1394-22-dev
  sudo apt-get -y install python3-dev python3-numpy
  sudo apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
  sudo apt-get -y install libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev
  sudo apt-get -y install libgtk2.0-dev libgtk-3-dev
  sudo apt-get -y install libjpeg-dev libpng-dev libtiff-dev
  sudo apt-get -y install libxvidcore-dev libx264-dev
  sudo apt-get -y install openexr libopenexr-dev
  sudo apt-get -y install libwebp-dev
  
  # Checkout target version
  cd $WORK_DIR/opencv_contrib
  git checkout $GIT_TAG
  cd $WORK_DIR/opencv
  git checkout $GIT_TAG
  
  # Expand swap
  expand_swap ${TEMP_SWAP_SIZE}
  
  # Configure the build
  rm -r ./cmake-build
  mkdir -p cmake-build && cd cmake-build
  
  # Run cmake
  cmake .. \
    -DOPENCV_EXTRA_MODULES_PATH=$WORK_DIR/opencv_contrib/modules \
    -DCMAKE_INSTALL_PREFIX=/usr/local \
    -DCMAKE_BUILD_TYPE=Release
    
  # Build and install
  make -j4
  sudo make install
  sudo ldconfig
  make clean
  
  # Shrink / revert swap
  shrink_swap ${TEMP_SWAP_SIZE}
)
  ;;
remove)
(
  rm -rf $WORK_DIR/opencv
  rm -rf $WORK_DIR/opencv_contrib
)
  ;;
uninstall)
  sudo rm -rf $OPENCV_HEADERS
  sudo rm -rf $OPENCV_SHARE_1
  sudo rm -rf $OPENCV_SHARE_2
  sudo rm $OPENCV_LIBS
  ;;
*)
  echo "Usage: $0 {download|build|remove|uninstall}"
  exit 1
  ;;
esac

exit 0
