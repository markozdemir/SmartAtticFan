// Author: James Mastran jam2454
// Columbia University Project
package com.example.smart_attic_fan;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.graphics.Typeface;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.RelativeLayout;
import android.widget.TextView;

import org.json.JSONException;
import org.w3c.dom.Text;

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
import java.util.Calendar;
import java.util.Date;
import java.util.concurrent.ExecutionException;


// Followed: https://www.tutorialspoint.com/how-to-integrate-android-speech-to-text
// For getting text to speech
public class MainMenu extends AppCompatActivity {
    RelativeLayout fan_info, fan_data, fan_options, about, register;
    TextView fan_info_text, fan_data_text, fan_options_text, about_text, server, register_text,
             person_text;
    private final String aws_url = "ec2-3-141-199-6.us-east-2.compute.amazonaws.com";
    final Handler handler = new Handler();
    final int delay = 20000;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Typeface font = Typeface.createFromAsset( getAssets(), "fontawesome-webfont.ttf" );
        setContentView(R.layout.menu);

        fan_info = (RelativeLayout) findViewById(R.id.fan_information);
        fan_info_text = (TextView) findViewById(R.id.fan_info_text);
        fan_info_text.setTypeface(font); // For font awesome
        fan_data = (RelativeLayout) findViewById(R.id.fan_data);
        fan_data_text = (TextView) findViewById(R.id.fan_data_text);
        fan_data_text.setTypeface(font); // For font awesome
        fan_options = (RelativeLayout) findViewById(R.id.fan_options);
        fan_options_text = (TextView) findViewById(R.id.fan_options_text);
        fan_options_text.setTypeface(font); // For font awesome
        about = (RelativeLayout) findViewById(R.id.about);
        about_text = (TextView) findViewById(R.id.about_text);
        about_text.setTypeface(font); // For font awesome
        server = (TextView) findViewById(R.id.server);
        register = (RelativeLayout) findViewById(R.id.register);
        register_text = (TextView) findViewById(R.id.register_text);
        register_text.setTypeface(font); // For font awesome
        person_text = (TextView) findViewById(R.id.person_text);

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

        register.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(v.getContext(), Register.class));
            }
        });

        run_check_server();
        person_text.setText("Welcome Back, James!");

        handler.postDelayed(new Runnable() {
            public void run() {
                run_check_server();
                handler.postDelayed(this, delay);
            }
        }, delay);
    }

    private void run_check_server() {
        try {
            check_server();
        } catch (ExecutionException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
    private void check_server() throws ExecutionException, InterruptedException {
        String type = "android_check";
        Date currentTime = Calendar.getInstance().getTime();
        String json = "{\"type\": \"" + type + "\"}";
        MainMenu.Connection c = new MainMenu.Connection();
        int r = c.execute("http://" + aws_url, json, type).get();
        if (r == 200)
            server.setText("server is on");
        else
            server.setText("server is off");
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
