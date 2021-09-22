package com.example.mdp_android;

import android.app.Activity;
import android.app.ProgressDialog;
import android.bluetooth.BluetoothDevice;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.text.method.ScrollingMovementMethod;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;

import com.example.mdp_android.Arena.Arena;


import java.nio.charset.Charset;

/** Main Activity:
 *  Will receive details like messages from chat, sending messages to RPI
 *  connStatusTextView, BT status will be shared onto MainActivity and across the whole app
 *  through sharedPreferences
 */

public class arena_map extends AppCompatActivity {
    private static final String TAG = "ARENA MAP";

    // Declare Variables
    private static SharedPreferences sharedPreferences;
    private static SharedPreferences.Editor editor;
    private static Context context;
    private TextView statusBox;
    private static Arena arenaMap;
    static TextView txtRobotDirection, txtRobotCoord;
    ProgressDialog myDialog;



    @Override
    protected void onCreate (Bundle savedInstanceState) {

        //Initialization
        super.onCreate(savedInstanceState);
        setContentView(R.layout.arena_map);

        //Get broadcasted msg
        LocalBroadcastManager.getInstance(this).registerReceiver(messageReceiver, new IntentFilter("incomingMessage"));

        //sharedPreferences set up
        arena_map.context = getApplicationContext();
        statusBox = findViewById(R.id.statusBox);
        statusBox.setMovementMethod(new ScrollingMovementMethod());
        this.sharedPreferences();
        editor.putString("message", "");
        editor.putString("direction","None");
        editor.putString("connStatus", "Disconnected");
        editor.commit();

        //Arena map
        arenaMap = new Arena(this);
        arenaMap = findViewById(R.id.mapView);
        txtRobotCoord = findViewById(R.id.txtRobotPosition);
        txtRobotDirection = findViewById(R.id.txtRobotDirection);

        //Process Dialog
        myDialog = new ProgressDialog(arena_map.this);
        myDialog.setMessage("Waiting for other device to reconnect...");
        myDialog.setCancelable(false);
        myDialog.setButton(DialogInterface.BUTTON_NEGATIVE, "Cancel", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.dismiss();
            }
        });

        Button set_robot = findViewById(R.id.button10);
        Button reset_map = findViewById(R.id.button11);
        Button startButton = findViewById(R.id.startButton);

        reset_map.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view){
                Arena tempArenaMap = arena_map.getArenaMap();
                tempArenaMap.resetArena();
            }
        });

        set_robot.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Arena tempArenaMap = arena_map.getArenaMap();
                tempArenaMap.setStartingPoint(true);
            }
        });

        startButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

            }
        });
    }


    private static void showLog(String message) {
        Log.d(TAG, message);
    }

    public static void sharedPreferences() {
        sharedPreferences = arena_map.getSharedPreferences(arena_map.context);
        editor = sharedPreferences.edit();
    }

    private static SharedPreferences getSharedPreferences(Context context){
        return context.getSharedPreferences("Shared Preferences", Context.MODE_PRIVATE);
    }

