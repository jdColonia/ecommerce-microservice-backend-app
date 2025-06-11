package com.selimhorri.app.config.template;

import java.time.Duration;

import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.cloud.client.loadbalancer.LoadBalanced;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

@Configuration
public class TemplateConfig {

	@LoadBalanced
	@Bean
	public RestTemplate restTemplateBean(RestTemplateBuilder builder) {
		return builder
				.setConnectTimeout(Duration.ofSeconds(5))
				.setReadTimeout(Duration.ofSeconds(10))
				.build();
	}

}
