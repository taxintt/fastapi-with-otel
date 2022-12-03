import os

STAGE = os.environ.get("STAGE") or "local"
GCP_PROJECT = os.environ.get("GCP_PROJECT")

# see https://cloud.google.com/run/docs/reference/container-contract#env-vars
K_SERVICE = os.environ.get("K_SERVICE")
K_REVISION = os.environ.get("K_REVISION")
K_CONFIGURATION = os.environ.get("K_CONFIGURATION")

ON_CLOUD_RUN = bool(K_SERVICE and K_REVISION and K_CONFIGURATION)