package utils;

import java.time.LocalTime;
import java.time.format.DateTimeFormatter;

public class MessageLogger {
    private static final DateTimeFormatter TIME_FORMATTER = DateTimeFormatter.ofPattern("HH:mm:ss");

    private static final String RESET = "\u001B[0m";

    private static final String BLUE = "\u001B[34m"; // locate
    private static final String GREEN = "\u001B[32m"; // create
    private static final String RED = "\u001B[31m"; // error
    private static final String YELLOW = "\u001B[33m"; // server
    private static final String PURPLE = "\u001B[35m"; // evict
    private static final String WHITE = "\u001B[37m"; // default logs

    public static void logLocate(String identity, String message) {
        logWithColor(BLUE, identity, message);
    }

    public static void logEvict(String identity, String message) {
        logWithColor(PURPLE, identity, message);
    }

    public static void logCreate(String identity, String message) {
        logWithColor(GREEN, identity, message);
    }

    public static void logError(String identity, String message) {
        logWithColor(RED, identity, message);
    }

    public static void logServer(String identity, String message) {
        logWithColor(YELLOW, identity, message);
    }

    public static void log(String identity, String message) {
        logWithColor(WHITE, identity, message);
    }

    private static void logWithColor(String color, String identity, String message) {
        String time = LocalTime.now().format(TIME_FORMATTER);
        System.out.println(color + "[" + time + "][" + identity + "] " + message + RESET);
    }

}
