import os
import sys
import re
from azure.storage import QueueService


class Queue:
    def __init__(self, name, account_name=None, account_key=None):
        self.name = name
        if not re.match("^[a-zA-Z0-9-]+$", self.name):
            print
            print "Invalid queue name"
            print "Queue names can only contain letters, numbers and hyphens."
            print
            sys.exit(1)
        # use default keys from account module
        # but also allow to override that if needed
        if not account_name and not account_key:
            if os.path.exists("account.py"):
                import account
                account_name = account.name
                account_key = account.key
            else:
                self.help_account()
        self.queue_service = QueueService(account_name, account_key)
        if not self.queue_exists():
            self.create_queue()

    def __repr__(self):
        return "Queue: {0}".self.name

    def __str__(self):
        return self.name

    def help_account(self):
        print
        print "You have not specified the 'account_name'"
        print "and the 'account_key' that should be used"
        print
        print "Please read the docs on how to do that."
        print
        sys.exit(1)

    def create_queue(self):
        return self.queue_service.create_queue(self.name)

    def queue_exists(self):
        "Return True if the specified queue name exists"
        if self.name in self.get_queue_names():
            return True
        return False

    def delete_queue(self):
        "Delete itself"
        return self.queue_service.delete_queue(self.name)

    def get_queues(self):
        "Return a list of queues"
        return self.queue_service.list_queues()

    def get_queue_names(self):
        "Return a list of queue names"
        queues_list = self.get_queues()
        queue_names_list = []
        for queue in queues_list:
            queue_names_list.append(queue.name)
        return queue_names_list

    def queue_count(self):
        "Return number of queues in this account"
        return len(self.get_queues())

    def length(self):
        queue_metadata = self.queue_service.get_queue_metadata(self.name)
        queue_length = queue_metadata['x-ms-approximate-messages-count']
        return int(queue_length)

    def put(self, msg, ttl=None):
        """
        msg - message text
        ttl - time to live in seconds. default is 7 days.
        """
        return self.queue_service.put_message(self.name, msg, messagettl=ttl)

    def get_messages(self, number_of_messages=1, timeout=30):
        messages = self.queue_service.get_messages(
            self.name,
            numofmessages=number_of_messages,
            visibilitytimeout=timeout)
        return messages

    def get_all_messages(self, timeout=30):
        return self.get_messages(number_of_messages=self.length(),
                                 timeout=timeout)

    def get_message(self, timeout=30):
        try:
            msg = self.get_messages(timeout=timeout)
            if len(msg) > 0:
                msg = msg[0]
            else:
                msg = None
        except Exception:
            msg = None
        return msg

    def delete_message(self, message):
        return self.queue_service.delete_message(self.name, message.message_id,
                                                 message.pop_receipt)

    def clear(self):
        return self.queue_service.clear_messages(self.name)

    def peek_messages(self, number_of_messages=1):
        return self.queue_service.peek_messages(
            self.name,
            numofmessages=number_of_messages)

    def peek_message(self):
        try:
            msg = self.peek_messages()
            return msg[0]
        except IndexError:
            print self.peek_messages()
            return None

    def peek_all_messages(self):
        return self.peek_messages(number_of_messages=self.length())
