import json
from pathlib import Path
from web3 import Web3

from app import config


class TokenError(Exception):
    """Понятная ошибка приложения о работе с токеном."""


def validate_positive_amount(amount):
    try:
        value = float(amount)
    except (TypeError, ValueError):
        raise ValueError("Введите корректное число токенов.")

    if value <= 0:
        raise ValueError("Количество токенов должно быть больше нуля.")

    if not value.is_integer():
        raise ValueError("Используйте целое число токенов.")

    return int(value)

def validate_address(address):
    if not isinstance(address, str) or not Web3.is_address(address):
        raise ValueError("Некорректный Ethereum-адрес.")

    return Web3.to_checksum_address(address)


class TokenClient:
    def __init__(self):
        if not config.RPC_URL:
            raise TokenError("Не задан RPC_URL в файле .env.")
        if not config.CONTRACT_ADDRESS:
            raise TokenError("Не задан CONTRACT_ADDRESS в файле .env.")

        self.w3 = Web3(
            Web3.HTTPProvider(
                config.RPC_URL,
                request_kwargs={"timeout": 20},
            )
        )

        if not self.w3.is_connected():
            raise TokenError(
                "Не удалось подключиться к Ethereum. "
                "Проверьте RPC_URL и интернет."
            )

        # Ищем ABI относительно корня проекта, а не рабочей папки PyCharm.
        abi_path = Path(__file__).resolve().parent.parent / config.ABI_PATH

        try:
            abi = json.loads(abi_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise TokenError(
                f"Не удалось прочитать ABI по пути: {abi_path}. "
                "Проверьте файл contract_abi.json."
            ) from exc

        if not isinstance(abi, list) or not abi:
            raise TokenError(
                "ABI пустой или имеет неверный формат. "
                "Скопируйте ABI контракта из Remix в contract_abi.json."
            )

        address = validate_address(config.CONTRACT_ADDRESS)
        self.contract = self.w3.eth.contract(address=address, abi=abi)

    def name(self):
        return self.contract.functions.name().call()

    def symbol(self):
        return self.contract.functions.symbol().call()

    def total_supply(self):
        raw = self.contract.functions.totalSupply().call()
        decimals = self.contract.functions.decimals().call()
        return raw / (10 ** decimals)

    def balance(self, address):
        address = validate_address(address)
        raw = self.contract.functions.balanceOf(address).call()
        decimals = self.contract.functions.decimals().call()
        return raw / (10 ** decimals)

    def transfer(self, recipient, amount):
        if not config.PRIVATE_KEY:
            raise TokenError(
                "Не задан PRIVATE_KEY в .env. "
                "Для чтения баланса ключ не нужен."
            )

        recipient = validate_address(recipient)
        amount = validate_positive_amount(amount)
        account = self.w3.eth.account.from_key(config.PRIVATE_KEY)

        decimals = self.contract.functions.decimals().call()
        value = amount * (10 ** decimals)

        try:
            nonce = self.w3.eth.get_transaction_count(account.address)
            tx = self.contract.functions.transfer(
                recipient, value
            ).build_transaction(
                {
                    "from": account.address,
                    "nonce": nonce,
                    "chainId": self.w3.eth.chain_id,
                    "gas": 150000,
                    "gasPrice": self.w3.eth.gas_price,
                }
            )

            signed = self.w3.eth.account.sign_transaction(
                tx, config.PRIVATE_KEY
            )
            tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(
                tx_hash, timeout=120
            )

            if receipt.status != 1:
                raise TokenError("Транзакция отклонена сетью.")

            return self.w3.to_hex(tx_hash)

        except TokenError:
            raise
        except Exception as exc:
            raise TokenError(
                f"Не удалось выполнить перевод: {exc}"
            ) from exc
