import sys
import Ice

sys.path.append("./gen")

import Servants


def main():
    with Ice.initialize(sys.argv) as communicator:
        baseDedicated = communicator.stringToProxy("Dedicated1:default -p 10000")
        # Dedicated
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


if __name__ == "__main__":
    main()
