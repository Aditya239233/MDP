package com.example.mdp_android;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

import java.nio.charset.Charset;

public class interactive_control extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.interactive_control_layout);
        Button north_button = findViewById(R.id.button4);
        Button south_button = findViewById(R.id.button5);
        Button west_button = findViewById(R.id.button6);
        Button east_button = findViewById(R.id.button7);

        north_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String message = "Go North";
                if (BluetoothConnectionService.BluetoothConnectionStatus == true) {
                    byte[] bytes = message.getBytes(Charset.defaultCharset());
                    BluetoothConnectionService.write(bytes);
                }
            }
        });

        south_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String message = "Go South";
                if (BluetoothConnectionService.BluetoothConnectionStatus == true) {
                    byte[] bytes = message.getBytes(Charset.defaultCharset());
                    BluetoothConnectionService.write(bytes);
                }
            }
        });

        west_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String message = "Go West";
                if (BluetoothConnectionService.BluetoothConnectionStatus == true) {
                    byte[] bytes = message.getBytes(Charset.defaultCharset());
                    BluetoothConnectionService.write(bytes);
                }
            }
        });

        east_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String message = "Go East";
                if (BluetoothConnectionService.BluetoothConnectionStatus == true) {
                    byte[] bytes = message.getBytes(Charset.defaultCharset());
                    BluetoothConnectionService.write(bytes);
                }
            }
        });

    }


}