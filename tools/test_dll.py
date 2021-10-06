# test_sentinel_DLL.py
# CS 1 class example by THC.
# Tests the Sentinel_DLL class.

from dll import Sentinel_DLL

def test_sentinel_DLL():
    # Make a linked list with Maine, Idaho, and Utah.
    l = Sentinel_DLL()
    l.append("Maine")
    l.append("Idaho")
    l.append("Utah")
    print(l)

    # Add Ohio after Idaho.
    node = l.find("Idaho")
    if node != None:
        print(node.get_data())
        l.insert_after(node, "Ohio")
    print(l)

    # Delete Idaho.
    if node != None:
        l.delete(node)
    print(l)

    # Add Paris after Ohio.
    node = l.find("Ohio")
    if node != None:
        print(node.get_data())
        l.insert_after(node, "Paris")
    print(l)

    l.prepend("Nantes")
    print(l)

    # Add Brest before Ohio.
    node = l.find("Ohio")
    if node != None:
        print(node.get_data())
        l.insert_before(node, "Brest")
    print(l)

    node = l.find("Brest")
    if node != None:
        print(node.get_data())
        l.insert_after(node, {'Float','45'})
    print(l)


    # Empty out the list, one node at a time.
    while l.first_node() != None:
        l.delete(l.first_node())

    print(l)

test_sentinel_DLL()