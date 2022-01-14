package sample;
import javafx.animation.*;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.Group;
import javafx.scene.Node;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;
import javafx.scene.image.ImageView;
import javafx.scene.layout.AnchorPane;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.shape.*;
import javafx.scene.text.Text;
import javafx.util.Duration;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Map;


public class Controller {




    @FXML
    private ImageView robot;
    @FXML
    private VBox idList;
    @FXML
    private Button forward;
    @FXML
    private Button reverse;

    @FXML
    private TextField obstacles;

    @FXML
    private TextField job_id;

    @FXML
    private Button playCoord;
    @FXML
    private Button playId;


    @FXML
    private GridPane grid;

    @FXML
    private AnchorPane pane;


    private String robot_direction = "N";



    private void printLocation() {
        System.out.println(robot.getTranslateX());
        System.out.println(robot.getTranslateY());
    }



    public void straight(ActionEvent e) {

        String dir = ((Node) e.getSource()).getId();
        switch (robot_direction) {
            case "N":
                robot.setTranslateY(dir.equals("forward") ? robot.getTranslateY() - 10 : robot.getTranslateY() + 10);
                break;
            case "E":
                robot.setTranslateX(dir.equals("forward") ? robot.getTranslateX() + 10 : robot.getTranslateX() - 10);
                break;
            case "S":
                robot.setTranslateY(dir.equals("forward") ? robot.getTranslateY() + 10 : robot.getTranslateY() - 10);
                break;
            case "W":
                robot.setTranslateX(dir.equals("forward") ? robot.getTranslateX() - 10 : robot.getTranslateX() + 10);
                break;
        }
        printLocation();
    }


    public void left(ActionEvent e) {

        double startAngle = 0.0f;
        double centerX = 0;
        double centerY = 0;
        switch (robot_direction) {
            case "N" -> {
                startAngle = 0.0f;
                centerX = robot.getTranslateX() - 20.0f;
                centerY = robot.getTranslateY() + 30.0f;
                robot_direction = "W";
            }
            case "E" -> {
                startAngle = -90.0f;
                centerX = robot.getTranslateX() + 30.0f;
                centerY = robot.getTranslateY() - 20.0f;
                robot_direction = "N";
            }
            case "S" -> {
                startAngle = 180.0f;
                centerX = robot.getTranslateX() + 80.0f;
                centerY = robot.getTranslateY() + 30.0f;
                robot_direction = "E";
            }
            case "W" -> {
                startAngle = 90.0f;
                centerX = robot.getTranslateX() + 30.0f;
                centerY = robot.getTranslateY() + 80.0f;
                robot_direction = "S";
            }
        }
        Arc arc = new Arc();
        arc.setCenterX(centerX);
        arc.setCenterY(centerY);
        arc.setRadiusX(50.0f);
        arc.setRadiusY(50.0f);
        arc.setStartAngle(startAngle);
        arc.setLength(90.0f);
        arc.setType(ArcType.OPEN);

        PathTransition transition = new PathTransition();
        transition.setNode(robot);
        transition.setDuration(Duration.seconds(3));
        transition.setPath(arc);
        transition.setAutoReverse(false);
        transition.setOrientation(PathTransition.OrientationType.ORTHOGONAL_TO_TANGENT);
        transition.play();

//        direction.setRotate(direction.getRotate()-90);

        printLocation();
        System.out.println(robot_direction);


    }
    public void right(ActionEvent e){
        double startAngle = 0.0f;
        double centerX = 0;
        double centerY = 0;
        switch (robot_direction) {
            case "N" -> {
                startAngle = 180.0f;
                centerX = robot.getTranslateX() + 80.0f;
                centerY = robot.getTranslateY() + 30.0f;
                robot_direction = "E";
            }
            case "E" -> {
                startAngle = 90.0f;
                centerX = robot.getTranslateX() + 30.0f;
                centerY = robot.getTranslateY() + 80.0f;
                robot_direction = "S";
            }
            case "S" -> {
                startAngle = 0.0f;
                centerX = robot.getTranslateX() - 20.0f;
                centerY = robot.getTranslateY() + 30.0f;
                robot_direction = "W";
            }
            case "W" -> {
                startAngle = -90.0f;
                centerX = robot.getTranslateX() + 30.0f;
                centerY = robot.getTranslateY() - 20.0f;
                robot_direction = "N";
            }
        }
        Arc arc = new Arc();
        arc.setCenterX(centerX);
        arc.setCenterY(centerY);
        arc.setRadiusX(50.0f);
        arc.setRadiusY(50.0f);
        arc.setStartAngle(startAngle);
        arc.setLength(-90.0f);
        arc.setType(ArcType.OPEN);



        PathTransition transition = new PathTransition();
        transition.setNode(robot);
        transition.setDuration(Duration.seconds(3));
        transition.setPath(arc);
        transition.setAutoReverse(false);

        transition.setOrientation(PathTransition.OrientationType.ORTHOGONAL_TO_TANGENT);
        transition.play();

//        RotateTransition rt = new RotateTransition(Duration.seconds(3), direction);
//        rt.setByAngle(90);
//        rt.play();
//        direction.setRotate(direction.getRotate()+90);

//
        printLocation();
        System.out.println(robot_direction);


    }

