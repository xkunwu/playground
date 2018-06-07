cmake_minimum_required(VERSION 2.8.3)
FIND_PACKAGE(PythonInterp)
FIND_PACKAGE(PythonLibs)
FIND_PACKAGE(Boost COMPONENTS python)

INCLUDE_DIRECTORIES(${Boost_INCLUDE_DIRS} ${PYTHON_INCLUDE_DIRS})

#PYTHON_ADD_MODULE(hello_ext SHARED hello.cpp)
add_library(hello_ext SHARED hello.cpp)
target_link_libraries( hello_ext ${Boost_LIBRARIES} )
set_target_properties( hello_ext PROPERTIES PREFIX "" )
FILE(COPY hello.py DESTINATION .)
