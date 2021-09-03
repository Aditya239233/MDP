package sample;
import javafx.animation.*;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.Group;
import javafx.scene.Node;
import javafx.scene.control.Button;
import javafx.scene.image.ImageView;
import javafx.scene.layout.GridPane;
import javafx.scene.shape.*;
import javafx.util.Duration;

import java.util.ArrayList;


public class Controller {
    @FXML
    private ImageView robot;
//    @FXML
//    private Polygon direction;
    @FXML
    private Button forward;
    @FXML
    private Button reverse;


    @FXML
    private GridPane grid;

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



        printLocation();
        System.out.println(robot_direction);


    }

    public void path(ActionEvent e) {
        Interface inter = new Interface();
        ArrayList<double[]> route = inter.getPath();

        Timeline timeline = new Timeline();





        var i = 0;
        for (double[] c: route) {
//            LineTo line = new LineTo(c[0], c[1]);
            KeyValue kv = new KeyValue(robot.rotateProperty(), c[2]);
            KeyValue kv2 = new KeyValue(robot.translateXProperty(), c[0]-20.0);
            KeyValue kv3 = new KeyValue(robot.translateYProperty(), c[1]+20);
            KeyFrame kf = new KeyFrame(Duration.millis(i), kv, kv2,kv3);
            timeline.getKeyFrames().add(kf);
            i += 100;
        }
        timeline.play();





    }
}
