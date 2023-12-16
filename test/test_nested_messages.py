from dobishem.nested_messages import BeginAndEndMessages

def test_nested_messages():
    print()
    with BeginAndEndMessages("outer one"):
        with BeginAndEndMessages("middle one") as mid:
            mid.print("inside mid one")
            with BeginAndEndMessages("inner") as inner:
                inner.print("inner")
        with BeginAndEndMessages("middle two") as mid:
            mid.print("inside mid two")
        with BeginAndEndMessages("middle three") as mid:
            mid.print("inside mid three")
