package server;

import com.zeroc.Ice.*;
import com.zeroc.Ice.Exception;

import server.servants.*;
import utils.MessageLogger;

public class Main {

    public static final String SERVER_IDENTITY = "Server";

    public static void main(String[] args) {
        try (Communicator communicator = Util.initialize(args, "config.server")) {

            ObjectAdapter adapter = communicator.createObjectAdapterWithEndpoints("CookieAdapter", "default -p 10000");
            adapter.addServantLocator(new DedicatedServantLocator(), "Dedicated");

            SharedImpl sharedServant = new SharedImpl();
            Identity sharedId = new Identity("SharedObject", "");
            adapter.add(sharedServant, sharedId);

            adapter.activate();
            MessageLogger.logServer(SERVER_IDENTITY, "Server started and ready...");
            communicator.waitForShutdown();
        } catch (Exception e) {
            MessageLogger.logError(SERVER_IDENTITY, "Exception: " + e);
            e.printStackTrace();
        }
    }
}
