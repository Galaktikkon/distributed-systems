package client;

import java.io.BufferedReader;
import java.io.IOException;

public class TCPListener implements Runnable {
    private final BufferedReader in;

    public TCPListener(BufferedReader in) {
        this.in = in;
    }

    @Override
    public void run() {
        try {
            String serverMessage;
            while ((serverMessage = in.readLine()) != null) {
                System.out.println(">[TCP]: " + serverMessage);
            }
        } catch (IOException e) {
            System.err.println("TCP Listener error: " + e);
        } finally {
            try {
                in.close();
            } catch (IOException e) {
                System.err.println("Error closing input stream: " + e.getMessage());
            }
            Client.shutdownListener();
        }
    }
}
