import os
from ayon_core.settings import get_project_settings
from ayon_core.lib import Logger


def create_workspace_mxp(workdir, project_name, project_settings=None):
    dst_filepath = os.path.join(workdir, "workspace.mxp")
    if os.path.exists(dst_filepath):
        return

    if not os.path.exists(workdir):
        os.makedirs(workdir)

    if not project_settings:
        project_settings = get_project_settings(project_name)
    max_script = project_settings["max"].get("mxp_workspace")
    directory_index = max_script.find("[Directories]")
    max_script = "{}ProjectFolder={}{}".format(
        max_script[:directory_index], workdir, max_script[directory_index:])
    print(max_script)

    # Skip if mxp script in settings is empty
    if not max_script:
        log = Logger.get_logger("create_workspace_mxp")
        log.debug("File 'workspace.mxp' not created. Settings value is empty.")
        return

    with open(dst_filepath, "w") as mxp_file:
        mxp_file.write(max_script)