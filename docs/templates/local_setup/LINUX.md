# 🐧 ++linux_setup++

++setup_instruction++

# 🐍 ++py_setup++

++py_version_table++

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
pyenv install ++py_recommended_version++
```

# 📦 ++dev_place_setup++

```bash
# ++dir_setup++
mkdir "$HOME\dynpy_project"
cd "$HOME\dynpy_project"

# ++venv_setup++
pyenv shell ++py_recommended_version++
python -m venv ".\venv"

# ++go_to_venv++
source ".\venv\Scripts\activate"

# ++install_pip_packages++
python -m pip install --upgrade pip
pip install ++pip_requirements++
```

# ⚒️ ++additional_packages_setup++

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

# 🐳 ++dynpy_setup++
```powershell
cd "$HOME\dynpy_project"

git clone https://github.com/bogumilchilinski/dynpy.git
git clone https://github.com/bogumilchilinski/dgeometry.git
```

## 🎉 ++to_run++
++symbolic_link++
```bash
cd "$HOME\dynpy_project"

mkdir ./._dynpy_env
ln -s "$HOME\dynpy_project\dynpy" "./._dynpy_env/dynpy"
```
👻 ++to_run_instruction++