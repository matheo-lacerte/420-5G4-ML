cmake_minimum_required(VERSION 3.21)
project(bibliotheque)

set(CORE_SOURCES
    book.cpp
    filemanager.cpp
    library.cpp
    user.cpp
)

add_library(bibliotheque_core STATIC ${CORE_SOURCES})
set_target_properties(bibliotheque_core PROPERTIES POSITION_INDEPENDENT_CODE ON)
add_executable(${PROJECT_NAME} main.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE bibliotheque_core)

# Specifie qu'on veut la version C++17 du langage
set_target_properties(bibliotheque_core ${PROJECT_NAME} PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED YES
    CXX_EXTENSIONS NO
)

# flag pour tous les warnings possible
target_compile_options(bibliotheque_core PRIVATE -Wall -Wextra -Wpedantic)
target_compile_options(${PROJECT_NAME} PRIVATE -Wall -Wextra -Wpedantic)

find_package(Python3 COMPONENTS Interpreter Development.Module REQUIRED)
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(bibliotheque_cpp bindings.cpp)
target_link_libraries(bibliotheque_cpp PRIVATE bibliotheque_core)
target_compile_options(bibliotheque_cpp PRIVATE -Wall -Wextra -Wpedantic)
