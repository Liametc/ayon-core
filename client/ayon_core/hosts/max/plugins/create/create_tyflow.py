# -*- coding: utf-8 -*-
"""Creator plugin for creating TyCache."""
from ayon_core.hosts.max.api import plugin


class CreateTyFlow(plugin.MaxCacheCreator):
    """Creator plugin for TyCache."""
    identifier = "io.openpype.creators.max.tyflow"
    label = "TyFlow"
    product_type = "tyflow"
    icon = "gear"