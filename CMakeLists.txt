cmake_minimum_required(VERSION 3.25)
project(advanced_depict LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Set a default install dir (local)
set(CMAKE_INSTALL_PREFIX "${CMAKE_BINARY_DIR}/dist" CACHE PATH "" FORCE)
message(STATUS "Install prefix: ${CMAKE_INSTALL_PREFIX}")

set(CONDA_DLL_DIR "${CMAKE_SOURCE_DIR}/.conda-env/Library/bin")
message(STATUS "Using Conda DLL directory: ${CONDA_DLL_DIR}")
# ------------------------------------------------------------------
# Modules
# ------------------------------------------------------------------
list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")

# ------------------------------------------------------------------
# Dependencies
# ------------------------------------------------------------------
find_package(RDKit REQUIRED)
find_package(Boost CONFIG COMPONENTS iostreams timer system REQUIRED)

# ------------------------------------------------------------------
# Build executable
# ------------------------------------------------------------------
set(SOURCES
    src/cpp/smiles_processing.cpp
)
add_executable(smiles_processing ${SOURCES})
target_link_libraries(smiles_processing
    PRIVATE
    RDKit::MolHash
    RDKit::FileParsers
    RDKit::SmilesParse
)

add_executable(tautomer_hash
    src/cpp/tautomer_hash.cpp
)
target_link_libraries(tautomer_hash
    RDKit::MolHash
    RDKit::FileParsers
    RDKit::SmilesParse
    Boost::timer
)

# ------------------------------------------------------------------
# RPATH (Unix)
# ------------------------------------------------------------------
if(APPLE)
    set_target_properties(smiles_processing PROPERTIES
        INSTALL_RPATH "@executable_path/../lib"
    )
elseif(UNIX)
    set_target_properties(smiles_processing PROPERTIES
        INSTALL_RPATH "\$ORIGIN/../lib"
        INSTALL_RPATH_USE_LINK_PATH TRUE
    )
endif()

# ------------------------------------------------------------------
# Install base targets
# ------------------------------------------------------------------
install(TARGETS smiles_processing
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
)

# ------------------------------------------------------------------
# Bundling logic
# ------------------------------------------------------------------
if(WIN32)
    include(BundleWindows)
    bundle_windows(smiles_processing)
    bundle_windows(tautomer_hash)
elseif(UNIX)
    include(BundleUnix)
    bundle_windows(smiles_processing)
    bundle_windows(tautomer_hash)
endif()
