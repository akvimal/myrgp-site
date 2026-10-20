# Static site image for https://myrgp.in
# Serves public/ on port 80 inside the container. TLS is handled by the
# Caddy front door on the VPS (see proxy/myrgp.caddy).
FROM nginx:1.27-alpine

COPY docker/site.conf /etc/nginx/conf.d/default.conf
COPY public/ /usr/share/nginx/html/

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget -q --spider http://127.0.0.1/ || exit 1
