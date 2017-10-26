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
from ..exceptions import ForemastTemplateNotFound

LOG = logging.getLogger(__name__)

HERE = os.path.dirname(os.path.realpath(__file__))
LOCAL_TEMPLATES = '{0}/../templates/'.format(HERE)


def get_template_object(template_file=''):
    """Retrieve template.

    Args:
        template_file (str): Name of template file.

    Returns:
        jinja2.Template: Template ready to render.

    Raises:
        AssertionError: Configured path for templates does not exist.
        :obj:`foremast.exceptions.ForemastTemplateNotFound`: Requested template
            is not available.

    """
    jinja_lst = []

    if TEMPLATES_PATH:
        external_templates = os.path.expanduser(TEMPLATES_PATH)
        assert os.path.isdir(external_templates), 'Template path {0} not found'.format(external_templates)
        jinja_lst.append(external_templates)

    jinja_lst.append(LOCAL_TEMPLATES)

    jinjaenv = jinja2.Environment(loader=jinja2.FileSystemLoader(jinja_lst))

    try:
        template = jinjaenv.get_template(template_file)
    except jinja2.TemplateNotFound:
        message = 'Unable to find template "{template_file}" in paths {paths}'.format(
            template_file=template_file, paths=jinjaenv.loader.searchpath)
        LOG.error(message)
        raise ForemastTemplateNotFound(message)

    return template


def get_template(template_file='', **kwargs):
    """Get the Jinja2 template and renders with dict _kwargs_.

    Args:
        template_file (str): name of the template file
        kwargs: Keywords to use for rendering the Jinja2 template.

    Returns:
        String of rendered JSON template.

    """
    try:
        template = get_template_object(template_file)
    except ForemastTemplateNotFound:
        raise

    LOG.info('Rendering template %s', template.filename)
    for key, value in kwargs.items():
        LOG.debug('%s => %s', key, value)

    rendered_json = template.render(**kwargs)
    LOG.debug('Rendered JSON:\n%s', rendered_json)

    return rendered_json
