package client;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Scanner;

import server.Server;

public class TCPClient {

    public static void main(String[] args) {
        String hostName = "localhost";
        int portNumber = Server.PORT;
        Socket socket = null;
        PrintWriter out = null;
        BufferedReader in = null;
        ServerOutputHandler serverOutputHandler = null;
        Scanner scanner = new Scanner(System.in);
        String nickname;
        try {
            socket = new Socket(hostName, portNumber);
            out = new PrintWriter(socket.getOutputStream(), true);
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            nickname = in.readLine();
            System.out.println(">Server: Your assigned nickname: " + nickname);

            serverOutputHandler = new ServerOutputHandler(in);
            new Thread(serverOutputHandler).start();

            while (true) {

                if (!scanner.hasNextLine()) {
                    break;
                }

                String userMessage = scanner.nextLine();
                System.out.print("\033[F\033[K");

                if (userMessage.equalsIgnoreCase("exit")) {
                    break;
                }

                out.println(userMessage);

            }
        } catch (IOException e) {
            System.err.println("Connection to server lost: " + e.getMessage());
        } finally {
            try {
                if (out != null)
                    out.close();
                if (in != null)
                    in.close();
                if (socket != null)
                    socket.close();
            } catch (IOException e) {
                System.err.println("Error closing resources: " + e.getMessage());
            }
            serverOutputHandler.stop();
            scanner.close();
            System.out.println("Client disconnected.");
        }
    }
}
