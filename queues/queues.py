from azure.storage import QueueService
import account


class Queue:

    def __init__(self, name):
        self.name = name
        self.queue_service = QueueService(
            account_name=account.name,
            account_key=account.key)

    def get_queues(self):
        "Return a list of queue names"
        queues_list = self.queue_service.list_queues()
        queue_names_list = []
        for queue in queues_list:
            queue_names_list.append(queue.name)
        return queue_names_list

    def queue_exists(self, name):
        "Return True if the specified queue name exists"
        if name in self.get_queues():
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
