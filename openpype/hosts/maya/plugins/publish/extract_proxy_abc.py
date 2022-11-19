import os

from maya import cmds

from openpype.pipeline import publish
from openpype.hosts.maya.api.lib import (
    extract_alembic,
    suspended_refresh,
    maintained_selection,
    iter_visible_nodes_in_range
)


class ExtractAlembic(publish.Extractor):
    """Produce an alembic for bounding box geometry
    """

    label = "Extract Proxy (Alembic)"
    hosts = ["maya"]
    families = ["proxyAbc"]

    def process(self, instance):

        nodes, roots = self.get_members_and_roots(instance)
        start = float(instance.data.get("frameStartHandle", 1))
        end = float(instance.data.get("frameEndHandle", 1))

        attrs = instance.data.get("attr", "").split(";")
        attrs = [value for value in attrs if value.strip()]
        attrs += ["cbId"]

        attr_prefixes = instance.data.get("attrPrefix", "").split(";")
        attr_prefixes = [value for value in attr_prefixes if value.strip()]

        self.log.info("Extracting Proxy Meshes...")

        dirname = self.staging_dir(instance)
        filename = "{name}.abc".format(**instance.data)
        path = os.path.join(dirname, filename)

        options = {
            "step": instance.data.get("step", 1.0),
            "attr": attrs,
            "attrPrefix": attr_prefixes,
            "writeVisibility": True,
            "writeCreases": True,
            "writeColorSets": instance.data.get("writeColorSets", False),
            "writeFaceSets": instance.data.get("writeFaceSets", False),
            "uvWrite": True,
            "selection": True,
            "worldSpace": instance.data.get("worldSpace", True)
        }

        if not instance.data.get("includeParentHierarchy", True):

            options["root"] = roots
        if instance.data.get("visibleOnly", False):
            nodes = list(iter_visible_nodes_in_range(nodes,
                                                     start=start,
                                                     end=end))
        with suspended_refresh():
            with maintained_selection():
                # TODO: select the bb geometry
                self.create_proxy_geometry(instance,
                                           start,
                                           end)
                extract_alembic(file=path,
                                startFrame=start,
                                endFrame=end,
                                **options)

        if "representations" not in instance.data:
            instance.data["representations"] = []

        representation = {
            'name': 'abc',
            'ext': 'abc',
            'files': filename,
            'stagingDir': dirname
        }
        instance.data["representations"].append(representation)

        instance.context.data["cleanupFullPaths"].append(path)

        self.log.info("Extracted {} to {}".format(instance, dirname))
        #TODO: delete the bounding box

    def get_members_and_roots(self, instance):
        return instance[:], instance.data.get("setMembers")

    def create_proxy_geometry(self, instance, start, end):

        inst_selection = cmds.ls(instance.name, long=True)
        name_suffix = instance.data.get("nameSuffix")
        if instance.data.get("single", True):
            pass
