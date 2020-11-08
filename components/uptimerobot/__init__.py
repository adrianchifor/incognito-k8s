from .resources import UptimeRobotProvider, UptimeRobotMonitor
from kapitan.inputs.kadet import BaseObj, inventory_global
inv = inventory_global()


def main():
    obj = BaseObj()

    for target in inv.keys():
        p = inv[target].parameters
        if "uptimerobot" in p:
            obj.root["uptimerobot_provider.tf"] = UptimeRobotProvider(
                version=p.uptimerobot.version,
                api_key=p.uptimerobot.api_key,
                email=p.uptimerobot.email
            )
        if "nodes" in p:
            for node_name in p.nodes.keys():
                node = p.nodes[node_name]
                obj.root[node_name + "_uptimerobot_monitor.tf"] = UptimeRobotMonitor(
                    name=node_name,
                    ip=node.public_ip,
                    port=node.rpc_port
                )

    return obj
