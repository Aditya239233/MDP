package com.example.mdp_android.Arena;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.Rect;
import android.graphics.Typeface;
import android.util.AttributeSet;
import android.util.Log;
import android.view.GestureDetector;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.core.view.GestureDetectorCompat;

import com.example.mdp_android.BluetoothConnectionService;
import com.example.mdp_android.arena_map;
import com.example.mdp_android.R;

import java.io.Serializable;
import java.util.ArrayList;

/**
 * The Arena is 2mx2m.
 * Obstacles are 10cmx10cm.
 * Robot is 20cmx20cm.
 * Every grid box should follow obstacle measurements.
 * There will be 5 obstacles in total.
 * Number of rows and columns = 20 by 20.
 *
 * What to draw - handled by Canvas
 * How to draw - handled by Paint
 * */

public class Arena extends View implements Serializable {

    private static final String TAG = "Arena Map";

    private static Cell[][] cells;
    private static final int mCols = 20, mRows = 20;
    private static float cellSize, hMargin, vMargin;
    private static int obsRow = -1, obsCol = -1;
    private static String robotDirection = "north";
    private static int[] obsCoord = new int[]{-1, -1};
    private static int[] curCoord = new int[]{-1, -1};
    private static int[] oldCoord = new int[]{-1, -1};
    private static ArrayList<int[]> obstacleCoord = new ArrayList<>();

    private static Obstacle [] obstacleList = new Obstacle[5];

    private static Paint wallPaint = new Paint();
    private static Paint robotPaint = new Paint();
    private static Paint directionPaint = new Paint();
    private static Paint obstaclePaint = new Paint();
    private static Paint unexploredPaint = new Paint();
    private static Paint exploredPaint = new Paint();
    private static Paint gridNumberPaint = new Paint();
    private static Paint obstacleNumberPaint = new Paint();
    private static Paint emptyPaint = new Paint();
    private static Paint virtualWallPaint = new Paint();

    private static Paint westPaint = new Paint();
    private static Paint eastPaint = new Paint();
    private static Paint southPaint = new Paint();
    private static Paint northPaint = new Paint();
    private static Paint linePaint = new Paint();

    //Create only avail when state is true
    private static boolean createCellStatus = false;
    private static boolean setRobotPostition = false;
    public static boolean setObstaclePosition = false;
    private static boolean validPosition = false;
    private static boolean canDrawRobot = false;
    private static boolean canDrawObstacle = false;
    private static boolean canUpdateObsFace = false;
    private static boolean canDrag = false;
    private static boolean isOnClick = false;

    private View mapView;
    private Rect r;

    private static final int MAX_CLICK_DURATION = 200;
    private long mStartClickTime;

    private GestureDetectorCompat mGestureDetector;
    private LongPressGestureListener longPressGestureListener;
    private GestureDetector.OnDoubleTapListener mDoubleTapListener;

    public static boolean gestureType;

//    Intent i = new Intent(ArenaMap.this, LongPressGestureListener.class).putExtra("Obstacle", obstacle1);

    public Arena(Context context) {
        super(context);
        init(null);
    }

