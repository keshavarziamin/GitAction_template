
include(GoogleTest)
add_subdirectory(googletest)
include_directories(${gtest_SOURCE_DIR}/include ${gtest_SOURCE_DIR})

set(UNIT_TEST_FILES_DIR ${CMAKE_CURRENT_SOURCE_DIR}/unit_test)
file(GLOB UNIT_TEST_FILES ${UNIT_TEST_FILES_DIR}/test_*.cpp)

set(TEST_NAME test_sort)

add_executable(${TEST_NAME} 
    ${UNIT_TEST_FILES_DIR}/main.cpp ${UNIT_TEST_FILES})

target_link_libraries(${TEST_NAME} gtest gtest_main)   

# link your libraries to gtest
target_link_libraries(${TEST_NAME} cserial)



include(GoogleTest)
gtest_discover_tests(${TEST_NAME})