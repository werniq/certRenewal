# Base Ansible Module: `certRenewal`

This project provides a foundational Ansible module written in Python, designed to renew TLS certificates for specified domains.

---

## Features

- **TLS Certificate Renewal**: Automates the process of renewing certificates for a given domain.
- **Customizable Parameters**: Flexible options for specifying domain, certificate, key, and CA file paths.
- **Reusable Base**: Implements best practices for Ansible module development, making it suitable for extensions.
- **Documentation**: Includes user-friendly examples, parameter descriptions, and return value details.

---

## Usage

### 1. Options
The `certRenewal` module supports the following parameters:

| Parameter   | Description                               | Required | Type   |
|-------------|-------------------------------------------|----------|--------|
| `domain_name` | Domain name for the certificate renewal   | Yes      | String |
| `cert_path`   | Path to the certificate file             | Yes      | String |
| `key_path`    | Path to the key file                     | Yes      | String |
| `ca_path`     | Path to the CA file                      | Yes      | String |

### 2. Example Playbook

Here's an example of how to use the `certRenewal` module in an Ansible playbook:

```yaml
- name: Renew TLS certificates for a domain
  hosts: localhost
  tasks:
    - name: Renew certificates
      certRenewal:
        domain_name: "example.com"
        cert_path: "/etc/ssl/certs/example.com.crt"
        key_path: "/etc/ssl/private/example.com.key"
        ca_path: "/etc/ssl/certs/ca.crt"
