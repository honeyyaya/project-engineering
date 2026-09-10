cmake_minimum_required(VERSION 3.16)
project(EngineeringGuardQueue LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
find_package(Qt5 REQUIRED COMPONENTS Core)
enable_testing()

add_executable(queue_tests tests/queue_tests.cpp)
target_include_directories(queue_tests PRIVATE src)
target_link_libraries(queue_tests PRIVATE Qt5::Core)
foreach(case_name fifo capacity empty overload zero)
    add_test(NAME queue_${case_name} COMMAND queue_tests ${case_name})
endforeach()

# Deliberately flawed baseline, never used as the implementation target.
add_executable(queue_negative_control tests/queue_tests.cpp)
target_include_directories(queue_negative_control PRIVATE negative-control)
target_link_libraries(queue_negative_control PRIVATE Qt5::Core)
