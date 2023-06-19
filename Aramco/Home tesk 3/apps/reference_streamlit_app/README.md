
# README

## How to run or build the app

### Instal Python

- Install Miniconda (Python 3.10)

### Activate environment

```bash
conda info --envs
conda activate etna_build
```

### Upgrade pip

```bash
pip install --upgrade pip
```

### Install the requirements

Go to root folder of the project via terminal and install packages specified in `reqirements.txt`.

```bash
pip install -r requirements.txt
```

## Run app using Streamlit

```bash
streamlit run src/app/run.py
```

## PyInstaller

### Build the config

```bash
pyi-makespec --onefile --add-data "<path>;." --collect-all streamlit --collect-all catboost --recursive-copy-metadata streamlit --recursive-copy-metadata catboost --paths . app.py 
```

#### Example MacOS

```bash
pyi-makespec --onefile --add-data "/Users/antonvoskresenskii/Yandex.Disk-voskresenskiianton.localized/ds/aramco/connectivity:." --collect-all streamlit --collect-all catboost --collect-all pandas --collect-all etna --collect-all path --collect-all networkx --collect-all shap --recursive-copy-metadata streamlit --recursive-copy-metadata catboost --recursive-copy-metadata pandas --recursive-copy-metadata etna --recursive-copy-metadata path --recursive-copy-metadata networkx --recursive-copy-metadata shap --paths . src/app/app.py
```

#### Example Windows

```bash
pyi-makespec --onefile --add-data "C:\Users\anton.voskresenskii\Downloads\con-main;." --collect-all streamlit --collect-all catboost --collect-all pandas --collect-all etna --collect-all path --collect-all networkx --collect-all shap --recursive-copy-metadata streamlit --recursive-copy-metadata catboost --recursive-copy-metadata pandas --recursive-copy-metadata etna --recursive-copy-metadata path --recursive-copy-metadata networkx --recursive-copy-metadata shap --paths . src/app/app.py
```

### Build the app

```bash
pyinstaller --clean run.spec
```

## Briefcase

### Run the app in developer mode

```bash
briefcase dev
```

### Build the app

```bash
briefcase run
```

### Build the app

```bash
briefcase build
```

### Build the `.msi` package

```bash
briefcase package
```
