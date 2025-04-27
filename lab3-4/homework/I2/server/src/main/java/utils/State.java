package utils;

import java.time.LocalTime;
import java.time.format.DateTimeFormatter;

public class State {

    private static final DateTimeFormatter TIME_FORMATTER = DateTimeFormatter.ofPattern("HH:mm:ss:SS");

    public int counter;
    public String lastUsedTimestamp;

    public State() {
    }

    public State(int counter) {
        this.counter = counter;
        this.lastUsedTimestamp = LocalTime.now().format(TIME_FORMATTER);
    }
}
