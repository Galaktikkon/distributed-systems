package server;

import com.zeroc.Ice.*;
import com.zeroc.Ice.Exception;

import server.evictor.DedicatedServantEvictor;
import server.servants.*;
import utils.CookieJarHandler;
import utils.MessageLogger;

public class Main {

    private static final int MAX_SERVANTS = 2;
    public static final String SERVER_IDENTITY = "Server";

    public static void main(String[] args) {
        try (Communicator communicator = Util.initialize(args, "config.server")) {
            ObjectAdapter adapter = communicator.createObjectAdapterWithEndpoints("CookieAdapter", "default -p 10000");

            SharedReporterImpl sharedReporter = new SharedReporterImpl();
            Identity sharedId = new Identity("SharedObject", "");
            adapter.add(sharedReporter, sharedId);

            CookieJarHandler handler = new CookieJarHandler(sharedReporter);

            DedicatedServantEvictor evictor = new DedicatedServantEvictor(adapter, MAX_SERVANTS, handler);
            adapter.addServantLocator(evictor, "Dedicated");

            adapter.activate();
            MessageLogger.logServer(SERVER_IDENTITY, "Server started and ready...");

            Runtime.getRuntime().addShutdownHook(new Thread(() -> {
                MessageLogger.logServer(SERVER_IDENTITY, "Graceful shutdown initiated...");

                try {
                    evictor.saveAllServants();
                    adapter.deactivate();
                    communicator.destroy();
                    MessageLogger.logServer(SERVER_IDENTITY, "Shutdown complete. Goodbye!");
                } catch (Exception e) {
                    MessageLogger.logError(SERVER_IDENTITY, "Error during shutdown: " + e);
                }
            }));

            communicator.waitForShutdown();
        } catch (Exception e) {
            MessageLogger.logError(SERVER_IDENTITY, "Exception: " + e);
            e.printStackTrace();
        }
    }
}
