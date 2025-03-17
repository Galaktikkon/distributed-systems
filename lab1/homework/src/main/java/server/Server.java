package server;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.concurrent.*;

import classes.Client;
import classes.Message;

public class Server {

    public static final int PORT = 12345;
    private static volatile boolean running = true;

    private static final BlockingQueue<Message> messageQueue = new LinkedBlockingQueue<>();
    private static final BlockingQueue<String> serverLogsQueue = new LinkedBlockingQueue<>();

    private static final ConcurrentHashMap<Integer, TCPHandler> clients = new ConcurrentHashMap<>();
    private static final ExecutorService clientExecutor = Executors.newFixedThreadPool(10);

    private static final ExecutorService serverHelperExecutor = Executors.newFixedThreadPool(4);
    private static final ServerLogsHandler serverLogsHandler = new ServerLogsHandler(serverLogsQueue);

    private static ServerSocket serverSocket;

    public static void main(String[] args) {
        serverHelperExecutor.submit(serverLogsHandler);

        serverLogsHandler.logServerMessage("Initializing server...");

        serverHelperExecutor.submit(new ServerShutdownListener((Server::shutdownServer)));

        try {
            serverSocket = new ServerSocket(PORT);
            serverLogsHandler.logServerMessage("Server running on port " + PORT);

            serverLogsHandler.logServerMessage("Initializing UDP Handler...");
            serverHelperExecutor.submit(new UDPHandler());
            serverLogsHandler.logServerMessage("UDP Handler initialized!");

            serverLogsHandler.logServerMessage("Initializing message queue...");
            serverHelperExecutor.submit(new ServerMessengerHandler());
            serverLogsHandler.logServerMessage("Message queue initialized!");

            while (running) {
                try {
                    Socket clientSocket = serverSocket.accept();
                    if (!running)
                        break;
                    registerNewClient(clientSocket);
                } catch (IOException e) {
                    if (running) {
                        serverLogsHandler.logServerMessage("Error accepting client connection: " + e.getMessage());
                    } else {
                        break;
                    }
                }
            }
        } catch (IOException e) {
            serverLogsHandler.logServerMessage("Server socket error: " + e.getMessage());
        } finally {
            shutdownServer();
        }
    }

    private static void registerNewClient(Socket clientSocket) {
        Client newClient = new Client(Generator.getNickName(), Generator.getUniqueID());
        TCPHandler clientHandler = new TCPHandler(newClient, clientSocket);
        clients.put(clientSocket.getPort(), clientHandler);
        clientExecutor.submit(clientHandler);
        serverLogsHandler.logServerMessage(
                "Registered a new client: id: " + newClient.id() + ", nickname: " + newClient.nickname());
    }

    private static void shutdownServer() {
        if (!running)
            return;

        serverLogsHandler.logServerMessage("Shutting down server...");

        running = false;
        shutdownAllClients();
        closeServerSocket();
        shutdownHelpers();
    }

    private static void shutdownAllClients() {

        for (TCPHandler clientHandler : clients.values()) {
            clientHandler.shutdownClient();
        }

        clientExecutor.shutdown();
        try {
            if (!clientExecutor.awaitTermination(5, TimeUnit.SECONDS)) {
                clientExecutor.shutdownNow();
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            clientExecutor.shutdownNow();
        }
    }

    private static void closeServerSocket() {
        try {
            if (serverSocket != null && !serverSocket.isClosed()) {
                serverSocket.close();
            }
        } catch (IOException e) {
            serverLogsHandler.logServerMessage("Error closing server socket: " + e.getMessage());
        }
    }

    private static void shutdownHelpers() {

        serverHelperExecutor.shutdown();
        try {
            if (!serverHelperExecutor.awaitTermination(5, TimeUnit.SECONDS)) {
                serverHelperExecutor.shutdownNow();
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            serverHelperExecutor.shutdownNow();
        }
    }

    public static BlockingQueue<Message> getMessageQueue() {
        return messageQueue;
    }

    public static ConcurrentHashMap<Integer, TCPHandler> getClients() {
        return clients;
    }

    public static ServerLogsHandler getServerLogsHandler() {
        return serverLogsHandler;
    }
}
