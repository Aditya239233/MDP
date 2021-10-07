package com.example.mdp_android.Arena;

import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.util.Log;

public class Obstacle {
    float x, y;
    float initX, initY;
    float xArena, yArena = -1;
    int touchCount = 0;
    boolean actionDown = false;
    String obsFace = "None";
    String obsID, targetID;
    Paint obsPaint;

    public Obstacle(float x, float y, float initX, float initY, String obsID, int touchCount, String obsFace, Paint obsPaint, String targetID){
        this.x = x;
        this.y = y;
        this.touchCount = touchCount;
        this.obsFace = "north";
        this.obsID = obsID;
        this.obsPaint = obsPaint;
        this.targetID = targetID;
        this.initX = initX;
        this.initY = initY;
    }

    public float getObsX(){
        return  x;
    }

    public float getObsY(){
        return  y;
    }

    public float [] getInitCoords () {
        return new float [] {initX,initY};}

    public String getObsFace(){
        return obsFace;
    }

    public String getObsID(){
        return obsID;
    }

    public int getTouchCount(){
        return touchCount;
    }

    public int incrTouchCount(){
        touchCount++;
        return touchCount;
    }

    public float setObsX(float x){
        this.x = x;
        return x;
    }

    public float setObsY(float y){
        this.y = y;
        return y;
    }

    public void setInitX(float initX){
        this.initX = initX;
    }

    public void setInitY(float initY){
        this.initY = initY;
    }

    public void setInitCoords (float initX, float initY) {
        this.initX = initX;
        this.initY = initY;
    }

    public String setObsFace(int touchCount){
        switch (touchCount){
            case 0:
                //Blue: Front
                obsFace = "North";
                break;
            case 1:
                //Green: Left (West)
                obsFace = "West";
                break;
            case 3:
                //Red: Right
                obsFace = "East";
                break;
            case 2:
                //Yellow: Down
                obsFace = "South";
                break;
            default:
                //Black
                obsFace = " ";
        }
        this.obsFace = obsFace;
        return obsFace;
    }

    public String setObsID(String obsID){
        this.obsID = obsID;
        return obsID;
    }

    //Setting action down status
    public void setActionDown(boolean status){
        //When touched down
        this.actionDown = status;
    }

    //Getting action down status
    public boolean getActionDown(){
        return actionDown;
    }

    //To set new position of draggable object
    public void setPosition(float x, float y){
        this.x = (float) (x-12.5);
        this.y = (float) (y-12.5);
    }

    //Use this for draggable object
    public boolean isTouched(float x, float y){
        Log.d("isTouched", x + ", " + y);
        Log.d("isTouched", this.x + ", " + this.y);

        boolean xIsInside = x > this.x && x < this.x + 100;
        boolean yIsInside = y > this.y && y < this.y + 100;

        Log.d("isTouched", xIsInside + ", " + yIsInside);

        return xIsInside && yIsInside;
    }

    public void setObsMapCoord (float xArena, float yArena){
        this.xArena = xArena;
        this.yArena = yArena;
    }

    public float[] getObsMapCoord (){
        return new float[]{xArena, yArena};
    }

    public int resetTouchCount() {
        touchCount = 0;
        return touchCount;
    }

    public Paint getObsPaint() {
        return obsPaint;
    }

    //Setting the obstacle's paint settings
    public Paint setObsPaint(Paint obsPaint) {
        this.obsPaint = obsPaint;
        return obsPaint;
    }

    public int setTouchCount(int touchCount) {
        this.touchCount = touchCount % 4;
        return this.touchCount;
    }

    public String setTargetID(String targetID) {
        this.targetID = targetID;
        return targetID;
    }

    public String getTargetID() {
        return targetID;
    }

    public void drawObj(Canvas canvas, Paint obstaclePaint){
        //Log.d(TAG, "drawObj: Drawing Object");
        Paint myPaint = new Paint();
        myPaint.setColor(Color.BLACK);
        canvas.drawRect(x,y,x+31,y+31,obstaclePaint);
    }
}
