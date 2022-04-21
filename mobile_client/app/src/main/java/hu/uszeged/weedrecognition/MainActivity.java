package hu.uszeged.weedrecognition;

import static androidx.camera.core.AspectRatio.RATIO_4_3;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.camera.core.Camera;
import androidx.camera.core.CameraSelector;
import androidx.camera.core.Preview;
import androidx.camera.lifecycle.ProcessCameraProvider;
import androidx.camera.view.PreviewView;
import androidx.coordinatorlayout.widget.CoordinatorLayout;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.graphics.PorterDuff;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.ProgressBar;

import com.google.android.material.snackbar.BaseTransientBottomBar;
import com.google.android.material.snackbar.Snackbar;
import com.google.common.util.concurrent.ListenableFuture;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import hu.uszeged.weedrecognition.image.predict.ImagePredictionClient;
import hu.uszeged.weedrecognition.image.predict.ImagePredictionFactory;


public class MainActivity extends AppCompatActivity implements ActivityCompat.OnRequestPermissionsResultCallback {

    private static final String[] REQUIRED_PERMISSIONS = new String[]{Manifest.permission.CAMERA, Manifest.permission.INTERNET};
    private static final int CAMERA_GRANT_SUCCESS_CODE = 1;

    private Camera camera;
    private ListenableFuture<ProcessCameraProvider> cameraProviderFuture;
    private ExecutorService cameraExecutor;
    private ProgressBar progressBar;
    private ImageView imageView;
    private PreviewView previewView;
    private CoordinatorLayout messageContainer;
    private Button takeImageButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        progressBar = findViewById(R.id.progressBar);
        imageView = findViewById(R.id.capturedImage);
        previewView = findViewById(R.id.previewView);
        messageContainer = findViewById(R.id.messageContainer);
        takeImageButton = findViewById(R.id.takePictureButton);

        progressBar.setVisibility(View.GONE);
        imageView.setVisibility(View.GONE);
        imageView.bringToFront();

        if(isAllPermissionToCameraGranted()) {
            startCamera();
        } else {
            requestPermissions(REQUIRED_PERMISSIONS, CAMERA_GRANT_SUCCESS_CODE);
        }
        cameraExecutor = Executors.newSingleThreadExecutor();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        cameraExecutor.shutdown();
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if(isAllPermissionToCameraGranted()) {
            startCamera();
        }
    }

    public void takePicture(View view) {
        takeImageButton.setAlpha(.5f);
        takeImageButton.setClickable(false);
        Bitmap bitmap = previewView.getBitmap();
        Log.i(MainActivity.class.getName(), "w: " + bitmap.getWidth() + ", h: " + bitmap.getHeight());
        imageView.setImageBitmap(bitmap);
        imageView.setVisibility(View.VISIBLE);
        progressBar.setVisibility(View.VISIBLE);
        cameraExecutor.submit(() -> {
            try {
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
                showErrorMessage("Connection Error");
            }
        });
    }

    boolean isAllPermissionToCameraGranted() {
        for (String permission : REQUIRED_PERMISSIONS) {
            if(ContextCompat.checkSelfPermission(this, permission)
                    == PackageManager.PERMISSION_DENIED) {
                return false;
            }
        }
        return true;
    }

    void startCamera() {
        cameraProviderFuture = ProcessCameraProvider.getInstance(this);
        cameraProviderFuture.addListener(() -> {
            try {
                ProcessCameraProvider cameraProvider = cameraProviderFuture.get();
                bindPreview(cameraProvider);
            } catch (ExecutionException | InterruptedException e) {
                // No errors need to be handled for this Future.
                // This should never be reached.
            }
        }, ContextCompat.getMainExecutor(this));
    }

    void bindPreview(ProcessCameraProvider cameraProvider) {
        Preview preview = new Preview.Builder()
                .setTargetAspectRatio(RATIO_4_3)
                .build();

        CameraSelector cameraSelector = new CameraSelector.Builder()
                .requireLensFacing(CameraSelector.LENS_FACING_BACK)
                .build();

        PreviewView previewView = findViewById(R.id.previewView);
        preview.setSurfaceProvider(previewView.getSurfaceProvider());

        cameraProvider.unbindAll();
        camera = cameraProvider.bindToLifecycle(this, cameraSelector, preview);
    }


    void showSuccessMessage(String text) {
        showMessage(text, "#a4c639");
    }

    void showErrorMessage(String text) {
        showMessage(text, "#db5a6b");
    }

    void showMessage(String text, String color) {
        progressBar.post(() -> progressBar.setVisibility(View.GONE));
        messageContainer.post(() -> {
            Snackbar snackbar = Snackbar.make(messageContainer, text, BaseTransientBottomBar.LENGTH_INDEFINITE);
            snackbar.setAction(R.string.ok, view -> {
                imageView.setVisibility(View.GONE);
                imageView.setImageBitmap(null);
                takeImageButton.setAlpha(1.0f);
                takeImageButton.setClickable(true);
            });
            View view = snackbar.getView();
            view.getBackground().setColorFilter(Color.parseColor(color), PorterDuff.Mode.SRC_IN);
            snackbar.show();
        });
    }

}