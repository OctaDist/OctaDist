!#/bin/bash

chmod +x octadist_main.py

pyinstaller --onefile --version-file=version.txt -i molecule.ico main.py

