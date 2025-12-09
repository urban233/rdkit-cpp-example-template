# ----------------------------------------------------------------------------#
# This file contains source code for the rdkit-cpp-example-template repository
# copyright (c) 2025 by Martin Urban.
# It is unlawful to modify or remove this copyright notice.
# Please see the accompanying LICENSE file for further information.
# ----------------------------------------------------------------------------#
import os

from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout, CMakeToolchain
from conan.tools.files import copy


class RDKitCppExampleConan(ConanFile):
  """Conan recipe for the RDKit C++ example project.

  This recipe manages the build configuration, dependency resolution,
  and packaging for a C++ application that utilizes RDKit and Boost.
  It includes logic for handling shared library distribution across
  Windows, Linux, and macOS.
  """

  name = "rdkit_cpp_example"
  version = "0.1.0"
  license = "BSD-3-Clause"
  author = "Martin Urban"
  url = "https://github.com/urban233/rdkit-cpp-example-template"
  description = (
    "Based on the blog post Using the RDKit in a C++ program as a "
    "ready-to-clone GitHub template."
  )
  topics = ("chemistry", "smiles", "rdkit", "boost")

  # Binary configuration
  settings = "os", "compiler", "build_type", "arch"

  options = {
    "shared": [True, False],
    "build_and_package": [True, False]
  }

  default_options = {
    "shared": True,
    "build_and_package": False
  }

  exports_sources = "src/*", "CMakeLists.txt", "cmake/*"
  generators = "CMakeDeps", "CMakeToolchain"

  requires = [
    "rdkit/2025.09.3@urban233/conan_testing",
    "boost/1.89.0"
  ]
  # Defaults to source_folder/bin
  local_package_dir = None

  # Configuration map for selective shared library copying.
  # Keys represent dependency names; Values are lists of specific libraries
  # to include. If the value is None, all libraries from that dependency are copied.
  dep_shared_whitelist = {
    "rdkit": None,  # Copy all RDKit libraries
    "boost": [
      "boost_iostreams",
      "boost_serialization",
      "boost_timer",
      "boost_system"
    ]
  }

  def layout(self):
    """Defines the directory layout for CMake."""
    cmake_layout(self)

  def configure(self):
    """Configures option values prior to dependency resolution.

    Enforces shared linkage for Boost to ensure compatibility with
    dynamic loading requirements in this specific project architecture.
    """
    self.options["boost"].shared = True

  def generate(self):
    """Generates the toolchain file for CMake.

    Sets the installation prefix and configures RPATH handling
    to ensure the executable can locate shared libraries relative
    to its location on Unix-like systems.
    """
    tc = CMakeToolchain(self)
    tc.variables["CMAKE_INSTALL_PREFIX"] = os.path.join(self.source_folder, "bin")

    # RPATH handling for Unix-like systems to allow relocatable binaries.
    # We skip the standard CMake RPATH stripping and enforce build-with-install RPATH.
    if self.settings.os in ["Linux", "Macos"]:
      tc.variables["CMAKE_SKIP_RPATH"] = "FALSE"
      tc.variables["CMAKE_BUILD_WITH_INSTALL_RPATH"] = "TRUE"

  def build(self):
    """Builds the project using CMake.

    If the 'build_and_package' option is enabled, this method will also
    perform a local install and aggregate shared libraries into the source
    bin folder for immediate testing.
    """
    cmake = CMake(self)
    cmake.configure()
    cmake.build()

    if self.options.build_and_package:
      print("Building and packaging...")
      cmake.install()
      if self.local_package_dir is not None:
        self._copy_shared_libraries(
          bin_folder=self.local_package_dir
        )
      else:
        self._copy_shared_libraries(
          bin_folder=os.path.join(self.source_folder, "bin")
        )

  def package(self):
    """Packages the artifacts for export.

    Installs the build artifacts and aggregates necessary shared libraries
    into the package's bin directory to create a self-contained runtime environment.
    """
    cmake = CMake(self)
    cmake.install()

    # Copy dependency shared libraries to the package bin folder.
    self._copy_shared_libraries(
      bin_folder=os.path.join(self.package_folder, "bin")
    )

  def _copy_shared_libraries(self, bin_folder):
    """Copies shared libraries from dependencies to a destination folder.

    This helper iterates through dependencies, filters them against the
    `dep_shared_whitelist`, and copies the relevant shared object files
    (.dll, .dylib, .so) to the specified binary folder.

    Args:
        bin_folder: The absolute path to the destination directory where
                    shared libraries should be copied.
    """
    # Determine platform-specific shared library extensions.
    if self.settings.os == "Windows":
      patterns = ["*.dll"]
    elif self.settings.os == "Macos":
      patterns = ["*.dylib"]
    else:  # Linux and others
      patterns = ["*.so", "*.so.*"]

    # Iterate through all direct dependencies.
    for dep_ref, dep in self.dependencies.items():
      # Extract the package name (e.g., 'rdkit' from 'rdkit/version...')
      dep_name = str(dep_ref).split("/")[0].lower()
      whitelist = self.dep_shared_whitelist.get(dep_name, None)

      # Search in both binary and library directories of the dependency.
      for folder in dep.cpp_info.bindirs + dep.cpp_info.libdirs:
        if not os.path.exists(folder):
          continue

        if whitelist is None:
          # Strategy: Copy all shared libraries matching the platform pattern.
          for pattern in patterns:
            copy(self, pattern, src=folder, dst=bin_folder, keep_path=False)
        else:
          # Strategy: Copy only specific libraries defined in the whitelist.
          for lib_name in whitelist:
            for pattern in patterns:
              # Use a wildcard match to catch version numbers or prefixes/suffixes.
              copy(
                self,
                f"*{lib_name}*",
                src=folder,
                dst=bin_folder,
                keep_path=False
              )

  def package_info(self):
    """Defines the package consumption information.

    Since this is an executable package, no libraries are exported.
    However, runtime environment variables are configured to ensure
    the executable can find its dependencies when run directly.
    """
    # No libraries exported (this is an executable package).
    self.cpp_info.bindirs = ["bin"]

    # Configure environment variables for runtime execution (LD_LIBRARY_PATH/PATH).
    if self.settings.os in ["Linux", "Macos"]:
      self.runenv_info.append_path(
        "LD_LIBRARY_PATH",
        os.path.join(self.package_folder, "bin")
      )
      if self.settings.os == "Macos":
        self.runenv_info.append_path(
          "DYLD_LIBRARY_PATH",
          os.path.join(self.package_folder, "bin")
        )
    elif self.settings.os == "Windows":
      self.runenv_info.append_path(
        "PATH",
        os.path.join(self.package_folder, "bin")
      )
