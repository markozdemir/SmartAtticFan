// Author: James Mastran jam2454
// Columbia University Project
package com.example.smart_attic_fan;

import android.os.Bundle;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;


// Followed: https://www.tutorialspoint.com/how-to-integrate-android-speech-to-text
// For getting text to speech
public class Register extends AppCompatActivity {
    private final int REQ_CODE = 100;
    private final String ngrokURL = "06e3e0a1a4ae.ngrok.io";
    private final String aws_url = "ec2-3-141-199-6.us-east-2.compute.amazonaws.com";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.register);
    }
}
