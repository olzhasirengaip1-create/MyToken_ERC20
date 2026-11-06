# MyToken — собственный токен ERC-20

Учебный проект для демонстрации создания ERC-20 токена в Ethereum Sepolia и управления им через Python/Web3.py.

## Возможности
- Чтение имени, символа и общего предложения токена.
- Проверка баланса Ethereum-адреса.
- Перевод токенов в тестовой сети Sepolia.
- Проверка адресов и количества токенов, обработка ошибок.
- Локальный веб-интерфейс Flask.
- 5 автотестов для проверок входных данных.

## Требования
Python 3.10+ (рекомендуется 3.12), PyCharm, аккаунт MetaMask, Remix IDE и RPC endpoint Sepolia.

## Установка в PyCharm / Windows PowerShell
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```
Если PowerShell запрещает активацию окружения, используйте Python напрямую:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Развёртывание контракта
1. Откройте https://remix.ethereum.org/.
2. Создайте файл `MyToken.sol` и вставьте код из `contracts/MyToken.sol`.
3. В Remix откройте Solidity Compiler, выберите компилятор 0.8.20 или совместимый 0.8.x и нажмите Compile.
4. В Deploy & Run Transactions выберите Injected Provider - MetaMask.
5. Убедитесь, что MetaMask подключён к Sepolia и кошелёк содержит тестовый Sepolia ETH для газа.
6. В поле конструктора укажите, например: `MyToken`, `MTK`, `1000000`.
7. Нажмите Deploy и подтвердите транзакцию в MetaMask.
8. Скопируйте адрес контракта из Remix.
9. В Remix откройте Compilation Details / ABI и скопируйте ABI. Вставьте JSON-массив в `contract_abi.json`.

Примечание: контракт использует OpenZeppelin ERC20. В Remix импорт обычно загружается автоматически по импорту:
`@openzeppelin/contracts/token/ERC20/ERC20.sol`. Если Remix не разрешит импорт, используйте его File Explorer / GitHub import для OpenZeppelin Contracts.

## Настройка приложения
1. Скопируйте `.env.example` в файл `.env`.
2. Заполните `RPC_URL` адресом Sepolia RPC от выбранного провайдера.
3. Заполните `CONTRACT_ADDRESS` адресом контракта.
4. `PRIVATE_KEY` оставьте пустым для просмотра информации и балансов. Для переводов используйте только отдельный тестовый кошелёк MetaMask с тестовым ETH и тестовыми токенами.
5. Никогда не отправляйте `.env`, приватный ключ или seed-фразу другим людям и не загружайте их в GitHub.

## Запуск
```powershell
python -m app.main
```
Откройте http://127.0.0.1:5000/.

## Тесты
```powershell
pytest -v
```

## Важные замечания
- Sepolia — тестовая сеть; токены не имеют реальной стоимости.
- Не используйте основной кошелёк и реальные средства.
- Не публикуйте приватный ключ или seed-фразу.
- Приложение предназначено для локальной демонстрации, а не для публичного размещения.
