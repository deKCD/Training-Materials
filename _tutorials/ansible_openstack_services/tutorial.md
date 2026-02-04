---
layout: tutorial_hands_on

title: Using Ansible to Deploy and Operate (Web)Services on the de.NBI Cloud
description: This tutorial teaches you how to use Ansible to deploy and manage (web)services on the de.NBI Cloud OpenStack infrastructure. It introduces you to the basics of Ansible and guides you through writing infrastructure-as-code to automate the deployment and operation of your services, using Docker and optionally Docker Swarm.
slug: ansible_webservices_denbi_cloud
time_estimation: 1H
questions:
  - Which questions are addressed by the tutorial?
objectives:
  - Learn to access and use the de.NBI Cloud OpenStack API with Ansible
  - Learn how to Write infrastructure-as-code using Ansible to deploy your (web)service
  - Learn how to set up additional 
key_points:
- The take-home messages
- They will appear at the end of the tutorial
version: main
life_cycle: alpha
contributions:
  authorship:
  - Nils Hoffmann
  editing: 
  funding: 
---

# Tutorial: Setting up a Docker Swarm Project with Ansible on OpenStack (de.NBI Cloud, Bielefeld)

## Introduction

This tutorial provides a step-by-step guide to setting up a Docker Swarm project using Ansible for automation and OpenStack integration on the de.NBI Cloud site in Bielefeld. The process involves preparing your local environment, configuring OpenStack resources, setting up Ansible, and deploying infrastructure and services.

