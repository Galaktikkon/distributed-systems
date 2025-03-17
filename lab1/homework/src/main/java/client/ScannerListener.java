package client;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.MulticastSocket;
import java.util.Scanner;

import server.Server;

class ScannerListener implements Runnable {

    private static Scanner scanner = new Scanner(System.in);
    private static final int port = Server.PORT;
    private static PrintWriter out = Client.getPrintWriter();
    private static DatagramSocket udpSocket = Client.getDatagramSocket();
    private static InetAddress serverAddress = Client.getServerAddress();
    private static InetAddress multicastAddress = Client.getMulticastAddress();
    private static MulticastSocket multicastSocket = Client.getMulticastSocket();
    private static volatile boolean running = true;
    private static int lineNumber = 1;

    static void stop() {
        if (running) {
            running = false;
            Thread.currentThread().interrupt();
        }
    }

    @Override
    public void run() {

        while (running) {
            String userMessage = scanner.nextLine();

            clearLines(lineNumber);

            if (userMessage.equalsIgnoreCase("exit")) {
                break;
            }

            if (userMessage.equalsIgnoreCase("U")) {
                sendUdpMessage();
                scanner = new Scanner(System.in);
                continue;
            }

            if (userMessage.equalsIgnoreCase("M")) {
                sendMulticastMessage();
                scanner = new Scanner(System.in);
                continue;
            }

            out.println(userMessage);
        }
        scanner.close();
    }

    private void sendUdpMessage() {
        System.out.print("Enter  UDP message: ");
        String udpMessage = readMultipleLines();

        byte[] buffer = udpMessage.getBytes();
        DatagramPacket packet = new DatagramPacket(buffer, buffer.length, serverAddress, port);
        try {
            udpSocket.send(packet);

        } catch (IOException e) {
            System.err.println("Error sending UDP message: " + e.getMessage());
        }
    }

    private void sendMulticastMessage() {
        System.out.print("Enter multicast UDP message: ");
        String multicastMessage = readMultipleLines();

        byte[] buffer = multicastMessage.getBytes();
        DatagramPacket packet = new DatagramPacket(buffer, buffer.length, multicastAddress, Client.MULTICAST_PORT);
        try {
            multicastSocket.send(packet);
        } catch (IOException e) {
            System.err.println("Error sending multicast message: " + e.getMessage());
        }
    }

    private static void clearLines(int lineNumber) {
        for (int i = 0; i < lineNumber; i++) {
            System.out.print("\033[F\033[K");
        }
    }

    private static String readMultipleLines() {
        lineNumber++;
        StringBuilder udpMessageBuilder = new StringBuilder();
        while (scanner.hasNextLine()) {
            String udpLine = scanner.nextLine();
            if (udpLine.trim().isEmpty())
                break;

            udpMessageBuilder.append(udpLine).append("\n");
        }

        clearLines(lineNumber);
        lineNumber = 1;
        return udpMessageBuilder.toString().trim();
    }
}
