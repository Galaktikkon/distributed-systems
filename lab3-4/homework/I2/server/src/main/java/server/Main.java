package server;

import com.zeroc.Ice.*;
import com.zeroc.Ice.Exception;

import server.servants.*;

public class Main {
    public static void main(String[] args) {
        try (Communicator communicator = Util.initialize(args, "config.server")) {
            ObjectAdapter adapter = communicator.createObjectAdapterWithEndpoints("MyAdapter", "default -p 10000");

            // Dodajemy "na sztywno" jeden dedykowany serwant dla "Dedicated1"
            DedicatedImpl dedicatedServant = new DedicatedImpl("Dedicated1");
            Identity dedicatedId = new Identity("Dedicated1", "");
            adapter.add(dedicatedServant, dedicatedId);

            // Dodajemy współdzielony serwant dla Shared
            SharedImpl sharedServant = new SharedImpl();
            Identity sharedId = new Identity("SharedObject", "");
            adapter.add(sharedServant, sharedId);

            adapter.activate();
            System.out.println("[Server] Server started and ready...");
            communicator.waitForShutdown();
        } catch (Exception e) {
            System.err.println("[Server] Exception: " + e);
            e.printStackTrace();
        }
    }
}
