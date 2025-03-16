package server;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;

public class JavaUdpServer {

    public static void main(String args[]) {
        System.out.println("JAVA UDP SERVER");
        DatagramSocket socket = null;
        int portNumber = 9008;

        try {
            socket = new DatagramSocket(portNumber);
            byte[] receiveBuffer = new byte[1024];

            while (true) {
                Arrays.fill(receiveBuffer, (byte) 0);

                System.out.println("Listening for Ping...");
                DatagramPacket receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
                socket.receive(receivePacket);

                // exercise 1

                // String msg = new String(receivePacket.getData());
                // System.out.println("Received message: " + msg + ", from: " +
                // receivePacket.getSocketAddress());
                // System.out.println("Sending Pong to Client...");
                // String responseMessage = new String("Pong Java UDP");
                // byte[] responseData = responseMessage.getBytes();

                // exercise 2

                // String msg = new String(receivePacket.getData());
                // System.out.println("Received message: " + msg + ", from: " +
                // receivePacket.getSocketAddress());
                // String responseMessage = new String("Żółta gęść je żółć");
                // byte[] responseData = responseMessage.getBytes(StandardCharsets.UTF_8);

                // exercise 3

                int nb = ByteBuffer.wrap(receivePacket.getData()).order(ByteOrder.LITTLE_ENDIAN).getInt();
                System.out.println("Received message: " + nb + ", from: " + receivePacket.getSocketAddress());
                nb++;
                byte[] responseData = ByteBuffer.allocate(4).putInt(nb).array();

                DatagramPacket sendPacket = new DatagramPacket(
                        responseData,
                        responseData.length,
                        receivePacket.getAddress(),
                        receivePacket.getPort());
                socket.send(sendPacket);
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (socket != null) {
                socket.close();
            }
        }
    }
}
