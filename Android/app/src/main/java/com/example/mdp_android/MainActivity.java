package com.example.mdp_android;

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

import androidx.appcompat.app.AppCompatActivity;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;

import java.nio.charset.Charset;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.home);
        Button interactive_button = findViewById(R.id.button1);
        Button bluetooth_button = findViewById(R.id.button2);

        interactive_button.setOnClickListener(v -> openInteractiveControlView());
        bluetooth_button.setOnClickListener(v -> openBluetoothView());
    }


    public void openInteractiveControlView() {
        Intent intent = new Intent(this, interactive_control.class);
        startActivity(intent);
    }

    public void openBluetoothView() {
        Intent intent = new Intent(this, bluetooth_home.class);
        startActivity(intent);
    }
}