    public Arena(Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
        init(attrs);

        wallPaint.setColor(Color.WHITE);
        robotPaint.setColor(Color.parseColor("#ccd8d7"));
        directionPaint.setColor(Color.BLACK);
        unexploredPaint.setColor(Color.parseColor("#ccd8d7"));
        exploredPaint.setColor(Color.GRAY);
        emptyPaint.setColor(Color.WHITE);
        virtualWallPaint.setColor(Color.parseColor("#FFA500"));

        obstaclePaint.setColor(Color.BLACK);
        obstaclePaint.setStyle(Paint.Style.FILL);
        obstaclePaint.setStrokeWidth(3f);

        obstacleNumberPaint.setColor(Color.WHITE);
        obstacleNumberPaint.setTextSize(20);
        obstacleNumberPaint.setTypeface(Typeface.DEFAULT_BOLD);
        obstacleNumberPaint.setAntiAlias(true);
        obstacleNumberPaint.setStyle(Paint.Style.FILL);
        obstacleNumberPaint.setTextAlign(Paint.Align.LEFT);

        gridNumberPaint.setColor(Color.BLACK);
        gridNumberPaint.setTextSize(15);
        gridNumberPaint.setStyle(Paint.Style.FILL_AND_STROKE);

        westPaint.setColor(Color.GREEN);
        westPaint.setStyle(Paint.Style.FILL);

        eastPaint.setColor(Color.RED);
        eastPaint.setStyle(Paint.Style.FILL);

        northPaint.setColor(Color.YELLOW);
        northPaint.setStyle(Paint.Style.FILL);

        southPaint.setColor(Color.BLUE);
        southPaint.setStyle(Paint.Style.FILL);

        linePaint.setStyle(Paint.Style.STROKE);
        linePaint.setColor(Color.YELLOW);
        linePaint.setStrokeWidth(3f);

        mapView = (View) findViewById(R.id.mapView);

        longPressGestureListener = new LongPressGestureListener();
        mGestureDetector = new GestureDetectorCompat(context, longPressGestureListener);

        obstacleList [0] = new Obstacle (670, 50, 670, 50,"1", 0, "None", obstaclePaint, "1");
        obstacleList [1] = new Obstacle(670, 125, 670, 125,"2", 0, "None", obstaclePaint, "2");
        obstacleList [2] = new Obstacle(670, 200, 670, 200,"3", 0, "None", obstaclePaint, "3");
        obstacleList [3] = new Obstacle(670, 275, 670, 275,"4", 0, "None", obstaclePaint, "4");
        obstacleList [4] = new Obstacle(670, 350, 670, 350,"5", 0, "None", obstaclePaint, "5");

        mDoubleTapListener = new GestureDetector.OnDoubleTapListener() {
            @Override
            public boolean onSingleTapConfirmed(MotionEvent e) {
                Toast.makeText(getContext(), "onSingleTapConfirmed", Toast.LENGTH_SHORT).show();
                return false;
            }

            @Override
            public boolean onDoubleTap(MotionEvent e) {
                Toast.makeText(getContext(), "onDoubleTap", Toast.LENGTH_SHORT).show();
                return false;
            }

            @Override
            public boolean onDoubleTapEvent(MotionEvent e) {
                Toast.makeText(getContext(), "onDoubleTapEvent", Toast.LENGTH_SHORT).show();

                mGestureDetector.setIsLongpressEnabled(false);

                float x = e.getX();
                float y = e.getY();

                Log.d(TAG, "Event--->" + e.getAction());

                //Increase counts for annotation
                for (Obstacle obstacles : obstacleList) {
                    //Check if it obstacle in touched.
                    if (obstacles.isTouched(x, y)) {
                        Log.d(TAG, "onDoubleTapEvent: this is touched--->" + obstacles);
                        if(obstacles.getTouchCount() > 5){
                            obstacles.resetTouchCount();
                        } else {
                            obstacles.incrTouchCount();
                        }
                        obstacles.setObsFace(obstacles.getTouchCount());
                        invalidate();
                    }
                }
                setFocusable(true);

                return true;

            }
        };

    }

    public static void canDrag(boolean b) {
        canDrag = b;
    }

    private void init(@Nullable AttributeSet set){
    }

