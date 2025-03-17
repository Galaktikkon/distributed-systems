package server;

import java.io.*;
import java.net.InetAddress;
import java.net.Socket;

import classes.Client;
import classes.Message;

public class TCPHandler implements Runnable {
    private final Socket clientSocket;
    private final Client client;
    private PrintWriter out;
    private BufferedReader in;
    private volatile boolean running = true;

    public TCPHandler(Client client, Socket clientSocket) {
        this.clientSocket = clientSocket;
        this.client = client;
    }

    int getClientID() {
        return client.id();
    }

    int getClientPort() {
        return clientSocket.getPort();
    }

    String getClientNickname() {
        return client.nickname();
    }

    InetAddress getClientAddress() {
        return clientSocket.getInetAddress();
    }

    PrintWriter getPrintWriter() {
        return this.out;
    }

    @Override
    public void run() {
        try {

            in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            out = new PrintWriter(clientSocket.getOutputStream(), true);

            Server.getServerLogsHandler()
                    .logServerMessage("Client connected: " + client.nickname());

            out.println(client.nickname());

            String message;
            while (running && (message = in.readLine()) != null) {
                ServerMessengerHandler.addMessage(new Message(message, client));
            }

        } catch (IOException e) {

            Server.getServerLogsHandler()
                    .logServerMessage("Client " + client.nickname() + " disconnected: " + e.getMessage());
        } finally {
            shutdownClient();
        }
    }

    void shutdownClient() {
        Server.getServerLogsHandler()
                .logServerMessage("Shutting down client: " + client.nickname());
        ServerMessengerHandler.addMessage(
                new Message(String.format("User %s disconnected", this.client.nickname()),
                        new Client("Server", -1)));
        cleanup();

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

            Server.getClients().remove(getClientPort());
            Server.getServerLogsHandler()
                    .logServerMessage("Client " + client.nickname() + " has been removed.");
        } catch (IOException e) {
            Server.getServerLogsHandler()
                    .logServerMessage(
                            "Error while closing resources for client " + client.nickname() + ": " + e.getMessage());
        }
    }
}
