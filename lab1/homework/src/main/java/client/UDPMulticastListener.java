package client;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;

import server.UDPHandler;

public class UDPMulticastListener implements Runnable {
    private final DatagramSocket multicastSocket;

    public UDPMulticastListener(DatagramSocket multicastSocket) {
        this.multicastSocket = multicastSocket;
    }

    @Override
    public void run() {
        byte[] buffer = new byte[UDPHandler.UDP_BUFFER_LENGTH];

        while (true) {
            try {
                DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
                multicastSocket.receive(packet);

                String receivedMessage = new String(packet.getData(), 0, packet.getLength());
                System.out.println(">[UDP Multicast]: " + receivedMessage);
            } catch (IOException e) {
                System.err.println("UDP Multicast Listener error: " + e.getMessage());
                break;
            }
        }
    }
}