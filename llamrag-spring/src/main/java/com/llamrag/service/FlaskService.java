package com.llamrag.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;

import java.util.Collections;
import java.util.Map;

@Service
public class FlaskService {

    private final RestTemplate restTemplate;
    private final String flaskUrl = "http://flask-rag-backend:5000/ask"; 

    @Autowired
    public FlaskService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public Map<String, Object> getRagResponse(String question) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        Map<String, String> map = Collections.singletonMap("question", question);

        HttpEntity<Map<String, String>> entity = new HttpEntity<>(map, headers);

        try {
            @SuppressWarnings("unchecked")
            Map<String, Object> response = restTemplate.postForObject(flaskUrl, entity, Map.class);
            return response;
        } catch (Exception e) {
            return Collections.singletonMap("error", "Failed to get response from RAG service: " + e.getMessage());
        }
    }
}
