package com.selimhorri.app.service.impl;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.transaction.annotation.Transactional;

import org.springframework.stereotype.Service;

import com.selimhorri.app.dto.VerificationTokenDto;
import com.selimhorri.app.exception.wrapper.VerificationTokenNotFoundException;
import com.selimhorri.app.helper.VerificationTokenMappingHelper;
import com.selimhorri.app.repository.VerificationTokenRepository;
import com.selimhorri.app.service.VerificationTokenService;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@Slf4j
@RequiredArgsConstructor
public class VerificationTokenServiceImpl implements VerificationTokenService {

	private final VerificationTokenRepository verificationTokenRepository;

	@Override
	@Transactional(readOnly = true)
	public List<VerificationTokenDto> findAll() {
		log.info("*** VerificationTokenDto List, service; fetch all verificationTokens *");
		return this.verificationTokenRepository.findAll()
				.stream()
				.map(VerificationTokenMappingHelper::map)
				.distinct()
				.collect(Collectors.toUnmodifiableList());
	}

	@Override
	@Transactional(readOnly = true)
	public VerificationTokenDto findById(final Integer verificationTokenId) {
		log.info("*** VerificationTokenDto, service; fetch verificationToken by ids *");
		return this.verificationTokenRepository.findById(verificationTokenId)
				.map(VerificationTokenMappingHelper::map)
				.orElseThrow(() -> new VerificationTokenNotFoundException(String
						.format("#### VerificationToken with id: %d not found! ####", verificationTokenId)));
	}

	@Override
	@Transactional
	public VerificationTokenDto save(final VerificationTokenDto verificationTokenDto) {
		log.info("*** VerificationTokenDto, service; save verificationToken *");
		return VerificationTokenMappingHelper.map(this.verificationTokenRepository
				.save(VerificationTokenMappingHelper.map(verificationTokenDto)));
	}

	@Override
	@Transactional
	public VerificationTokenDto update(final VerificationTokenDto verificationTokenDto) {
		log.info("*** VerificationTokenDto, service; update verificationToken *");
		return VerificationTokenMappingHelper.map(this.verificationTokenRepository
				.save(VerificationTokenMappingHelper.map(verificationTokenDto)));
	}

	@Override
	@Transactional
	public VerificationTokenDto update(final Integer verificationTokenId,
			final VerificationTokenDto verificationTokenDto) {
		log.info("*** VerificationTokenDto, service; update verificationToken with verificationTokenId *");
		return VerificationTokenMappingHelper.map(this.verificationTokenRepository.save(
				VerificationTokenMappingHelper.map(this.findById(verificationTokenId))));
	}

	@Override
	@Transactional
	public void deleteById(final Integer verificationTokenId) {
		log.info("*** Void, service; delete verificationToken by id *");
		this.verificationTokenRepository.deleteById(verificationTokenId);
	}

}
