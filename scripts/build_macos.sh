#!/usr/bin/env bash
set -euo pipefail

project_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
build_dir=${BUILD_DIR:-"$project_dir/build/macos"}
install_dir="$build_dir/libnabo-install"
eigen_dir=$(brew --prefix eigen@3)
openmp_dir=$(brew --prefix libomp)

EIGEN3_INC_DIR="$eigen_dir/include/eigen3" cmake \
  -S "$project_dir/3rd-party/libnabo" \
  -B "$build_dir/libnabo" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX="$install_dir" \
  -DLIBNABO_BUILD_DOXYGEN=OFF \
  -DLIBNABO_BUILD_EXAMPLES=OFF \
  -DLIBNABO_BUILD_PYTHON=OFF \
  -DLIBNABO_BUILD_TESTS=OFF
cmake --build "$build_dir/libnabo" --parallel 2
cmake --install "$build_dir/libnabo"

cmake \
  -S "$project_dir" \
  -B "$build_dir/raycloud" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="$install_dir;$openmp_dir;$eigen_dir" \
  -DCMAKE_CXX_FLAGS="-I$install_dir/include" \
  '-DOpenMP_CXX_FLAGS=-Xpreprocessor;-fopenmp' \
  -DOpenMP_CXX_LIB_NAMES=omp \
  -DOpenMP_omp_LIBRARY="$openmp_dir/lib/libomp.dylib" \
  -DOpenMP_CXX_INCLUDE_DIR="$openmp_dir/include" \
  -DRAYCLOUD_BUILD_TESTS=OFF \
  -DRAYLIB_DOUBLE_RAYS=ON \
  -DRAYLIB_WITH_LAS=OFF \
  -DRAYLIB_WITH_QHULL=OFF \
  -DRAYLIB_WITH_TBB=OFF \
  -DRAYLIB_WITH_TIFF=OFF
cmake --build "$build_dir/raycloud" --target rayextract --parallel 2

echo "rayextract: $build_dir/raycloud/raycloudtools/rayextract/rayextract"
echo "raylib: $build_dir/raycloud/raylib"
