# azurepy

Currently, a place for me to play with Azure features.

It is sort of a wrapper around python Azure module

## Installing
```
python setup.py install
```
## Components
**queues.py** - wrapper around Azure queues

## Passing Azure account credentials 
In order to use any of the modules you have to either pass along variables 'account_name' and 'account_key'
or you can have a file 'account.py' in the path from where your script will be invoked that cotains two variables: 'name' and 'key'.
## Examples
```python
from azurepy import queues

account_name = "myazureacount"
account_key = "supersecretandlonghash"

q = queues.Queue("example-queue", account_name, account_key)
q.put("Wow, it really is that simple")
```
See [examples](https://github.com/fxlv/azurepy/tree/master/examples) directory for more examples.
