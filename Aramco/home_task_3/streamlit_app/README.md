# Instructions for building the app
1. Install python.
2. From the project directory, create a new Python environment using Python version `3.10`:
```bash
$ python3.10 -m venv environment
```
3. Activate the newly created environment:
```bash
$ source environment/bin/activate
```
for windows:
```
$ \venv\Scripts\activate.bat
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
	1. Run application in developer mode:
	```bash
	$ briefcase dev
	```
	2. Build and run application in distribution mode:
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
$ open dist/app-0.0.1.dmg
```
