from django.contrib import admin
from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from forwarder.utils import add_config, remove_config, run_certbot, restart_nginx

class Forwarding(models.Model):
    subdomain = models.CharField(max_length=40)
    destination = models.CharField(max_length=40)

@admin.register(Forwarding)
class ForwardingAdmin(admin.ModelAdmin):
    fields = ("subdomain", "destination")
    list_display = ("subdomain", "destination")

@receiver(pre_save, sender=Forwarding)
def create_or_save(sender, instance, raw, using, update_fields, **kwargs):
    add_config(instance)
    run_certbot()
    restart_nginx()


@receiver(pre_delete, sender=Forwarding)
def delete(sender, instance, **kwargs):
    remove_config(instance)
    restart_nginx()
