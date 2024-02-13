# -*- coding: utf-8 -*-
"""Collect current work file."""
import os
import pyblish.api

from pymxs import runtime as rt


class CollectWorkfile(pyblish.api.InstancePlugin):
    """Inject the current working file into context"""

    order = pyblish.api.CollectorOrder - 0.01
    label = "Collect 3dsmax Workfile"
    hosts = ['max']

    def process(self, instance):
        """Inject the current working file."""
        context = instance.context
        folder = rt.maxFilePath
        file = rt.maxFileName
        if not folder or not file:
            self.log.error("Scene is not saved.")
        current_file = os.path.join(folder, file)

        context.data['currentFile'] = current_file

        ext = os.path.splitext(file)[-1].lstrip(".")

        data = {}

        # create instance

        data.update({
            "setMembers": [current_file],
            "frameStart": context.data['frameStart'],
            "frameEnd": context.data['frameEnd'],
            "handleStart": context.data['handleStart'],
            "handleEnd": context.data['handleEnd']
        })

        data['representations'] = [{
            'name': ext,
            'ext': ext,
            'files': file,
            "stagingDir": folder,
        }]

        instance.data.update(data)
        self.log.debug('Collected data: {}'.format(data))
        self.log.debug('Collected instance: {}'.format(file))
        self.log.debug('Scene path: {}'.format(current_file))
        self.log.debug('staging Dir: {}'.format(folder))
