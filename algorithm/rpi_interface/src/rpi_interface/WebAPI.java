package rpi_interface;


import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.Map;

import org.apache.hc.client5.http.classic.methods.HttpGet;
import org.apache.hc.client5.http.classic.methods.HttpPost;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.CloseableHttpResponse;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.core5.http.ContentType;
import org.apache.hc.core5.http.HttpEntity;
import org.apache.hc.core5.http.impl.DefaultConnectionReuseStrategy;
import org.apache.hc.core5.http.io.entity.EntityUtils;
import org.apache.hc.core5.http.io.entity.StringEntity;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import rpi_interface.Entity.Arena;

public class WebAPI {	
	
	
	public static Map get(String url) throws IOException {
		GsonBuilder builder = new GsonBuilder();
    	Gson gson = builder.create();
    	CloseableHttpClient httpclient = HttpClients.createDefault();
    	HttpGet httpGet = new HttpGet(url);
        
        try (CloseableHttpResponse response = httpclient.execute(httpGet)) {
            System.out.println(response.getCode() + " " + response.getReasonPhrase());
            HttpEntity entity = response.getEntity();
            InputStream in = entity.getContent();
            String jsonString = new String(in.readAllBytes(), StandardCharsets.UTF_8);
            System.out.println(jsonString);
            EntityUtils.consume(entity);
            
        	Map params = gson.fromJson(jsonString, Map.class);
        	
        	return params;
        }
	}
	
	public static Map post(String url, Arena arena) throws IOException {
		CloseableHttpClient httpclient = HttpClients.createDefault();
		GsonBuilder builder = new GsonBuilder();
    	Gson gson = builder.create();
    	
		HttpPost httpPost = new HttpPost(url);
		String arenaJson = gson.toJson(arena);
		System.out.println(arenaJson);
		StringEntity se = new StringEntity(arenaJson, ContentType.APPLICATION_JSON);
		httpPost.setEntity(se);
		
		try (CloseableHttpResponse response = httpclient.execute(httpPost)) {
            System.out.println(response.getCode() + " " + response.getReasonPhrase());
            HttpEntity entity = response.getEntity();
            InputStream in = entity.getContent();
            String jsonString = new String(in.readAllBytes(), StandardCharsets.UTF_8);
            EntityUtils.consume(entity);
            
        	Map params = gson.fromJson(jsonString, Map.class);
        	
        	return params;
        }
	}
}
