package server.servants;

import Servants.*;
import com.zeroc.Ice.Current;
import com.fasterxml.jackson.databind.ObjectMapper;
import utils.MessageLogger;
import utils.State;

import java.io.File;
import java.io.IOException;

public class DedicatedJarImpl implements DedicatedJar {
    private final String identity;
    private int eatenCookieCounter = 0;

    private static final ObjectMapper objectMapper = new ObjectMapper();

    public DedicatedJarImpl(String identity) {
        this.identity = identity;
        MessageLogger.logCreate(identity, "Servant created");
        loadStateFromFile();
    }

    @Override
    public String eatCookie(Current current) {
        eatenCookieCounter++;
        MessageLogger.log(identity, "Eaten a cookie! Cookies eaten from this jar: " + eatenCookieCounter);
        return "Eaten a cookie! Cookies eaten from " + identity + ": " + eatenCookieCounter;
    }

    public void saveStateToFile() {
        String filename = "state_" + identity + ".json";
        State state = new State(eatenCookieCounter);
        try {
            objectMapper.writeValue(new File(filename), state);
            MessageLogger.logEvict(identity,
                    "State saved to file: " + filename + ", with timestamp: " + state.lastUsedTimestamp);
        } catch (IOException e) {
            MessageLogger.logError(identity, "Failed to save state: " + e.getMessage());
        }
    }

    public void loadStateFromFile() {
        String filename = "state_" + identity + ".json";
        File file = new File(filename);
        if (file.exists()) {
            try {
                State state = objectMapper.readValue(file, State.class);
                this.eatenCookieCounter = state.counter;
                MessageLogger.logCreate(identity,
                        "State loaded from file: " + filename + ", with timestamp: " + state.lastUsedTimestamp);
            } catch (IOException e) {
                MessageLogger.logError(identity, "Failed to load state: " + e.getMessage());
            }
        }
    }
}
