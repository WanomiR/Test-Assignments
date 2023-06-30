import sys
from streamlit.web import cli
from streamlit.web.cli import configurator_options, main
from path import Path
from streamlit.web import bootstrap
import os


@main.command("hello")
@configurator_options
def main_wceapp(**kwargs):
    """Runs the script."""
    bootstrap.load_config_options(flag_options=kwargs)
    app_directory = Path(__file__).parent
    filename = str(app_directory.joinpath("script.py"))  # .abspath()
    cli._main_run(filename, flag_options=kwargs)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    kwargs = {
        "--server.enableXsrfProtection=false",
        "--server.enableCORS=true",
        "--server.port=3031",
        "--global.developmentMode=false",
    }
    sys.exit(main_wceapp(kwargs))

# import os
# import subprocess
# from path import Path  # library for handling file paths

# path = os.path.dirname(__file__)
# path = Path(path)
# path = Path(__file__).parent
# os.chdir(path)  # Change working directory


# if __name__ == "__main__":
#     result = subprocess.run(["streamlit", "script", "script.py"], stdout=subprocess.PIPE)