    //Create Cell method
    private void createCells(){
        cells = new Cell[mCols][mRows];
        for (int x = 0; x < mCols; x++) {
            for (int y = 0; y < mRows; y++) {

                cells[x][mRows - y - 1] = new Cell(x * cellSize + (cellSize / 30),
                        y * cellSize + (cellSize / 30),
                        (x + 1) * cellSize - (cellSize / 40),
                        (y + 1) * cellSize - (cellSize / 60), unexploredPaint);

            }
        }
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        int coordinates[];
        float x = event.getX();
        float y = event.getY();

        mGestureDetector.onTouchEvent(event);
        mDoubleTapListener.onSingleTapConfirmed(event);

        //Get touched coordinate
        coordinates = findGridOnTouch(x, y);

        Log.d(TAG, "onTouchEvent: Touched coordinates are " +
                coordinates[0] + " " + coordinates[1]);

        mGestureDetector.setIsLongpressEnabled(true);

        switch (event.getAction()) {
            case MotionEvent.ACTION_DOWN:
                //Touch down code
                Log.d(TAG, "onTouchEvent: ACTION_DOWN");
                if (canDrag) {
                    for (int i = 0; i < obstacleList.length; i++) {
                        if (obstacleList[i].isTouched(x, y) && !obstacleList[i].getActionDown()) {
                            Log.d(TAG, "onTouchEvent: this is touched--->" + obstacleList[i]);
                            Log.d(TAG, "onTouchEvent: Coordinates are " +
                                    coordinates[0] + " " + coordinates[1]);
                            obstacleList[i].setActionDown(true);
                        }
                    }
                }
                isOnClick = true;
                break;
            case MotionEvent.ACTION_MOVE:
                Log.d(TAG, "onTouchEvent: ACTION_MOVE");
                //Touch move code
                for (Obstacle obstacles : obstacleList) {
                    if (obstacles.getActionDown() ) {
                        obstacles.setPosition(x, y);
                        isOnClick = false;
                        invalidate();
                    }
                }
                break;
            case MotionEvent.ACTION_UP:
                Log.d(TAG, "onTouchEvent: ACTION_UP");

                if (!gestureType) {
                    //Touch up code
                    for (Obstacle obstacles : obstacleList) {
                        if (obstacles.getActionDown()) {
                            if (isInArena(coordinates)) {
//                                obstacles.setPosition(cells[coordinates[0]][coordinates[1]].startX, cells[coordinates[0]][coordinates[1]].startY);
                                obstacles.setObsMapCoord(coordinates[0], coordinates[1]);
                                String message = ""+ obstacles.getObsID()+","+  + coordinates[0]+ ","+ coordinates[1];
                                BluetoothConnectionService.sendMessage(message);
                                Log.d("Hello"+coordinates[0], ""+coordinates[1]);
                                obstacles.setActionDown(false);
                                Arena.canDrag(false);
                                invalidate();
                                //Direct message to Main Activity
//                            arena_map.printMessage("ADDOBSTACLE," + obstacles.getObsID() + "," + coordinates[0] + "," + coordinates[1]);

                            } else {
                                // Out of bounce = go back to starting point
                                obstacles.setPosition(obstacles.getInitCoords()[0], obstacles.getInitCoords()[1]);
                                obstacles.setObsMapCoord(-1, -1);
                                obstacles.setActionDown(false);
                                Arena.canDrag(false);
                                invalidate();

                                //Direct message to Main Activity
//                            MainActivity.printMessage("SUBOBSTACLE," + obstacles.getObsID() + "," + coordinates[0] + "," + coordinates[1]);
                            }
                        }
                    }
                }
                else {
                    for (Obstacle obstacles : obstacleList) {
                        if (obstacles.isTouched(x, y) && !obstacles.getActionDown()) {
                            obstacles.setTouchCount(obstacles.getTouchCount()+1);
                            obstacles.setObsFace(obstacles.getTouchCount());
                            invalidate();
                        }
                    }
                }
                break;
        }

        if (setRobotPostition) {
            if (isInArena(coordinates)) {
                if ((coordinates[0] != 0 && coordinates[0] != 19) && (coordinates[1] != 0 && coordinates[1] != 19)) {
                    setCurCoord(coordinates[0], coordinates[1]);

                    invalidate();
                }
            }
        }

        Log.d(TAG, "onTouchEvent: Exiting onTouchEvent");
        //Must be true, else it will only call ACTION_DOWN
        return true;
        //return super.onTouchEvent(event);
    }

