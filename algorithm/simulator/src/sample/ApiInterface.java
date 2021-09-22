package sample;

import com.google.gson.Gson;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;





public class ApiInterface {

    static class Path {
        String status;
        ArrayList<ArrayList<Double>> data;
        public Path(String status, ArrayList<ArrayList<Double>> data) {
            this.status = status;
            this.data = data;
        }
    }
    private static String POSTS_API_URL = "http://127.0.0.1:3000/get-path/?obstacles=[(10,14,'E'),(20,20,'E'),(10,30,'E'),(36,34,'W'),(8,30,'S')]";


    public ArrayList<Map> getObstacles( ) {
        ArrayList<Map> obstacles = new ArrayList<>();
//        ArrayList<int[]> x = new ArrayList<>(Arrays.asList(new int[] {10,8},
//                new int[] {10,16},
//                new int[] {10,24},
//                new int[] {10, 30},
//                new int[] {10, 36}));
//        ArrayList<String> dir = new ArrayList<>(Arrays.asList("W", "W", "W",  "W", "W"));
        ArrayList<int[]> x = new ArrayList<>(Arrays.asList(new int[] {10,14},
                new int[] {20,20},
                new int[] {10,30},
                new int[] {36, 34},
                new int[] {8, 30}));
        ArrayList<String> dir = new ArrayList<>(Arrays.asList("E", "E", "E",  "W", "S"));

        String obsString = "http://127.0.0.1:3000/get-path/?obstacles=[";
        for (int i = 0; i < dir.size(); i++ ) {
            String coordStr = "(" + x.get(i)[0] + "," + x.get(i)[1] + ",'" + dir.get(i) + "'),";
            obsString = obsString + coordStr;
            Map<String, Object> obs1 = new HashMap<String, Object>();
            obs1.put("x", (int) x.get(i)[0]/2);
            obs1.put("y", (int) (19-x.get(i)[1]/2));
            obs1.put("direction", dir.get(i));
            obstacles.add(obs1);

        }
        obsString = obsString + "]";
        POSTS_API_URL = obsString;
        return obstacles;

    }




    public ArrayList<ArrayList<Double>> getPath() {
        HttpClient client = HttpClient.newBuilder().followRedirects(HttpClient.Redirect.NORMAL).build();
        HttpRequest request = HttpRequest.newBuilder()
                .GET()
                .header("accept", "application/json")
                .uri(URI.create(POSTS_API_URL))
                .build();

        HttpResponse<String> response = null;
        try {
            response = client.send(request, HttpResponse.BodyHandlers.ofString());
        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        String res = response.body();
        Gson gson = new Gson();
        Path path = gson.fromJson(res, Path.class);
//        System.out.println(path.data.get(0));
//        System.out.println(path.data.get(0).get(1));
        return path.data;

    }



}
