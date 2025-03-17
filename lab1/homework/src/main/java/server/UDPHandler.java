package server;

import java.io.IOException;
import java.net.*;
import java.util.*;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.LinkedBlockingQueue;

import classes.Client;
import classes.Message;

public class UDPHandler implements Runnable {

    private final BlockingQueue<Message> messageQueue = new LinkedBlockingQueue<>();
    private DatagramSocket socket;
    private ServerLogsHandler serverLogsHandler = Server.getServerLogsHandler();
    private final ConcurrentHashMap<Integer, TCPHandler> clients = Server.getClients();
    public static final int UDP_BUFFER_LENGTH = 1024;

    @Override
    public void run() {
        try {
            socket = new DatagramSocket(Server.PORT);
            byte[] receiveBuffer = new byte[UDP_BUFFER_LENGTH];

            while (!Thread.currentThread().isInterrupted()) {
                try {
                    Arrays.fill(receiveBuffer, (byte) 0);
                    DatagramPacket receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
                    socket.receive(receivePacket);

                    String receivedMessage = new String(receivePacket.getData(), 0, receivePacket.getLength());
                    Integer receivePort = receivePacket.getPort();
                    TCPHandler tcpHandler = clients.get(receivePort);

                    if (tcpHandler != null) {
                        Client author = new Client(tcpHandler.getClientNickname(), tcpHandler.getClientID());
                        Message message = new Message(receivedMessage, author);
                        messageQueue.put(message);
                        serverLogsHandler.logServerMessage(
                                String.format(">[UDP]: %s to all: %s", message.author().nickname(), message.content()));
                        broadcastMessage(message);
                    } else {
                        serverLogsHandler
                                .logServerMessage("Received UDP message from unknown client on port: " + receivePort);
                    }

                } catch (IOException e) {
                    serverLogsHandler.logServerMessage("Error receiving UDP message: " + e.getMessage());
                    e.printStackTrace();
                } catch (InterruptedException e) {
                    serverLogsHandler
                            .logServerMessage("Thread interrupted while adding message to queue: " + e.getMessage());
                    Thread.currentThread().interrupt();
                }
            }
        } catch (SocketException e) {
            serverLogsHandler.logServerMessage("Error creating UDP socket: " + e.getMessage());
            e.printStackTrace();
        } finally {
            if (socket != null && !socket.isClosed()) {
                socket.close();
            }
        }
    }

    private void broadcastMessage(Message message) {
        for (TCPHandler client : clients.values()) {
            try {
                Integer clientPort = client.getClientPort();
                InetAddress clientAddress = client.getClientAddress();

                String modifiedMessage = (client.getClientID() == message.author().id())
                        ? "(you) " + message.author().nickname() + ": " + message.content()
                        : message.author().nickname() + ": " + message.content();

                byte[] modifiedMessageData = modifiedMessage.getBytes();
                DatagramPacket sendPacket = new DatagramPacket(
                        modifiedMessageData,
                        modifiedMessageData.length,
                        clientAddress,
                        clientPort);

                socket.send(sendPacket);
            } catch (IOException e) {
                serverLogsHandler.logServerMessage("Error broadcasting message to client: " + client.getClientID());
                e.printStackTrace();
            }
        }
    }
}