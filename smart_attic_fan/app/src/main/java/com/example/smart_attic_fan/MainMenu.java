// Author: James Mastran jam2454
// Columbia University Project
package com.example.smart_attic_fan;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.drawable.RoundedBitmapDrawable;
import androidx.core.graphics.drawable.RoundedBitmapDrawableFactory;

import android.content.Context;
import android.content.Intent;
import android.content.res.Resources;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Typeface;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.TextView;

import com.pusher.pushnotifications.PushNotifications;

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
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import java.util.Calendar;
import java.util.Date;
import java.util.concurrent.ExecutionException;


// Followed: https://www.tutorialspoint.com/how-to-integrate-android-speech-to-text
// For getting text to speech
public class MainMenu extends AppCompatActivity {
    RelativeLayout fan_info, fan_data, fan_options, about, register;
    TextView fan_info_text, fan_data_text, fan_options_text, about_text, server, register_text,
            person_text, fan_work_text, fan_work_icon, fan_broke_icon, edit_icon;
    private Context mContext;
    private Resources mResources;
    private RelativeLayout mRelativeLayout;
    private Button mBTN;
    private ImageView mImageView;
    private Bitmap mBitmap;
    private final String aws_url = "ec2-3-141-199-6.us-east-2.compute.amazonaws.com";
    final Handler handler = new Handler();
    final int delay = 5000;
    String name, email, img;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Typeface font = Typeface.createFromAsset(getAssets(), "fontawesome-webfont.ttf");
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
        fan_work_text = (TextView) findViewById(R.id.fan_work);
        fan_work_icon = (TextView) findViewById(R.id.fan_work_icon);
        fan_work_icon.setTypeface(font); // For font awesome
        fan_broke_icon = (TextView) findViewById(R.id.fan_broke_icon);
        fan_broke_icon.setTypeface(font); // For font awesome
        mImageView = (ImageView) findViewById(R.id.profile_pic);
        edit_icon = (TextView) findViewById(R.id.edit_icon);
        edit_icon.setTypeface(font); // For font awesome

        PushNotifications.start(getApplicationContext(), "a765f340-7836-4b30-9876-beadf29c5b52");
        PushNotifications.addDeviceInterest("hello");

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

