mkdir -p /tmp/zookeeper/zk1 /tmp/zookeeper/zk2 /tmp/zookeeper/zk3
echo 1 > /tmp/zookeeper/zk1/myid
echo 2 > /tmp/zookeeper/zk2/myid
echo 3 > /tmp/zookeeper/zk3/myid

cd ../apache-zookeeper


zkServer.sh --config /conf/zoo2.cfg start-foreground
zkServer.sh --config /conf/zoo3.cfg start-foreground