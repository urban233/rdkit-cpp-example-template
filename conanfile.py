from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout, CMakeToolchain
from conan.tools.files import copy
import os

class RDKitCppExampleConan(ConanFile):
  name = "rdkit_cpp_example"
  version = "0.1.0"
  license = "MIT"
  author = "Your Name <you@example.com>"
  url = "https://github.com/urban233/rdkit-cpp-example-template"
  description = "Based on the blog post Using the RDKit in a C++ program as a ready-to-clone GitHub template."
  topics = ("chemistry", "smiles", "rdkit", "boost")
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

  # Whitelist of shared libraries to copy per dependency
  dep_shared_whitelist = {
    "rdkit": None,  # Copy all RDKit libraries
    "boost": ["boost_iostreams", "boost_serialization", "boost_timer", "boost_system"]
  }

  def layout(self):
    cmake_layout(self)

  def configure(self):
    # Force shared libraries for certain dependencies
    self.options["boost"].shared = True

  def generate(self):
    tc = CMakeToolchain(self)
    tc.variables["CMAKE_INSTALL_PREFIX"] = os.path.join(self.source_folder, "bin")

    # RPATH handling for Unix-like systems
    if self.settings.os in ["Linux", "Macos"]:
      tc.variables["CMAKE_SKIP_RPATH"] = "FALSE"
      tc.variables["CMAKE_BUILD_WITH_INSTALL_RPATH"] = "TRUE"

  def build(self):
    cmake = CMake(self)
    cmake.configure()
    cmake.build()

    if self.options.build_and_package:
      print("Building and packaging...")
      cmake.install()
      self._copy_shared_libraries(bin_folder = os.path.join(self.source_folder, "bin"))

  def package(self):
    cmake = CMake(self)
    cmake.install()

    # Copy dependency shared libraries to bin folder
    self._copy_shared_libraries(bin_folder = os.path.join(self.package_folder, "bin"))

  def _copy_shared_libraries(self, bin_folder):
    """Copy shared libraries from dependencies to package bin folder"""

    # Platform-specific shared library extensions
    if self.settings.os == "Windows":
      patterns = ["*.dll"]
    elif self.settings.os == "Macos":
      patterns = ["*.dylib"]
    else:  # Linux
      patterns = ["*.so", "*.so.*"]

    # Copy from each dependency
    for dep_ref, dep in self.dependencies.items():
      dep_name = str(dep_ref).split("/")[0].lower()
      whitelist = self.dep_shared_whitelist.get(dep_name, None)

      # Search in both bindirs and libdirs
      for folder in dep.cpp_info.bindirs + dep.cpp_info.libdirs:
        if not os.path.exists(folder):
          continue

        if whitelist is None:
          # Copy all shared libraries
          for pattern in patterns:
            copy(self, pattern, src=folder, dst=bin_folder, keep_path=False)
        else:
          # Copy only whitelisted libraries
          for lib_name in whitelist:
            for pattern in patterns:
              # Match files containing lib_name
              copy(self, f"*{lib_name}*",
                   src=folder, dst=bin_folder, keep_path=False)

  def package_info(self):
    # No libraries exported (this is an executable package)
    self.cpp_info.bindirs = ["bin"]

    # Set environment variables for runtime (helpful for testing)
    if self.settings.os in ["Linux", "Macos"]:
      self.runenv_info.append_path("LD_LIBRARY_PATH",
                                   os.path.join(self.package_folder, "bin"))
      if self.settings.os == "Macos":
        self.runenv_info.append_path("DYLD_LIBRARY_PATH",
                                     os.path.join(self.package_folder, "bin"))
    elif self.settings.os == "Windows":
      self.runenv_info.append_path("PATH",
                                   os.path.join(self.package_folder, "bin"))

