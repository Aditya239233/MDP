package rpi_interface;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Map;

import rpi_interface.Entity.Arena;

public class Main {

	
	public static void main(String[] args) {
		Runnable pathPusher = new PathPusher();
		Thread pathPusherThread = new Thread(pathPusher);
		
		Runnable RPIsocket = new RPISocket();
		Thread RPISocketThread = new Thread(RPIsocket);
		
		pathPusherThread.start();
		RPISocketThread.start();
	}
	
	private static void testAPI() {
		String curr_id = "";
		Map params;
		
		System.out.println("Waiting for RPI...");
		wait(2000);
		System.out.println("Received info from RPI");
		System.out.println("Sending job request to path planner");
		
		try {
			
			//get last job id
			params = WebAPI.get("http://127.0.0.1:5000/");		
			System.out.println("Last job id is " + params.get("job-id"));
			
			//info from RPI
			int ROW = 20;
			int COL = 20;
			
			Arena arena = new Arena(ROW, COL);
			arena.setObstacle(4,5,"N");
			arena.setObstacle(5,7,"S");
			arena.setObstacle(7,10,"E");
			
			//send job request to path planner
			params = WebAPI.post("http://127.0.0.1:5000/planner", arena);
			curr_id = (String)params.get("job-id");
			System.out.println("Current job is " + curr_id);
			
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		while(true) {
			try {
				params = WebAPI.get("http://127.0.0.1:5000/job/" + curr_id);
				
				if(params.get("done") == null) {
					wait(10 * 1000);
				} else {
					ArrayList actions = (ArrayList)params.get("actions");
					System.out.println("Path planning found this actions: ");
					System.out.println(actions);
					break;
				}
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}
	
	private static void wait(int ms) {
		try {
			Thread.sleep(ms);
		} catch (InterruptedException e) {
			Thread.currentThread().interrupt();
		}
	}

}