    //Draw shapes on the canvas
    @Override
    protected  void onDraw(Canvas canvas){
        super.onDraw(canvas);

        //Background color of the canvas
//        canvas.drawColor(Color.RED);

        //Set width and height of the canvas
        int width = getWidth();
        int height = getHeight();

        Log.d(TAG,"Width and Height: " + width + height);

        //Calculate margin size of canvas
        hMargin = ((width - mCols * cellSize) / 2 - 45);
        vMargin = (height - mRows * cellSize) / 2;

        Log.d(TAG,"Cell size: " + cellSize);

        //Calculate cellsize based on dimensions of the canvas
        if(width/height < mCols/mRows){
            cellSize = width / (mCols + 1);
        } else {
            cellSize = height / (mRows + 1);
        }

        //Create cell
        if(!createCellStatus){
            //Create cell coordincates
            //Log.d(TAG, "onDraw: Creating cells");
            createCells();
            createCellStatus = true;
        }

        //Set Margin
        canvas.translate(hMargin, vMargin);

        drawBorder(canvas);
        drawCell(canvas);
        drawGridNumber(canvas);
        drawRobot(canvas);

        for(Obstacle obstacles : obstacleList) {
            obstacles.drawObj(canvas, obstaclePaint);
            canvas.drawText(obstacles.getTargetID(), obstacles.getObsX() + 9, obstacles.getObsY() + 21, obstacleNumberPaint);
            paintObsFace(canvas);

        }

    }

    //Draw individual cell
    private void drawCell(Canvas canvas){
        //Log.d(TAG, "drawCell(): in drawCell");
        for (int x = 0; x < mCols; x++) {
            for (int y = 0; y < mRows; y++) {
                //Draw cells
                canvas.drawRect(cells[x][y].startX,cells[x][y].startY,cells[x][y].endX,cells[x][y].endY,cells[x][y].paint);
            }
        }
    }

    //Draw border for each cell
    private void drawBorder(Canvas canvas){
        for (int x = 0; x < mCols; x++) {
            for (int y = 0; y < mRows; y++) {
                //Top
                canvas.drawLine(x * cellSize, y * cellSize, (x + 1) * cellSize, y * cellSize, wallPaint);
                //Right
                canvas.drawLine((x + 1) * cellSize, y * cellSize, (x + 1) * cellSize, (y + 1) * cellSize, wallPaint);
                //Left
                canvas.drawLine(x * cellSize, y * cellSize, x * cellSize, (y + 1) * cellSize, wallPaint);
                //Bottom
                canvas.drawLine(x * cellSize, (y + 1) * cellSize, (x + 1) * cellSize, (y + 1) * cellSize, wallPaint);
            }
        }
    }

