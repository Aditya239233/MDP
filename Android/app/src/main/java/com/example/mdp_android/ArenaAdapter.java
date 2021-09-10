package com.example.mdp_android;

import android.content.ClipData;
import android.content.Context;
import android.util.Log;
import android.view.GestureDetector;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import java.util.ArrayList;

public class ArenaAdapter extends ArrayAdapter<Arena> {
    private GestureDetector gestureDetector;
    private static final String TAG = "Inside ArenaAdapter";
    public ArenaAdapter(@NonNull Context context, ArrayList<Arena> courseModelArrayList) {
        super(context, 0, courseModelArrayList);
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        gestureDetector = new GestureDetector(getContext(), new SingleTapConfirm2());
        View listitemView = convertView;
        if (listitemView == null) {
            // Layout Inflater inflates each item to be displayed in GridView.
            listitemView = LayoutInflater.from(getContext()).inflate(R.layout.card_item, parent, false);
        }
        Arena arena = getItem(position);
        ImageView block = listitemView.findViewById(R.id.idVBlock);
        block.setImageResource(arena.getImgid());
        block.setOnTouchListener(new MyTouchListener());
        block.setOnLongClickListener(new View.OnLongClickListener() {

            @Override
            public boolean onLongClick(View view) {
                ClipData data = ClipData.newPlainText("", "");
                View.DragShadowBuilder shadowBuilder = new View.DragShadowBuilder(
                        view);
                view.startDrag(data, shadowBuilder, view, 0);
                return true;
            }
        });
        return listitemView;
    }

    private final class MyTouchListener implements View.OnTouchListener {
        public boolean onTouch(View view, MotionEvent motionEvent) {
            if (gestureDetector.onTouchEvent(motionEvent)) {
                view.setRotation(view.getRotation() + 90);
                Log.d(TAG, "rotation : " + view.getRotation());
                return true;
            }
//            else if (motionEvent.getAction() == MotionEvent.ACTION_DOWN){
//                ClipData data = ClipData.newPlainText("", "");
//                DragShadowBuilder shadowBuilder = new View.DragShadowBuilder(
//                        view);
//                view.startDrag(data, shadowBuilder, view, 0);
//                return true;
//            }
            return false;
        }
    }

    private class SingleTapConfirm2 extends GestureDetector.SimpleOnGestureListener {
        @Override
        public boolean onSingleTapUp(MotionEvent event) {
            return true;
        }
    }


}