function(bundle_windows target)
    if(NOT WIN32)
        return()
    endif()

    if(NOT TARGET ${target})
        message(FATAL_ERROR "Target ${target} does not exist")
    endif()

    set(DLL_DIRS "")

    # Collect all linked targets
    get_target_property(LINKED ${target} LINK_LIBRARIES)
    foreach(lib ${LINKED})
        if(TARGET ${lib})
            # Try various CMake properties for DLL location
            foreach(cfg RELEASE DEBUG RELWITHDEBINFO MINSIZEREL)
                get_target_property(loc ${lib} IMPORTED_LOCATION_${cfg})
                if(loc)
                    get_filename_component(dir "${loc}" DIRECTORY)
                    list(APPEND DLL_DIRS "${dir}")

                    # Conan DLLs typically live in ../bin
                    get_filename_component(parent "${dir}" DIRECTORY)
                    if (EXISTS "${parent}/bin")
                        list(APPEND DLL_DIRS "${parent}/bin")
                    endif()
                endif()
            endforeach()
        endif()
    endforeach()

    list(REMOVE_DUPLICATES DLL_DIRS)

    if(DLL_DIRS STREQUAL "")
        message(WARNING "bundle_windows: No DLL directories found for target ${target}")
        return()
    endif()

    install(CODE "
        message(STATUS \"Bundling DLLs for ${target}...\")
        file(GET_RUNTIME_DEPENDENCIES
            EXECUTABLES \$<TARGET_FILE:${target}>
            RESOLVED_DEPENDENCIES_VAR RESOLVED
            UNRESOLVED_DEPENDENCIES_VAR UNRESOLVED
            DIRECTORIES ${DLL_DIRS}
        )

        if(UNRESOLVED)
            message(WARNING \"Unresolved DLLs:\")
            foreach(u \${UNRESOLVED})
                message(WARNING \"  - \${u}\")
            endforeach()
        endif()

        foreach(dep \${RESOLVED})
            get_filename_component(name \"\${dep}\" NAME)
            file(INSTALL \"\${dep}\" DESTINATION \"${CMAKE_INSTALL_PREFIX}/bin\")
        endforeach()
    ")
endfunction()
