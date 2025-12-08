cmake_minimum_required(VERSION 3.25)
project(rdkit_cpp_example LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# ------------------------------------------------------------------
# Dependencies
# ------------------------------------------------------------------
find_package(RDKit REQUIRED)
find_package(Boost CONFIG COMPONENTS iostreams timer system REQUIRED)

# ------------------------------------------------------------------
# Helper function to create executables with common settings
# ------------------------------------------------------------------
function(add_rdkit_executable TARGET_NAME SOURCE_FILE)
    add_executable(${TARGET_NAME} ${SOURCE_FILE})

    # Link libraries (passed as additional arguments)
    target_link_libraries(${TARGET_NAME} PRIVATE ${ARGN})

    # RPATH handling (Unix-like systems)
    if(APPLE)
        set_target_properties(${TARGET_NAME} PROPERTIES
                BUILD_WITH_INSTALL_RPATH TRUE
                INSTALL_RPATH "@executable_path"
        )
    elseif(UNIX)
        set_target_properties(${TARGET_NAME} PROPERTIES
                BUILD_WITH_INSTALL_RPATH TRUE
                INSTALL_RPATH "$ORIGIN"
        )
    endif()

    # Install target
    install(TARGETS ${TARGET_NAME}
            RUNTIME DESTINATION bin
            LIBRARY DESTINATION lib
            ARCHIVE DESTINATION lib
    )
endfunction()

# ------------------------------------------------------------------
# Build executables
# ------------------------------------------------------------------
add_rdkit_executable(smiles_processing
        src/cpp/smiles_processing.cpp
        RDKit::Depictor
        RDKit::MolHash
        RDKit::FileParsers
        RDKit::SmilesParse
)

add_rdkit_executable(tautomer_hash
        src/cpp/tautomer_hash.cpp
        RDKit::GraphMol
        RDKit::MolHash
        RDKit::FileParsers
        RDKit::SmilesParse
        Boost::timer
)
