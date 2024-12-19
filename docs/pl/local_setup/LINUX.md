# 🐧 **W TRAKCIE OPRACOWYWANIA** Konfiguracja pod Linuxem

Aby skonfigurować lokalne środowisko uruchomieniowe, podążaj za instrukcją

# 🐍 Konfiguracja Pythona

| Wersja | Status | Opis |
| --- | --- | --- |
| 3.10 | ✅ | Zalecane, działa w pełni |
| 3.11 | ❔✅ | Testy w toku |
| 3.12 | ❔⚠️ | Pokazuje błędy |
| 3.13 | ❔❌ | Mogą pojawić się spore problemy |

## 1. 
Debian/Ubuntu: 
```bash
sudo apt update; sudo apt install build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl git \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

Fedora:
```bash
sudo dnf install make gcc patch zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel libuuid-devel gdbm-libs libnsl2
```
Others: https://github.com/pyenv/pyenv/wiki#suggested-build-environment

## 2.
```bash
curl https://pyenv.run | bash
pyenv install 3.10.16
```

# 📦 Konfiguracja katalogu projektu

```bash
# Utwórz katalog
mkdir "$HOME\dynpy_project"
cd "$HOME\dynpy_project"

# Stwórz wirtualne środowisko dla Pythona
pyenv shell 3.10.16
python -m venv ".\venv"

# Użyj świeżo stworzonego środowiska wirtualnego
source ".\venv\Scripts\activate"

# Zainstaluj wymagane zależności pip
python -m pip install --upgrade pip
pip install ipykernel~=6.29.5 sympy~=1.13.3 numpy~=2.2.0 scipy~=1.14.1 pylatex~=1.4.2 pandas~=2.2.3 matplotlib~=3.10.0 pint~=0.24.4 wand~=0.6.13 PyGithub~=2.5.0
```

# ⚒️ Instalacja wymaganych zależności

*Ubuntu-based instructions, for other distros use some google and your package manager ;)*
## [Git](https://github.com/Git/Git)
```bash
sudo apt install git
```

## [ImageMagick](https://imagemagick.org/script/download.php#linux)
```bash
sudo apt install imagemagick
```

## [TeXLive](https://www.tug.org/texlive/quickinstall.html)
```bash
sudo apt install texlive-pictures texlive-science texlive-latex-extra latexmk
```

## [Ghostscript](https://ghostscript.com/releases/)
```bash
sudo apt install ghostscript
```

# 🐳 Instalacja dynpy i dgeometry
```powershell
cd "$HOME\dynpy_project"

git clone https://github.com/bogumilchilinski/dynpy.git
git clone https://github.com/bogumilchilinski/dgeometry.git
```

## 🎉 Uruchomienie!
Musimy stworzyć symboliczny link, przekierowujący katalog `._dynpy_env` na katalog `dynpy`, ze względu na kompatybilność
```bash
cd "$HOME\dynpy_project"

mkdir ./._dynpy_env
ln -s "$HOME\dynpy_project\dynpy" "./._dynpy_env/dynpy"
```
👻 Aby uruchomić kod, otwórz ścieżkę z projektem w Visual Studio Code, stwórz plik `test.ipynb`, otwórz i wybierz "venv" z dostępnych kerneli do Pythona w rozszerzeniu Jupiter