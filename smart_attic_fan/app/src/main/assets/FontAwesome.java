package com.example.smart_attic_fan;

import android.content.Context;
import android.graphics.Typeface;
import android.util.AttributeSet;

public class FontAwesome extends androidx.appcompat.widget.AppCompatTextView {

    public FontAwesome(Context context, AttributeSet attrs, int defStyle) {
        super(context, attrs, defStyle);
        init();
    }

    public FontAwesome(Context context, AttributeSet attrs) {
        super(context, attrs);
        init();
    }

    public FontAwesome(Context context) {
        super(context);
        init();
    }

    private void init() {

        //Font name should not contain "/".
        Typeface tf = Typeface.createFromAsset(getContext().getAssets(),
                "fontawesome-webfront.ttf");
        setTypeface(tf);
    }

}