> ## Prerequisites
> This tutorial assumes a familiarity with the following concepts:
> - [Linux command line and SSH]( {% link _tutorials/unix-course/main/tutorial.md %} )
> - [Basic knowledge of Ansible and YAML syntax](https://training.galaxyproject.org/training-material/topics/admin/tutorials/ansible/tutorial.html)
> - [Familiarity with OpenStack concepts (projects, flavors, networks)](https://cloud.denbi.de/wiki/Concept/basics/)
> - [Basic understanding of Docker and containerization](https://carpentries-incubator.github.io/docker-introduction/index.html)
>
> This tutorial is designed for advanced users who are comfortable with command-line tools, automation and who want to deploy and expose their own (bioinformatics) services to outside users. In order to follow along, you will **should** have an active OpenStack project on the de.NBI Cloud platform. If you do not have an account, please register at [de.NBI Cloud](https://cloud.denbi.de/) and apply for a project. 
> Most steps in this tutorial can be adapted to other OpenStack providers with minor modifications.
> 
{: .details}

Note: This tutorial is generalized from the LipidCompass deployment playbooks. Docker Swarm setup is optional and can be skipped if not required for your project.

## Concepts Covered

- ssh key management and secure access
- OpenStack project and resource configuration
- Ansible basics and role-based architecture
- OpenStack resource management with Ansible
- Docker Swarm setup and service deployment
- Infrastructure-as-code principles

## Prerequisites

### Local Machine Setup

Ensure the following software is installed on your local machine:

- Ansible >= 2.16
- Python >= 3.8
- OpenStack SDK >= 4.0.0

Install the required Python packages in a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements-pip.txt
```

Install necessary Ansible collections:

```bash
ansible-galaxy collection install ansible.posix community.general openstack.cloud community.docker
```

### SSH Key Setup

Generate or use an existing SSH key pair for secure connections:

```bash
# Generate a new key pair (optional)
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

Refer to [de.NBI Cloud SSH setup guide](https://cloud.denbi.de/wiki/quickstart/#ssh-setup) for detailed instructions.

## OpenStack Preparations

### Create a New Project

1. Access your OpenStack project dashboard.
2. Create a new project or select an existing one with appropriate permissions.
3. Ensure required VM flavors are available (check `group_vars/openstack.yml` for specifics).
4. Create a router named `<your-project-shortname>-router` if it doesn't exist (under Network > Routers).

### Configure OpenStack Credentials

1. Go to Identity > Application Credentials.
2. Create new application credentials and save the secret securely.
3. Download the `clouds.yaml` file from API Access > Download OpenStack RC-File.
4. Place or append it to `~/.config/openstack/clouds.yaml`.
5. Edit the file to configure your cloud:

```yaml
clouds:
  <your-project-shortname>-prod:
    auth:
      auth_url: https://openstack.cebitec.uni-bielefeld.de:5000
      application_credential_id: "your-application-credential-id"
      application_credential_secret: "your-secret"
    region_name: "Bielefeld"
    interface: "public"
    identity_api_version: 3
    auth_type: "v3applicationcredential"
```

## Ansible Configuration

### Prepare Ansible Config

1. Copy the template configuration:

```bash
cp ansible.cfg.tmpl ansible.cfg
chmod go-rwx ansible.cfg
```

2. Review and adapt `ansible.cfg` as needed.

### Update OpenStack Deployment Variables

Edit `group_vars/openstack.yml` to set your SSH key path and other variables:

```yaml
my:
  openstack_cloud: "openstack"
  openstack_project: "YourProjectName"
  ssh:
    key:
      name: "YOUR_USER_NAME"
      public: "/home/YOUR_USER_NAME/.ssh/ID_OF_YOUR_PUBLIC_KEY.pub"
```

### Configure SSH Access

Add the following to your `~/.ssh/config` file:

```bash
Host <your-project-shortname>
  HostName FLOATING_IP_OF_YOUR_JUMPHOST
  IdentityFile ~/.ssh/ID_OF_YOUR_PRIVATE_KEY
  User ubuntu
  Port 22
  ForwardAgent yes
  AddKeysToAgent yes
  UserKnownHostsFile /dev/null
  StrictHostKeyChecking no

# Internal network subnet
Host 192.168.1.*
  User ubuntu
  IdentityFile ~/.ssh/ID_OF_YOUR_PRIVATE_KEY
  Port 22
  ProxyJump <your-project-shortname>
```

### Prepare Secrets

1. Copy the secrets template:

```bash
cp secrets.tmpl group_vars/all/secrets
```

2. Edit the secrets file with your passwords and sensitive data.
3. Encrypt the secrets file:

```bash
ansible-vault encrypt group_vars/all/secrets
```

4. Set up the vault password file:

```bash
mkdir -p ~/.<your-project-shortname>
chmod -R go-rwx ~/.<your-project-shortname>
chmod -R g+s ~/.<your-project-shortname>
echo "your_vault_password" > ~/.<your-project-shortname>/vault.pwd
chmod o-rwx ~/.<your-project-shortname>/vault.pwd
```

## Deployment Configuration and Topology

The main deployment configuration is located in `group_vars/openstack.yml`. This file defines the infrastructure topology, including VM flavors, network settings, and firewall rules. Adjust these settings to fit your project's requirements.

> ## Customization of Deployment Configuration
> Please note that the provided configurations are examples and should be tailored to your specific needs and to the OpenStack quotas and available flavors in your project. 
> The flavors defined in the example are based on the de.NBI Cloud OpenStack environment at the Bielefeld cloud site.
> 
{: .details}



## Bootstrapping the Infrastructure

Run the bootstrap playbooks to set up the basic infrastructure:

```bash
export ANSIBLE_CONFIG=ansible.bi.cfg
ansible-playbook bootstrap-openstack.yml
ansible-playbook bootstrap.yml
```

This process may take some time. The playbooks will create VMs, networks, and other necessary resources in your OpenStack project.

## Service Configuration and Deployment

Separation of concerns and DRY (Don't Repeat Yourself) are important design principles in software engineering and IT operations. For infrastructure-as-code, this means separating the configuration of different services into distinct roles and configurations, maintaining clear responsibilities. Ultimately, we want to avoid monolithic playbooks that handle everything in one place and instead have modular, reusable components, which can be granularly composed to form the desired infrastructure.

To realize this requirement, Ansible supports you with the 'role' abstraction. 

### Introduction to Ansible Roles

Ansible roles are self-contained units of configuration that can be shared and reused across different playbooks. Each role contains tasks, variables, files, templates, and handlers related to a specific functionality. Roles are defined in a directory structure below the 'roles' folder with specific subdirectories for each component. 

A helpful guide on creating Ansible roles can be found [here](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html).

Roles can be understood as modular components that encapsulate specific configurations or functionalities, typically of a service, but also of cross-cutting functionalities. They help in organizing playbooks and promoting code reuse, following the DRY (Don't Repeat Yourself) principle.

1. Create a custom ansible role for your application by creating a new directory in the `roles/` folder.

The directory structure for a role with the name 'your_service_role' should look like this:

```roles/
└── your_service_role/
    ├── tasks/main.yml
    ├── handlers/main.yml
    ├── vars/main.yml
    ├── templates/
    │   └── docker-compose.yml.j2
    └── files/
```

2. Define tasks, handlers, variables, and templates specific to your service within the role's subdirectories.
3. Create a templated docker compose file for your service in `templates/`.


## Deploying Docker Swarm Infrastructure Services

Deploy the core infrastructure services:

```bash
ansible-playbook swarm-services.yml
```

This sets up services like monitoring, logging, and storage that your application may depend on.

## Optional: Docker Swarm Setup

If you need to set up Docker Swarm for container orchestration:

```bash
ansible-playbook swarm-setup.yml
ansible-playbook swarm-bootstrap.yml
```

Then deploy your application stacks:

```bash
ansible-playbook swarm-<your-project-shortname>.yml  # Replace with your application playbook
```

## Maintenance

### Update and Upgrade

To update packages and reboot if necessary:

```bash
ansible-playbook update.yml reboot.yml
```

### Database Backup and Restore

If your project includes databases, refer to the backup procedures in the original README for automated backups and manual restore processes.

## Troubleshooting

- Ensure all prerequisites are met and virtual environment is activated.
- Check OpenStack quotas and resource availability.
- Verify SSH connectivity and key permissions.
- Use `ansible-playbook --check` for dry-run testing.
- Check logs in `/var/log/ansible/` on target hosts.

## Additional Resources

- [Ansible Documentation](https://docs.ansible.com/)
- [OpenStack SDK Documentation](https://docs.openstack.org/openstacksdk/)
- [de.NBI Cloud Documentation](https://cloud.denbi.de/)
- [Docker Swarm Documentation](https://docs.docker.com/engine/swarm/)

This tutorial provides a foundation for deploying containerized applications on OpenStack using Ansible. Adapt the playbooks and variables to fit your specific project requirements.


