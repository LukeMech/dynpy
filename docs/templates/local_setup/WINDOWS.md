# 🪟 ++win_setup++

++win_setup_instruction++

# 🐍 ++py_setup++

++py_version_table++

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process; Invoke-Expression "& { $(Invoke-WebRequest -UseBasicParsing -Uri 'https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1').Content }"
<now reopen powershell>
pyenv install ++py_recommended_version++
```

# 📦 ++dev_place_setup++

```powershell
# ++dir_setup++
mkdir "$env:USERPROFILE\dynpy_project"
cd "$env:USERPROFILE\dynpy_project"

# ++venv_setup++
pyenv shell ++py_recommended_version++
python -m venv ".\venv"

# ++go_to_venv++
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
& ".\venv\Scripts\Activate.ps1"

# ++install_pip_packages++
python -m pip install --upgrade pip
pip install ++pip_requirements++
```

# ⚒️ ++additional_packages_setup++

## [Git](https://github.com/Microsoft/Git/releases)
```powershell
winget install Microsoft.Git
```

## [ImageMagick](https://imagemagick.org/script/download.php#windows)
1. ++download_first_start_install++. <br> 
2. ++check++ "Install development headers for C and C++". <br>
3. ++after_install++ ++set_env_vars++, ++add_magickhome_as_currenVersion++

## [TeXLive](https://www.tug.org/texlive/windows.html#install)
1. ++download_first_start_install++

# 🐳 ++dynpy_setup++
```powershell
cd "$env:USERPROFILE\dynpy_project"

git clone https://github.com/bogumilchilinski/dynpy.git
git clone https://github.com/bogumilchilinski/dgeometry.git
```

## 🎉 ++to_run++
++symbolic_link++
```powershell
cd "$env:USERPROFILE\dynpy_project"

mkdir ./._dynpy_env
New-Item -ItemType SymbolicLink -Path .\._dynpy_env\dynpy -Target .\dynpy
```
👻 ++to_run_instruction++