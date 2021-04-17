// Author: James Mastran jam2454
// Columbia University Project
package com.example.smart_attic_fan;

import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.graphics.Typeface;
import android.os.AsyncTask;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONException;
import org.json.JSONObject;

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
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.Iterator;
import java.util.concurrent.ExecutionException;


// Followed: https://www.tutorialspoint.com/how-to-integrate-android-speech-to-text
// For getting text to speech
public class FanInformation extends AppCompatActivity {

    TextView temp, humid, rpm, power, time, local_temp;
    TextView temp_t, humid_t, rpm_t, power_t, time_t;
    private final String aws_url = "ec2-3-141-199-6.us-east-2.compute.amazonaws.com";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.fan_information);
        Typeface font = Typeface.createFromAsset( getAssets(), "fontawesome-webfont.ttf" );

        temp = (TextView) findViewById(R.id.temp);
        temp.setTypeface(font); // For font awesome
        humid = (TextView) findViewById(R.id.humid);
        humid.setTypeface(font); // For font awesome
        rpm = (TextView) findViewById(R.id.rpm);
        rpm.setTypeface(font); // For font awesome
        power = (TextView) findViewById(R.id.power);
        power.setTypeface(font); // For font awesome
        time = (TextView) findViewById(R.id.time);
        time.setTypeface(font); // For font awesome
        local_temp = (TextView) findViewById(R.id.local_temp);
        local_temp.setTypeface(font); // For font awesome

        temp_t = (TextView) findViewById(R.id.temp_t);
        humid_t = (TextView) findViewById(R.id.humid_t);
        rpm_t = (TextView) findViewById(R.id.rpm_t);
        power_t = (TextView) findViewById(R.id.power_t);
        time_t = (TextView) findViewById(R.id.time_t);

        try {
            set_information();
        } catch (IOException | ExecutionException | InterruptedException | JSONException e) {
            e.printStackTrace();
        }
    }

    String get_date(int unix_seconds) {
        Date date = new Date(unix_seconds * 1000);
        SimpleDateFormat jdf = new SimpleDateFormat("HH:mm:ss");
        String java_date = jdf.format(date);
        return java_date;
    }

    private void set_information() throws IOException, ExecutionException, InterruptedException, JSONException {
        String type = "req_data_climate";
        Date currentTime = Calendar.getInstance().getTime();
        String json = "{\"type\": \"" + type + "\"}";
        Connection c = new Connection();
        String response = c.execute("http://" + aws_url, json, type).get();
        response = response.replaceAll("u'", "'");
        JSONObject responseObj = new JSONObject(response);
        JSONObject mostRecent = (JSONObject) responseObj.get("recent");
        Iterator<String> keys = responseObj.keys();
        while (keys.hasNext()) {
            String key = keys.next();
            System.out.println(key);
        }

        temp_t.setText(" Temp:  " + to_fahrenheit( (Double) mostRecent.get("temp (C)")) + " F");
        humid_t.setText(" Humidity:  " + mostRecent.get("hum") + " %");
        rpm_t.setText(" RPMs:  " + mostRecent.get("RPM") + " RPMs");
        power_t.setText(" Power:  " + mostRecent.get("power") + " W");
        time_t.setText(" Time:  "  + get_date((Integer) mostRecent.get("time")));
        local_temp.setText(responseObj.get("local_temp") + " F " + responseObj.get("local_desc"));
    }

    double to_fahrenheit(double celsius) {
        return ( ( celsius*9 ) / 5 ) + 32;
    }

    // Idea is from https://stackoverflow.com/questions/2938502/sending-post-data-in-android
    private class Connection extends AsyncTask<String, String, String> {
        @Override
        protected String doInBackground(String... args) {
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
                con.setReadTimeout(2500);
                con.setConnectTimeout(2500);
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
                if (responseCode == HttpURLConnection.HTTP_OK) {
                    con.connect();
                    String line;
                    InputStream is = con.getInputStream();
                    BufferedReader in = new BufferedReader(new InputStreamReader(is));
                    while (!(line = in.readLine()).equals("END")) {
                        if (line == null)
                            break;
                        response += line;
                        break;
                    }
                    out.close();
                    con.disconnect();
                }

                // Error handling
            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (SocketTimeoutException e) {
                // do nothing
            } catch (Exception e) {
                e.printStackTrace();
            }

            if (!response.equals("")) {
                System.out.println("response: " + response);
            }
            return response + "\nStatus Code: " + responseCode;
        }
    }

}
