package server;

import java.io.*;
import java.net.Socket;
import java.util.concurrent.BlockingQueue;

import classes.Client;
import classes.Message;

public class ClientHandler implements Runnable {
    private final Socket clientSocket;
    private final BlockingQueue<Message> messageQueue;
    private final Client client;
    private PrintWriter out;
    private BufferedReader in;
    private volatile boolean running = true;

    public ClientHandler(Client client, Socket clientSocket, BlockingQueue<Message> messageQueue) {
        this.clientSocket = clientSocket;
        this.messageQueue = messageQueue;
        this.client = client;
    }

    protected int getClientID() {
        return client.id();
    }

    protected PrintWriter getPrintWriter() {
        return this.out;
    }

    @Override
    public void run() {
        try {
            in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            out = new PrintWriter(clientSocket.getOutputStream(), true);

            Server.serverLogsHandler
                    .logServerMessage("Client connected: " + client.nickname());

            // send nickname to the client
            out.println(client.nickname());

            String message;
            while (running && (message = in.readLine()) != null) {
                messageQueue.put(new Message(message, client));
            }
        } catch (IOException e) {
            Server.serverLogsHandler
                    .logServerMessage("Client " + client.nickname() + " disconnected: " + e.getMessage());
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            shutdownClient();
        }
    }

    protected void shutdownClient() {
        Server.serverLogsHandler
                .logServerMessage("Shutting down client: " + client.nickname());
        try {
            messageQueue.put(
                    new Message(String.format("User %s disconnected", this.client.nickname()),
                            new Client("Server", -1)));
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            cleanup();
        }
    }

    private void cleanup() {
        try {

            running = false;
            if (in != null)
                in.close();
            if (out != null)
                out.close();
            if (!clientSocket.isClosed())
                clientSocket.close();

            Server.serverLogsHandler
                    .logServerMessage("Client " + client.nickname() + " has been removed.");
        } catch (IOException e) {
            Server.serverLogsHandler
                    .logServerMessage(
                            "Error while closing resources for client " + client.nickname() + ": " + e.getMessage());
        }
    }
}
