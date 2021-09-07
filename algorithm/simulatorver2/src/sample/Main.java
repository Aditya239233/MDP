package sample;

import javafx.application.Application;

import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.layout.GridPane;
import javafx.scene.shape.Rectangle;
import javafx.stage.Stage;

import javafx.scene.Scene;


import java.util.ArrayList;
import java.util.Map;


public class Main extends Application {


    public static void main(String[] args) {
        launch(args);
    }

    public void initializeObstacles(GridPane grid) {
        Interface inter = new Interface();
        ArrayList<Map> obstacles = inter.getObstacles();

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
            grid.add(r, (int) obs.get("x"), (int) obs.get("y"));
        }

    }

    @Override
    public void start(Stage stage) throws Exception {
//        Robot Movement Area Simulator
        //1. display robots 2x2 m movement area //
        //2. display start zone//
        // 3. display  locations of obstacles and positions of images - get locations as coordinates and display//
        // 4. position of robot as it moves forward, backward and turns //
        // ........a. forward
        // ........b. backward
        //.........c. turn left
        //.........d. turn right (arrow turn, turn with diff start point)
        // 5. display a grid map of area //
        // need to check if need to turn left or right while reversing


//        Parent root = FXMLLoader.load(getClass().getResource("sample.fxml"));
        Parent root = FXMLLoader.load(getClass().getResource("sim.fxml"));
        Scene scene = new Scene(root);
        String css = this.getClass().getResource("application.css").toExternalForm();
        scene.getStylesheets().add(css);


        stage.setTitle("Playing with FX");
        stage.setScene(scene);

        GridPane grid = (GridPane) scene.lookup("#grid");
        initializeObstacles(grid);


        stage.show();


        // x, y (left corner) and orientation (angle)








    }
}
