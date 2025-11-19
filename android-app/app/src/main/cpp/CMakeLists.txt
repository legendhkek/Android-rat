cmake_minimum_required(VERSION 3.18.1)

project("apkmodifier")

# Enable C++14
set(CMAKE_CXX_STANDARD 14)

# Compile with optimizations for FUD
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3 -fvisibility=hidden -ffunction-sections -fdata-sections")
set(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE} -O3 -fvisibility=hidden -ffunction-sections -fdata-sections")

# Strip symbols for obfuscation
set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -Wl,--gc-sections -Wl,--strip-all")

add_library(
    native-lib
    SHARED
    native-lib.cpp
)

find_library(
    log-lib
    log
)

target_link_libraries(
    native-lib
    ${log-lib}
)
