# Introduction 
TODO: Give a short introduction of your project. Let this section explain the objectives or the motivation behind this project.

# Getting Started
1.	Installation process.
    #### Create and activate a python virtual env:

    Select the Git Bash terminal in your IDE terminal options to run the commands listed below.
    
    Create a virtual environment using via ```python -m venv /path/to/new/virtual/environment```
    and activate it via:
    - MacOS or Unix: ```source /path/to/venv/bin/activate```
    - Windows: ```path\to\venv\Scripts\activate.bat```


    #### Install pip-tools and pip-audit:
    pip-tools is a combination of two packages: pip-compile and pip-sync. You can read more about it here: https://github.com/jazzband/pip-tools
    pip-audit helps audit our dependencies for known vulnerabilities to ctach them before Nexus does. More here: https://pypi.org/project/pip-audit/

    ``` 
    # Install pip-tools
    python -m pip install pip-tools
    pip install pip-audit
    # Check if the installation was successful
    pip-compile --version
    pip-sync --version
    pip-audit --version
    ```
    #### Install Taskfile (optional):
    Taskfile is a task runner hat aims to be simpler and easier to use than GNU Make (Makefile). Documentation here: https://taskfile.dev/
    
    - If you are using MacOs, install it via homebrew: ```brew install go-task/tap/go-task```
    - If you are using Windows you can download the binaries and add them to $PATH: https://taskfile.dev/installation/#get-the-binary. Or use the other options mentioned in the documentation.

2.	Prepare your local environment
    
    Once you have completed the previous steps, prepare your local environment by compiling and installing the dependencies listed in ```pyproject.toml```.
    
    If you are using **Taskfile**, you can just run the following command. It will:
    - compile the requirements, 
    - audit them to check for vulnerabilities that might be flagged by Nexus, 
    - and sync those requirements to your virtual environment so you have ONLY what it is stated in the requirements_test.txt 
    - Install the necessary pre-commit hooks
    ```
    task prepare-local-env
    ```

    If you are **NOT** using Taskfile then run these commands to compile the requirements:
    ```
    pip-compile --extra test -o requirements/requirements_test.txt pyproject.toml --verbose
    pip-compile -o requirements/requirements.txt --verbose  -c requirements/requirements_test.txt pyproject.toml
    ```

    Audit the dependencies (OPTIONAL)
    ```
    pip-audit -r requirements/requirements_test.txt --fix --dry-run 
    ```

    Sync the requirements to your virtual environment. It will install them and delete anything not listed in the requirements file
    ```
    pip-sync requirements/requirements_test.txt
    ```

    There should be a file in the root folder named hash.txt, it shuld contain the most recent hash of the pyproject.toml. If it is not there, create it and then run the following command to add the hash to it.
    ```
    echo $(cksum < pyproject.toml | awk 'NR==1{print $1}') > hash.txt
    # Check that what was written in to hash.txt makes sense (ithas to be a number)
    cat hash.txt
    ```

    FOR MAC USERS: Make sure the files inside the scripts folder are executable so pre-commit can run them
    ```
    chmod +x scripts/upload-requirements.sh
    git update-index --chmod=+x scripts/upload-requirements.sh
    ```
    #### Install pre-commit hooks: 
    You can find pre-commit documentation here: https://pre-commit.com/

    pre-commit should be in the dependencies listed under project.optional-dependencies in pyproject.toml and therefore will be installed with the rest of the depencies (previous steps).
    To verify it is correctly installed you can run:
    ```
    pre-commit --version
    ```
    After verifying pre-commit is installed, please run the followng command to install further hooks.
    ```
    pre-commit install --install-hooks -t pre-push
    ```

    After completing those steps your virtual environment should be ready 😀. 

    **IMPORTANT!**: Run commands [1-4] everytime you modify the dependencies list in pyproject.toml


# Push code to remote repo
It is recommended that you push after multiple commits (if multiple commits are necessary) instead of pushing afetr every commit. A ```.pre-commit-config.yaml``` file is configured to run several code quality checks and fixes (although it wont fix everything) before you commit or push your code. It will also run pytest over your tests folder to make sure your unit tests are successful.

# Check code coverage

```
pytest --cov=pb_customer_journey_investments  tests/
```
# Contribute
TODO: Explain how other users and developers can contribute to make your code better. 

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)