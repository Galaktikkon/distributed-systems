from kazoo.client import KazooClient
from kazoo.protocol.states import EventType
import subprocess
import time

APP_CMD = ["xpaint"]

app_process = None


def start_app():
    global app_process
    if app_process is None:
        app_process = subprocess.Popen(APP_CMD)


def stop_app():
    global app_process
    if app_process:
        app_process.terminate()
        app_process = None


def watch_a_children(event):
    if event.type == EventType.CHILD:
        children = zk.get_children("/a", watch=watch_a_children)
        print(f"Current number of /a childrend: {len(children)}")  # type: ignore


def watch_a_node(event):
    if event.type == EventType.CREATED:
        print("/a created - starting application")
        start_app()
        zk.get_children("/a", watch=watch_a_children)

    elif event.type == EventType.DELETED:
        print("/a deleted - stopping application")
        stop_app()


zk = KazooClient(hosts="127.0.0.1:2181")
zk.start()


@zk.DataWatch("/a")
def watch_node_data(data, stat, event):
    if event:
        watch_a_node(event)


print("Watching /a node for changes...")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    zk.stop()
