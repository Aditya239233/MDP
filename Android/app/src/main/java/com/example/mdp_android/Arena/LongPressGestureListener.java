package com.example.mdp_android.Arena;

import android.util.Log;
import android.view.GestureDetector;
import android.view.MotionEvent;
import android.view.View;

import androidx.core.view.MotionEventCompat;
import static com.example.mdp_android.Arena.Arena.findGridOnTouch;


public class LongPressGestureListener extends GestureDetector.SimpleOnGestureListener {

    @Override
    public boolean onSingleTapUp(MotionEvent event) {
        Log.d("", "Single Tap");
        Arena.gestureType = true;
        return true;
    }

    @Override
    public boolean onDoubleTap(MotionEvent e) {
        super.onLongPress(e);
        Log.d("TAG","onLongPress: LONG PRESS!");
        Arena.gestureType = false;
        Arena.setObstaclePosition = true;
        // e will give you the location and everything else you want
        // This is where you will be doing whatever you want to.
        int eIndex = MotionEventCompat.getActionIndex(e);
        float eX = MotionEventCompat.getX(e, eIndex);
        float eY = MotionEventCompat.getY(e, eIndex);
        int coordinates [] = findGridOnTouch(eX,eY);

        Log.d("TAG","X:Y = " + eX + " : " + eY);
//        Log.d("TAG","X:Y = " + coordinates[0] + " : " + coordinates[1]);

        Log.d("onLongPress","can Drag");
        Arena.canDrag(true);

        return true;
    }

    @Override
    public boolean onDown(MotionEvent e) {

//        Arena.canDrag(false);
        return false;
    }
}
