// Author: James Mastran jam2454
// Columbia University Project
package com.example.smart_attic_fan;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.RelativeLayout;


// Followed: https://www.tutorialspoint.com/how-to-integrate-android-speech-to-text
// For getting text to speech
public class MainMenu extends AppCompatActivity {
    RelativeLayout fan_info, fan_data, fan_options, about;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.menu);

        fan_info = (RelativeLayout) findViewById(R.id.fan_information);
        fan_data = (RelativeLayout) findViewById(R.id.fan_data);
        fan_options = (RelativeLayout) findViewById(R.id.fan_options);
        about = (RelativeLayout) findViewById(R.id.about);

        fan_info.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(v.getContext(), FanInformation.class));
            }
        });

        fan_data.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(v.getContext(), FanData.class));
            }
        });

        fan_options.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(v.getContext(), FanOptions.class));
            }
        });

        about.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(v.getContext(), AboutUs.class));
            }
        });

    }

}
