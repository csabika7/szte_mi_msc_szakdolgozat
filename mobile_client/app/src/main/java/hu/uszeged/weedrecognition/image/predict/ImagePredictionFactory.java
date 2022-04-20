package hu.uszeged.weedrecognition.image.predict;

import android.util.Log;

import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.security.cert.CertificateException;
import java.util.concurrent.TimeUnit;

import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSocketFactory;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;

import okhttp3.OkHttpClient;

public final class ImagePredictionFactory {

    private ImagePredictionFactory() {}

    public static ImagePredictionClient create() {
        try {
            // TODO configurable address
            return new ImagePredictionClient(createHttpClient(), "https", "weedrecognition.com", "31152");
        } catch (NoSuchAlgorithmException | KeyManagementException ex) {
            Log.e(ImagePredictionFactory.class.getName(), "Unable to create http client", ex);
            return null;
        }
    }


    private static OkHttpClient createHttpClient() throws NoSuchAlgorithmException, KeyManagementException {
        X509TrustManager trustAllCerts = getTrustManager();
        // Install the all-trusting trust manager
        final SSLContext sslContext = SSLContext.getInstance("SSL");
        sslContext.init(null, new TrustManager[] {trustAllCerts}, new java.security.SecureRandom());
        // Create an ssl socket factory with our all-trusting manager
        final SSLSocketFactory sslSocketFactory = sslContext.getSocketFactory();

        OkHttpClient.Builder builder = new OkHttpClient.Builder();
        builder.sslSocketFactory(sslSocketFactory, trustAllCerts);
        builder.hostnameVerifier((hostname, session) -> true);
        builder.readTimeout(120, TimeUnit.SECONDS);
        builder.writeTimeout(120, TimeUnit.SECONDS);
        builder.connectTimeout(120, TimeUnit.SECONDS);

        return builder.build();
    }

    private static X509TrustManager getTrustManager() {
        return new X509TrustManager() {
            @Override
            public void checkClientTrusted(java.security.cert.X509Certificate[] chain, String authType) throws CertificateException {
            }

            @Override
            public void checkServerTrusted(java.security.cert.X509Certificate[] chain, String authType) throws CertificateException {
            }

            @Override
            public java.security.cert.X509Certificate[] getAcceptedIssuers() {
                return new java.security.cert.X509Certificate[]{};
            }
        };
    }
}
