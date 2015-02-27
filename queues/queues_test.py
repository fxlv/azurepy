import queues
from azure.storage import QueueMessage

initial_length = 34

q = queues.Queue("test")

def test_type():
    assert isinstance(q, queues.Queue)

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
