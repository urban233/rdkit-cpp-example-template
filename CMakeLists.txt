cmake_minimum_required(VERSION 3.25)
project(advanced_depict LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_STANDARD_REQUIRED True)
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
    RDKit::Depictor
    RDKit::MolHash
    RDKit::FileParsers
    RDKit::SmilesParse
)

#add_executable(tautomer_hash
#    src/cpp/tautomer_hash.cpp
#)
#target_link_libraries(tautomer_hash
#    RDKit::MolHash
#    RDKit::FileParsers
#    RDKit::SmilesParse
#    Boost::timer
#)

# ------------------------------------------------------------------
# RPATH (Unix)
# ------------------------------------------------------------------
#if(APPLE)
#    set_target_properties(smiles_processing PROPERTIES
#        INSTALL_RPATH "@executable_path/../lib"
#    )
#elseif(UNIX)
#    set_target_properties(smiles_processing PROPERTIES
#        INSTALL_RPATH "\$ORIGIN/../lib"
#        INSTALL_RPATH_USE_LINK_PATH TRUE
#    )
#endif()

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
set(CMAKE_INSTALL_PREFIX ${CMAKE_BINARY_DIR}/install CACHE PATH "" FORCE)

#if(WIN32)
#    # Copy DLLs at install time (CMake ≥ 3.21)
#    install(TARGETS smiles_processing
#            RUNTIME DESTINATION bin
#            RUNTIME_DEPENDENCIES
#            POST_EXCLUDE_REGEXES ".*system32/.*"
#    )
#    include(BundleWindows)
#    bundle_windows(smiles_processing)
#    bundle_windows(tautomer_hash)
#elseif(UNIX)
#    include(BundleUnix)
#    bundle_windows(smiles_processing)
#    bundle_windows(tautomer_hash)
#endif()
