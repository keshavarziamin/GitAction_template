cmake_minimum_required(VERSION 3.10)
set (PROJECT_NAME Test-CICD VERSION 1.1.0)

project(${PROJECT_NAME})
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_C_STANDARD 11)

#add cserial library
include_directories(
    ${PROJECT_SOURCE_DIR}/src/sort)


#make executable file
set(EXE_FILE ${PROJECT_NAME}_exe )
add_executable(${EXE_FILE} example.c)
target_link_libraries(${EXE_FILE} cserial)


# add test framework
enable_testing() # enable ctest
add_subdirectory(test)
