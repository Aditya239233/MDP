package simulator;
import javafx.application.Application;
import simulator.Entity.Arena;

import java.io.IOException;
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpResponse.BodyHandlers;
import java.time.Duration;
import java.util.HashMap;
import java.util.Map;

import com.google.gson.*;


public class Main {
    public static void main(String[] args) {
        //Application.launch(MainWindow.class);
    	Arena arena = getArena();
    	System.out.println(arena);    	
    }
    
    private static Arena getArena() {
    	try {
			Map params = (Map)(WebAPI.get("http://127.0.0.1:5000/arena").get("arena"));
			return new Arena(params);
		} catch (IOException e) {
			e.printStackTrace();
		}
    	
    	return null;
    }
    
    
}

