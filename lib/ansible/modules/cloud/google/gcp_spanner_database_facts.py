#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Google
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# ----------------------------------------------------------------------------
#
#     ***     AUTO GENERATED CODE    ***    AUTO GENERATED CODE     ***
#
# ----------------------------------------------------------------------------
#
#     This file is automatically generated by Magic Modules and manual
#     changes will be clobbered when the file is regenerated.
#
#     Please read more about how to change this file at
#     https://www.github.com/GoogleCloudPlatform/magic-modules
#
# ----------------------------------------------------------------------------

from __future__ import absolute_import, division, print_function
__metaclass__ = type

################################################################################
# Documentation
################################################################################

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ["preview"],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: gcp_spanner_database_facts
description:
- Gather facts for GCP Database
short_description: Gather facts for GCP Database
version_added: 2.8
author: Google Inc. (@googlecloudplatform)
requirements:
- python >= 2.6
- requests >= 2.18.4
- google-auth >= 1.3.0
options:
  instance:
    description:
    - The instance to create the database on.
    - 'This field represents a link to a Instance resource in GCP. It can be specified
      in two ways. You can add `register: name-of-resource` to a gcp_spanner_instance
      task and then set this instance field to "{{ name-of-resource }}" Alternatively,
      you can set this instance to a dictionary with the name key where the value
      is the name of your Instance'
    required: true
extends_documentation_fragment: gcp
'''

EXAMPLES = '''
- name:  a database facts
  gcp_spanner_database_facts:
      instance: "{{ instance }}"
      project: test_project
      auth_kind: serviceaccount
      service_account_file: "/tmp/auth.pem"
'''

RETURN = '''
items:
  description: List of items
  returned: always
  type: complex
  contains:
    name:
      description:
      - A unique identifier for the database, which cannot be changed after the instance
        is created. Values are of the form projects/<project>/instances/[a-z][-a-z0-9]*[a-z0-9].
        The final segment of the name must be between 6 and 30 characters in length.
      returned: success
      type: str
    extraStatements:
      description:
      - 'An optional list of DDL statements to run inside the newly created database.
        Statements can create tables, indexes, etc. These statements execute atomically
        with the creation of the database: if there is an error in any statement,
        the database is not created.'
      returned: success
      type: list
    instance:
      description:
      - The instance to create the database on.
      returned: success
      type: dict
'''

################################################################################
# Imports
################################################################################
from ansible.module_utils.gcp_utils import navigate_hash, GcpSession, GcpModule, GcpRequest, replace_resource_dict
import json

################################################################################
# Main
################################################################################


def main():
    module = GcpModule(
        argument_spec=dict(
            instance=dict(required=True, type='dict')
        )
    )

    if not module.params['scopes']:
        module.params['scopes'] = ['https://www.googleapis.com/auth/spanner.admin']

    items = fetch_list(module, collection(module))
    if items.get('databases'):
        items = items.get('databases')
    else:
        items = []
    return_value = {
        'items': items
    }
    module.exit_json(**return_value)


def collection(module):
    res = {
        'project': module.params['project'],
        'instance': replace_resource_dict(module.params['instance'], 'name')
    }
    return "https://spanner.googleapis.com/v1/projects/{project}/instances/{instance}/databases".format(**res)


def fetch_list(module, link):
    auth = GcpSession(module, 'spanner')
    response = auth.get(link)
    return return_if_object(module, response)


def return_if_object(module, response):
    # If not found, return nothing.
    if response.status_code == 404:
        return None

    # If no content, return nothing.
    if response.status_code == 204:
        return None

    try:
        module.raise_for_status(response)
        result = response.json()
    except getattr(json.decoder, 'JSONDecodeError', ValueError) as inst:
        module.fail_json(msg="Invalid JSON response with error: %s" % inst)

    if navigate_hash(result, ['error', 'errors']):
        module.fail_json(msg=navigate_hash(result, ['error', 'errors']))

    return result


if __name__ == "__main__":
    main()
