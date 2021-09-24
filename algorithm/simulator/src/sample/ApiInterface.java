package sample;

import com.google.gson.Gson;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.*;


public class ApiInterface {

    private RobotPath path;

    static class RobotPath {
        String status;
        ArrayList<ArrayList<Double>> data;
        int id;
        public RobotPath(String status, ArrayList<ArrayList<Double>> data) {
            this.status = status;
            this.data = data;
            this.id = id;
        }
    }
    private static String POSTS_API_URL = "http://127.0.0.1:3000/get-path/?obstacles=[(10,14,'E'),(20,20,'E'),(10,30,'E'),(36,34,'W'),(8,30,'S')]";

    private String getDirection(Integer i){
        switch (i) {
            case 0 -> {
                return "E";
            }
            case 1 -> {
                return "N";
            }
            case 2 -> {
                return "W";
            }
            case 3 -> {
                return "S";
            }
        }
        return "E";
    }

    public ArrayList<Map> getObstacles(String obsStr) {
        List<String> strList = new ArrayList<String>(Arrays.asList(obsStr.split(",")));
        List<Integer> obsList = new ArrayList<Integer>();
        for(String s : strList) obsList.add(Integer.valueOf(s));

        ArrayList<Map> obstacles = new ArrayList<>();
        ArrayList<int[]> x = new ArrayList<>(Arrays.asList(new int[] {obsList.get(0),obsList.get(1)},
                new int[] {obsList.get(3),obsList.get(4)},
                new int[] {obsList.get(6),obsList.get(7)},
                new int[] {obsList.get(9),obsList.get(10)},
                new int[] {obsList.get(12),obsList.get(13)}));
        ArrayList<String> dir = new ArrayList<>(Arrays.asList(getDirection(obsList.get(2)), getDirection(obsList.get(5)), getDirection(obsList.get(8)),  getDirection(obsList.get(11)), getDirection(obsList.get(14))));
//        ArrayList<int[]> x = new ArrayList<>(Arrays.asList(new int[] {10,8},
//                new int[] {10,16},
//                new int[] {10,24},
//                new int[] {10, 30},
//                new int[] {10, 36}));
//        ArrayList<String> dir = new ArrayList<>(Arrays.asList("W", "W", "W",  "W", "W"));
//        ArrayList<int[]> x = new ArrayList<>(Arrays.asList(new int[] {16,0},
//                new int[] {36,0},
//                new int[] {22,22},
//                new int[] {10, 32},
//                new int[] {20, 32}));
//        ArrayList<String> dir = new ArrayList<>(Arrays.asList("N", "N", "E",  "E", "W"));
//        ArrayList<int[]> x = new ArrayList<>(Arrays.asList(new int[] {10,14},
//                new int[] {20,20},
//                new int[] {10,30},
//                new int[] {36, 34},
//                new int[] {8, 30}));
//        ArrayList<String> dir = new ArrayList<>(Arrays.asList("E", "E", "E",  "W", "S"));

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




    public RobotPath getPath(String obsStr) {
        getObstacles(obsStr);
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
        path = gson.fromJson(res, RobotPath.class);
//        System.out.println(path.data.get(0));
//        System.out.println(path.data.get(0).get(1));
        return path;

    }

    public ArrayList<ArrayList<Double>> getPathById(String id) {
        HttpClient client = HttpClient.newBuilder().followRedirects(HttpClient.Redirect.NORMAL).build();
        HttpRequest request = HttpRequest.newBuilder()
                .GET()
                .header("accept", "application/json")
                .uri(URI.create("http://127.0.0.1:3000/from-id/?id=" + id))
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
        path = gson.fromJson(res, RobotPath.class);
        return path.data;

    }

    public ArrayList<ArrayList<Double>> replayPath() {
        return path.data;
    }



}
