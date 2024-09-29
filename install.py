import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

dependencies = [
    'beautifulsoup4',
    'pyodbc',
]

for package in dependencies:
    install(package)

print("Tüm bağımlılıklar yüklendi.")