package server;

import java.util.concurrent.BlockingQueue;

public class ServerLogsHandler implements Runnable {
    private final BlockingQueue<String> logQueue;
    private static final String STOP_SIGNAL = "STOP";

    public ServerLogsHandler(BlockingQueue<String> logQueue) {
        this.logQueue = logQueue;
    }

    public void stop() {
        logQueue.offer(STOP_SIGNAL);
    }

    protected void logServerMessage(String message) {
        try {
            logQueue.put(message);
        } catch (InterruptedException e) {
            System.err.println("Error while adding log message to queue: " + e.getMessage());
            Thread.currentThread().interrupt();
        }
    }

    @Override
    public void run() {
        while (true) {
            try {
                String messageToLog = logQueue.take();

                if (STOP_SIGNAL.equals(messageToLog)) {
                    break;
                }

                System.out.println(messageToLog);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
        System.out.println("Server log handler thread stopped.");
    }
}
