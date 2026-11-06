// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

/**
 * Учебный ERC-20 токен.
 * initialSupply задаётся в целых токенах; decimals() по умолчанию равен 18.
 */
contract MyToken is ERC20 {
    constructor(
        string memory tokenName,
        string memory tokenSymbol,
        uint256 initialSupply
    ) ERC20(tokenName, tokenSymbol) {
        _mint(msg.sender, initialSupply * 10 ** decimals());
    }
}
