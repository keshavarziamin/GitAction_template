cmake_minimum_required(VERSION 3.10)
set (PROJECT_NAME Test-CICD VERSION 1.1.0)

project(${PROJECT_NAME})
set(CMAKE_CXX_STANDARD 20)
# set(CMAKE_C_STANDARD 11)



#add library directory
set(SORT_DIR ${CMAKE_SOURCE_DIR}/src/sort)
include_directories(${SORT_DIR}) #include files
#add library
set(SORT_LIB sort)
file(GLOB SORT_FILES ${SORT_DIR}/*.cpp ${SORT_DIR}/*.hpp)
add_library(${SORT_LIB} ${SORT_FILES})

#make executable file
set(EX_DIR ${CMAKE_SOURCE_DIR}/src/simple-example) #add exmaple directory

set(EX_FILE ${EX_DIR}/example1.cpp)
set(EX_EXE ex1)
add_executable(${EX_EXE} ${EX_FILE})
target_link_libraries(${EX_EXE} PUBLIC ${SORT_LIB})


# add test framework
enable_testing() # enable ctest
add_subdirectory(test)
