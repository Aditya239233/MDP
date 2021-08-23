package com.example.mdp_android;

import android.os.Bundle;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

public class interactive_control extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.interactive_control_layout);
        Button north_button = findViewById(R.id.button4);
        Button south_button = findViewById(R.id.button5);
        Button west_button = findViewById(R.id.button6);
        Button east_button = findViewById(R.id.button7);
    }

}