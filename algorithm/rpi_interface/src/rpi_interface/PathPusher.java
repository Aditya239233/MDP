package rpi_interface;

public class PathPusher implements Runnable{
	
	public PathPusher() {
		
	}
	
	public void run() {
		while(true) {
			System.out.println("Waiting for job to finish");
			wait(5*1000);
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
