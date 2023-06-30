# Instructions for building the app
## Miniconda

1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html).
2. Open the **project root directory** and create a new conda environment with dependencies specified in the `requirements.yml` file:
	> Note: `$` character marks the beginning of a command, you don’t need to use it in the command itself.

	```bash
	$ conda env create -f requirements.yml
	```

3. Activate the newly created environment:
	```bash
	$ conda activate environment
	```
4. Run the application script with Streamlit to make sure that it works as expected:
	```bash
	$ cd srs/app
	$ streamlit run sript.py
	```
5. Return to the root directory and create application spec with `Pyinstaller`:
	```bash
	$ pyi-makespec --onefile \
	--collect-all streamlit \
	--collect-all catboost \
	--collect-all etna \
	--collect-all pandas \
	--collect-all path \
	--recursive-copy-metadata streamlit \
	--recursive-copy-metadata catboost \
	--recursive-copy-metadata etna \
	--recursive-copy-metadata pandas \
	--recursive-copy-metadata path \
	--paths . src/app/script.py
	```
6. Prepare application files:
	```bash
	$ pyinstaller --clean script.spec
	```
7. Conduct test runs with `briefcase`:
	Run the app in developer mode:
	```bash
	$ briefcase dev
	```
	Build and run the app in distribution mode:
	```bash
	$ briefcase run
	```
10. Build the app and generate executable:
	```bash
	$ briefcase build
	$ briefcase package --adhoc-sign
	```
11. Deactivate your conda environment and run the executable:
	```bash
	$ conda deactivate
	$ open dist/app-0.0.1.dmg
	```


## Vanilla Python
> Note: The following instructions are only macOS compatible.

1. Install [Python](https://www.python.org/downloads/macos/).
2. Open the **project root directory** and create a new Python environment using `3.10` Python version:
	> Note: `$` character marks the beginning of a command, you don’t need to use it in the command itself.

	```bash
	$ python3.10 -m venv environment
	```

3. Activate the newly created environment:
	```bash
	$ source environment/bin/activate
	```
4. Upgrade `pip` and install project’s packages specified in the `requirements.txt` file:
	```bash
	$ pip install --upgrade pip
	$ pip install -r requirements.txt
	```
5. Run the application script with Streamlit to make sure that it works as expected:
	```bash
	$ cd srs/app
	$ streamlit run sript.py
	```
6. Return to the root directory and create application spec with `Pyinstaller`:
	```bash
	$ pyi-makespec --onefile \
	--collect-all streamlit \
	--collect-all catboost \
	--collect-all etna \
	--collect-all pandas \
	--collect-all path \
	--recursive-copy-metadata streamlit \
	--recursive-copy-metadata catboost \
	--recursive-copy-metadata etna \
	--recursive-copy-metadata pandas \
	--recursive-copy-metadata path \
	--paths . src/app/script.py
	```
7. Prepare application files:
	```bash
	$ pyinstaller --clean script.spec
	```
9. Conduct test runs with `briefcase`:
	Run application in developer mode:
	```bash
	$ briefcase dev
	```
	Build and run application in distribution mode:
	```bash
	$ briefcase run
	```
10. Build the app and generate executable:
	```bash
	$ briefcase build
	$ briefcase package --adhoc-sign
	```
11. Deactivate your Python environment and run the executable:
	```bash
	$ deactivate
	$ open dist/app-0.0.1.dmg
	```

