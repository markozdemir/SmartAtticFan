// Author: James Mastran jam2454
// Columbia University Project
package com.example.smart_attic_fan;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.graphics.Typeface;
import android.os.Bundle;
import android.view.View;
import android.widget.RelativeLayout;
import android.widget.TextView;

import org.w3c.dom.Text;


// Followed: https://www.tutorialspoint.com/how-to-integrate-android-speech-to-text
// For getting text to speech
public class MainMenu extends AppCompatActivity {
    RelativeLayout fan_info, fan_data, fan_options, about;
    TextView fan_info_text, fan_data_text, fan_options_text, about_text;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Typeface font = Typeface.createFromAsset( getAssets(), "fontawesome-webfont.ttf" );
        setContentView(R.layout.menu);

        fan_info = (RelativeLayout) findViewById(R.id.fan_information);
        fan_info_text = (TextView) findViewById(R.id.fan_info_text);
        fan_info_text.setTypeface(font);
        fan_data = (RelativeLayout) findViewById(R.id.fan_data);
        fan_data_text = (TextView) findViewById(R.id.fan_data_text);
        fan_data_text.setTypeface(font);
        fan_options = (RelativeLayout) findViewById(R.id.fan_options);
        fan_options_text = (TextView) findViewById(R.id.fan_options_text);
        fan_options_text.setTypeface(font);
        about = (RelativeLayout) findViewById(R.id.about);
        about_text = (TextView) findViewById(R.id.about_text);
        about_text.setTypeface(font);

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
