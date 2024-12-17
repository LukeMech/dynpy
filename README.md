# Introduction

It's a module that allows to engineering calculations on dynamical systems. 

There are four main parts of the entire project:

- dynamics module

- mechanical models - lead of development and maintenance: Amadeusz Radomski (@amvdek); Grzegorz Długopolski (@grzegorzdl);

- symbolic and numeric solvers for ODE systems;

- reporting module.

First step for starting a project is to create an account in [COCALC](https://cocalc.com/). 

Then, using the following [LINK](https://cocalc.com/app?project-invite=hXnPFLqokQsoK6TG), accept the invitation.

Afterwards, you will be directed to the page, where you should click the [README FIRST](https://cocalc.com/projects/b51ce971-5b39-4911-ad97-ef59f15f0039/files/README%20FIRST.ipynb) file (you can click this link if you have trouble seeing the page). There, you have access to the introductory code, which is prepared for you.

In this file, you will find the essential information on how to create a blank Jupiter (where you will run the codes), use Cocalc, access usefull commands and more...

# Help and guides for DynPy

You can access the introductory guide with the following code:

```python {kernel="python3"}
from dynpy.utilities.documents.guides import IntroToCocalcGuide, UsageOfDynamicSystemsGuide

IntroToCocalcGuide();
```

You can list all of the available guides with the following call:

```python {kernel="python3"}
from dynpy.utilities.creators import list_of_guides
list_of_guides()
```

If you are looking for information on reporting and creating a PDF file, we can use the command below to view the tutorial:

```python {kernel="python3"}
from dynpy.utilities.documents.guides import BasicsOfReportingGuide
BasicsOfReportingGuide();
```

# Dynamic systems

Next for an example, run the codes below and you will see how it works:

You can preview the pendulum using such a function.

```python {kernel="python3"}
import sympy 
from sympy import Symbol

from dynpy.models.mechanics.pendulum import Pendulum

Pendulum().interactive_preview()
```

# 🐳 Using locally

*While it's highly unrecommended, you can run the project locally. With all libraries it may take ~10GB of disk space.*

Checked python versions: `3.10`
<details>
  <summary>🪟 Windows</summary>

  1. Install [ImageMagick](https://imagemagick.org/index.php), [Python](https://www.python.org/) (using [pyenv-win](https://github.com/pyenv-win/pyenv-win)) and [git](https://github.com/microsoft/git) <br>
  Step 1: Download [ImageMagick](https://imagemagick.org/script/download.php#windows) (1st one on page) -> check "Install development headers for C and C++", then hit "Install" <br>
  Step 2: Set enviroment variables (search in start menu), then add MAGICK_HOME set as `C:\Program Files\ImageMagick-VERSION(-Q16)` (make sure the folder is right) <br>
  Step 3:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process; Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
  <now reopen powershell>
  pyenv install 3.10
  winget install Microsoft.Git
  ```

  2. Create your work folder (can be any path) and create python virtual enviroment:
  ```powershell
  mkdir "$env:USERPROFILE\dynpy_project"
  pyenv shell 3.10.11 # Use "pyenv versions" to get the exact version number
  python -m venv "$env:USERPROFILE\dynpy_project\venv"
  cd "$env:USERPROFILE\dynpy_project"
  ```

  3. Clone required libraries:
  ```powershell
  git clone https://github.com/bogumilchilinski/dynpy
  git clone https://github.com/bogumilchilinski/dgeometry
  ```
 
  4. Get into the environment:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
  & ".\venv\Scripts\Activate.ps1"
  ```
 
  5. Install required packages:
  ```powershell
  python -m pip install --upgrade pip
  pip install -r dynpy/requirements.txt 
  ```

  6. (BYPASS, TO BE DONE BETTER) Make symbolic link (redirect ._dynpy_env to dynpy) (need admin rights for this):
  ```powershell
  mkdir ./._dynpy_env
  New-Item -ItemType SymbolicLink -Path .\._dynpy_env\dynpy -Target .\dynpy
  ```
  
  7. Create `something.ipynb` file in your work folder and open with vscode - it should prompt for choosing kernel. Choose python `from venv`.
</details>

<details>
  <summary>🐧 Linux</summary>

  1. Install [ImageMagick](https://imagemagick.org/index.php), [Python](https://www.python.org/) (using [pyenv](https://github.com/pyenv/pyenv)) and [git](https://github.com/git/git)<br>
  ```bash
  sudo apt install imagemagick git
  curl https://pyenv.run | bash
  pyenv install 3.10
  ```

  2. Create your work folder (can be any path) and create python virtual enviroment:
  ```bash
  mkdir "$HOME\dynpy_project"
  pyenv shell 3.10.11 # Use "pyenv versions" to get the exact version number
  python -m venv "$HOME\dynpy_project\venv"
  cd "$HOME\dynpy_project"
  ```

  3. Clone required libraries:
  ```bash
  git clone https://github.com/bogumilchilinski/dynpy
  git clone https://github.com/bogumilchilinski/dgeometry
  ```
 
  4. Get into the environment:
  ```bash
  source ".\venv\Scripts\activate"
  ```
 
  5. Install required packages:
  ```bash
  python -m pip install --upgrade pip
  pip install -r dynpy/requirements.txt 
  ```
  
  6. (BYPASS, TO BE DONE BETTER) Make symbolic link (redirect ._dynpy_env to dynpy)
  ```bash
  mkdir ./._dynpy_env
  ln -s ./dynpy ./._dynpy_env/dynpy
  ```

  7. Create `something.ipynb` file in your work folder and open with vscode - it should prompt for choosing kernel. Choose python `from venv`.
</details>

🎉 And you're good to go! Create code blocks in your file and run them to find out more.