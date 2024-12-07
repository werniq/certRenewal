#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: certRenewal

short_description: Module for renewing TLS certificates

version_added: "1.0.0"

description: This module renews TLS certificates for a given domain.

options:
    domain_name:
        description: Domain name for which the certificate needs to be renewed 
        required: true
        type: str
    cert_path: 
        description: Path to the certificate file
        required: true
        type: str
    key_path:
        description: Path to the key file
        required: true
        type: str
    ca_path:
        description: Path to the CA file
        required: true
        type: str

author:
    - Your Name (@werniq)
'''

EXAMPLES = r'''
- name: Test the module
    certRenewal:
        domain_name: "example.com"
        cert_path: "/etc/ssl/certs/example.com.crt"
        key_path: "/etc/ssl/private/example.com.key"
        ca_path: "/etc/ssl/certs/ca.crt"
'''

RETURN = r'''
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        domain_name=dict(type='str', required=True),
        cert_path=dict(type='str', required=True),
        key_path=dict(type='str', required=True),
        ca_path=dict(type='str', required=True),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    domain_name = module.params['domain_name']
    cert_path = module.params['cert_path']
    key_path = module.params['key_path']
    ca_path = module.params['ca_path']

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['message'] = 'Certificates were successfully renewed for domain: ' + domain_name

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['new']:
        result['changed'] = True

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()