    //Draw robot on canvas
    private void drawRobot(Canvas canvas) {
        Log.d(TAG,"Drawing Robot");
        int robotCoordinates [] = getCurCoord();
        int x = robotCoordinates[0];
        int y = robotCoordinates[1];
        String direction = getRobotDirection();

        if(x != -1 && y != -1){
            float halfWidth = ((cells[x][y - 1].endX) - (cells[x][y - 1].startX)) / 2;

            //row and col is the middle of the robot
            Log.d(TAG,"drawRobot: Coordinates are= " + x + " , " + y);

            //Draw Robot box
//            canvas.drawRect(cells[x][y].startX, cells[x][y].startY, cells[x][y].endX, cells[x][y].endY, robotPaint);
//            canvas.drawRect(cells[x][y - 1].startX, cells[x][y - 1].startY, cells[x][y - 1].endX, cells[x][y - 1].endY, robotPaint);
//            canvas.drawRect(cells[x + 1][y].startX, cells[x + 1][y].startY, cells[x + 1][y].endX, cells[x + 1][y].endY, robotPaint);
//            canvas.drawRect(cells[x - 1][y].startX, cells[x - 1][y].startY, cells[x - 1][y].endX, cells[x - 1][y].endY, robotPaint);
//            canvas.drawRect(cells[x + 1][y - 1].startX, cells[x + 1][y - 1].startY, cells[x + 1][y - 1].endX, cells[x + 1][y - 1].endY, robotPaint);
//            canvas.drawRect(cells[x - 1][y - 1].startX, cells[x - 1][y - 1].startY, cells[x - 1][y - 1].endX, cells[x - 1][y - 1].endY, robotPaint);
//            canvas.drawRect(cells[x][y + 1].startX, cells[x][y + 1].startY, cells[x][y + 1].endX, cells[x][y + 1].endY, robotPaint);
//            canvas.drawRect(cells[x + 1][y + 1].startX, cells[x + 1][y + 1].startY, cells[x + 1][y + 1].endX, cells[x + 1][y + 1].endY, robotPaint);
//            canvas.drawRect(cells[x - 1][y + 1].startX, cells[x - 1][y + 1].startY, cells[x - 1][y + 1].endX, cells[x - 1][y + 1].endY, robotPaint);

            //Robot direction (Arrow)
            Path path = new Path();
            Log.d(TAG,"Robot direction: " + direction);
            switch (direction){
                case "north":
                    path.moveTo(cells[x][y].startX, cells[x][y].startY + 2*halfWidth);
                    path.lineTo(cells[x][y].startX + ( (int) (2*halfWidth) >> 1),
                            cells[x][y].startY);
                    path.lineTo(cells[x][y].startX + 2*halfWidth, cells[x][y].startY + 2*halfWidth);
                    break;
                case "south":
                    path.moveTo(cells[x][y].startX, cells[x][y].startY);
                    path.lineTo(cells[x][y].startX + ( (int) (2*halfWidth) >> 1),
                            cells[x][y].startY + 2* halfWidth);
                    path.lineTo(cells[x][y].startX + 2*halfWidth, cells[x][y].startY);
                    break;
                case "east":
//                    path.moveTo(cells[x+1][y].startX + (2*halfWidth), cells[x][y].startY + halfWidth); // Top
//                    path.lineTo(cells[x][y].startX, cells[x][y].startY); // Bottom left
//                    path.lineTo(cells[x][y+1].startX, cells[x+1][y+1].startY); // Bottom right
//                    path.lineTo(cells[x+1][y].startX + (2*halfWidth) , cells[x][y].startY + halfWidth); // Back to Top
//                    canvas.drawText("0", cells[x+1][y].startX, cells[x+1][y].startY , obstacleNumberPaint);
//                    canvas.drawText("1", cells[x+1][y+1].startX, cells[x+1][y+1].startY , obstacleNumberPaint);
//                    canvas.drawText("2",cells[x+1][y].startX + (1*halfWidth) , cells[x][y].startY + halfWidth , obstacleNumberPaint);
                    path.moveTo(cells[x][y].startX, cells[x][y].startY);
                    path.lineTo(cells[x][y].startX + 2*halfWidth,
                            cells[x][y].startY + ( (int) (2*halfWidth) >> 1));
                    path.lineTo(cells[x][y].startX, cells[x][y].startY + 2*halfWidth);
                    break;
                case "west":
                    path.moveTo(cells[x][y].startX + halfWidth*2, cells[x][y].startY);
                    path.lineTo(cells[x][y].startX,
                            cells[x][y].startY + ( (int) (2*halfWidth) >> 1));
                    path.lineTo(cells[x][y].startX + halfWidth*2, cells[x][y].startY + 2*halfWidth);
                    break;
            }
            path.close();
            canvas.drawPath(path, directionPaint);

            //After drawing, set drawing to false
            setRobotPostition = false;
            arena_map.setRobotDetails(x, y, direction);
            String message = ""+"ROBOT"+","+x+","+ y+","+direction;
            BluetoothConnectionService.sendMessage(message);
        }
    }

