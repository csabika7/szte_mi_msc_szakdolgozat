package hu.uszeged.weedrecognition.image.predict;

import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.UUID;

import hu.uszeged.weedrecognition.MainActivity;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class ImagePredictionClient {

    private final OkHttpClient okHttpClient;
    private final String predictUrl;

    public ImagePredictionClient(OkHttpClient okHttpClient, String proto, String host, String port) {
        this.okHttpClient = okHttpClient;
        this.predictUrl = String.format("%s://%s:%s/v1/model/predict", proto, host, port);

    }

    public String predict(byte[] pngImg) throws IOException {
        Request request = new Request.Builder()
                .url(predictUrl)
                .post(new MultipartBody.Builder()
                        .setType(MultipartBody.FORM)
                        .addFormDataPart("img",
                                UUID.randomUUID().toString() + ".png",
                                RequestBody.create(pngImg, MediaType.parse("image/png"))).build())
                .build();
        try (Response response = okHttpClient.newCall(request).execute()) {
            String responseBody = response.body().string();
            Log.i(MainActivity.class.getName(), responseBody);
            JSONObject json = new JSONObject(responseBody);
            return json.getString("name");
        } catch (JSONException e) {
            throw new IOException(e);
        }
    }

}
