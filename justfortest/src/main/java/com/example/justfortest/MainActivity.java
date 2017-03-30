package com.example.justfortest;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.view.View;

import java.io.File;

public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void doPatch(View view) {
        String oldApkPath = getApplicationContext().getApplicationInfo().sourceDir;
        Log.i("justin", oldApkPath);
        final File newApk = new File(Environment.getExternalStorageDirectory(), "new.apk");
        final File patch = new File(Environment.getExternalStorageDirectory(), "patch.patch");

        if (patch.exists()) {
            BspatchUtils.bspatch(oldApkPath, newApk.getAbsolutePath(), patch.getAbsolutePath());
        }

        if (newApk.exists()) {
            install(this,newApk.getAbsolutePath());

        }

    }

    public static void install(Context context, String apkPath) {
        Intent i = new Intent(Intent.ACTION_VIEW);
        i.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        i.setDataAndType(Uri.fromFile(new File(apkPath)),
                "application/vnd.android.package-archive");
        context.startActivity(i);
    }

}
