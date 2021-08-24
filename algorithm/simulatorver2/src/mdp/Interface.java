package mdp;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class Interface {
    private int[][] obstacles = {{0,0,1}, {0,0,1}};

    // path
    public ArrayList<Map> getObstacles() {
        Map<String, Object> obs1 = new HashMap<String, Object>();
        obs1.put("x", 10);
        obs1.put("y", 10);
        obs1.put("direction", "N");
        Map<String, Object> obs2 = new HashMap<String, Object>();
        obs2.put("x", 10);
        obs2.put("y", 19);
        obs2.put("direction", "E");
        Map<String, Object> obs3 = new HashMap<String, Object>();
        obs3.put("x", 5);
        obs3.put("y", 10);
        obs3.put("direction", "N");
        Map<String, Object> obs4 = new HashMap<String, Object>();
        obs4.put("x", 8);
        obs4.put("y", 10);
        obs4.put("direction", "S");
        Map<String, Object> obs5 = new HashMap<String, Object>();
        obs5.put("x", 15);
        obs5.put("y", 10);
        obs5.put("direction", "W");


        ArrayList<Map> obstacles = new ArrayList<>();
        obstacles.add(obs1);
        obstacles.add(obs2);
        obstacles.add(obs3);
        obstacles.add(obs4);
        obstacles.add(obs5);

        System.out.println(obstacles);

        return obstacles;

    }
}
