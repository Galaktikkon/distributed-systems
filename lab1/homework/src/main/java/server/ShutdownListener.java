package server;

import java.util.Scanner;

public class ShutdownListener implements Runnable {
    private final Runnable shutdownCallback;

    public ShutdownListener(Runnable shutdownCallback) {
        this.shutdownCallback = shutdownCallback;
    }

    @Override
    public void run() {
        try (Scanner scanner = new Scanner(System.in)) {
            while (true) {
                if (scanner.hasNextLine()) {
                    String command = scanner.nextLine();
                    if ("exit".equalsIgnoreCase(command)) {
                        shutdownCallback.run();
                        break;
                    }
                }
            }
        } catch (Exception e) {
            System.err.println("Error in shutdown listener: " + e.getMessage());
        }
        System.out.println("Server shutdown listener thread stopped.");
    }
}
