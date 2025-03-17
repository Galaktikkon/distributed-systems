package server;

import java.io.PrintWriter;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ConcurrentHashMap;

import classes.Message;

public class ServerMessengerHandler implements Runnable {
    private static BlockingQueue<Message> messageQueue = Server.getMessageQueue();
    private final ConcurrentHashMap<Integer, TCPHandler> clients = Server.getClients();

    static void addMessage(Message message) {
        if (messageQueue == null) {
            System.out.println("Message queue is not initialized!");
            return;
        }
        try {
            messageQueue.put(message);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.out.println("Thread interrupted while adding message: " + e.getMessage());
        }
    }

    @Override
    public void run() {
        while (true) {
            try {
                Message message = messageQueue.take();

                Server.getServerLogsHandler()
                        .logServerMessage(
                                String.format(">[TCP]: %s to all: %s", message.author().nickname(), message.content()));

                broadcastMessage(message);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                System.out.println("Messenger thread interrupted: " + e.getMessage());
                break;
            }
        }
        messageQueue.clear();
        Server.getServerLogsHandler().logServerMessage("Messenger thread stopped.");

    }

    private void broadcastMessage(Message message) {
        for (TCPHandler client : clients.values()) {
            PrintWriter out = client.getPrintWriter();
            String modifiedMessage = (client.getClientID() == message.author().id())
                    ? "(you) " + message.author().nickname() + ": " + message.content()
                    : message.author().nickname() + ": " + message.content();
            out.println(modifiedMessage);

        }
    }
}
