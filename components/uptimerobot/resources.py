from kapitan.inputs.kadet import BaseObj


class UptimeRobotProvider(BaseObj):
    def body(self):
        self.root.terraform.required_providers.uptimerobot = {
            "source": "louy/uptimerobot",
            "version": self.kwargs.version
        }
        self.root.provider.uptimerobot.api_key = self.kwargs.api_key
        self.root.data.uptimerobot_alert_contact.default.friendly_name = self.kwargs.email


class UptimeRobotMonitor(BaseObj):
    def body(self):
        self.root.resource.uptimerobot_monitor[self.kwargs.name] = {
            "friendly_name": self.kwargs.name,
            "url": self.kwargs.ip,
            "type": "port",
            "sub_type": "custom",
            "port": self.kwargs.port,

            "alert_contact": {
                "id": "${data.uptimerobot_alert_contact.default.id}"
            }
        }
