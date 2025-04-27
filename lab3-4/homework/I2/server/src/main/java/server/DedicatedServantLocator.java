package server;

import server.servants.DedicatedJarImpl;
import utils.MessageLogger;

import com.github.benmanes.caffeine.cache.Cache;
import com.github.benmanes.caffeine.cache.Caffeine;
import com.github.benmanes.caffeine.cache.RemovalCause;
import com.zeroc.Ice.*;

public class DedicatedServantLocator implements ServantLocator {

    private final String LOCATOR_IDENTITY = "Locator";
    private final int MAX_SERVANTS = 2;

    private final Cache<String, DedicatedJarImpl> servantsCache = Caffeine.newBuilder()
            .maximumSize(MAX_SERVANTS)
            .removalListener((String key, DedicatedJarImpl servant, RemovalCause cause) -> {
                if (cause != RemovalCause.REPLACED) {
                    evict(key, servant, cause);
                }
            })
            .build();

    @Override
    public LocateResult locate(Current current) {
        String id = current.id.name;
        MessageLogger.logLocate(this.LOCATOR_IDENTITY, "Locate called for ID: " + id);

        DedicatedJarImpl servant = servantsCache.get(id, key -> {
            MessageLogger.logCreate(this.LOCATOR_IDENTITY, "Creating servant for ID: " + key);
            return new DedicatedJarImpl(key);
        });

        return new LocateResult(servant, null);
    }

    @Override
    public void deactivate(String category) {
        MessageLogger.log(this.LOCATOR_IDENTITY, "Deactivate called for category: " + category);
    }

    @Override
    public void finished(Current current, com.zeroc.Ice.Object servant, java.lang.Object cookie) {
        MessageLogger.log(this.LOCATOR_IDENTITY, "Finished called for ID: " + current.id.name);
    }

    private void evict(String key, DedicatedJarImpl servant, RemovalCause cause) {
        if (key == null || cause == null) {
            MessageLogger.logError(this.LOCATOR_IDENTITY, "Eviction listener received null key or cause!");
            return;
        }

        if (servant != null) {
            servant.saveStateToFile();
        }

        MessageLogger.logEvict(this.LOCATOR_IDENTITY, "Evicted servant ID: " + key + " (Reason: " + cause + ")");
    }
}
