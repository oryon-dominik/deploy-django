from pathlib import Path as __Path

BASE_PATH = __Path(__file__).parent

# The script that will be called to make the deployment:
DEPLOYMENT_SCRIPT = __Path(BASE_PATH, 'example_deployment.py')
