package utils;

import server.servants.SharedReporterImpl;

public class CookieJarHandler {
    private final SharedReporterImpl sharedReporter;

    public CookieJarHandler(SharedReporterImpl sharedReporter) {
        this.sharedReporter = sharedReporter;
    }

    public void reportCookieEaten() {
        sharedReporter.eatCookie();
    }
}
