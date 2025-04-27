package server.servants;

import Servants.*;
import utils.MessageLogger;

import com.zeroc.Ice.Current;

public class SharedImpl implements SharedReporter {

    private volatile int totalCookiesEaten = 0;

    @Override
    public String getEatenStatus(Current current) {
        MessageLogger.log("SharedReporter", "Total cookies eaten: " + this.totalCookiesEaten);
        return "Total cookies eaten: " + this.totalCookiesEaten;
    }

    public void eatCookie() {
        totalCookiesEaten++;
    }
}
