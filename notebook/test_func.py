import os
from pathlib import Path  

print(Path(__file__).resolve())
print(Path(__file__).resolve().parent) 
print(Path(__file__).resolve().parent.parent) 