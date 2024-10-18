# School server - crowdsec
Installs crowdsec agent and configures it to scan Traefik logs. Additionally
the firewall bouncer is installed to enforce bans by blocking malicious actors.

Most tasks are heavily inspired by https://github.com/papanito/ansible-role-crowdsec/tree/main

Crowdsec is deployed as packages directly from the creators repositories. It
could also be deployed as Docker containers (https://hub.docker.com/r/crowdsecurity/crowdsec).

Sources:
 - https://www.heise.de/ratgeber/Intrusion-Prevention-Boeswillige-IP-Adressen-sperren-mit-CrowdSec-9957242.html
 - https://doc.crowdsec.net/docs/getting_started/install_crowdsec/
 - https://doc.crowdsec.net/u/bouncers/firewall/
 - https://plugins.traefik.io/plugins/6335346ca4caa9ddeffda116/crowdsec-bouncer-traefik-plugin
 - https://github.com/crowdsecurity/grafana-dashboards/
 - https://goneuland.de/traefik-v2-3-reverse-proxy-mit-crowdsec-im-stack-einrichten/
