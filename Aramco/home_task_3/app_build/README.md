# Instructions for building the app
## Anaconda

1. Install [Anaconda](https://docs.anaconda.com/free/anaconda/install/index.html)
2. Open the **project root directory** and create a new conda environment using `3.10` Python version:
	> Note: `$` character marks the beginning of a command, you don’t need to use it in the command itself.

	```bash
    	$ conda create -n environment python=3.10
	```

3. Activate the newly created environment:
	```bash
	$ conda activate environment
	```
4. Instll packages necessary for building the app:
   	```bash
    	$ conda install -c conda-forge streamlit pyinstaller
    	$ conda install -c anaconda path.py
    	$ pip install etna==1.15.0 briefcase 
    	```
4. Run the application script with Streamlit to make sure that it works:
	```bash
	$ cd srs/app
	$ streamlit run sript.py
	```
5. Return to the root directory and run the `Pyinstaller` command to create the application config:
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
	$ briefcase package
	```
11. Deactivate Python environment and run your application:
	```bash
	$ deactivate
	$ dist/app-0.0.1.msi
	```


## Vanilla Python
> Note: The following instructions are only macOS compatible.

1. Install [Python](https://www.python.org/downloads/macos/)
2. Open the **project root directory** and create a new Python environment using `3.10` Python version:
	> Note: `$` character marks the beginning of a command, you don’t need to use it in the command itself.

	```bash
	$ python3.10 -m venv environment
	```

3. Activate the newly created environment:
	```bash
	$ source environment/bin/activate
	```
4. Upgrade `pip`:
	```bash
	$ pip install --upgrade pip
	```
5. Install packages specified in the `requirements.txt` file:
	```
	$ pip install -r requirements.txt
	```
6. Run the application script with Streamlit to make sure that it works:
	```bash
	$ cd srs/app
	$ streamlit run sript.py
	```
7. Return to the root directory and run the `Pyinstaller` command to create the application config:
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
8. Prepare application files:
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
11. Deactivate Python environment and run your application:
	```bash
	$ deactivate
	$ open dist/app-0.0.1.dmg
	```

