package server.servants;

import Servants.*;
import com.zeroc.Ice.Current;

public class DedicatedImpl implements Dedicated {
    private final String identity;

    public DedicatedImpl(String identity) {
        this.identity = identity;
        System.out.println("[Dedicated] Created servant for identity: " + identity);
    }

    @Override
    public String sayHello(Current current) {
        System.out.println("[Dedicated] sayHello called on identity: " + identity +
                ", Ice identity: " + current.id.name + " / " + current.id.category);
        return "Hello from Dedicated: " + identity;
    }
}
