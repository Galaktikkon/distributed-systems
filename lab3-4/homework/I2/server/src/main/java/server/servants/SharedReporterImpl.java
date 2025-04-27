package server.servants;

import Servants.*;
import utils.MessageLogger;

import com.zeroc.Ice.Current;

public class SharedReporterImpl implements SharedReporter {

    private volatile int totalCookiesEaten = 0;

    @Override
    public String getEatenStatus(Current current) {
        MessageLogger.log("SharedReporter", "Total cookies eaten: " + this.totalCookiesEaten);
        return "Total cookies eaten: " + this.totalCookiesEaten;
    }

    public synchronized void eatCookie() {
        totalCookiesEaten++;
    }
}
