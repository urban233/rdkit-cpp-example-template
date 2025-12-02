# cmake/BundleWindows.cmake

function(bundle_windows target)
    if(NOT TARGET ${target})
        message(FATAL_ERROR "Target ${target} does not exist")
    endif()

    if(NOT EXISTS "${CONDA_DLL_DIR}")
        message(WARNING "Conda DLL directory not found, skipping DLL bundling for ${target}")
        return()
    endif()

    install(CODE "
        message(STATUS \"Bundling Windows DLL dependencies for target ${target}...\")

        file(GET_RUNTIME_DEPENDENCIES
            EXECUTABLES \$<TARGET_FILE:${target}>
            RESOLVED_DEPENDENCIES_VAR RESOLVED
            UNRESOLVED_DEPENDENCIES_VAR UNRESOLVED
            DIRECTORIES \"${CONDA_DLL_DIR}\"
        )

        if(UNRESOLVED)
            message(WARNING \"Unresolved DLLs for ${target}:\")
            foreach(u \${UNRESOLVED})
                message(WARNING \"  - \${u}\")
            endforeach()
        endif()

        message(STATUS \"Copying resolved dependencies for ${target}:\")
        foreach(dep \${RESOLVED})
            get_filename_component(name \"\${dep}\" NAME)
            message(STATUS \"  - \${name}\")
            file(INSTALL \"\${dep}\" DESTINATION \"${CMAKE_INSTALL_PREFIX}/bin\")
        endforeach()
    ")
endfunction()
