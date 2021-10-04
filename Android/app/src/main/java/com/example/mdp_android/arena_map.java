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
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.text.method.ScrollingMovementMethod;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;

import com.example.mdp_android.Arena.Arena;
import com.example.mdp_android.Arena.Obstacle;


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
    BluetoothConnectionService mBluetoothConnection;
    ProgressDialog myDialog;


    @Override
    protected void onCreate (Bundle savedInstanceState) {

        //Initialization
        super.onCreate(savedInstanceState);
        setContentView(R.layout.arena_map);

        //Get broadcasted msg
        LocalBroadcastManager.getInstance(this).registerReceiver(messageReceiver, new IntentFilter("incomingMessage"));
        mBluetoothConnection = new BluetoothConnectionService(arena_map.this);
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
        Button fastConnectButton = findViewById(R.id.fastConnectButton);
        Button rotateButton = findViewById(R.id.rotate);

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
                Log.d(TAG,"start button called");
                BluetoothConnectionService.sendMessage(Arena.sendArenaInformation());
            }
        });

        fastConnectButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mBluetoothConnection.fastConnect();
            }
        });

        rotateButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Log.d(TAG,"rotate button called");
                Arena.canRotate = !Arena.canRotate;
                if (Arena.canRotate)
                    rotateButton.setText("rotate:true");
                else
                    rotateButton.setText("rotate:false");
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
//                reconnectionHandler.postDelayed(reconnectionRunnable, 5000);
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
            if (message.charAt(0) == '(')
                handleData(message);
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

    public void handleData(String message) {
        AsyncTask.execute(new Runnable() {
            @Override
            public void run() {
//                String message = "(df0456,1.266,2.009,1.059),(w1471,4.758,8.231,1.059),(df1400,7.544,9.016,5.771),(ar0944,6.500,10.800,4.712)|(ar1509,8.796,12.831,3.019),(dr0219,9.295,12.831,3.265),(af1290,7.500,10.800,4.712)|(df0845,6.651,9.141,3.764),(ar0938,8.694,9.340,2.712),(df1017,7.500,11.200,1.571)|(dr0245,7.576,10.647,1.846),(af0652,6.707,11.817,2.578),(dr0502,7.800,11.500,3.142)";
                String[] messages = message.split("\\|");
                String main = "";
                for (String part: messages) {
                    part = part.replaceAll(" ", "");
                    part = part.replaceAll("\\),\\(", "-");

                    String[] instructions = part.split("-");
//                    Log.d(TAG, part);


                    for (String instruction : instructions) {
                        instruction = part.substring(1);
                        instruction = instruction.replaceAll("\\(", "");
                        instruction = instruction.replaceAll("\\)", "");
//                        Log.d(TAG, instruction);

                        String[] i = instruction.split("-");
                        for (String commands : i) {
//                            Log.d(TAG, commands);
                            String[] command = commands.split(",");
                            String time = command[0];
                            time = time.replaceAll("\\D+","");
                            int x = (int) Double.parseDouble(command[1]);
                            int y = (int) Double.parseDouble(command[2]);
                            int angle = (int) Math.toDegrees(Double.parseDouble(command[3]));
                            main += "(" + x +"," + y  +"," + angle + "," + time + ")";
//                            Log.d(""+angle, ""+x+" "+y);
                        }
                        main += ";";
                        break;
                    }
                }
                Log.d(TAG, main);
                String[] commands_set = main.split(";");
                for (String commands: commands_set) {
                    String[] command = commands.split("\\)\\(");
                    for (String c: command) {
                        c = c.replace("(", "");
                        c = c.replace(")", "");
                        String[] i = c.split(",");
                        int x = Integer.parseInt(i[0]);
                        int y = Integer.parseInt(i[1]);
                        int angle = Integer.parseInt(i[2]);
                        i[3] = i[3].replaceAll(";", "");
                        int time = Integer.parseInt(i[3]);


                        Log.d(TAG, ""+x +" "+y + " "+ angle + " "+ time);
                        String direction = "";
                        if ((angle >=0 && angle <= 45) || angle >= 315 && angle <= 360)
                            direction = "east";
                        else if (angle >=45 && angle <= 135)
                            direction = "north";
                        else if (angle >=135 && angle <= 225)
                            direction = "west";
                        else
                            direction = "south";
                        arenaMap.setRobotLocation(x, y, direction);
                        try {
                            Thread.sleep(time);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }

                    }
                    try {
                        Thread.sleep(10000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                }


            }
        });

    }
}