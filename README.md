# rdkit-cpp-example-template

[![License](https://img.shields.io/badge/license-BSD-blue.svg)](https://github.com/rdkit/rdkit/blob/master/LICENSE)
[![Conan](https://img.shields.io/badge/conan-ready-brightgreen.svg)](https://conan.io/)

This repository is based on the blog post [Using the RDKit in a C++ program](https://greglandrum.github.io/rdkit-blog/posts/2021-07-24-setting-up-a-cxx-dev-env.html)
as a ready-to-use GitHub template.

**NOTE**: This branch contains a new variant that uses `Conan` to build the library.
To get the `Conda` version, please check the `conda` branch.

## Contents of this document
* [Prerequisite](#Prerequisite)
* [Build](#Build)
    * [From source](#From-source)
    * [Package as standalone folder](#Package-as-standalone-folder)
    * [Building the Conan RDKit package](#Building-the-Conan-RDKit-package)
* [Working with CLion](#Working-with-CLion)
* [Using Conda](#Using-Conda)
* [License](#License)

## Prerequisite
- [Python](https://www.python.org/)
- [Visual Studio](https://visualstudio.microsoft.com/vs/community/) (for Windows builds)
- gcc (for GNU Linux)
- clang/Xcode (for macOS)

## Build

## From source
1. Create a new Python virutal environment:
    ```shell
    python -m venv .venv
    ```
2. Activate the new Python virtual environment (for Windows):
    ```shell
    .\.venv\Scripts\activate
    ```
3. Install the `Conan` Python package:
    ```shell
    pip install conan
    ```
4. Run Conan configuration step<br>
   **IMPORTANT**: You must have a Conan package of RDKit in your local Conan cache!<br>
   You can get the Conan RDKit package by following the guide [Building the RDKit Conan package](#Building-the-RDKit-Conan-package).<br>
   Once you've built the Conan RDKit package, adjust `line 45` of the `conanfile.py` so that it contains the correct channel. Most common is `rdkit/2025.09.3`.
    ```shell
    conan install .
    ```
5. Run CMake build step using the appropriate Conan profile (e.g. Windows):
    ```shell
    conan build . --profile .\profiles\windows_release
    ```
    or for **Linux** use:
    ```shell
    conan build . --profile .\profiles\linux_release
    ```
   or for **macOS** use:
    ```shell
    conan build . --profile .\profiles\macos_release
    ```

**IMPORTANT**: Be aware that the profiles for Linux and macOS are only tested via the GitHub action workflow. 

### Package as standalone folder
**NOTE**: This procedure has been only tested on Windows yet. For macOS and Linux proceed with caution.

The default profiles located under the `profiles` folder can be used to package the library as a standalone folder.
To change the output folder, modify the `local_package_dir` property in the `conanfile.py` file.

### Building the Conan RDKit package
In order to build this example using Conan, you'll need to build the RDKit Conan package first, so that it's 
available via the local Conan cache.
To do this, clone the RDKit conan package repo:
```shell
git clone https://github.com/urban233/rdkit-conan-package.git
cd rdkit-conan-package
```
After that, proceed with creating the package:
```bash
conan create . rdkit/2025.09.03
```

This will build the RDKit library and create a local Conan package.

---

Now you can proceed with step 4 of the [From source](#From-source) section.

## Working with CLion
To build this example in IDE's such as CLion, you can use **CMake** profiles.
Start with cloning the repository:
```shell
git clone https://github.com/urban233/rdkit-cpp-example-template.git
cd rdkit-cpp-example-template
```
After that, install the Conan dependencies by running:
```shell
conan install .
```
Be aware that for this, the Conan RDKit package must be present in the local Conan cache.
Then, create the **CMake** profile by running:
```shell
cmake . --preset=conan-default
```
After that you could also build the Conan RDKit package with the command:
```shell
cmake --build --preset=conan-release
```
or activate the new **CMake** profile within CLion and then use the GUI to build 
the project.

## Using Conda
This repository also contains a Conda variant that can be used for dependency management.
To use it, please first clone the repo:
```shell
git clone https://github.com/urban233/rdkit-cpp-example-template.git
```
and then switch to the `conda` branch:
```shell
cd rdkit-cpp-example-template
git checkout conda
```

This branch contains a `README.md` file with instructions on how to use Conda to build the library.

## License

This project is licensed under the **BSD License** – see the [LICENSE](https://github.com/rdkit/rdkit/blob/master/LICENSE) file for details.
