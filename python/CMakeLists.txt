cmake_minimum_required(VERSION 3.22)
project(raycloudtools VERSION 0.1.0 LANGUAGES CXX)

set(source_dir "${CMAKE_CURRENT_SOURCE_DIR}/..")
set(nabo_prefix "${CMAKE_CURRENT_BINARY_DIR}/libnabo-install")

if(APPLE)
  set(nabo_options -DUSE_OPEN_MP=OFF)
  list(PREPEND CMAKE_PREFIX_PATH
    /opt/homebrew/opt/eigen@3 /usr/local/opt/eigen@3
    /opt/homebrew/opt/libomp /usr/local/opt/libomp)
  find_path(omp_include omp.h PATH_SUFFIXES include REQUIRED)
  find_library(omp_library omp REQUIRED)
  set(OpenMP_CXX_FLAGS "-Xpreprocessor -fopenmp" CACHE STRING "")
  set(OpenMP_CXX_LIB_NAMES omp CACHE STRING "")
  set(OpenMP_omp_LIBRARY "${omp_library}" CACHE FILEPATH "")
  set(OpenMP_CXX_INCLUDE_DIR "${omp_include}" CACHE PATH "")
  set(CMAKE_INSTALL_RPATH "@loader_path")
else()
  set(CMAKE_INSTALL_RPATH "$ORIGIN")
endif()

find_package(Eigen3 REQUIRED)
execute_process(
  COMMAND "${CMAKE_COMMAND}" -S "${source_dir}/3rd-party/libnabo"
    -B "${CMAKE_CURRENT_BINARY_DIR}/libnabo"
    "-DCMAKE_INSTALL_PREFIX=${nabo_prefix}"
    "-DCMAKE_PREFIX_PATH=${CMAKE_PREFIX_PATH}"
    "-DEIGEN_INCLUDE_DIR=${EIGEN3_INCLUDE_DIR}"
    -DCMAKE_BUILD_TYPE=Release -DCMAKE_POSITION_INDEPENDENT_CODE=ON
    -DLIBNABO_BUILD_DOXYGEN=OFF -DLIBNABO_BUILD_EXAMPLES=OFF
    -DLIBNABO_BUILD_PYTHON=OFF -DLIBNABO_BUILD_TESTS=OFF
    ${nabo_options}
  COMMAND_ERROR_IS_FATAL ANY)
execute_process(
  COMMAND "${CMAKE_COMMAND}" --build "${CMAKE_CURRENT_BINARY_DIR}/libnabo" --parallel 2
  COMMAND_ERROR_IS_FATAL ANY)
execute_process(
  COMMAND "${CMAKE_COMMAND}" --install "${CMAKE_CURRENT_BINARY_DIR}/libnabo"
  COMMAND_ERROR_IS_FATAL ANY)

list(PREPEND CMAKE_PREFIX_PATH "${nabo_prefix}")
include_directories("${nabo_prefix}/include")
set(RAYLIB_DOUBLE_RAYS ON CACHE BOOL "")
add_subdirectory("${source_dir}" raycloud)
set_property(TARGET rayextract PROPERTY VERSION)
install(TARGETS rayextract raylib
  RUNTIME DESTINATION raycloud_tools/_native COMPONENT python
  LIBRARY DESTINATION raycloud_tools/_native COMPONENT python)
