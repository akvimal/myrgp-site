#!/usr/bin/env bash
# Pull the latest site, rebuild the container, and sync the Caddy block. Run on the VPS:
#   cd /root/apps/myrgp-site && ./scripts/deploy.sh
set -euo pipefail
cd "$(dirname "$0")/.."

CADDY_CONTAINER="${CADDY_CONTAINER:-$(docker ps -q --filter label=com.docker.compose.project=caddy --filter label=com.docker.compose.service=caddy | head -n1)}"
CADDY_SITES="${CADDY_SITES:-/root/apps/edge-caddy/sites}"

git fetch --quiet origin
git reset --hard origin/main
docker compose up -d --build --remove-orphans
docker image prune -f >/dev/null
docker exec myrgp-web wget -q --spider http://127.0.0.1/ && echo "myrgp-web is serving"

# Sync the Caddy site block only when it changed; roll back if Caddy rejects it
if ! cmp -s proxy/myrgp.caddy "$CADDY_SITES/myrgp.caddy"; then
  [ -f "$CADDY_SITES/myrgp.caddy" ] && cp "$CADDY_SITES/myrgp.caddy" /tmp/myrgp.caddy.prev
  cp proxy/myrgp.caddy "$CADDY_SITES/myrgp.caddy"
  if docker exec "$CADDY_CONTAINER" caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile 2>&1 | tail -n 20 >&2; [ "${PIPESTATUS[0]}" -eq 0 ]; then
    docker exec "$CADDY_CONTAINER" caddy reload --config /etc/caddy/Caddyfile --adapter caddyfile
    echo "Caddy reloaded with new myrgp.caddy"
  else
    echo "Caddy rejected myrgp.caddy, restoring previous version" >&2
    if [ -f /tmp/myrgp.caddy.prev ]; then cp /tmp/myrgp.caddy.prev "$CADDY_SITES/myrgp.caddy"; else rm -f "$CADDY_SITES/myrgp.caddy"; fi
    exit 1
  fi
fi
