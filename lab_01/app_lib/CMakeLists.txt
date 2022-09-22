cmake_minimum_required(VERSION 3.22)
project(app_lib C)

set(CMAKE_C_STANDARD 99)

add_library(app_lib library.c library.h)