import os

from aws_cdk import Environment

from .helper import load_yamls, load_yamls_to_dict

# Load environment definitions
dirname = os.path.dirname(__file__)

#props_paths=f"./{os.environ['props_paths']}"
props_paths=f"../environment_options/environment_options.yaml"
#props = (load_yamls(os.path.join(dirname, "environment_options_example.yaml")))[0]

props = (load_yamls(os.path.join(dirname,props_paths )))[0]

env_devsecops_account = Environment(account=props['devsecops_account'], region=props['devsecops_region'])
env_client_deployment_account = Environment(account=props['deployment_account'], region=props['deployment_region'])
env_client_stg_account = Environment(account=props['stg_account'], region=props['stg_region'])
# load tags
#tags = (load_yamls(os.path.join(dirname,props_paths )))[1]['tags']
tags = props['tags']

