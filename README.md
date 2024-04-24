# taro_arcana
🔮비밀, 신비함

<div align=center>
  
  |환경|version|
  |:--:|:--:|
  |python|3.10.12|
  |ubuntu|22.04|
  |mysql|8.3.0|
  |workbench|8.0.34|

</div>

# 🐳 docker로 접속 방법
```
docker pull m005/arcana:v1.5
```
```
docker run --name taro -p 8000:8000 -d m005/arcana:v1.5
```
---
# 💻 로컬 접속 (MacOS M1)
### :octocat: 원하는 디렉토리에서 git clone
```
git clone https://github.com/M-05/taro_arcana.git
cd taro_arcana
```
#### 📁taro_arcana에 📋.env 생성 후 값 채우기
```.env
OPENAI_API_KEY=
SQL=mysql
USERNAME=
PASSWORD=
HOST=
PORT=
DBNAME=
```
### 🐍 미니콘다 사이트에서 직접 설치
```
https://docs.anaconda.com/free/miniconda/index.html
```
### 🐍 미니콘다 설치 후 가상 환경 생성 및 접속
```
conda create -n arcana python=3.10.12
conda activate arcana
```
### 📦 관련 모듈 설치
```
brew install mysql pkg-config
pip install -r arcana/requirements.txt
```
### 실행
```
python arcana/main.py
```
---
# 🐧리눅스 환경 접속 방법 (우분투 22.04)
### :octocat: 원하는 디렉토리에서 git clone
```
git clone https://github.com/M-05/taro_arcana.git
cd taro_arcana
```
#### 📁taro_arcana에 📋.env 생성 후 값 채우기
```.env
OPENAI_API_KEY=
SQL=mysql
USERNAME=
PASSWORD=
HOST=
PORT=
DBNAME=
```
### 🐍 미니콘다 설치
```
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
```
### 🐍 미니콘다 실행
```
~/miniconda3/bin/conda init bash
```
### 가상 환경 생성 및 접속
```
conda create -n arcana python=3.10.12
conda activate arcana
```
### 📦 관련 모듈 설치
```
sudo apt-get update
sudo apt-get install libmysqlclient-dev
pip install -r arcana/requirements.txt
```
### 실행
```
python arcana/main.py
```

