# cmake/BundleUnix.cmake

function(bundle_unix target)
    if(NOT TARGET ${target})
        message(FATAL_ERROR "Target ${target} does not exist")
    endif()

    include(BundleUtilities)

    install(CODE "
        message(STATUS \"Bundling Unix/macOS shared libraries for target ${target}...\")

        file(MAKE_DIRECTORY \"${CMAKE_INSTALL_PREFIX}/lib\")

        fixup_bundle(
            \"${CMAKE_INSTALL_PREFIX}/bin/\$<TARGET_FILE_NAME:${target}>\"
            \"\"
            \"${CMAKE_INSTALL_PREFIX}/lib\"
        )
    ")
endfunction()
