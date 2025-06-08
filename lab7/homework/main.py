from kazoo.client import KazooClient
from kazoo.protocol.states import EventType
from subprocess import Popen
import networkx as nx
import matplotlib.pyplot as plt

PROMPT = "> "

APP_CMD = ["konsole", "--noclose", "-e", "xpaint"]
NODE_TO_WATCH = "/a"

app_process = None
watched_paths = set()

zk = KazooClient(hosts="127.0.0.1:2181")
zk.start()


def start_app():
    global app_process
    if app_process is None:
        print(f"{PROMPT} Starting external application...")
        app_process = Popen(APP_CMD)


def stop_app():
    global app_process
    if app_process:
        print(f"{PROMPT} Stopping external application...")
        app_process.terminate()
        app_process = None


def count_children(path):
    if not zk.exists(path):
        return 0

    children = zk.get_children(path)

    total = 1 if path != NODE_TO_WATCH else 0

    for child in children:
        total += count_children(f"{path}/{child}")
    return total


def make_child_watch(path):
    def _watch(event):
        if event and event.type == EventType.CHILD:
            print(
                f"{PROMPT} Total descendants of {NODE_TO_WATCH}: {count_children(NODE_TO_WATCH)}"
            )
            watched_paths.discard(path)
            watch_children(path)

    return _watch


def watch_children(path):
    if not zk.exists(path) or path in watched_paths:
        return

    zk.get_children(path, watch=make_child_watch(path))
    watched_paths.add(path)
    for child in zk.get_children(path):
        child_path = f"{path}/{child}"
        watch_children(child_path)


def watch_a_node(event):
    if event.type == EventType.CREATED:
        start_app()
        watch_children(NODE_TO_WATCH)
        print(
            f"{PROMPT} Total descendants of {NODE_TO_WATCH}: {count_children(NODE_TO_WATCH)}"
        )
    elif event.type == EventType.DELETED:
        print(f"{PROMPT} {NODE_TO_WATCH} deleted.")
        stop_app()


@zk.DataWatch(NODE_TO_WATCH)
def watch_node_data(data, stat, event):
    if event:
        watch_a_node(event)


def get_tree(path=NODE_TO_WATCH, graph=None, parent=None):
    if graph is None:
        graph = nx.DiGraph()

    if not zk.exists(path):
        return graph

    children = zk.get_children(path)
    for child in children:
        child_path = f"{path}/{child}"
        graph.add_edge(path, child_path)
        graph.nodes[child_path]["label"] = f"/{child}"
        get_tree(child_path, graph, path)

    return graph


def show_tree():
    if not zk.exists(NODE_TO_WATCH):
        print(f"{PROMPT} Node {NODE_TO_WATCH} does not exist.")
        return

    print(f"{PROMPT} Drawing tree for {NODE_TO_WATCH}...")
    tree = get_tree(NODE_TO_WATCH)
    pos = nx.spring_layout(tree)
    labels = {
        node: (f"{NODE_TO_WATCH}" if "label" not in data else data["label"])
        for node, data in tree.nodes(data=True)
    }

    plt.figure(figsize=(8, 6))
    nx.draw(
        tree,
        pos,
        labels=labels,
        with_labels=True,
        node_color="lightblue",
        edge_color="gray",
        node_size=2000,
        font_size=10,
    )
    plt.title(f"Zookeeper Tree Structure for {NODE_TO_WATCH}")
    plt.show()


if zk.exists(NODE_TO_WATCH):
    print(f"{PROMPT} {NODE_TO_WATCH} already exists.")
    start_app()
    watch_children(NODE_TO_WATCH)
    print(
        f"{PROMPT} Total descendants of {NODE_TO_WATCH}: {count_children(NODE_TO_WATCH)}"
    )


try:
    print(f"{PROMPT} Watching node: {NODE_TO_WATCH}")
    while True:
        command = input(f"{PROMPT} ").strip().lower()
        if command == "tree":
            show_tree()
        elif command == "help":
            print(f"{PROMPT} Available commands: tree, help, exit")
        elif command == "exit":
            break
        else:
            print(f"{PROMPT} Unknown command. Type 'help' for options.")
except KeyboardInterrupt:
    print(f"{PROMPT} Exiting...")
finally:
    stop_app()
    zk.stop()
    print(f"{PROMPT} ZooKeeper connection closed.")
