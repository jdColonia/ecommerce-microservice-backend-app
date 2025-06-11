package com.selimhorri.app.helper;

import com.selimhorri.app.domain.Cart;
import com.selimhorri.app.dto.CartDto;
import com.selimhorri.app.dto.UserDto;

public interface CartMappingHelper {

	public static CartDto map(final Cart cart) {
		return CartDto.builder()
				.cartId(cart.getCartId())
				.userId(cart.getUserId())
				.userDto(cart.getUserId() != null ? UserDto.builder()
						.userId(cart.getUserId())
						.build() : null)
				.build();
	}

	public static Cart map(final CartDto cartDto) {
		return Cart.builder()
				.cartId(cartDto.getCartId() != null ? cartDto.getCartId() : null)
				.userId(cartDto.getUserId() != null ? cartDto.getUserId() : null)
				.build();
	}

}