    public void visualiseObstacles(ActionEvent e) {
        String coordinatesStr = obstacles.getText();
        showObstacles(coordinatesStr);
    }
    private void showObstacles(String coordStr) {
        ApiInterface inter = new ApiInterface();
        ArrayList<Map> obstacles = inter.getObstacles(coordStr);
        int i = 0;
        Scene scene = grid.getScene();
        grid.getChildren().removeAll(scene.lookup("#obs0"), scene.lookup("#obs1"), scene.lookup("#obs2"), scene.lookup("#obs3"), scene.lookup("#obs4"));
        for (Map obs : obstacles) {
            Rectangle r = new Rectangle();
            r.setWidth(20);
            r.setHeight(20);

            switch (obs.get("direction").toString()) {
                case "N":
                    r.setStyle("-fx-fill: linear-gradient(to top,#000000 80%, #FF0000 1%)");
                    break;
                case "E":
                    r.setStyle("-fx-fill: linear-gradient(to right,#000000 80%, #FF0000 1%)");
                    break;
                case "S":
                    r.setStyle("-fx-fill: linear-gradient(to bottom,#000000 80%, #FF0000 1%)");
                    break;
                case "W":
                    r.setStyle("-fx-fill: linear-gradient(to left,#000000 80%, #FF0000 1%)");
                    break;
            }
            r.setId("obs" + String.valueOf((i)));
            i++;

            grid.add(r, (int) obs.get("x"), (int) obs.get("y"));
        }


    }



    public void getPath(ActionEvent e) {

        String playType = ((Node) e.getSource()).getId();

        ApiInterface inter = new ApiInterface();
        ApiInterface.RobotPath path;
        ArrayList<ArrayList<Double>> route;

        if (playType.equals("playCoord")) {
            String coordinatesStr = obstacles.getText();
            showObstacles(coordinatesStr);
            path = inter.getPath(coordinatesStr);
            System.out.println(path.id);
            route = path.data;
            Text t = new Text();
            t.setText(String.valueOf(path.id) + ": " + coordinatesStr);
            idList.getChildren().add(t);
//            idList.setText(String.valueOf(path.id) + ": " + coordinatesStr);

        } else {
            String id = job_id.getText();
            route = inter.getPathById(id);
        }



        if (route == null) {
            System.out.println("No path found!");
            return;
        }
        playPath(route);
    }


    public void replayPath(ActionEvent e) {
        ApiInterface inter = new ApiInterface();
        ArrayList<ArrayList<Double>> route = inter.replayPath();
        if (route == null) {
            System.out.println("No path found!");
            return;
        }
        playPath(route);
    }

    public void playPath(ArrayList<ArrayList<Double>> route) {

        pane.getChildren().remove(pane.lookup("#path"));
        Path path = new Path();


        path.setStroke(Color.RED);
//        path.setStrokeWidth(1.0);

        MoveTo moveTo = new MoveTo();
        moveTo.setX((route.get(0).get(0)) *10 -120.0);
        moveTo.setY((route.get(0).get(1))*-10 +120);
        path.getElements().add(moveTo);
        path.setLayoutX(20);
        path.setLayoutY(380);


        Timeline timeline = new Timeline();

        var i = 0;
        for (ArrayList<Double> c: route) {

            if (c.get(0) == -1) {
                i += 300;
                continue;
            }

            double x = c.get(0) *10 -120;
            double y = c.get(1) *-10 +120;


            LineTo lineTo = new LineTo();
            lineTo.setX(x);
            lineTo.setY(y);
            path.getElements().add(lineTo);

//            LineTo line = new LineTo(c[0], c[1]);
            double rotate = c.get(2) * (180/Math.PI) * -1;
            System.out.println(rotate);
            if (rotate >= 0) {
                rotate = rotate -360;
            }
            KeyValue kv = new KeyValue(robot.rotateProperty(), rotate );
            KeyValue kv2 = new KeyValue(robot.translateXProperty(), c.get(0) *10 -120.0);
            KeyValue kv3 = new KeyValue(robot.translateYProperty(), c.get(1) *-10 +120);
            KeyFrame kf = new KeyFrame(Duration.millis(i), kv, kv2,kv3);
            timeline.getKeyFrames().add(kf);
            i += 100;
//            path.getElements().add(new LineTo(c[0], c[1]));
//            robot.setRotate(c[2]);
        }
        path.setId("path");
        pane.getChildren().add(path);
        timeline.play();
//        System.out.println(path);
//        PathTransition transition = new PathTransition();
//
//        transition.setDuration(Duration.seconds(10));
////        transition.setNode(forward);
//        transition.setPath(path);
//        transition.setAutoReverse(false);

//        transition.play();
//        printLocation();
//
//        RotateTransition rt = new RotateTransition(Duration.seconds(10), robot);
//        rt.setByAngle(90);
//        rt.play();




    }



}
