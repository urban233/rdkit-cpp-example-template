from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.files import copy
import os

class SmilesProcessingConan(ConanFile):
  name = "smiles_processing"
  version = "0.1.0"
  license = "MIT"
  author = "Your Name <you@example.com>"
  url = "https://github.com/yourusername/smiles_processing"
  description = "C++ library for SMILES processing using RDKit"
  topics = ("chemistry", "smiles", "rdkit", "boost")
  settings = "os", "compiler", "build_type", "arch"
  options = {"shared": [True, False]}
  default_options = {"shared": True}
  exports_sources = "src/*", "CMakeLists.txt", "cmake/*"
  generators = "CMakeDeps", "CMakeToolchain"
  requires = [
    "rdkit/2025.09.3@urban233/conan_testing",
    "boost/1.89.0"
  ]

  def layout(self):
    cmake_layout(self)

  def configure(self):
    # Always build as shared library (DLL)
    self.options.shared = True

  def build(self):
    cmake = CMake(self)
    cmake.configure()
    cmake.build()

  def package(self):
    cmake = CMake(self)
    # Install target and library files
    cmake.install()

    # Copy headers
    copy(self, "*.h",
         src=os.path.join(self.source_folder, "src"),
         dst=os.path.join(self.package_folder, "include"),
         keep_path=True)

    # Copy import libraries (.lib) if needed
    copy(self, "*.lib",
         src=os.path.join(self.build_folder, "lib"),
         dst=os.path.join(self.package_folder, "lib"),
         keep_path=False)

  def package_info(self):
    self.cpp_info.libs = ["smiles_processing"]
    self.cpp_info.includedirs = ["include"]
    self.cpp_info.libdirs = ["lib"]
    self.cpp_info.bindirs = ["bin"]

  def deploy(self):
    """
    This method is called when using `conan deploy`.
    It copies the DLLs of this package and all its dependencies
    into a single folder so the executable or JNA can find them.
    """
    bin_dir = os.path.join(self.deploy_folder, "bin")
    os.makedirs(bin_dir, exist_ok=True)

    # Copy our own DLLs
    copy(self, "*.dll",
         src=os.path.join(self.package_folder, "bin"),
         dst=bin_dir,
         keep_path=False)

    # Copy all DLLs from dependencies
    for dep_name, dep_cpp_info in self.dependencies.items():
      for dep_bin_dir in dep_cpp_info.bindirs:
        copy(self, "*.dll",
             src=dep_bin_dir,
             dst=bin_dir,
             keep_path=False)
