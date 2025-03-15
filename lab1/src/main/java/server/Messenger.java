package server;

import java.io.PrintWriter;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ConcurrentHashMap;

import classes.Message;

public class Messenger implements Runnable {
    private final BlockingQueue<Message> messageQueue;
    private final ConcurrentHashMap<Integer, ClientHandler> clients;
    private volatile boolean running = true;

    public Messenger(BlockingQueue<Message> messageQueue, ConcurrentHashMap<Integer, ClientHandler> clients) {
        this.messageQueue = messageQueue;
        this.clients = clients;
    }

    protected void stop() {
        running = false;
        messageQueue.clear();
        Thread.currentThread().interrupt();
    }

    @Override
    public void run() {
        while (running) {
            try {
                Message message = messageQueue.take();
                if (!running)
                    break;

                Server.serverLogsHandler
                        .logServerMessage(
                                String.format(">%s to all: %s", message.author().nickname(), message.content()));

                broadcastMessage(message);
            } catch (InterruptedException e) {
                if (!running)
                    break;
                Thread.currentThread().interrupt();
            }
        }
        Server.serverLogsHandler
                .logServerMessage("Messenger thread stopped.");
    }

    private void broadcastMessage(Message message) {
        for (ClientHandler client : clients.values()) {
            PrintWriter out = client.getPrintWriter();
            String modifiedMessage = (client.getClientID() == message.author().id())
                    ? "(you) " + message.author().nickname() + ": " + message.content()
                    : message.author().nickname() + ": " + message.content();
            out.println(modifiedMessage);
        }
    }

}
