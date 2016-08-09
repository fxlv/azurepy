import os
import sys
sys.path.append("../")
from azurepy import vm

if os.path.exists("account.py"):
    import account
    subscription_id = account.subscription_id
else:
    print "No account data available"
    sys.exit(1)

vm_name = "cloudhawkbuild"
resource_group_location = "northeurope"

a = vm.AzureVM(subscription_id)


def test_object():
    # was the object created successfully?
    assert str(a) == "AzureVM"
    assert isinstance(a, vm.AzureVM)


def test_list():
    vm_list = a.list()
    # was a list returned?
    assert isinstance(vm_list, list)
