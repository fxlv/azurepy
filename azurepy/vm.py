from subprocess import Popen, PIPE
import json
import os
import sys

class AzureVM():
    def __init__(self, subscription_id):
        self.subscription_id = subscription_id
        if not self.check_subscription():
            print "Invalid subscription provided"
            print "You have the following ones available:"
            for name, sub_id in self.get_subscriptions():
                print name, sub_id
            sys.exit(1)
        self.set_subscription()

    def set_subscription(self):
        self.run_command("azure account set --json {}".format(self.subscription_id))

    def run_command(self, command):
        print "DEBUG: running command: {}".format(command)
        process = Popen(command.split(), stdout=PIPE, stderr=PIPE)
        process.wait()
        stdout, stderr = process.communicate()
        if stderr:
            print "DEBUG: Stderr: {}".format(stderr)
            return False
        if stdout == "":
            stdout = "{}"  # always return JSON, even when empty
        try:
            return_json = json.loads(stdout)
            return return_json
        except Exception, e:
            print "DEBUG: JSON exception {}".format(e)
            print "DATA: {}".format(stdout)
            return False
    def delete_vm(vm_name, resource_group_name):
        self.run_command("azure vm delete -n {} -g {}".format(vm_name, resource_group_name))
    def check_subscription(self):
        """Return True if the provided subscription_id is valid."""
        accounts = self.get_accounts()
        for account in accounts:
            if account["id"] == self.subscription_id:
                return True
        return False

    def get_subscriptions(self):
        subscriptions = []
        for line in self.get_accounts():
            subscriptions.append((line["name"], line["id"]))
        return subscriptions

    def get_accounts(self):
        return self.run_command("azure account list --json")

    def list(self):
        print self.run_command("azure vm list --json")

    def get_groups(self):
        groups = {}
        for group in self.run_command("azure group list --json"):
            groups[group['name']] = {'id':group['id'], 'location':group['location']}
        return groups

    def get_group(self, group_name):
        group = self.run_command("azure group show --json {}".format(group_name))
        if not group:
            return False
        else:
            return group
    def resource_group_exists(self):
        return self.get_group(self.resource_group_name)

    def create_group(self, resource_group_name, resource_group_location):
        self.run_command("azure group create --json -n {} -l {}".format(resource_group_name, resource_group_location))

    def create_vm(self, deployment_name, resource_group_name, resource_group_location, template_file_path, parameters_file_path):
        self.resource_group_name = resource_group_name
        self.resource_group_location = resource_group_location
        # first check if requested resource group exists
        if not self.resource_group_exists():
            self.create_group(resource_group_name, resource_group_location)
        # create the VM itself
        self.run_command("azure group deployment create --json -n {} -g {} -f {} -e {}".format(deployment_name, resource_group_name, template_file_path, parameters_file_path))

