package server.servants;

import Servants.*;
import com.zeroc.Ice.Current;

public class SharedImpl implements Shared {
    @Override
    public String getStatus(Current current) {
        System.out.println("[Shared] getStatus called on SharedObject");
        return "Shared servant is alive!";
    }
}
