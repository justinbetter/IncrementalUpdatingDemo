package com.example.justfortest;

/**
 * Created by justi on 2017/3/29.
 */

public class BspatchUtils {

    static {
        System.loadLibrary("bspatch");
    }

    public static native int bspatch(String oldApk, String newApk, String patch);
}
