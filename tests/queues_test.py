import random
import time
import sys
sys.path.append("../")
from azurepy import queues
from azure.storage import QueueMessage, QueueEnumResults, QueueMessagesList


initial_length = 0
initial_queue_count = 1

random_number = random.randint(0,100)
test_queue_name = "test-{0}".format(random_number)

q = queues.Queue(test_queue_name)

def test_init():
    assert isinstance(q, queues.Queue)

def test_queue_exists():
    assert q.queue_exists()

def test_get_queues():
    queues = q.get_queues()
    assert isinstance(queues, QueueEnumResults)

def test_get_queue_names():
    "make sure the newly created queue is in the list of queues"
    names = q.get_queue_names()
    assert test_queue_name in names

def test_queue_count():
    "make sure queue_count is integer and is greater than 0"
    queue_count = q.queue_count()
    assert isinstance(queue_count, int)
    assert queue_count > 0

def test_length():
    assert q.length() == initial_length

def test_put():
    length_before = q.length()
    q.put("test")
    assert q.length() == length_before + 1
    q.put("test2")
    assert q.length() == length_before + 2


def test_get_messages():
    messages = q.get_messages(timeout=1)
    assert isinstance(messages, QueueMessagesList)

def test_get_all_messages():
    # need to make sure visibilitytimeout is reached before
    # we query for list of all the messages
    time.sleep(1)
    messages = q.get_all_messages(timeout=1)
    assert isinstance(messages, QueueMessagesList)
    assert len(messages) == q.length()

def test_get_message():
    time.sleep(1)
    message = q.get_message(timeout=1)
    assert isinstance(message, QueueMessage)

def test_delete_message():
    time.sleep(1)
    length_before = q.length()
    message = q.get_message(timeout=10)
    assert q.delete_message(message) == None
    assert q.length() == length_before - 1 

def test_peek_messages():
    messages = q.peek_messages()
    assert isinstance(messages, QueueMessagesList)

def test_peek_message():
    message = q.peek_message()
    assert isinstance(message, QueueMessage)

def test_peek_all_messages():
    messages = q.peek_messages()
    assert isinstance(messages, QueueMessagesList)
    assert len(messages) == q.length()

def test_delete_queue():
    q.delete_queue()
    assert not q.queue_exists()
