package rpi_interface.Entity;

import java.util.ArrayList;

public class Arena {
	private int row, col;
	private ArrayList<Obstacle> obstacles;
	
	public Arena(int row, int col) {
		this.row = row;
		this.col = col;
		obstacles = new ArrayList<>();
	}
	
	public void setObstacle(int r, int c, String orientation) {
		obstacles.add(new Obstacle(r, c, orientation));
	}
	
}
