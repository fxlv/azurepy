# azurepy

[![Build Status](https://travis-ci.org/fxlv/azurepy.svg?branch=master)](https://travis-ci.org/fxlv/azurepy)


Currently, a place for me to play with Azure features.
Main idea is to make things simpler, deployments faster and remove the need to write boilerplate code.
Perhaps better idea would be to use Terraform, but this allows me to do something nice :) 

## Installing
```
python setup.py install
```
## Components
**queues.py** - wrapper around Azure queues

**vm.py** - wrapper aroung `azure vm` and `azure group`

## Passing Azure account credentials to use Queues
In order to use any of the modules you have to either pass along variables 'account_name' and 'account_key'
or you can have a file 'account.py' in the path from where your script will be invoked that cotains two variables: 'name' and 'key'.

## Credentials for working with VMs
In the case of VMs, you have to have an `account.py` file with a variable `subscription_id` set.
Such as 

```
subscription_id="lalala-lalala-lalala-lalala"
```

## Examples
```python
from azurepy import queues

account_name = "myazureacount"
account_key = "supersecretandlonghash"

q = queues.Queue("example-queue", account_name, account_key)
q.put("Wow, it really is that simple")
```
See [examples](https://github.com/fxlv/azurepy/tree/master/examples) directory for more examples.
