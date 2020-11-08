# incognito-k8s

[Incognito](https://incognito.org/) [virtual nodes](https://we.incognito.org/t/how-to-host-a-virtual-node/194) management on Kubernetes, using [Kapitan](https://kapitan.dev/).

### Install

```
pip3 install --user kapitan
```

### Prerequisites

- VMs setup and Kubernetes cluster up and running

### Setup

```
$ kapitan compile

Compiled uptimerobot (0.11s)
Compiled aws (0.15s)
Compiled private (0.31s)

$ tree
.
├── LICENSE
├── README.md
├── compiled
│   ├── aws
│   │   └── manifests
│   │       ├── node4_host_deployment.yml
│   │       └── node4_pvc.yml
│   ├── private
│   │   └── manifests
│   │       ├── node1_pvc.yml
│   │       ├── node1_tunnel_configmap.yml
│   │       ├── node1_tunnel_deployment.yml
│   │       ├── node1_tunnel_secret.yml
│   │       ├── node2_pvc.yml
│   │       ├── node2_tunnel_configmap.yml
│   │       ├── node2_tunnel_deployment.yml
│   │       ├── node2_tunnel_secret.yml
│   │       ├── node3_pvc.yml
│   │       ├── node3_tunnel_configmap.yml
│   │       ├── node3_tunnel_deployment.yml
│   │       └── node3_tunnel_secret.yml
│   └── uptimerobot
│       └── terraform
│           ├── node1_uptimerobot_monitor.tf.json
│           ├── node2_uptimerobot_monitor.tf.json
│           ├── node3_uptimerobot_monitor.tf.json
│           ├── node4_uptimerobot_monitor.tf.json
│           └── uptimerobot_provider.tf.json
├── components
│   ├── incognito
│   │   ├── __init__.py
│   │   ├── configmap.yml
│   │   ├── deployment_host.yml
│   │   ├── deployment_tunnel.yml
│   │   ├── pvc.yml
│   │   ├── resources.py
│   │   ├── secret.yml
│   │   └── tunnel.sh.j2
│   └── uptimerobot
│       ├── __init__.py
│       └── resources.py
├── inventory
│   ├── classes
│   │   └── common.yml
│   └── targets
│       ├── aws.yml
│       ├── private.yml
│       └── uptimerobot.yml
└── refs
    ├── ssh-key
    └── uptimerobot-api-key
```

### Examples

- Pods exposed as host ports on public cloud cluster
  - [aws.yml](./inventory/targets/aws.yml) -> using [incognito component](./components/incognito) -> compiles to [compiled/aws/manifests/](./compiled/aws/manifests)
  - Apply with `kubectl apply -f compiled/aws/manifests`
- Tunneled pods on private cluster to a public VM
  - [private.yml](./inventory/targets/private.yml) -> using [incognito component](./components/incognito) -> compiles to [compiled/private/manifests/](./compiled/private/manifests)
  - Makes use of an [encrypted SSH key](./refs/ssh-key) to SSH-tunnel to a public VM
  - Apply with `kapitan refs --reveal -f compiled/private/manifests/ | kubectl apply -f -`
- [UptimeRobot](https://uptimerobot.com/) alerts setup with Terraform
  - [uptimerobot.yml](./inventory/targets/uptimerobot.yml) -> using [uptimerobot component](./components/uptimerobot) -> compiles to [compiled/uptimerobot/terraform/](./compiled/uptimerobot/terraform)
  - Makes use of an [encrypted API key](./refs/uptimerobot-api-key) for authenticate with UptimeRobot API. Decrypt provider before applying `kapitan refs --reveal -f compiled/uptimerobot/terraform/uptimerobot_provider.tf.json`
  - Apply with `terraform apply compiled/uptimerobot/terraform`

### Public VM setup for tunneling

Using fresh Ubuntu on a cloud provider of your choice

```bash
# Check updates and patch
apt update && apt upgrade -y

# Add fail2ban to limit SSH spam
apt install fail2ban -y

# Create incognito user
adduser --disabled-password incognito

# Enable SSH gateway ports
sed -i 's/GatewayPorts no/GatewayPorts yes/g' /etc/ssh/sshd_config
systemctl restart ssh

# Add SSH key to incognito user
su incognito
mkdir ~/.ssh
echo "<SSH public key>" > ~/.ssh/authorized_keys
chown -R incognito:incognito ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh

# reboot and it's good to go!

# Don't forget to add your SSH key to 'refs/ssh-key' and set your VM public IP in inventory
```