    private void drawObstacle(Canvas canvas){
        Log.d(TAG,"drawObstacle: Drawing obstacle");
        int x, y;
        Paint obsPaint;

        for (Obstacle obstacles : obstacleList) {
            r = new Rect((int)obstacles.getObsX(), (int)obstacles.getObsY(),(int)obstacles.getObsX() + 31, (int)obstacles.getObsY() + 31);
            canvas.drawText(obstacles.getTargetID(), obstacles.getObsX() , obstacles.getObsY(), obstacleNumberPaint);

            canvas.drawRect(r, obstaclePaint);
            canvas.drawText(obstacles.getTargetID(), obstacles.getObsX() + 9, obstacles.getObsY() + 21, obstacleNumberPaint);

        }
        paintObsFace(canvas);

//        canvas.drawLine(obstacle1.getObsX(), obstacle1.getObsY(), obstacle1.getObsX() + 31, obstacle1.getObsY() + 31, linePaint);


//        Log.d(TAG,"--->" + obstacle1.getObsX() + ", " + obstacle1.getObsY());

        //Check if it is within the arena
        //if(setRobotPostition = true){ //LOL this let me move the robot
//        if(obsRow != -1 && obsCol != -1) {
//            //Redraw all obstacles and newly added obstacle
//            for(int i = 0; i < obstacleList.size(); i++){
//
//                //Check if obstacle already exist
//                x = (int) obstacleList.get(i).getObsX();
//                y = (int) obstacleList.get(i).getObsY();
//                obsPaint = obstacleList.get(i).getObsPaint();
//
//                canvas.drawRect(cells[x][y].startX, cells[x][y].startY, cells[x][y].endX, cells[x][y].endY, obsPaint);
//                canvas.drawText(obstacleList.get(i).getTargetID(), cells[x][y].startX, cells[x][y].endY, obstacleNumberPaint);
//
//            }
//        }
//        setObstaclePosition = false;
//        canDrawObstacle = false;
    }


//    private void drawDigit(Canvas canvas) {
//        String text = obstacle1.getTargetID();
////        float textWidth = obstacleNumberPaint.measureText(text);
//
//        canvas.getClipBounds(r);
//        int mHeight = r.height();
//        int mWidth = r.width();
//
//        obstacleNumberPaint.getTextBounds(text, 0, text.length(), r);
//
//        float x = mWidth / 2f - r.width() / 2f - r.left;
//        float y = mHeight / 2f + r.height() / 2f - r.bottom;
//
//        Log.d(TAG,"DRAWDIGIT: " + x +", " + y);
//
//        canvas.drawText(text, x, y, obstacleNumberPaint);
//        drawTextBounds(canvas, (int)x, (int)y);
//    }
//
//    private void drawTextBounds(Canvas canvas, int x, int y) {
//        Paint rPaint = new Paint();
//        RectF bounds = new RectF(r);
//        rPaint.setColor(Color.TRANSPARENT);
//        rPaint.setStyle(Paint.Style.STROKE);
//        r.offset(x, y);
//        canvas.drawRect(r, rPaint);
//    }

    //Draw numbers
    private void drawGridNumber(Canvas canvas) {
        //Row
        for (int x = 0; x < 20; x++) {
            if(x >9 && x <20){
                canvas.drawText(Integer.toString(x), cells[x][0].startX + (cellSize / 5), cells[x][0].endY + (cellSize / 1.5f), gridNumberPaint);
            } else {
                canvas.drawText(Integer.toString(x), cells[x][0].startX + (cellSize / 3), cells[x][0].endY + (cellSize / 1.5f), gridNumberPaint);
            }
        }
        //Column
        for (int x = 0; x <20; x++) {
            if(x >9 && x <20){
                canvas.drawText(Integer.toString(x), cells[0][x].startX - (cellSize / 1.2f), cells[0][x].endY - (cellSize / 3.5f), gridNumberPaint);
            } else {
                canvas.drawText(Integer.toString(x), cells[0][x].startX - (cellSize / 1.5f), cells[0][x].endY - (cellSize / 3.5f), gridNumberPaint);
            }
        }
    }

    //Inverting rows
    private int inverseCoordinates(int y){
        return (19 - y);
    }

    public int getXCoord(){
        return curCoord[0];
    }

    public int getYCoord(){
        return inverseCoordinates(curCoord[1]);
    }

