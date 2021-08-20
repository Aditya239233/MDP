package simulator;

import java.util.ArrayList;

import javafx.animation.*;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;
import javafx.scene.control.*;
import javafx.event.*;
import javafx.stage.Stage;
import javafx.util.Duration;

public class MainWindow extends Application {
	
	private static int HEIGHT=600, WIDTH=600;

	private static double radToDeg(double rad) {
		return rad * 180/Math.PI;
	}
	
	private static double degToRad(double deg) {
		return deg * Math.PI/180;
	}
	
    @Override
    public void start(Stage stage) {
    	
    	BorderPane root = new BorderPane();
    	Pane arena = new Pane();
    	Rectangle car = new Rectangle(10, 20);
    	
    	arena.getChildren().add(car);
    	root.getChildren().add(arena);
    	
    	
    	car.relocate(100, 100);
    	
        Timeline timeline = new Timeline(new KeyFrame(Duration.millis(20), new EventHandler<ActionEvent>() {
        	double dx, dy, dTheta=Math.PI/45;
        	double radius = 100;
        	double theta = Math.PI;
        			
        	double posX = 100;
        	double posY = 100;
        	double orientation = 180;
        	
            @Override
            public void handle(ActionEvent t) {
            	theta += dTheta;
            	
            	dx = -radius * Math.sin(theta) * dTheta;
            	dy = radius * Math.cos(theta) * dTheta;
            	
            	double orientInRad = Math.atan(-1.0/Math.tan(theta));
            	orientation = radToDeg(orientInRad);
            	
            	posX += dx;
            	posY += dy;
            	
            	car.setLayoutX(posX);
            	car.setLayoutY(posY);
            	car.setRotate(orientation+90);
            	
            	System.out.println(posX + " " + posY + " " + theta + " " + orientation);
                
            }
        }));
        timeline.setCycleCount(Timeline.INDEFINITE);
        timeline.play();
    	
    	
    	Scene scene = new Scene(root, HEIGHT, WIDTH);
    	stage.setScene(scene);
    	stage.setTitle("Hello");
    	stage.show();
    }

}


//
//String javaVersion = System.getProperty("java.version");
//String javafxVersion = System.getProperty("javafx.version");
//Label l = new Label("Hello, JavaFX " + javafxVersion + ", running on Java " + javaVersion + ".");
//Scene scene = new Scene(new StackPane(l), 640, 480);
//stage.setScene(scene);
//stage.show();