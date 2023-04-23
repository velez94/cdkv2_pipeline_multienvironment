import os

from aws_cdk import Environment

from .helper import load_yamls, load_yamls_to_dict

# Load environment definitions
dirname = os.path.dirname(__file__)

# props_paths=f"./{os.environ['props_paths']}"
props_paths = f"../environment_options/environment_options.yaml"
# props = (load_yamls(os.path.join(dirname, "environment_options_example.yaml")))[0]

props = (load_yamls(os.path.join(dirname, props_paths)))[0]

env_devsecops_account = Environment(account=props['devsecops_account'], region=props['devsecops_region'])
props["def_environments"] = {}
environments = {}

for e in props["environments"]:

    environments[e["name"]] = Environment(account=e['deployment_account'], region=e['deployment_region'])
    # Create environment definitions copy

    props["def_environments"][e["name"]] = {
        "deployment_region": e["deployment_region"],
        "deployment_account": e["deployment_account"],
        "enable": e["enable"]
    }

    if "partner_review_email" in e.keys():
        props["def_environments"][e["name"]]["partner_review_email"] = e["partner_review_email"]

props["environments"] = environments

# load tags
tags = props['tags']
