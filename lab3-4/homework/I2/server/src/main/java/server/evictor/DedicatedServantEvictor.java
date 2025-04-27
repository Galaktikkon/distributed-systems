package server.evictor;

import com.zeroc.Ice.*;
import server.servants.DedicatedJarImpl;
import utils.CookieJarHandler;
import utils.MessageLogger;

import java.util.LinkedHashMap;
import java.util.Map;

public class DedicatedServantEvictor implements ServantLocator {

    private static final String EVICTOR_IDENTITY = "Evictor";
    private final ObjectAdapter adapter;
    private final int maxServants;
    private final CookieJarHandler handler;

    private final LinkedHashMap<Identity, DedicatedJarImpl> servantCache;

    public DedicatedServantEvictor(ObjectAdapter adapter, int maxServants, CookieJarHandler handler) {
        this.adapter = adapter;
        this.maxServants = maxServants;
        this.servantCache = new LinkedHashMap<>(maxServants, 0.75f, true); // LRU
        this.handler = handler;
    }

    @Override
    public synchronized LocateResult locate(Current current) throws UserException {
        Identity id = current.id;
        MessageLogger.logLocate(EVICTOR_IDENTITY, "Locate called for ID: " + id.name);

        DedicatedJarImpl servant = servantCache.get(id);
        if (servant != null) {
            servantCache.get(id);
            return new LocateResult(servant, null);
        }

        if (servantCache.size() >= maxServants) {
            evictOldest();
        }

        DedicatedJarImpl newServant = new DedicatedJarImpl(id.name, this.handler);
        adapter.add(newServant, id);
        servantCache.put(id, newServant);
        MessageLogger.logCreate(EVICTOR_IDENTITY, "Created servant for ID: " + id.name);

        return new LocateResult(newServant, null);
    }

    @Override
    public synchronized void finished(Current current, com.zeroc.Ice.Object servant, java.lang.Object cookie)
            throws UserException {
        MessageLogger.log(EVICTOR_IDENTITY, "Finished called for ID: " + current.id.name);
    }

    @Override
    public synchronized void deactivate(String category) {
        MessageLogger.log(EVICTOR_IDENTITY, "Deactivate called for category: " + category);
        for (Map.Entry<Identity, DedicatedJarImpl> entry : servantCache.entrySet()) {
            entry.getValue().saveStateToFile();
            adapter.remove(entry.getKey());
        }
        servantCache.clear();
    }

    public synchronized void saveAllServants() {
        for (Map.Entry<Identity, DedicatedJarImpl> entry : servantCache.entrySet()) {
            Identity id = entry.getKey();
            DedicatedJarImpl servant = entry.getValue();
            servant.saveStateToFile();
            MessageLogger.logEvict(EVICTOR_IDENTITY, "Saved state of servant ID: " + id.name);
            adapter.remove(id);
        }
        servantCache.clear();
    }

    private void evictOldest() {
        servantCache.entrySet().stream().findFirst().ifPresent(entry -> {
            Identity id = entry.getKey();
            DedicatedJarImpl servant = entry.getValue();
            MessageLogger.logEvict(EVICTOR_IDENTITY, "Evicting servant ID: " + id.name);
            servant.saveStateToFile();
            adapter.remove(id);
            servantCache.remove(id);
        });
    }
}
