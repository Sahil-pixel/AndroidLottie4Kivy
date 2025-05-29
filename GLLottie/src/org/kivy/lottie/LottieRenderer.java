package org.kivy.lottie;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.PorterDuff;

import android.graphics.SurfaceTexture;
import android.util.Log;
import android.view.Surface;

import com.airbnb.lottie.LottieComposition;
import com.airbnb.lottie.LottieCompositionFactory;
import com.airbnb.lottie.LottieDrawable;
import com.airbnb.lottie.LottieListener;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;

import android.animation.Animator;

public class LottieRenderer {
    private final LottieDrawable drawable;
    private Surface surface;
    private LottieComposition composition;
    private boolean loaded = false;
    private final OnLottieLoadListener listener;
    private InputStream inputStream;
    private final Context context;

    public LottieRenderer(Context context,OnLottieLoadListener listener) {
        this.context = context;
        this.drawable = new LottieDrawable();
        this.listener = listener;
        //setFile(filePath);
    }

    public void setFile(String filePath) {
        clear();  // Clear existing animation if any

        try {
            inputStream = new FileInputStream(new File(filePath));

            LottieCompositionFactory.fromJsonInputStream(inputStream, null)
                .addListener(new LottieListener<LottieComposition>() {
                    @Override
                    public void onResult(LottieComposition comp) {
                        composition = comp;
                        drawable.setComposition(comp);
                        drawable.setRepeatCount(LottieDrawable.INFINITE);
                        loaded = true;
                        Log.i("python", "Lottie file loaded successfully");

                        if (listener != null) {
                            listener.onLoaded(comp, loaded);
                        }
                    }
                })
                .addFailureListener(new LottieListener<Throwable>() {
                    @Override
                    public void onResult(Throwable e) {
                        loaded = false;
                        Log.e("python", "Failed to load Lottie file", e);
                        if (listener != null) {
                            listener.onFailed(e);
                        }
                    }
                });

        } catch (FileNotFoundException e) {
            loaded = false;
            Log.e("python", "Lottie file not found at: " + filePath, e);
            if (listener != null) {
                listener.onFailed(e);
            }
        }
    }

    public void setSurfaceTexture(SurfaceTexture st) {
        if (surface != null) {
            surface.release();
        }
        this.surface = new Surface(st);
    }

    public void renderFrame() {
    if (!loaded || surface == null || !surface.isValid()) return;

    Canvas canvas = surface.lockCanvas(null);
    if (canvas != null) {
        // 🔴 Clear old frame before drawing
        canvas.drawColor(Color.TRANSPARENT, PorterDuff.Mode.CLEAR);

        int w = canvas.getWidth();
        int h = canvas.getHeight();
        if (w > 0 && h > 0) {
            drawable.setBounds(0, 0, w, h);
            drawable.draw(canvas);
        }
        surface.unlockCanvasAndPost(canvas);
    }
}


    public boolean isLoaded() {
        return loaded;
    }

    public int getIntrinsicWidth() {
        return (composition != null) ? composition.getBounds().width() : 0;
    }

    public int getIntrinsicHeight() {
        return (composition != null) ? composition.getBounds().height() : 0;
    }

    // Playback Controls
    public void play() {
        if (loaded) drawable.playAnimation();
    }

    public void pause() {
        if (loaded) drawable.pauseAnimation();
    }

    public void resume() {
        if (loaded) drawable.resumeAnimation();
    }

    public void stop() {
        if (loaded) drawable.cancelAnimation();
    }

    public void setSpeed(float speed) {
        if (loaded) drawable.setSpeed(speed);
    }

    public void setRepeatCount(int count) {
        if (loaded) drawable.setRepeatCount(count);
    }

    public int getRepeatCount() {
        return loaded ? drawable.getRepeatCount() : 0;
    }

    public void setRepeatMode(int mode) {
        if (loaded) drawable.setRepeatMode(mode);
    }

    public int getRepeatMode() {
        return loaded ? drawable.getRepeatMode() : -1;
    }

    public boolean isRunning() {
        return loaded && drawable.isAnimating();
    }

    // Progress Controls
    public void setProgress(float progress) {
        if (loaded) drawable.setProgress(progress);
    }

    public float getProgress() {
        return loaded ? drawable.getProgress() : 0f;
    }

    public float getDuration() {
        return (composition != null) ? composition.getDuration() : 0f;
    }

    // Animator Listeners
    public void addAnimatorListener(Animator.AnimatorListener listener) {
        if (loaded) drawable.addAnimatorListener(listener);
    }

    public void removeAnimatorListener(Animator.AnimatorListener listener) {
        if (loaded) drawable.removeAnimatorListener(listener);
    }

    // Cleanup
    public void clear() {
        stop();
        composition = null;
        drawable.clearComposition();
        if (surface != null) {
            surface.release();
            surface = null;
        }
        loaded = false;
    }

    public void clearSurface() {
    if (surface != null && surface.isValid()) {
        try {
            Canvas canvas = surface.lockCanvas(null);
            if (canvas != null) {
                canvas.drawColor(Color.TRANSPARENT, PorterDuff.Mode.CLEAR);
                surface.unlockCanvasAndPost(canvas);
            }
        } catch (Exception e) {
            Log.e("LottieRenderer", "Failed to clear surface", e);
        }
    }
}

}
