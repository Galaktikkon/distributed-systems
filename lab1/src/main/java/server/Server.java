package server;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;
import java.util.concurrent.*;

import classes.Client;
import classes.Message;

public class Server {

    public static final int PORT = 12345;
    private static volatile boolean running = true;

    private static final BlockingQueue<Message> messageQueue = new LinkedBlockingQueue<>();
    private static final BlockingQueue<String> serverLogsQueue = new LinkedBlockingQueue<>();

    private static final ConcurrentHashMap<Integer, ClientHandler> clients = new ConcurrentHashMap<>();
    private static final ExecutorService clientExecutor = Executors.newFixedThreadPool(10);

    protected static final ServerLogsHandler serverLogsHandler = new ServerLogsHandler(serverLogsQueue);
    private static ServerSocket serverSocket;

    public static void main(String[] args) {
        new Thread(serverLogsHandler).start();
        serverLogsHandler.logServerMessage("Initializing server...");

        try {
            serverSocket = new ServerSocket(PORT);
            serverLogsHandler.logServerMessage("Server running on port " + PORT);
            serverLogsHandler.logServerMessage("Initializing message queue...");

            clientExecutor.submit(new Messenger(messageQueue, clients));

            serverLogsHandler.logServerMessage("Message queue initialized!");

            startShutdownListener();

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
        ClientHandler clientHandler = new ClientHandler(newClient, clientSocket, messageQueue);
        clients.put(newClient.id(), clientHandler);
        clientExecutor.submit(clientHandler);
        serverLogsHandler.logServerMessage(
                "Registered a new client: id: " + newClient.id() + ", nickname: " + newClient.nickname());
    }

    private static void startShutdownListener() {
        new Thread(() -> {
            Scanner scanner = new Scanner(System.in);
            while (running) {
                if (scanner.hasNextLine()) {
                    String command = scanner.nextLine();
                    if ("exit".equalsIgnoreCase(command)) {
                        shutdownServer();
                        break;
                    }
                }
            }
            scanner.close();
        }).start();
    }

    private static void shutdownServer() {
        if (!running)
            return;

        serverLogsHandler.logServerMessage("Shutting down server...");

        running = false;
        shutdownAllClients();
        closeServerSocket();

        serverLogsHandler.logServerMessage("Server shut down successfully.");
        serverLogsHandler.stop();
    }

    private static void shutdownAllClients() {

        for (ClientHandler clientHandler : clients.values()) {
            clientHandler.shutdownClient();
        }
        clients.clear();

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

}
