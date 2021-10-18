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
        l.insert_after(node, {
        "Terminals": {
            "1": {
                "attribute": 0.0,
                "category": "Category",
                "name": "Name",
                "mass": "Mass (kg, Wet)",
                "length": "Length (m)",
                "projected_area": "Projected area (m\u00b2)",
                "nl_drag_cf": "Normal drag coeff",
                "tl_drag_cf": "Tangential drag coeff",
                "breaking_strength": "Breaking strength (kg)",
                "image_file": "Image file"
            },
            "2": {
                "attribute": 1.0,
                "category": "LPO",
                "name": "Shackle 5/8",
                "mass": -0.635,
                "length": 0.05,
                "projected_area": 0.001,
                "nl_drag_cf": 1.3,
                "tl_drag_cf": 0.1,
                "breaking_strength": 18000.0,
                "image_file": "\\Pictures\\Terminals\\shackle2.bmp"
        }}})
    print(l)


    # Empty out the list, one node at a time.
    while l.first_node() != None:
        l.delete(l.first_node())

    print(l)

test_sentinel_DLL()