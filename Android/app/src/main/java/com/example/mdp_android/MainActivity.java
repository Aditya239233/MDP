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
        Button button = findViewById(R.id.button1);

        button.setOnClickListener(v -> openInteractiveControlView());
    }

    public void openInteractiveControlView() {
        Intent intent = new Intent(this, interactive_control.class);
        startActivity(intent);
    }
}