//    @Override
//    protected void onActivityResult(int requestCode, int resultCode, Intent data){
//        super.onActivityResult(requestCode, resultCode, data);
//
//        switch (requestCode){
//            case 1:
//                if(resultCode == Activity.RESULT_OK){
//                    mBTDevice = (BluetoothDevice) data.getExtras().getParcelable("mBTDevice");
//                    myUUID = (UUID) data.getSerializableExtra("myUUID");
//                }
//        }
//    }

    // Send message to bluetooth
    public static void printMessage(String message) {
        showLog("Entering printMessage");
        editor = sharedPreferences.edit();

        if (BluetoothConnectionService.BluetoothConnectionStatus == true) {
            byte[] bytes = message.getBytes(Charset.defaultCharset());
            BluetoothConnectionService.write(bytes);
        }
        showLog(message);
//        editor.putString("message", ChatFragment.getMessageReceivedTextView().getText() + "\n" + message);
        editor.commit();
        refreshMessageReceived();
    }

    public static void refreshMessageReceived() {
        String received = sharedPreferences.getString("message", "");
//        ChatFragment.getMessageReceivedTextView().setText(sharedPreferences.getString("message", ""));
    }

    private BroadcastReceiver mBroadcastReceiver5 = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            Log.d(TAG,"BroadcastReceiver 5: ");

            BluetoothDevice mDevice = intent.getParcelableExtra("Device");
            String status = intent.getStringExtra("Status");
            sharedPreferences();

            if(status.equals("connected")){
                try {
                    myDialog.dismiss();
                } catch(NullPointerException e){
                    e.printStackTrace();
                }

                Log.d(TAG, "mBroadcastReceiver5: Successfully connected to "+mDevice.getName());
                Toast.makeText(arena_map.this, "Successfully connected to "+mDevice.getName(), Toast.LENGTH_LONG).show();
                editor.putString("connStatus", "Connected to " + mDevice.getName());

            }
            else if(status.equals("disconnected")){
                Log.d(TAG, "mBroadcastReceiver5: Disconnected from "+mDevice.getName());
                Toast.makeText(arena_map.this, "Disconnected from "+mDevice.getName(), Toast.LENGTH_LONG).show();
                editor.putString("connStatus", "Disconnected");
                myDialog.show();
            }
            editor.commit();
        }
    };

    BroadcastReceiver messageReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            String message = intent.getStringExtra("receivedMessage");
            statusBox.append(message+"\n");
            String[] parts = message.split(",");
            String type = parts[0];
            switch(type)
            {
                case "TARGET":
                {
                    Log.d(TAG,"Interpreting TARGET message");
                    try {
                        String obsID = parts[1];
                        String targetID = parts[2];
                        arenaMap.setBlockId(obsID,targetID);
                        // your code here
                    }catch(Exception e)
                    {
                        Log.d(TAG,"Invalid message");
                        e.printStackTrace();
                    }
                }
                case "ROBOT":
                {
                    Log.d(TAG,"Interpreting ROBOT message");
                    try {
                        int x = Integer.parseInt(parts[1]);
                        int y = Integer.parseInt(parts[2]);
                        String direction = parts[3];
                        arenaMap.setRobotLocation(x,y,direction);
                        // your code here
                    }catch(Exception e)
                    {
                        Log.d(TAG,"Invalid message");
                        e.printStackTrace();
                    }
                }
                case "INSTRUCTIONS":
                {
                    Log.d(TAG,"Interpreting ROBOT message");
                    // your code here
                }
                default:
                {
                    Log.d(TAG,"Invalid format: unable to recognize message type");
                }
            }
            arenaMap.updateMap(message);
            sharedPreferences();
            String receivedText = sharedPreferences.getString("message", "") + "\n" + message;
            editor.putString("message", receivedText);
            editor.commit();
            refreshMessageReceived();
        }
    };

    public static Arena getArenaMap(){
        return arenaMap;
    }

    public static void setRobotDetails(int x, int y, String direction){
        Log.d(TAG, "setRobotDetails: Getting current robot coordinates");

        if (x == -1 && y == -1) {
            txtRobotCoord.setVisibility(View.INVISIBLE);
            txtRobotDirection.setVisibility(View.INVISIBLE);
        } else {
            txtRobotCoord.setText(String.valueOf(x) + "," +
                    String.valueOf(y));
            txtRobotDirection.setText(direction);
        }
    }

    @Override
    protected void onDestroy(){
        super.onDestroy();
        try{
            LocalBroadcastManager.getInstance(this).unregisterReceiver(messageReceiver);
            LocalBroadcastManager.getInstance(this).unregisterReceiver(mBroadcastReceiver5);
        } catch(IllegalArgumentException e){
            e.printStackTrace();
        }
    }

    @Override
    protected void onPause(){
        super.onPause();
        try{
            LocalBroadcastManager.getInstance(this).unregisterReceiver(mBroadcastReceiver5);
        } catch(IllegalArgumentException e){
            e.printStackTrace();
        }
    }

    @Override
    protected void onResume(){
        super.onResume();
        try{
            IntentFilter filter2 = new IntentFilter("ConnectionStatus");
            LocalBroadcastManager.getInstance(this).registerReceiver(mBroadcastReceiver5, filter2);
        } catch(IllegalArgumentException e){
            e.printStackTrace();
        }
    }

    @Override
    public void onSaveInstanceState(Bundle outState) {
        showLog("Entering onSaveInstanceState");
        super.onSaveInstanceState(outState);

        outState.putString(TAG, "onSaveInstanceState");
        showLog("Exiting onSaveInstanceState");
    }
}