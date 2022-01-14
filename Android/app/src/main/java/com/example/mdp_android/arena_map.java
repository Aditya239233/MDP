package com.example.mdp_android;
import java.util.concurrent.TimeUnit;
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
    public boolean canRecieve = true;

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
                if (Arena.canRotate) {
                    if (tempArenaMap.getRobotDirection().toUpperCase().charAt(0) == 'N')
                        tempArenaMap.setRobotDirection("W");
                    else if (tempArenaMap.getRobotDirection().toUpperCase().charAt(0) == 'W')
                        tempArenaMap.setRobotDirection("S");
                    else if (tempArenaMap.getRobotDirection().toUpperCase().charAt(0) == 'S')
                        tempArenaMap.setRobotDirection("E");
                    else if (tempArenaMap.getRobotDirection().toUpperCase().charAt(0) == 'E')
                        tempArenaMap.setRobotDirection("N");
                }
                else {

                    tempArenaMap.resetArena();
                }
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
//                handleData("");
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
            int index;
            switch(type)
            {
                case "TARGET":
                {
                    Log.d(TAG,"Interpreting TARGET message");
                    try {
                        String obsID = parts[1];
                        String targetID = parts[2];
                        if (targetID.contains("TARGET"))
                            if (targetID.indexOf("T") != 0) {
                                index = targetID.indexOf("T");
                                targetID = targetID.substring(0, index);
                            }

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
            try {
                if (message.charAt(0) == '(' && canRecieve) {
                    handleData(message);
                    canRecieve = false;
                }
            }
            catch (Exception e) {
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

    public void handleData(String message) {
        AsyncTask.execute(new Runnable() {
            @Override
            public void run() {
//                String message = "(w1500,1.000,8.500,1.571),(af0238,0.939,9.000,1.815),(w0599,0.214,11.906,1.815),(df0675,0.398,13.371,1.081),(w0177,0.814,14.151,1.081),(df1400,3.583,14.995,5.793),(ar0973,2.500,16.800,4.712)|(ar1911,5.663,18.515,2.569),(s0079,5.994,18.301,2.569),(dr1401,8.825,18.906,4.141),(af0519,8.500,17.800,4.712)|(df0040,8.500,17.795,4.712),(w0199,8.500,16.800,4.712),(df0260,8.441,16.310,4.466),(ar2735,12.440,15.451,1.397),(s1016,11.562,10.447,1.397),(ar2645,7.500,10.800,4.712)|(af1692,10.196,8.859,0.327),(dr0603,9.154,8.062,0.981),(af0536,9.500,9.200,1.571)|(df1510,11.806,11.230,6.159),(w1057,17.051,10.577,6.159),(df2690,16.800,6.500,3.142)";
                String[] messages = message.split("\\|");
                String main = "";
                Log.d(TAG,message);
                for (String part: messages) {
                    part = part.replaceAll(" ", "");
                    part = part.replaceAll("\\),\\(", "_");

                    String[] instructions = part.split("_");
//                    Log.d(TAG, part);


                    for (String instruction : instructions) {
                        instruction = part.substring(1);
                        instruction = instruction.replaceAll("\\(", "");
                        instruction = instruction.replaceAll("\\)", "");
//                        Log.d(TAG, instruction);

                        String[] i = instruction.split("_");
                        for (String commands : i) {
//                            Log.d(TAG, commands);
                            String[] command = commands.split(",");
                            String time = command[0];
                            time = time.replaceAll("\\D+","");
                            Log.d(TAG, commands);
;                           int x = (int) Double.parseDouble(command[1]);
                            int y = (int) Double.parseDouble(command[2]);
                            if (x < 0)
                                x = 0;
                            if (y < 0)
                                y = 0;
                            if (x > 19)
                                x = 19;
                            if (y > 19)
                                y = 19;
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
                try {
                    TimeUnit.SECONDS.sleep(1);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
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
                        try {
                            TimeUnit.MILLISECONDS.sleep(1750);
                            TimeUnit.MILLISECONDS.sleep(time);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                        arenaMap.setRobotLocation(x, y, direction);

                    }
                    try {
//                        Thread.sleep(10000);
                        TimeUnit.SECONDS.sleep(11);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                }


            }
        });

    }
}