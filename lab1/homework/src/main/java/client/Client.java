package client;

import java.io.*;
import java.net.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

import server.Server;

public class Client {

    private static final String hostName = "localhost";
    private static final int PORT = Server.PORT;
    private static Socket tcpSocket = null;
    private static PrintWriter out = null;
    private static BufferedReader in = null;

    private static DatagramSocket udpSocket = null;
    private static InetAddress serverAddress;

    private static final String MULTICAST_ADDRESS = "235.1.2.3";
    public static final int MULTICAST_PORT = 16821;
    private static MulticastSocket multicastSocket = null;
    private static InetAddress multicastAddress = null;
    private static NetworkInterface networkInterface = null;

    private static String nickname;

    private static final ExecutorService clientHelpers = Executors.newFixedThreadPool(4);
    private volatile static boolean running = true;

    static InetAddress getServerAddress() {
        return serverAddress;
    }

    static InetAddress getMulticastAddress() {
        return multicastAddress;
    }

    static DatagramSocket getDatagramSocket() {
        return udpSocket;
    }

    static PrintWriter getPrintWriter() {
        return out;
    }

    static MulticastSocket getMulticastSocket() {
        return multicastSocket;
    }

    public static void main(String[] args) {

        try {
            tcpSocket = new Socket(hostName, PORT);
            out = new PrintWriter(tcpSocket.getOutputStream(), true);
            in = new BufferedReader(new InputStreamReader(tcpSocket.getInputStream()));

            multicastAddress = InetAddress.getByName(args.length > 0 && args[0] != null ? args[0] : MULTICAST_ADDRESS);
            multicastSocket = new MulticastSocket(MULTICAST_PORT);

            networkInterface = NetworkInterface.getByInetAddress(InetAddress.getLocalHost());
            multicastSocket.joinGroup(new InetSocketAddress(multicastAddress,
                    MULTICAST_PORT), networkInterface);

            udpSocket = new DatagramSocket(tcpSocket.getLocalPort());
            serverAddress = InetAddress.getByName(hostName);

            nickname = in.readLine();
            System.out.println(">Server: Your assigned nickname: " + nickname);

            TCPListener tcpListener = new TCPListener(in);
            clientHelpers.submit(new Thread(tcpListener));

            UDPListener udpListener = new UDPListener(udpSocket);
            clientHelpers.submit(new Thread(udpListener));

            ScannerListener scannerListener = new ScannerListener();
            clientHelpers.submit(scannerListener);

            UDPMulticastListener multicastListener = new UDPMulticastListener(multicastSocket);
            clientHelpers.submit(multicastListener);

            while (running) {
            }

        } catch (Exception e) {
            System.err.println("Unexpected error: " + e.getMessage());
        } finally {
            shutdownClient();
        }
    }

    static void shutdownListener() {
        running = false;
    }

    private static void shutdownClient() {
        System.out.println("Shutting down client...");
        running = false;

        ScannerListener.stop();
        clientHelpers.shutdownNow();

        try {
            if (!clientHelpers.awaitTermination(5, TimeUnit.SECONDS)) {
                System.out.println("Forcing client shutdown...");
                clientHelpers.shutdownNow();
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        try {
            if (out != null)
                out.close();
            if (in != null)
                in.close();
            if (tcpSocket != null)
                tcpSocket.close();
            if (udpSocket != null)
                udpSocket.close();
            if (multicastSocket != null)
                multicastSocket.close();

        } catch (IOException e) {
            System.err.println("Error closing resources: " + e.getMessage());
        }

        System.out.println("Client disconnected.");
    }
}
