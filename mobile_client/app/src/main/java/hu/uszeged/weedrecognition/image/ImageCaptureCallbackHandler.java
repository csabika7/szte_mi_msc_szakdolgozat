package hu.uszeged.weedrecognition.image;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.graphics.PorterDuff;
import android.util.Log;
import android.view.View;
import android.widget.ProgressBar;

import androidx.annotation.NonNull;
import androidx.camera.core.ImageCapture;
import androidx.camera.core.ImageCaptureException;

import com.google.android.material.snackbar.BaseTransientBottomBar;
import com.google.android.material.snackbar.Snackbar;

import java.io.ByteArrayOutputStream;
import java.util.concurrent.ExecutorService;

import hu.uszeged.weedrecognition.MainActivity;
import hu.uszeged.weedrecognition.image.predict.ImagePredictionClient;
import hu.uszeged.weedrecognition.image.predict.ImagePredictionFactory;

public class ImageCaptureCallbackHandler implements ImageCapture.OnImageSavedCallback {

    private final View view;
    private final ProgressBar progressBar;
    private final ExecutorService executorService;
    private final ByteArrayOutputStream resultBuffer;

    public ImageCaptureCallbackHandler(View view, ProgressBar progressBar,
                                       ExecutorService executorService,
                                       ByteArrayOutputStream resultBuffer) {
        this.view = view;
        this.progressBar = progressBar;
        this.executorService = executorService;
        this.resultBuffer = resultBuffer;
    }

    @Override
    public void onImageSaved(@NonNull ImageCapture.OutputFileResults outputFileResults) {
        executorService.submit(() -> {
            Log.i(MainActivity.class.getName(), "Picture taken " + resultBuffer.size());
            try {
                Bitmap bitmap = BitmapFactory.decodeByteArray(resultBuffer.toByteArray(), 0, resultBuffer.size());
                ByteArrayOutputStream pngImg = new ByteArrayOutputStream();
                bitmap.compress(Bitmap.CompressFormat.PNG, 100, pngImg);
                ImagePredictionClient client = ImagePredictionFactory.create();
                String result = client.predict(pngImg.toByteArray());
                if(result == null || "".equals(result)) {
                    showErrorMessage("Unknown");
                } else {
                    showSuccessMessage(result);
                }
            } catch (Exception ex) {
                Log.e(MainActivity.class.getName(), "Connection error", ex);
                showErrorMessage("Connection Error.");
            }
        });
    }

    @Override
    public void onError(@NonNull ImageCaptureException ex) {
        Log.e(ImageCaptureCallbackHandler.class.getName(), "Unable to take picture", ex);
        showErrorMessage("Unable to take picture.");
    }

    private void showSuccessMessage(String text) {
        showMessage(text, "#a4c639");
    }

    private void showErrorMessage(String text) {
        showMessage(text, "#db5a6b");
    }

    private void showMessage(String text, String color) {
        progressBar.post(() -> progressBar.setVisibility(View.GONE));
        view.post(() -> {
            Snackbar snackbar = Snackbar.make(view, text, BaseTransientBottomBar.LENGTH_SHORT);
            View view = snackbar.getView();
            view.getBackground().setColorFilter(Color.parseColor(color), PorterDuff.Mode.SRC_IN);
            snackbar.show();
        });
    }
}
