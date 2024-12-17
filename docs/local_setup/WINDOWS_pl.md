# 🪟 Konfiguracja pod Windowsem

Aby skonfigurować lokalne środowisko uruchomieniowe w systemie Windows, podążaj za instrukcją

# 🐍 Konfiguracja Pythona

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
pyenv install 3.10.11
```

# 📦 Konfiguracja katalogu projektu

```powershell
# Utwórz katalog
mkdir "$env:USERPROFILE\dynpy_project"
cd "$env:USERPROFILE\dynpy_project"

# Stwórz wirtualne środowisko dla Pythona
pyenv shell 3.10.11
python -m venv ".\venv"

# Użyj świeżo stworzonego środowiska wirtualnego
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
& ".\venv\Scripts\Activate.ps1"

# Zainstaluj wymagane zależności pip
python -m pip install --upgrade pip
pip install ipykernel~=6.29.5 
sympy~=1.13.3 
numpy~=2.2.0
scipy~=1.14.1
pylatex~=1.4.2
pandas~=2.2.3
matplotlib~=3.10.0
pint~=0.24.4
wand~=0.6.13
PyGithub~=2.5.0

```

# ⚒️ Instalacja wymaganych zależności

## [ImageMagick](https://imagemagick.org/script/download.php#windows)
1. Pobierz instalator z pierwszego z brzegu linku i go wystartuj. <br> 
2. Zaznacz "Install development headers for C and C++". <br>
3. Po instalacji w menu start wyszukaj "Edytuj zmienne środowiskowe", następnie kliknij "Zmienne środowiskowe" (dół okna)., Potem dodaj MAGICK_HOME jako "C:\Program Files\ImageMagick-VERSION-Q16)" (zamień VERSION na numer wersji)

## [Git](https://github.com/Microsoft/Git/releases)
```powershell
winget install Microsoft.Git
```

# 🐳 Instalacja dynpy i dgeometry
```powershell
cd "$env:USERPROFILE\dynpy_project"

git clone https://github.com/bogumilchilinski/dynpy.git
git clone https://github.com/bogumilchilinski/dgeometry.git
```

## 🎉 Uruchomienie!
Aby uruchomić kod, otwórz utworzoną ścieżkę w Visual Studio Code, stwórz plik `test.ipynb, otwórz i wybierz "venv" z dostępnych kerneli do Pythona w rozszerzeniu Jupiter