        mImageView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(v.getContext(), Update.class);
                Bundle user_info = new Bundle();
                user_info.putString("name", name);
                user_info.putString("email", email);
                user_info.putString("image", img);
                intent.putExtras(user_info); //Put your id to your next Intent
                startActivity(intent);
            }
        });

        run_check_server();

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
        } catch (ExecutionException | JSONException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    private void check_server() throws ExecutionException, InterruptedException, JSONException {
        String type = "android_check";
        Date currentTime = Calendar.getInstance().getTime();
        String json = "{\"type\": \"" + type + "\"}";
        person_text.setText("Offline. Limited\nfunctionality.");
        fan_work_icon.setVisibility(View.INVISIBLE);
        fan_broke_icon.setVisibility(View.INVISIBLE);
        edit_icon.setVisibility(View.INVISIBLE);
        MainMenu.Connection c = new MainMenu.Connection();
        CodeAndString cas = c.execute("http://" + aws_url, json, type).get();
        String response =  cas.response.replaceAll("u'", "'");
        JSONObject obj = new JSONObject(response);
        name = obj.getString("name");
        boolean broke = obj.getBoolean("is_broke");
        if (!broke) {
            fan_work_text.setText("Fan is Working");
            int col = Color.parseColor("#5B5B5B");
            fan_work_text.setTextColor(col);
            fan_work_icon.setVisibility(View.VISIBLE);
            fan_broke_icon.setVisibility(View.INVISIBLE);
        } else {
            fan_work_text.setText("Fan is Broken - Email sent");
            int col = Color.parseColor("#FF2424");
            fan_work_text.setTextColor(col);
            fan_broke_icon.setVisibility(View.VISIBLE);
            fan_work_icon.setVisibility(View.INVISIBLE);
        }
        String default_img = "https://i.pinimg.com/originals/54/7a/9c/547a9cc6b93e10261f1dd8a8af474e03.jpg";
        img = obj.getString("image");
        email = obj.getString("email");
        if (img.length() < 5)
            img = default_img;
        if (!img.startsWith("http://") && !img.startsWith("https://"))
            img = "http://" + img;
        int valid = obj.getInt("valid");
        if (cas.code == 200) {
            server.setText("");
            if (valid == 1) {
                person_text.setText("Welcome Back,\n" + name + "!");
                mContext = getApplicationContext();
                mResources = getResources();
                mImageView = (ImageView) findViewById(R.id.profile_pic);
                GetBitmapFromURLAsync getBitmapFromURLAsync = new GetBitmapFromURLAsync();
                mBitmap = getBitmapFromURLAsync.execute(img).get();
                mImageView.setImageBitmap(mBitmap);
                mImageView.setImageBitmap(mBitmap);
                RoundedBitmapDrawable drawable = null;
                drawable = createRoundedBitmapDrawableWithBorder(mBitmap);
                mImageView.setImageDrawable(drawable);
                edit_icon.setVisibility(View.VISIBLE);

            } else {
                person_text.setText("Please register for\nmore functionality.");
            }
        } else {
            server.setText("");
            person_text.setText("Offline. Limited\nfunctionality.");
        }
    }

    private class CodeAndString {
        int code;
        String response;

        public CodeAndString(int c, String r) {
            code = c;
            response = r;
        }
    }
    public static Bitmap getBitmapFromURL(String src) {
        try {
            URL url = new URL(src);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setDoInput(true);
            connection.connect();
            InputStream input = connection.getInputStream();
            Bitmap myBitmap = BitmapFactory.decodeStream(input);
            return myBitmap;
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }
    private class GetBitmapFromURLAsync extends AsyncTask<String, Void, Bitmap> {
        @Override
        protected Bitmap doInBackground(String... params) {
            return getBitmapFromURL(params[0]);
        }
    }

    // https://stackoverflow.com/questions/2471935/how-to-load-an-imageview-by-url-in-android
    private class DownloadImageTask extends AsyncTask<String, Void, Bitmap> {
        ImageView bmImage;

        public DownloadImageTask(ImageView bmImage) {
            this.bmImage = bmImage;
        }

        protected Bitmap doInBackground(String... urls) {
            String urldisplay = urls[0];
            Bitmap mIcon11 = null;
            try {
                InputStream in = new java.net.URL(urldisplay).openStream();
                mIcon11 = BitmapFactory.decodeStream(in);
            } catch (Exception e) {
                Log.e("Error", e.getMessage());
                e.printStackTrace();
            }
            return mIcon11;
        }

        protected void onPostExecute(Bitmap result) {
            bmImage.setImageBitmap(result);
        }
    }
    // Idea is from https://stackoverflow.com/questions/2938502/sending-post-data-in-android
    private class Connection extends AsyncTask<String, String, CodeAndString> {
        @Override
        protected CodeAndString doInBackground(String... args) {
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
                }
                con.disconnect();

                // Error handling
            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            } catch (ProtocolException e) {
                e.printStackTrace();
            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
            CodeAndString c = new CodeAndString(responseCode, response);
            return c;

        }

    }

    /* Inspiration from Android's docs */
    private RoundedBitmapDrawable createRoundedBitmapDrawableWithBorder(Bitmap bitmap){
        if (bitmap == null)
            return null;
        int bitmapWidth = bitmap.getWidth();
        int bitmapHeight = bitmap.getHeight();
        int borderWidthHalf = 40;
        int bitmapRadius = Math.min(bitmapWidth,bitmapHeight)/2;
        int bitmapSquareWidth = Math.min(bitmapWidth,bitmapHeight);
        int newBitmapSquareWidth = bitmapSquareWidth+borderWidthHalf;
        Bitmap roundedBitmap = Bitmap.createBitmap(newBitmapSquareWidth,newBitmapSquareWidth,Bitmap.Config.ARGB_8888);
        Canvas canvas = new Canvas(roundedBitmap);
        canvas.drawColor(Color.WHITE);
        int x = borderWidthHalf + bitmapSquareWidth - bitmapWidth;
        int y = borderWidthHalf + bitmapSquareWidth - bitmapHeight;
        canvas.drawBitmap(bitmap, x, y, null);

        Paint borderPaint = new Paint();
        borderPaint.setStyle(Paint.Style.STROKE);
        borderPaint.setStrokeWidth(borderWidthHalf*2);
        int col = Color.parseColor("#000000");
        borderPaint.setColor(col);

        canvas.drawCircle(canvas.getWidth()/2, canvas.getWidth()/2, newBitmapSquareWidth/2, borderPaint);

        RoundedBitmapDrawable roundedBitmapDrawable = RoundedBitmapDrawableFactory.create(mResources,roundedBitmap);

        roundedBitmapDrawable.setCornerRadius(bitmapRadius);

        roundedBitmapDrawable.setAntiAlias(true);
        return roundedBitmapDrawable;
    }
}
