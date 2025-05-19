import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Z1_Producer {

    public static void main(String[] argv) throws Exception {

        // info
        System.out.println("Z1 PRODUCER");

        // connection & channel
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        Connection connection = factory.newConnection();
        Channel channel = connection.createChannel();

        // queue
        String QUEUE_NAME = "queue1";
        channel.queueDeclare(QUEUE_NAME, false, false, false, null);
        channel.basicQos(1);

        // // ex base

        // producer (publish msg)
        // String message = "Hello world!";

        // channel.basicPublish("", QUEUE_NAME, null, message.getBytes());
        // System.out.println("Sent: " + message);

        // ex 1a

        // BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        // System.out.println("Enter message: ");
        // String message = br.readLine();

        // channel.basicPublish("", QUEUE_NAME, null, message.getBytes());

        // ex 1b

        String[] tasks = { "1", "5", "1", "5", "1", "5", "1", "5", "1", "5" };
        for (String task : tasks) {
            channel.basicPublish("", QUEUE_NAME, null, task.getBytes());
            System.out.println("Sent: " + (task == "5" ? "long" : "short") + " task:" + task);
        }

        // close
        // channel.close();
        // connection.close();
    }
}
