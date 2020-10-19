# incognito-k8s

[Incognito](https://incognito.org/) [virtual node](https://we.incognito.org/t/how-to-host-a-virtual-node/194) on Kubernetes.

### Standalone

For exposing the virtual node directly from k8s.

Deployment + PVC + Service:

```
kubectl apply -f deployment-standalone.yaml
```

### Tunneled

For exposing the virtual node from private compute through a tunnel to a public VM.

Deployment (w/ tunnel sidecar) + PVC + ConfigMap + Secret:

```
kubectl apply -f deployment-tunnel.yaml
```

Public VM setup (fresh Ubuntu in this example):

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
```

### ARM

If you want to run the virtual node on ARM, like a Raspberry Pi4+ / k3s, Incognito  maintain [an ARM image](https://hub.docker.com/r/incognitochain/incognito-mainnet-arm/tags).

Also RPis don't like more than 1 incognito pod per host, so you can specify pod anti-affinity:

```yaml
spec:
  containers:
  ...
  affinity:
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - incognito
        topologyKey: "kubernetes.io/hostname"
```
