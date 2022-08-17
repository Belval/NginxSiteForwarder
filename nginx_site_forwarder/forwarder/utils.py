import os
import subprocess

with open("nginx_template.conf", "r") as f:
    NGINX_CONF_TEMPLATE = f.read()

def run_certbot():
    """
    Runs certbot to update the certificates
    """
    out = subprocess.run(["./scripts/update_certs"], capture_output=True)
    if out.returncode != 0:
        raise Exception("Failed to update certificates")

def restart_nginx():
    """
    Restart Nginx
    """
    out = subprocess.run(["./scripts/restart_nginx"])
    if out.returncode != 0:
        raise Exception("Failed to restart Nginx")

def add_config(forwarding):
    """
    Creates and save a new Nginx config
    """
    conf = NGINX_CONF_TEMPLATE.replace("[SUBDOMAIN]", forwarding.subdomain)
    conf = conf.replace("[DESTINATION]", forwarding.destination)

    with open(f"/etc/nginx/conf.d/{forwarding.subdomain}.belval.conf", "w") as f:
        f.write(conf)

def remove_config(forwarding):
    """
    Deletes an Nginx config
    """

    os.remove(f"/etc/nginx/conf.d/{forwarding.subdomain}.belval.conf")
