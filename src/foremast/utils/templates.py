#   Foremast - Pipeline Tooling
#
#   Copyright 2016 Gogo, LLC
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""Render Jinja2 template."""
import logging
import os

import jinja2

from ..consts import TEMPLATES_PATH

LOG = logging.getLogger(__name__)


def get_template(template_file='', **kwargs):
    """Get the Jinja2 template and renders with dict _kwargs_.

    Args:
        template_file (str): name of the template file
        kwargs: Keywords to use for rendering the Jinja2 template.

    Returns:
        String of rendered JSON template.
    """

    here = os.path.dirname(os.path.realpath(__file__))
    templatedir = '{0}/../templates/'.format(here)

    if TEMPLATES_PATH:
        if not os.path.isdir(TEMPLATES_PATH):
            templatedir = '{0}/../../../{1}'.format(here, TEMPLATES_PATH)
            assert os.path.isdir(templatedir), 'Template path {0} not found'.format(
                    TEMPLATES_PATH)
        else:
            templatedir = TEMPLATES_PATH

    if TEMPLATES_PATH and not os.path.isfile( templatedir + template_file):
        templatedir = '{0}/../templates/'.format(here)

    LOG.info('Rendering template %s from %s', template_file, templatedir)

    LOG.debug('Template directory: %s', templatedir)
    LOG.debug('Template file: %s', template_file)

    jinjaenv = jinja2.Environment(loader=jinja2.FileSystemLoader(templatedir))
    template = jinjaenv.get_template(template_file)
    for key, value in kwargs.items():
        LOG.debug('%s => %s', key, value)
    rendered_json = template.render(**kwargs)

    LOG.debug('Rendered JSON:\n%s', rendered_json)
    return rendered_json
