cmake_minimum_required(VERSION 3.4)
project(cmake_wrapper)

if(WIN32 AND BUILD_SHARED_LIBS)
    set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif()

include(conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

add_definitions(-D_SILENCE_EXPERIMENTAL_FILESYSTEM_DEPRECATION_WARNING)
add_subdirectory(source_subfolder)
