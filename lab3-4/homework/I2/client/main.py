import sys
import Ice
import gen.Servants_ice as Servants

sys.path.append("./gen")

import Servants  # type: ignore


def client_cli(server_port=10000):
    with Ice.initialize(sys.argv) as communicator:
        print("\n[Client] Connected to server successfully.")
        print("[Client] Use the menu below to interact with the server.\n")

        while True:
            print("\n[Client] Menu:")
            print("1) Call sayHello on Dedicated")
            print("2) Call getStatus on Shared")
            print("3) Exit")

            choice = input("Choose option: ").strip()

            if choice == "1":
                object_id = input(
                    "Enter Dedicated object name (e.g., DedicatedJar1): "
                ).strip()
                try:
                    base = communicator.stringToProxy(
                        f"Dedicated/{object_id}:default -p {server_port}"
                    )
                    dedicated = Servants.DedicatedJarPrx.checkedCast(base)
                    if not dedicated:
                        print(f"[Client] Invalid proxy for Dedicated/{object_id}")
                        continue

                    reply = dedicated.eatCookie()
                    print(f"[Client] Reply from Dedicated/{object_id}: {reply}")

                except Ice.Exception as e:
                    print(f"[Client] Error calling Dedicated/{object_id}: {e}")

            elif choice == "2":
                try:
                    shared_proxy = communicator.stringToProxy(
                        f"SharedObject:default -p {server_port}"
                    )
                    shared = Servants.SharedReporterPrx.checkedCast(shared_proxy)
                    if not shared:
                        print("[Client] Invalid proxy for SharedObject")
                        continue

                    reply = shared.getEatenStatus()
                    print(f"[Client] Reply from Shared: {reply}")

                except Ice.Exception as e:
                    print(f"[Client] Error calling Shared: {e}")

            elif choice == "3":
                print("[Client] Exiting gracefully.")
                break

            else:
                print("[Client] Invalid option, try again.")


if __name__ == "__main__":
    client_cli()
