package client;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class JavaUdpClient {

    public static void main(String args[]) throws Exception {
        System.out.println("JAVA UDP CLIENT");
        DatagramSocket socket = null;
        int portNumber = 9008;

        try {
            socket = new DatagramSocket();
            InetAddress address = InetAddress.getByName("localhost");
            byte[] sendBuffer = "Ping Java Udp".getBytes();

            System.out.println("Sending Ping to Server...");
            DatagramPacket sendPacket = new DatagramPacket(sendBuffer, sendBuffer.length, address, portNumber);
            socket.send(sendPacket);

            System.out.println("Listening for Pong...");
            DatagramPacket receivePacket = new DatagramPacket(sendBuffer, sendBuffer.length);
            socket.receive(receivePacket);

            String msg = new String(receivePacket.getData());
            System.out.println("Received message: " + msg + ", from: " + receivePacket.getSocketAddress());

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (socket != null) {
                socket.close();
            }
        }
    }
}
