package org.kivy.lottie;
import com.airbnb.lottie.LottieComposition;
public interface OnLottieLoadListener {
    void onLoaded(LottieComposition composition, boolean loaded);
    void onFailed(Throwable e);
}
