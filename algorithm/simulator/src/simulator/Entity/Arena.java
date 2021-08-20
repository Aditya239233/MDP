package simulator.Entity;

import java.util.ArrayList;
import java.util.Map;

public class Arena {
	private int row, col;
	private ArrayList<Obstacle> obstacles;
	
	public Arena(int row, int col) {
		this.row = row;
		this.col = col;
		obstacles = new ArrayList<>();
	}
	
	private static int convertDoubleToInteger(double x) {
		return (int)x;
	}
	
	public Arena(Map params) {
		this.row = convertDoubleToInteger((Double)params.get("row"));
		this.col = convertDoubleToInteger((Double)params.get("col"));
		obstacles = new ArrayList<>();
		
		ArrayList<Map> arr = (ArrayList<Map>)params.get("obstacles");
		
		for(Map obstacle : arr) {
			int r = convertDoubleToInteger((Double)obstacle.get("row_pos"));
			int c = convertDoubleToInteger((Double)obstacle.get("col_pos"));
			String orient = (String)obstacle.get("orientation");
			Obstacle ob = new Obstacle(r, c , orient);
			obstacles.add(ob);
		}
	}
	
	public void setObstacle(int r, int c, String orientation) {
		obstacles.add(new Obstacle(r, c, orientation));
	}
	
	public String toString() {
		return String.format("Rows: %d, Cols: %d, Obstacles: %s | %s", row, col, obstacles.get(0), obstacles.get(1));
	}
	
}
