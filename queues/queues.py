from azure.storage import QueueService
import account


class Queue:

    def __init__(self, name, account_name=None, account_key=None):
        self.name = name
        # use default keys from account module
        # but also allow to override that if needed
        if not account_name and not account_key:
            account_name = account.name
            account_key = account.key
        self.queue_service = QueueService(
            account_name, account_key)

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

    def queue_exists(self, name):
        "Return True if the specified queue name exists"
        if name in self.get_queue_names():
            return True
        return False

    def create_queue(self, name):
        self.queue_service.create_queue(name)

    def put(self, msg):
        return self.queue_service.put_message(self.name, msg)

    def length(self):
        queue_metadata = self.queue_service.get_queue_metadata(self.name)
        queue_length = queue_metadata['x-ms-approximate-messages-count']
        return int(queue_length)

    def get_messages(self, number_of_messages=1):
        messages = self.queue_service.get_messages(
            self.name,
            numofmessages=number_of_messages)
        return messages[0]

    def get_all_messages(self):
        return self.get_messages(number_of_messages=self.length())

    def get_message(self):
        return self.get_messages()

    def delete_message(self, message):
        return self.queue_service.delete_message(
            self.name,
            message.message_id,
            message.pop_receipt)

    def peek_message(self, number_of_messages=1):
        messages = self.queue_service.peek_messages(
            self.name, numofmessages=number_of_messages)
        for message in messages:
            print message.message_id, message.message_text

    def peek_all_messages(self):
        self.peek_message(number_of_messages=self.length())
