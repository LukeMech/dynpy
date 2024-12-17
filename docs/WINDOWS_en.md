# 🪟 Windows setup

To properly configure project enviroment in Windows, follow the steps below

# 🐍 Python configuration

<details>
  <summary> Python</summary>
  
  | Python Version | Status                       | Notes                                        |
  |----------------|------------------------------|----------------------------------------------|
  | **3.10**       | ✅ **Recommended**           | **Fully working**                           |
  | 3.11           | ✅ Runs OK                   | Tests in progress                            |
  | 3.12           | ✅⚠️ Warnings shown         | Not tested, optimization may be required     |
  | 3.13           | ⚠️ A lot of warnings         | Significant problems may exist               |

</details>

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process; Invoke-Expression "& { $(Invoke-WebRequest -UseBasicParsing -Uri 'https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1').Content }"
<now reopen powershell>
pyenv install ++py_recommended_version++
```

# 📦 Configure working directory

```powershell
# Setup directory
mkdir "$env:USERPROFILE\dynpy_project"
cd "$env:USERPROFILE\dynpy_project"

# Configure Python virtual enviroment
pyenv shell ++py_recommended_version++
python -m venv ".\venv"

# Use virtual directory installed Python
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
& ".\venv\Scripts\Activate.ps1"

# Install pip packages
python -m pip install --upgrade pip
pip install ++pip_requirements++
```

# ⚒️ Install required dependencies

## [ImageMagick](https://imagemagick.org/script/download.php#windows)
1. Download the first one, then start the installer. <br> 
2. Check "Install development headers for C and C++". <br>
3. After install in start menu search for "Set enviroment variables", then click "Enviroment variables" (bottom of the window), Then add MAGICK_HOME as "C:\Program Files\ImageMagick-VERSION-Q16)" (replace VERSION with what is installed)

## [Git](https://github.com/Microsoft/Git/releases)
```powershell
winget install Microsoft.Git
```

# 🐳 Setup the dynpy and dgeometry
```powershell
cd "$env:USERPROFILE\dynpy_project"

git clone https://github.com/bogumilchilinski/dynpy.git
git clone https://github.com/bogumilchilinski/dgeometry.git
```

## 🎉 Run!
To run the code, open the project directory in VSCode, create `test.ipynb` file, open it and choose "venv" from available Python kernels in Jupiter extension