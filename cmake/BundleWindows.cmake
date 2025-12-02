# ------------------------------------------------------------------
# Windows runtime bundling (DLL copying)
# ------------------------------------------------------------------

if(NOT EXISTS "${CONDA_DLL_DIR}")
    message(WARNING "Conda DLL directory not found, skipping DLL bundling.")
    return()
endif()

# Add Conda DLL directory so CMake can search for DLLs
list(APPEND CMAKE_INSTALL_SYSTEM_RUNTIME_LIBS "${CONDA_DLL_DIR}")

# Force CMake to treat Conda DLLs as possible dependencies
file(GLOB CONDA_DLLS "${CONDA_DLL_DIR}/*.dll")
set_property(TARGET sample APPEND PROPERTY
    IMPORTED_LOCATION "${CONDA_DLLS}"
)

# Install rule
install(CODE "
    message(STATUS \"Bundling Windows DLL dependencies...\")

    file(GET_RUNTIME_DEPENDENCIES
        EXECUTABLES \$<TARGET_FILE:sample>
        RESOLVED_DEPENDENCIES_VAR RESOLVED
        UNRESOLVED_DEPENDENCIES_VAR UNRESOLVED
        DIRECTORIES \"${CONDA_DLL_DIR}\"
    )

    if(UNRESOLVED)
        message(WARNING \"Unresolved DLLs:\")
        foreach(u \${UNRESOLVED})
            message(WARNING \"  - \${u}\")
        endforeach()
    endif()

    message(STATUS \"Copying resolved dependencies:\")
    foreach(dep \${RESOLVED})
        get_filename_component(name \"\${dep}\" NAME)
        message(STATUS \"  - \${name}\")
        file(INSTALL \"\${dep}\" DESTINATION \"${CMAKE_INSTALL_PREFIX}/bin\")
    endforeach()
")
