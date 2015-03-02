from azurepy import queues

account_name = "<put your account name here>"
account_key = "<put your secret key here>"

q = queues.Queue("example-queue", account_name, account_key)
print "Queue created"
q.put("Wow, it really is that simple")
print "Our queue length is {0}".format(q.length())
q.put("Couldn't be easier")
print "Our queue length is {0}".format(q.length())
q.put("Really.")
print "Our queue length is {0}".format(q.length())


for message in q.get_all_messages():
    print message.message_id, message.message_text
