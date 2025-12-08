# rdkit-cpp-example-template
This repository is based on the blog post [Using the RDKit in a C++ program](https://greglandrum.github.io/rdkit-blog/posts/2021-07-24-setting-up-a-cxx-dev-env.html)
as a ready-to-clone GitHub template.

**NOTE**: This branch contains a new variant that uses `Conan` to build the library.
To get the `Conda` version, please check the `conda` branch.

## Contents of this document
* [Prerequisite](#Prerequisite)
* [Build](#Build)
    * [From source](#From-source)
    * [Package as standalone folder](#Package-as-standalone-folder)
* [Using Conda](#Using-Conda)

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
4. Run Conan configuration step
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

**IMPORTANT**: The profiles for Linux and macOS are not yet tested. 


### Package as standalone folder
**NOTE**: This procedure has been only tested on Windows yet. For macOS and Linux proceed with caution.

The default profiles located under the `profiles` folder can be used to package the library as a standalone folder.
To change the output folder, modify the `local_package_dir` property in the `conanfile.py` file.

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
