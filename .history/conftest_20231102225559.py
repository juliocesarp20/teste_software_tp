import os
import sys

# Get the absolute path to the 'model' directory
model_path = os.path.abspath("model")

# Add the 'model' directory to the Python path
sys.path.append(model_path)

repository_path = os.path.abspath("repository")

# Add the 'model' directory to the Python path
sys.path.append(repository_path)