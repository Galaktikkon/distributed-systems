import sys
import Ice
import gen.Servants_ice as Servants

with Ice.initialize(sys.argv) as communicator:
    # Dedicated
    baseDedicated = communicator.stringToProxy("Dedicated1:default -p 10000")
    dedicated = Servants.DedicatedPrx.checkedCast(baseDedicated)

    if not dedicated:
        raise RuntimeError("Invalid proxy for Dedicated1")

    reply = dedicated.sayHello()
    print("Reply from Dedicated:", reply)

    # Shared
    baseShared = communicator.stringToProxy("SharedObject:default -p 10000")
    shared = Servants.SharedPrx.checkedCast(baseShared)

    if not shared:
        raise RuntimeError("Invalid proxy for SharedObject")

    status = shared.getStatus()
    print("Reply from Shared:", status)
