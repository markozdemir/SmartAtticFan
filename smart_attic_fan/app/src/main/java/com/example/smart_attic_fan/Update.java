// Author: James Mastran jam2454
// Columbia University Project
package com.example.smart_attic_fan;

import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import java.io.BufferedOutputStream;
import java.io.BufferedWriter;
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
public class Update extends AppCompatActivity {
    private final int REQ_CODE = 100;
    private final String ngrokURL = "06e3e0a1a4ae.ngrok.io";
    private final String aws_url = "ec2-3-141-199-6.us-east-2.compute.amazonaws.com";

    TextView desc;
    Button submit;
    EditText name_edit, email_edit, img_edit;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.update);

        submit = (Button) findViewById(R.id.button);
        desc = (TextView) findViewById(R.id.desc_text);
        name_edit   = (EditText)findViewById(R.id.edit_name);
        email_edit   = (EditText)findViewById(R.id.edit_email);
        img_edit   = (EditText)findViewById(R.id.edit_img);

        Bundle user_info = getIntent().getExtras();
        name_edit.setText(user_info.getString("name"));
        email_edit.setText(user_info.getString("email"));
        img_edit.setText(user_info.getString("img"));

        desc.setText("Update your account details below.");
        submit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    register();
                } catch (ExecutionException e) {
                    e.printStackTrace();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });
    }

    private void register() throws ExecutionException, InterruptedException {
        String type = "android_register";
        String name = name_edit.getText().toString();
        String email = email_edit.getText().toString();
        String img = img_edit.getText().toString();
        Date currentTime = Calendar.getInstance().getTime();
        String json = "{\"type\": \"" + type + "\", \"data\": {\"name\": \""+name+"\", \"email\": \""+email+"\", \"image\": \""+img+"\", \"update\": \"yes\"}}";
        Update.Connection c = new Update.Connection();
        int r = c.execute("http://" + aws_url, json, type).get();
        if (r == 200) {
            desc.setText("Updated! Please wait up to a minute for us to process your request.");
        } else {
            desc.setText("We are experiencing technical difficulties currently. Please try again later." +
                    "\n\nTry again:");
        }
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
