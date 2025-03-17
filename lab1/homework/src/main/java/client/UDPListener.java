package client;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;

import server.UDPHandler;

public class UDPListener implements Runnable {
    private final DatagramSocket udpSocket;

    public UDPListener(DatagramSocket udpSocket) {
        this.udpSocket = udpSocket;
    }

    @Override
    public void run() {
        byte[] buffer = new byte[UDPHandler.UDP_BUFFER_LENGTH];

        while (true) {
            try {
                DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
                udpSocket.receive(packet);

                String receivedMessage = new String(packet.getData(), 0, packet.getLength());
                System.out.println(">[UDP]: " + receivedMessage);
            } catch (IOException e) {
                System.err.println("UDP Listener error: " + e.getMessage());
                break;
            }
        }
    }
}