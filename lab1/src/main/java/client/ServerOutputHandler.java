package client;

import java.io.BufferedReader;
import java.io.IOException;

public class ServerOutputHandler implements Runnable {
    private final BufferedReader in;
    private volatile boolean running = true;

    public ServerOutputHandler(BufferedReader in) {
        this.in = in;
    }

    protected void stop() {
        running = false;
    }

    @Override
    public void run() {
        try {
            String serverMessage;
            while ((serverMessage = in.readLine()) != null && running) {
                System.out.flush();
                System.out.println(">" + serverMessage);
            }
        } catch (IOException e) {
            System.err.println("Server disconnected.");
        } finally {
            try {
                in.close();
            } catch (IOException e) {
                System.err.println("Error closing input stream: " + e.getMessage());
            }
        }
    }
}
