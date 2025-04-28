import sys
import Ice

sys.path.append("./gen")

import Servants  # type: ignore


def client_cli(server_port=10000):
    with Ice.initialize(sys.argv) as communicator:
        print("\n[Client] Connected to Cookie Jar Server")
        print("[Client] Use the menu below to interact with the jars.\n")

        while True:
            print("\n[Client] Cookie Jar Menu:")
            print("1) Eat a cookie from a specific jar")
            print("2) Check how many cookies were eaten (shared report)")
            print("3) Exit")

            choice = input("Choose option: ").strip()

            if choice == "1":
                jar_name = input(
                    "Enter the Cookie Jar name (e.g., Jar1, Jar2): "
                ).strip()
                try:
                    base = communicator.stringToProxy(
                        f"Dedicated/{jar_name}:default -p {server_port}"
                    )
                    jar = Servants.DedicatedJarPrx.checkedCast(base)
                    if not jar:
                        print(f"[Client] Invalid proxy for Dedicated/{jar_name}")
                        continue

                    reply = jar.eatCookie()
                    print(f"[Client] You ate a cookie from {jar_name}! {reply}")

                except Ice.Exception as e:
                    print(f"[Client] Error calling Dedicated/{jar_name}: {e}")

            elif choice == "2":
                try:
                    shared_proxy = communicator.stringToProxy(
                        f"SharedObject:default -p {server_port}"
                    )
                    reporter = Servants.SharedReporterPrx.checkedCast(shared_proxy)
                    if not reporter:
                        print("[Client] Invalid proxy for SharedObject")
                        continue

                    report = reporter.getEatenStatus()
                    print(f"[Client] Session cookie consumption report: {report}")

                except Ice.Exception as e:
                    print(f"[Client] Error calling Shared Reporter: {e}")

            elif choice == "3":
                print("[Client] Exiting gracefully.")
                break

            else:
                print("[Client] Invalid option, please try again.")


if __name__ == "__main__":
    client_cli()
