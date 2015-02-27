import queues
import account
from azure.storage import QueueMessage, QueueEnumResults

account_name = account.test_name
account_key = account.test_key

initial_length = 34
initial_queue_count = 1

test_queue_name = "test"

q = queues.Queue(test_queue_name, account_name, account_key)

def test_queue_object_creation():
    assert isinstance(q, queues.Queue)

def test_get_queues():
   queues = q.get_queues()
   assert isinstance(queues, QueueEnumResults)

def test_get_queue_names():
    names = q.get_queue_names()[0]
    assert names == test_queue_name

def test_queue_count():
    assert initial_queue_count == q.queue_count()

def test_queue_exists():
    assert q.queue_exists(test_queue_name)

def test_initial_queue_length():
    assert q.length() == initial_length

def test_add():
    q.put("test")
    assert q.length() == initial_length + 1

def test_get_message():
    message = q.get_message()
    assert isinstance(message, QueueMessage)

def test_delete():
    message = q.get_message()
    assert q.length() == initial_length + 1
    q.delete_message(message)
    assert q.length() == initial_length
