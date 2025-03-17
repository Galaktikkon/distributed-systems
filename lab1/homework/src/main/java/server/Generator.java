package server;

import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;
import org.json.JSONObject;

public class Generator {

    private static int id = 0;

    public static String getNickName() {
        String animal = null;
        try {
            HttpClient client = HttpClient.newHttpClient();
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("https://random-animal-api.vercel.app/api/random-animal"))
                    .GET()
                    .build();

            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            JSONObject jsonResponse = new JSONObject(response.body());

            animal = jsonResponse.getString("city");

        } catch (Exception e) {
            e.printStackTrace();
        }
        return animal;
    }

    public static int getUniqueID() {
        return id++;
    }
}
