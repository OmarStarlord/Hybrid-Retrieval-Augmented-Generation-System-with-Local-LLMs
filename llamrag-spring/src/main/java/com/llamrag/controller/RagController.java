package com.llamrag.controller;

import com.llamrag.service.FlaskService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.Map;

@RestController
@RequestMapping("/api/rag")
public class RagController {

    private final FlaskService flaskService;

    @Autowired
    public RagController(FlaskService flaskService) {
        this.flaskService = flaskService;
    }

    @PostMapping("/chat")
    public Map<String, Object> chatWithRag(@RequestBody Map<String, String> payload) {
        String question = payload.get("question");
        return flaskService.getRagResponse(question);
    }
}
