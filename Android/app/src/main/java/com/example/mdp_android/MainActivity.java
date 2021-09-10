package com.example.mdp_android;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.home);
        Button interactive_button = findViewById(R.id.button1);
        Button bluetooth_button = findViewById(R.id.button2);
        Button arena_button = findViewById(R.id.button3);

        interactive_button.setOnClickListener(v -> openInteractiveControlView());
        bluetooth_button.setOnClickListener(v -> openBluetoothView());
        arena_button.setOnClickListener(v -> openArenaView());
    }


    public void openInteractiveControlView() {
        Intent intent = new Intent(this, interactive_control.class);
        startActivity(intent);
    }

    public void openBluetoothView() {
        Intent intent = new Intent(this, bluetooth_home.class);
        startActivity(intent);
    }

    public void openArenaView() {
        Intent intent = new Intent(this, arena_map.class);
        startActivity(intent);
    }
}