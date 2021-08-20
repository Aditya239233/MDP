package rpi_interface;

import java.util.*;

public class RPISocket implements Runnable{
	
	public void run() {
		while(true) {
			System.out.println("Listening for RPI...");
			wait(2*1000);
		}
		
	}
	
	public RPISocket() {
		//System.out.println("Socket established to get info from RPI");
	}
	
	public HashMap<String, String> getData() {
		System.out.println("Info received from RPISocket.");
		HashMap<String, String> hash = new HashMap<>();
		hash.put("arena_row", "20");
		hash.put("arena_col", "20");
		hash.put("o_1", "4,5,N");
		hash.put("o_2", "5,7,S");
		hash.put("o_3", "7,10,E");
		
		return hash;
	}
	
	public void sendData(ArrayList<String> actions) {
		Iterator<String> it = actions.iterator();
		while(it.hasNext()) {
			System.out.println("Sending to RPI: " + it.next());
		}
		System.out.println("All actions sent to RPI.");
	}
	
	private static void wait(int ms) {
		try {
			Thread.sleep(ms);
		} catch (InterruptedException e) {
			Thread.currentThread().interrupt();
		}
	}
}
