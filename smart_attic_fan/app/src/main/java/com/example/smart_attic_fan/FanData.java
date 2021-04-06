// Author: James Mastran jam2454
// Columbia University Project
package com.example.smart_attic_fan;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.SocketTimeoutException;
import java.net.URL;
import java.sql.Connection;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.concurrent.ExecutionException;

public class FanData extends AppCompatActivity {
    private final String aws_url = "ec2-3-141-199-6.us-east-2.compute.amazonaws.com";
    TextView data_text, dataTextView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.fan_data);
        data_text = (TextView) findViewById(R.id.data_text);
        set_information(0);
    }
    private void set_information() throws Exception {
        String type = "req_test_img";
        String json =   "{\"type\": \"" + type + "\"}";
        data_text.setText("Downloading data...");
        Connection c = new Connection();
        Bitmap b = c.execute("http://" + aws_url, json, type).get();
        if (b == null) {
            throw new Exception();
        }
        ImageView myImage = (ImageView) findViewById(R.id.imageView3);
        myImage.setImageBitmap(b);
        data_text.setText("Graph 1:");
    }

    private void set_information(int attmpts)  {
        int threshold = 5;
        if (attmpts > threshold) {
            data_text.setText("Failed Loading Data");
            return;
        }
        try {
            set_information();
        } catch (IOException | ExecutionException | InterruptedException e) {
            e.printStackTrace();
            set_information(attmpts+1);
        } catch (Exception e2) {
            e2.printStackTrace();
            set_information(attmpts+1);
        }
    }

    // Idea is from https://stackoverflow.com/questions/2938502/sending-post-data-in-android
    private class Connection extends AsyncTask<String, String, android.graphics.Bitmap> {
        @Override
        protected android.graphics.Bitmap doInBackground(String... args) {
            String ngrokString = args[0]; // URL to call
            String commandJson = args[1]; //data to post
            OutputStream out = null;
            android.graphics.Bitmap bitmap = null;

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
                InputStream is = con.getInputStream();
                bitmap = BitmapFactory.decodeStream(new BufferedInputStream(is));
                out.close();
                con.disconnect();

                // Error handling
            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (SocketTimeoutException e) {
                // do nothing
            } catch (Exception e) {
                e.printStackTrace();
            }

            return bitmap;
        }
    }
}