    public void updateMap(String message) {
        Log.d(TAG,"updateMap: Updating Map!");

        String receivedMessage [] = message.split(",");
        String item = receivedMessage[0];
        int x,y;
        String obsID, targetID;
        String direction;

        switch (item){
            case "TARGET":
                //Update obstacle by displaying image ID
                obsID = receivedMessage[1];
                targetID = receivedMessage[2];

                updateTargetText(obsID, targetID);
                break;
            case "ROBOTPOSITION":
                //Get new robot position
                x = Integer.valueOf(receivedMessage[1]) + 1;
                y = Integer.valueOf(receivedMessage[2]) + 1;
                direction = receivedMessage[3];

                Log.d(TAG, "New coordinates: " + x + "," + y);
                Log.d(TAG, "Direction " + direction);


                break;
            case "ADDOBSTACLE":
                //Get new robot position
                break;
            case "REMOVEOBSTACLE:":
                //Get new robot position
                break;
        }
    }

    private void updateTargetText(String obsID, String targetID) {
        //Go through list of obstacles
        String ID;
        for (Obstacle obstacles : obstacleList) {
            ID = obstacles.getObsID();
            if(ID.equals(obsID)){
                Log.d(TAG,"obsID: " + obsID);
                Log.d(TAG,"targetID: " + targetID);
                obstacles.setTargetID(targetID);
            }
        }
        invalidate();
    }

    //Resetting Arena by resetting everything
    public void resetArena(){
        Log.d("HERE", "I'm Here");
        curCoord = new int [] {-1, -1};
        createCellStatus = false;
        setRobotPostition = false;
        setObstaclePosition = false;
        validPosition = false;
        canDrawRobot = false;
        canDrawObstacle = false;
        canUpdateObsFace = false;

        setStartingPoint(false);
        arena_map.setRobotDetails(-1, -1, "west");
        for (Obstacle obstacles : obstacleList) {
            obstacles.setPosition(obstacles.getInitCoords()[0], obstacles.getInitCoords()[1]);
        }

        invalidate();
    }

    private ArrayList<int[]> getObstacleCoord() {
        return obstacleCoord;
    }

    private boolean isInArena(int touchedCoord []){
        //Check if coordinates is within the Arena
        Log.d(TAG,"isInArena: Check if touched coordinates is within the Arena");
        boolean isInArena = false;

        //If in Arena, return true
        if (touchedCoord[0] != -1 && touchedCoord[1] != -1) {
            isInArena = true;
        }

        return isInArena;
    }

    /**
     * Change color of the obstacle to indicate face of the image
     * Black: Default, Green: Left, Red: Right, Yellow: Down, Blue: Front
     * Need to attach count to the object
     *
     * @return*/

    public void paintObsFace(Canvas canvas){
        //Paint newPaint = new Paint();
//        int x, y;
        String obsFace;
        for (Obstacle obstacles : obstacleList) {
            obsFace = obstacles.getObsFace();
            switch (obsFace){
                case "West":
                    //Green: Left (West)
//                    obstacleList.get(i).setObsPaint(westPaint);
//                    MainActivity.printMessage("FACE,W");
                    //Left = "West"
                    canvas.drawLine(obstacles.getObsX() + 3f, obstacles.getObsY() , obstacles.getObsX() + 3f, obstacles.getObsY() + 31, linePaint);
                    break;

                case "East":
                    //Red: Right
//                    obstacleList.get(i).setObsPaint(eastPaint);
//                    MainActivity.printMessage("FACE,E");
                    //Right = "East"
                    canvas.drawLine(obstacles.getObsX() + 28, obstacles.getObsY() , obstacles.getObsX() + 28, obstacles.getObsY() + 31, linePaint);
                    break;

                case "South":
                    //Yellow: Down
//                    obstacleList.get(i).setObsPaint(northPaint);
//                    MainActivity.printMessage("FACE,S");
                    //Bottom = "South"
                    canvas.drawLine(obstacles.getObsX(), obstacles.getObsY() + 29, obstacles.getObsX() + 31, obstacles.getObsY() + 29, linePaint);
                    break;

                case "North":
                    //Blue: Front
//                    obstacleList.get(i).setObsPaint(southPaint);
//                    MainActivity.printMessage("FACE,N");
                    //Top = "North"
                    canvas.drawLine(obstacles.getObsX(), obstacles.getObsY() + 2.2f, obstacles.getObsX() + 31, obstacles.getObsY() + 2.2f, linePaint);
                    break;

                default:
                    //Black

                    break;

            }
        }
        canUpdateObsFace = false;
    }


