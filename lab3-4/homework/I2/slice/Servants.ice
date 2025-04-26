module Servants {
    interface Dedicated {
        string sayHello();
    };

    interface Shared {
        string getStatus();
    };
};