# from conan import ConanFile
# from conan.tools.cmake import CMake, cmake_layout, CMakeToolchain
# from conan.tools.files import copy
# import os
#
# class SmilesProcessingConan(ConanFile):
#   name = "smiles_processing"
#   version = "0.1.0"
#   license = "MIT"
#   author = "Your Name <you@example.com>"
#   url = "https://github.com/yourusername/smiles_processing"
#   description = "C++ library for SMILES processing using RDKit"
#   topics = ("chemistry", "smiles", "rdkit", "boost")
#   settings = "os", "compiler", "build_type", "arch"
#   options = {
#     "shared": [True, False],
#     "build_and_package": [True, False]
#   }
#   default_options = {
#     "shared": True,
#     "build_and_package": False
#   }
#   exports_sources = "src/*", "CMakeLists.txt", "cmake/*"
#   generators = "CMakeDeps", "CMakeToolchain"
#   requires = [
#     "rdkit/2025.09.3@urban233/conan_testing",
#     "boost/1.89.0"
#   ]
#
#   # Map dependency name -> whitelist of DLLs to include
#   # None or empty list means include all DLLs
#   dep_shared_whitelist = {
#     "rdkit": None,  # copy all RDKit DLLs
#     "boost": ["boost_iostreams", "boost_serialization"]  # only these Boost libs
#   }
#
#   def layout(self):
#     cmake_layout(self)
#
#   def configure(self):
#     # Always build as shared library
#     self.options.shared = True
#
#   def generate(self):
#     tc = CMakeToolchain(self)
#     tc.variables["CMAKE_INSTALL_PREFIX"] = os.path.join(self.source_folder, "bin")
#     if self.settings.os in ["Linux", "Macos"]:
#       tc.variables["CMAKE_SKIP_RPATH"] = "FALSE"
#       tc.variables["CMAKE_BUILD_WITH_INSTALL_RPATH"] = "TRUE"
#
#   def build(self):
#     cmake = CMake(self)
#     cmake.configure()
#     cmake.build()
#     if self.options.build_and_package:
#       cmake.install()
#       self._copy_shared_libraries(os.path.join(self.source_folder, "bin"))
#
#   def _copy_shared_libraries(self, bin_folder):
#     if self.settings.os == "Windows":
#       patterns = ["*.dll"]
#     elif self.settings.os == "Macos":
#       patterns = ["*.dylib"]
#     else:  # Linux
#       patterns = ["*.so", "*.so.*"]
#
#     for dep_ref, dep in self.dependencies.items():
#       dep_name = str(dep_ref).split("/")[0].lower()
#       whitelist = self.dep_shared_whitelist.get(dep_name, None)
#
#       for folder in dep.cpp_info.bindirs + dep.cpp_info.libdirs:
#         if whitelist is None:
#           for pattern in patterns:
#             copy(self, pattern, src=folder, dst=bin_folder, keep_path=False)
#         else:
#           for lib_name in whitelist:
#             for pattern in patterns:
#               # Better pattern matching
#               copy(self, f"*{lib_name}*", src=folder, dst=bin_folder, keep_path=False)
#
#     # shared_exts = ["*.dll", "*.so", "*.so.*", "*.dylib"]
#     # # Copy dependency shared libraries according to whitelist
#     # for dep_ref, dep in self.dependencies.items():
#     #   dep_name = str(dep_ref).split("/")[0].lower()  # extract package name
#     #   whitelist = self.dep_shared_whitelist.get(dep_name, None)
#     #
#     #   for folder in dep.cpp_info.bindirs + dep.cpp_info.libdirs:
#     #     if whitelist is None:  # copy everything
#     #       for ext in shared_exts:
#     #         print(f"Copying {ext} from {folder} to {bin_folder}")
#     #         copy(self, ext, src=folder, dst=bin_folder, keep_path=False)
#     #     else:
#     #       # copy only DLLs that match the whitelist
#     #       for lib_name in whitelist:
#     #         for ext in shared_exts:
#     #           pattern = f"*{lib_name}*{ext.replace('*','')}"
#     #           print(f"Copying {pattern} from {folder} to {bin_folder}")
#     #           copy(self, pattern, src=folder, dst=bin_folder, keep_path=False)
#
#   def package(self):
#     cmake = CMake(self)
#     cmake.install()
#     # # Copy headers
#     # copy(self, "*.h",
#     #      src=os.path.join(self.source_folder, "src"),
#     #      dst=os.path.join(self.package_folder, "include"),
#     #      keep_path=True)
#     #
#     # # Copy import libraries (.lib)
#     # copy(self, "*.lib",
#     #      src=os.path.join(self.build_folder, "lib"),
#     #      dst=os.path.join(self.package_folder, "lib"),
#     #      keep_path=False)
#
#     # Prepare bin folder
#     self._copy_shared_libraries(os.path.join(self.package_folder, "bin"))
#
#   def package_info(self):
#     self.cpp_info.libs = ["smiles_processing"]
#     self.cpp_info.includedirs = ["include"]
#     self.cpp_info.libdirs = ["lib"]
#     self.cpp_info.bindirs = ["bin"]
