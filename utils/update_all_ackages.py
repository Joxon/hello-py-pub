import pkg_resources
from subprocess import call

packages = [dist.project_name for dist in pkg_resources.working_set]
print(packages)
call("pip install --upgrade " + ' '.join(packages), shell=True)
