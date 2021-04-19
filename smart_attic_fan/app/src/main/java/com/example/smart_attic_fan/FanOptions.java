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
import android.widget.CompoundButton;
import android.widget.ImageView;
import android.widget.Switch;
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
public class FanOptions extends AppCompatActivity {

    Switch fan_on_off;
    private final String aws_url = "ec2-3-141-199-6.us-east-2.compute.amazonaws.com";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.fan_options);
        fan_on_off = (Switch) findViewById(R.id.fan_on_off);
        fan_on_off.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked) {
                    try {
                        update_fan_on_off(true);
                    } catch (ExecutionException e) {
                        e.printStackTrace();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                } else {
                    try {
                        update_fan_on_off(false);
                    } catch (ExecutionException e) {
                        e.printStackTrace();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        });
    }

    private void update_fan_on_off(boolean off) throws ExecutionException, InterruptedException {
        String type = "android_toggle_fan";
        String json = "{\"type\": \"" + type + "\", \"data\": {\"off\": \""+off+"\"}}";
        FanOptions.Connection c = new FanOptions.Connection();
        int r = c.execute("http://" + aws_url, json, type).get();
    }

    // Idea is from https://stackoverflow.com/questions/2938502/sending-post-data-in-android
    private class Connection extends AsyncTask<String, String, Integer> {
        @Override
        protected Integer doInBackground(String... args) {
            String ngrokString = args[0]; // URL to call
            String commandJson = args[1]; //data to post
            String raw_cmd = args[2];
            OutputStream out = null;
            String response = "";
            int responseCode = -1;

            try {
                // Url info
                URL url = new URL(ngrokString);
                HttpURLConnection con = (HttpURLConnection) url.openConnection();
                con.setReadTimeout(400);
                con.setConnectTimeout(400);
                con.setRequestMethod("GET");
                con.setDoInput(true);
                con.setDoOutput(true);
                out = new BufferedOutputStream(con.getOutputStream());

                // Send command json
                BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(out, "UTF-8"));
                writer.write(commandJson);
                writer.flush();
                writer.close();

                // Get response
                responseCode = con.getResponseCode();
                con.disconnect();

                // Error handling
            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (SocketTimeoutException e) {
                // do nothing
            } catch (Exception e) {
                e.printStackTrace();
            }
            return responseCode;
        }
    }
}
