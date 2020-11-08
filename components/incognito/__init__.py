from .resources import DeploymentHost, DeploymentTunnel, ConfigMap, Secret, PersistentVolumeClaim
from kapitan.inputs.kadet import BaseObj, inventory
p = inventory().parameters


def main():
    obj = BaseObj()

    for node_name in p.nodes.keys():
        node = p.nodes[node_name]
        if node.type == "host":
            obj.root[node_name + "_host_deployment"] = DeploymentHost(
                name=node_name,
                image=node.image,
                validator_key=node.validator_key,
                infura_url=node.infura_url,
                rpc_port=node.rpc_port,
                node_port=node.node_port,
                node_selector=node.node_selector
            )
        elif node.type == "tunnel":
            obj.root[node_name + "_tunnel_deployment"] = DeploymentTunnel(
                name=node_name,
                image=node.image,
                tunnel_image=node.tunnel_image,
                validator_key=node.validator_key,
                infura_url=node.infura_url,
                node_selector=node.node_selector
            )
            obj.root[node_name + "_tunnel_configmap"] = ConfigMap(
                name=node_name + "-ssh-script",
                rpc_port=node.rpc_port,
                node_port=node.node_port,
                public_ip=node.public_ip
            )
            obj.root[node_name + "_tunnel_secret"] = Secret(
                name=node_name + "-ssh",
                key=node.ssh_key
            )
        else:
            raise Exception(f"Expected node.type to be 'host' or 'tunnel', got {node.type}")

        obj.root[node_name + "_pvc"] = PersistentVolumeClaim(
            name=node_name + "-data",
            storage=node.pvc_storage
        )

    return obj
