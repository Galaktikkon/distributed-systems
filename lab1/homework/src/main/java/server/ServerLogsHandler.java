package server;

import java.util.concurrent.BlockingQueue;

public class ServerLogsHandler implements Runnable {
    private final BlockingQueue<String> logQueue;
    private volatile boolean running = true;

    public ServerLogsHandler(BlockingQueue<String> logQueue) {
        this.logQueue = logQueue;
    }

    protected void stop() {
        running = false;
    }

    protected void logServerMessage(String message) {
        try {
            logQueue.put(message);
        } catch (InterruptedException e) {
            System.err.println("Error while adding log message to queue: " + e.getMessage());
        }
    }

    @Override
    public void run() {
        while (running) {
            try {
                String messageToLog = logQueue.take();
                if (!running) {
                    break;
                }

                System.out.println(messageToLog);

            } catch (InterruptedException e) {
                if (!running) {
                    break;
                }
                System.err.println("Log handler interrupted, stopping...");
                Thread.currentThread().interrupt();
            }
        }
        System.out.println("Server log handler thread stopped.");
    }
}
