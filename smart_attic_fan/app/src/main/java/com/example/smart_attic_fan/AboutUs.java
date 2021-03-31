// Author: James Mastran jam2454
// Columbia University Project
package com.example.smart_attic_fan;

import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.SocketTimeoutException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.concurrent.ExecutionException;


// Followed: https://www.tutorialspoint.com/how-to-integrate-android-speech-to-text
// For getting text to speech
public class AboutUs extends AppCompatActivity {
    private final int REQ_CODE = 100;
    private final String ngrokURL = "06e3e0a1a4ae.ngrok.io";
    private final String aws_url = "ec2-3-141-199-6.us-east-2.compute.amazonaws.com";
    TextView about_us_text;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.about_us);
        about_us_text = (TextView) findViewById(R.id.about_us_text);
        about_us_text.setText("Columbia University \n" +
                "EECS E4764 Fall'19 IoT \n \n" +
                "Smart Attic Fan \n \n" +
                "James Mastran, jam2454 \n" +
                "Mark Ozdemir, mo2804 \n" +
                "Yin Zhang, yz4053");
    }
}
