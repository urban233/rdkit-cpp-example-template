# ------------------------------------------------------------------
# Unix/MacOS library bundling
# ------------------------------------------------------------------
include(BundleUtilities)

install(CODE "
    message(STATUS \"Bundling Unix/macOS shared library dependencies...\")

    file(MAKE_DIRECTORY \"${CMAKE_INSTALL_PREFIX}/lib\")

    fixup_bundle(
        \"${CMAKE_INSTALL_PREFIX}/bin/sample\"
        \"\"
        \"${CMAKE_INSTALL_PREFIX}/lib\"
    )
")
