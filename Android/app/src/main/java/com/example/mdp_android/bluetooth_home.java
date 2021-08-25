package com.example.mdp_android;

import androidx.appcompat.app.AppCompatActivity;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;

import android.app.ProgressDialog;
import android.bluetooth.BluetoothDevice;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.nio.charset.Charset;

public class bluetooth_home extends AppCompatActivity {

    private static final String TAG = "Main Activity";
    TextView showReceived;
    EditText inputMessage;
    Button sendButton;
    ProgressDialog myDialog;
    SharedPreferences sharedPreferences;
    SharedPreferences.Editor editor;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.bluetooth_home);

        Button bluetoothButton = (Button) findViewById(R.id.bluetoothButton);
        showReceived = findViewById(R.id.showReceived);
        inputMessage = findViewById(R.id.inputMessage);
        sendButton = findViewById((R.id.sendButton));
        LocalBroadcastManager.getInstance(this).registerReceiver(messageReceiver, new IntentFilter("incomingMessage"));
        bluetoothButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent popup = new Intent(bluetooth_home.this, BluetoothPopUp.class);
                startActivity(popup);
            }
        });

        sendButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                inputMessage =  findViewById(R.id.inputMessage);
                String message = inputMessage.getText().toString();
                if (BluetoothConnectionService.BluetoothConnectionStatus == true) {
                    byte[] bytes = message.getBytes(Charset.defaultCharset());
                    BluetoothConnectionService.write(bytes);
                }
            }
        });

        myDialog = new ProgressDialog(bluetooth_home.this);
        myDialog.setMessage("Waiting for other device to reconnect...");
        myDialog.setCancelable(false);
        myDialog.setButton(DialogInterface.BUTTON_NEGATIVE, "Cancel", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.dismiss();
            }
        });

    }
    private BroadcastReceiver connectionWatcher2 = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            BluetoothDevice mDevice = intent.getParcelableExtra("Device");
            String status = intent.getStringExtra("Status");
            Log.d(TAG, "I'm in MAIN ACTIVITY");
            if(status.equals("connected")){
                try {
                    myDialog.dismiss();
                } catch(NullPointerException e){
                    e.printStackTrace();
                }
                if (sharedPreferences.contains("connStatus"))
                {
                    editor = sharedPreferences.edit();
                    editor.putString("connStatus", "Connected to " + mDevice.getName());
                    editor.commit();
                }
                Log.d(TAG, "connectionWatcher2: Device now connected to "+mDevice.getName());
//                Toast.makeText(MainActivity.this, "Device now connected to "+mDevice.getName(), Toast.LENGTH_LONG).show();

            }
            else if(status.equals("disconnected")){
                sharedPreferences = getApplicationContext().getSharedPreferences("Shared Preferences", Context.MODE_PRIVATE);
                if (sharedPreferences.contains("connStatus"))
                {
                    editor = sharedPreferences.edit();
                    editor.putString("connStatus", "Disconnected");
                    editor.commit();
                }
                Log.d(TAG, "connectionWatcher2: Disconnected from "+mDevice.getName());
//                Toast.makeText(MainActivity.this, "Disconnected from "+mDevice.getName(), Toast.LENGTH_LONG).show();

                myDialog.show();
            }
        }
    };

    BroadcastReceiver messageReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            String message = intent.getStringExtra("receivedMessage");
            showReceived.setText(message);
        }
    };
    @Override
    protected void onDestroy(){
        super.onDestroy();
        try{
            LocalBroadcastManager.getInstance(this).unregisterReceiver(messageReceiver);
            LocalBroadcastManager.getInstance(this).unregisterReceiver(connectionWatcher2);
        } catch(IllegalArgumentException e){
            e.printStackTrace();
        }
    }

    @Override
    protected void onPause(){
        super.onPause();
        try{
            LocalBroadcastManager.getInstance(this).unregisterReceiver(connectionWatcher2);
        } catch(IllegalArgumentException e){
            e.printStackTrace();
        }
    }

    @Override
    protected void onResume(){
        super.onResume();
        try{
            IntentFilter filter2 = new IntentFilter("ConnectionStatus");
            LocalBroadcastManager.getInstance(this).registerReceiver(connectionWatcher2, filter2);
        } catch(IllegalArgumentException e){
            e.printStackTrace();
        }
    }
}