    //Find coordinates of cell in arena
    public static int[] findGridOnTouch(float x, float y) {
        int row = -1, cols = -1;
        //FIND COLS OF THE MAZE BASED ON ONTOUCH
        for (int i = 0; i < mCols; i++) {
            if (cells[i][0].endX >= (x - hMargin) && cells[i][0].startX <= (x - hMargin)) {
                cols = i;
                //Log.d(TAG, "cols = " + cols);
                break;
            }
        }
        //FIND ROW OF THE MAZE BASED ON ONTOUCH
        for (int j = 0; j < mRows; j++) {
            if (cells[0][j].endY >= (y - vMargin) && cells[0][j].startY <= (y - vMargin)) {
                row = j;
                //Log.d(TAG, "row = " + row);
                break;
            }
        }
        return new int[]{cols, row};
    }

    //Get current robot Coordinates
    public int[] getCurCoord(){
        return curCoord;
    }

    public void setRobotDirection(String direction){
        Log.d(TAG,"setRobotDirection");
        if(direction.equals("N")){
            robotDirection = "north";
        } else if (direction.equals("E")){
            robotDirection = "east";
        } else if (direction.equals("S")) {
            robotDirection = "south";
        } else if (direction.equals("W")){
            robotDirection = "west";
        }
        Log.d(TAG,robotDirection);
    }

    public String getRobotDirection(){
        return robotDirection;
    }

    //Allow user to set Robot position
    public void setStartingPoint(boolean status){
        canDrawRobot = true;
        setRobotPostition = status;
    }

//    //Ensuring that the number of obstacles does not go beyond 5
//    public void addObstacles(boolean status){
//         Log.d(TAG,"addObstacles enter");
//         if(obstacleList.size() == maxObs){
//             setObstaclePosition = false;
//         } else {
//             setObstaclePosition = status;
//             //addDroppedObstacle();
//         }
//    }



    public void setCurCoord(int col, int row) {
        Log.d(TAG,"Entering setCurCoord");
        curCoord[0] = col;
        curCoord[1] = row;

        Log.d(TAG, col + "," + row);

        for (int x = col - 1; x <= col + 1; x++)
            for (int y = curCoord[1] - 1; y <= curCoord[1] + 1; y++)
                cells[x][y].setType("robot");
        Log.d(TAG,"Exiting setCurCoord");
    }

    private class Cell {
        float startX, startY, endX, endY;
        Paint paint;
        String type;

        private Cell(float startX, float startY, float endX, float endY, Paint paint){
            this.startX = startX;
            this.startY = startY;
            this.endX = endX;
            this.endY = endY;
            this.paint = paint;
        }

        public void setPaint(Paint paint){
            this.paint = paint;
        }

        public void setType(String type) {
            this.type = type;
            switch (type) {
                case "obstacle":
                    this.paint = obstaclePaint;
                    break;
                case "robot":
                    this.paint = robotPaint;
                    break;
                case "unexplored":
                    this.paint = unexploredPaint;
                    break;
                case "explored":
                    this.paint = exploredPaint;
                    break;
                case "arrow":
                    this.paint = directionPaint;
                    break;
                case "id":
                    this.paint = obstacleNumberPaint;
                    break;
                default:
                    Log.d(TAG,"setTtype default: " + type);
                    break;
            }
        }
    }

    public void setRobotLocation(int column, int row, String direction) {
//        resetArena();
        robotDirection = direction;
        setCurCoord(column, row);
        invalidate();
    }

    public void setBlockId(String id, String target) {
        for(Obstacle obstacles : obstacleList)
            if (obstacles.obsID == id)
                obstacles.setTargetID(target);
            invalidate();

    }
}