package rpi_interface.Entity;

public class Obstacle {
	private int row_pos, col_pos;
	private String orientation;
	
	public Obstacle(int row, int col, String orientation) {
		row_pos = row;
		col_pos = col;
		this.orientation = orientation;
	}
}
