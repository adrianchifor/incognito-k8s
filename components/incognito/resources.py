from kapitan.inputs.kadet import BaseObj
from kapitan.utils import render_jinja2_file


class DeploymentHost(BaseObj):
    def new(self):
        self.update_root("components/incognito/deployment_host.yml")

    def body(self):
        self.root.metadata.name = self.kwargs.name
        self.root.spec.template.spec.volumes[0].persistentVolumeClaim.claimName = self.kwargs.name + "-data"
        self.root.spec.template.spec.containers[0].image = self.kwargs.image
        self.root.spec.template.spec.containers[0].ports[0].hostPort = self.kwargs.rpc_port
        self.root.spec.template.spec.containers[0].ports[1].hostPort = self.kwargs.node_port
        self.root.spec.template.spec.containers[0].env[0].value = self.kwargs.validator_key
        self.root.spec.template.spec.containers[0].env[1].value = self.kwargs.infura_url
        if self.kwargs.node_selector:
            self.root.spec.template.spec.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[
                0].matchExpressions[0]["values"][0] = self.kwargs.node_selector
        else:
            self.root.spec.template.spec.affinity = {}


class DeploymentTunnel(BaseObj):
    def new(self):
        self.update_root("components/incognito/deployment_tunnel.yml")

    def body(self):
        self.root.metadata.name = self.kwargs.name
        self.root.spec.template.spec.volumes[0].persistentVolumeClaim.claimName = self.kwargs.name + "-data"
        self.root.spec.template.spec.volumes[1].configMap.name = self.kwargs.name + "-ssh-script"
        self.root.spec.template.spec.volumes[2].secret.secretName = self.kwargs.name + "-ssh"
        self.root.spec.template.spec.containers[0].image = self.kwargs.image
        self.root.spec.template.spec.containers[0].env[0].value = self.kwargs.validator_key
        self.root.spec.template.spec.containers[0].env[1].value = self.kwargs.infura_url
        self.root.spec.template.spec.containers[1].image = self.kwargs.tunnel_image
        if self.kwargs.node_selector:
            self.root.spec.template.spec.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[
                0].matchExpressions[0]["values"][0] = self.kwargs.node_selector
        else:
            self.root.spec.template.spec.affinity = {}


class ConfigMap(BaseObj):
    def new(self):
        self.update_root("components/incognito/configmap.yml")

    def body(self):
        self.root.metadata.name = self.kwargs.name
        self.root.data["tunnel.sh"] = render_jinja2_file("components/incognito/tunnel.sh.j2", {
            "rpc_port": self.kwargs.rpc_port,
            "node_port": self.kwargs.node_port,
            "public_ip": self.kwargs.public_ip
        })


class Secret(BaseObj):
    def new(self):
        self.update_root("components/incognito/secret.yml")

    def body(self):
        self.root.metadata.name = self.kwargs.name
        self.root.data.key = self.kwargs.key


class PersistentVolumeClaim(BaseObj):
    def new(self):
        self.update_root("components/incognito/pvc.yml")

    def body(self):
        self.root.metadata.name = self.kwargs.name
        self.root.spec.resources.requests.storage = self.kwargs.storage
