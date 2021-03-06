package com.example.mdp_android;

import android.content.BroadcastReceiver;
import android.content.ClipData;
import android.content.ClipDescription;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Point;
import android.graphics.drawable.ColorDrawable;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;

import java.nio.charset.Charset;

public class interactive_control extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.interactive_control_layout);
        Button foward_button = findViewById(R.id.button4);
        Button reverse_button = findViewById(R.id.button5);
        Button left_button = findViewById(R.id.button6);
        Button right_button = findViewById(R.id.button7);
        Button rotate_left_button = findViewById(R.id.button9);
        Button rotate_right_button = findViewById(R.id.button8);
        TextView showReceived = findViewById(R.id.showReceived);
        BroadcastReceiver messageReceiver = new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                String message = intent.getStringExtra("receivedMessage");
                showReceived.setText(message);
            }
        };
        LocalBroadcastManager.getInstance(this).registerReceiver(messageReceiver, new IntentFilter("incomingMessage"));
        foward_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String message = "f";
                if (BluetoothConnectionService.BluetoothConnectionStatus == true) {
                    byte[] bytes = message.getBytes(Charset.defaultCharset());
                    BluetoothConnectionService.write(bytes);
                }
            }
        });

        reverse_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String message = "r";
                if (BluetoothConnectionService.BluetoothConnectionStatus == true) {
                    byte[] bytes = message.getBytes(Charset.defaultCharset());
                    BluetoothConnectionService.write(bytes);
                }
            }
        });

        left_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String message = "sl";
                if (BluetoothConnectionService.BluetoothConnectionStatus == true) {
                    byte[] bytes = message.getBytes(Charset.defaultCharset());
                    BluetoothConnectionService.write(bytes);
                }
            }
        });

        right_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String message = "sr";
                if (BluetoothConnectionService.BluetoothConnectionStatus == true) {
                    byte[] bytes = message.getBytes(Charset.defaultCharset());
                    BluetoothConnectionService.write(bytes);
                }
            }
        });

        rotate_left_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String message = "tl";
                if (BluetoothConnectionService.BluetoothConnectionStatus == true) {
                    byte[] bytes = message.getBytes(Charset.defaultCharset());
                    BluetoothConnectionService.write(bytes);
                }
            }
        });

        rotate_right_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String message = "tr";
                if (BluetoothConnectionService.BluetoothConnectionStatus == true) {
                    byte[] bytes = message.getBytes(Charset.defaultCharset());
                    BluetoothConnectionService.write(bytes);
                }
            }
        });
//        right_button.setTag("right_button");
//        // Sets a long click listener for the ImageView using an anonymous listener object that
//// implements the OnLongClickListener interface
//        right_button.setOnLongClickListener(new View.OnLongClickListener() {
//
//            // Defines the one method for the interface, which is called when the View is long-clicked
//            public boolean onLongClick(View v) {
//
//                // Create a new ClipData.
//                // This is done in two steps to provide clarity. The convenience method
//                // ClipData.newPlainText() can create a plain text ClipData in one step.
//
//                // Create a new ClipData.Item from the ImageView object's tag
//                ClipData.Item item = new ClipData.Item((String)v.getTag());
//
//                // Create a new ClipData using the tag as a label, the plain text MIME type, and
//                // the already-created item. This will create a new ClipDescription object within the
//                // ClipData, and set its MIME type entry to "text/plain"
//                ClipData dragData = new ClipData(
//                        (String)v.getTag(),
//                        new String[] { ClipDescription.MIMETYPE_TEXT_PLAIN },
//                        item);
//
//                // Instantiates the drag shadow builder.
//                View.DragShadowBuilder myShadow = new MyDragShadowBuilder(right_button);
//
//                // Starts the drag
//
//                v.startDrag(dragData,  // the data to be dragged
//                        myShadow,  // the drag shadow builder
//                        null,      // no need to use local data
//                        0          // flags (not currently used, set to 0)
//                );
//                return true;
//            }
//        });

    }


//    private static class MyDragShadowBuilder extends View.DragShadowBuilder {
//
//        // The drag shadow image, defined as a drawable thing
//        private static Drawable shadow;
//
//        // Defines the constructor for myDragShadowBuilder
//        public MyDragShadowBuilder(View v) {
//
//            // Stores the View parameter passed to myDragShadowBuilder.
//            super(v);
//
//            // Creates a draggable image that will fill the Canvas provided by the system.
//            shadow = new ColorDrawable(Color.LTGRAY);
//        }
//
//        // Defines a callback that sends the drag shadow dimensions and touch point back to the
//        // system.
//        @Override
//        public void onProvideShadowMetrics (Point size, Point touch) {
//            // Defines local variables
//            int width, height;
//
//            // Sets the width of the shadow to half the width of the original View
//            width = getView().getWidth() / 2;
//
//            // Sets the height of the shadow to half the height of the original View
//            height = getView().getHeight() / 2;
//
//            // The drag shadow is a ColorDrawable. This sets its dimensions to be the same as the
//            // Canvas that the system will provide. As a result, the drag shadow will fill the
//            // Canvas.
//            shadow.setBounds(0, 0, width, height);
//
//            // Sets the size parameter's width and height values. These get back to the system
//            // through the size parameter.
//            size.set(width, height);
//
//            // Sets the touch point's position to be in the middle of the drag shadow
//            touch.set(width / 2, height / 2);
//        }
//
//        // Defines a callback that draws the drag shadow in a Canvas that the system constructs
//        // from the dimensions passed in onProvideShadowMetrics().
//        @Override
//        public void onDrawShadow(Canvas canvas) {
//
//            // Draws the ColorDrawable in the Canvas passed in from the system.
//            shadow.draw(canvas);
//        }
//    }

}

