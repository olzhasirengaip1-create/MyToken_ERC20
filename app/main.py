
"""Локальный веб-интерфейс MyToken ERC-20."""

from flask import Flask, request, render_template_string

from app.blockchain import (
    TokenClient,
    TokenError,
    validate_address,
    validate_positive_amount,
)

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MyToken — OGURI</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            font-family: Arial, sans-serif;
            color: #f5f0ff;
            background:
                radial-gradient(ellipse at 5% 40%, #4b087e55, transparent 35%),
                radial-gradient(ellipse at 95% 30%, #27117b55, transparent 35%),
                linear-gradient(135deg, #090516, #100820 55%, #080515);
        }

        main {
            max-width: 1320px;
            margin: auto;
            padding: 25px 35px 50px;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
            padding-bottom: 22px;
            border-bottom: 1px solid #7136b8;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 15px;
            font-size: 25px;
            font-weight: bold;
        }

        .logo {
            color: #a855ff;
            font-size: 38px;
        }

        .network {
            padding: 13px 22px;
            border: 1px solid #7542a9;
            border-radius: 30px;
            background: #211436;
        }

        .green {
            color: #35e878;
        }

        .hero {
            margin: 45px 0 35px;
        }

        h1 {
            margin: 0 0 15px;
            font-size: clamp(32px, 5vw, 58px);
        }

        .purple {
            color: #b45cff;
        }

        .subtitle {
            color: #c8bddb;
            font-size: 18px;
            line-height: 1.5;
        }

        .panels {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }

        .panel, .notice, .message {
            background: linear-gradient(145deg, #211333, #130d25);
            border: 1px solid #8242c4;
            border-radius: 22px;
            box-shadow: 0 0 25px #7b2bd522;
        }

        .panel {
            padding: 35px;
        }

        .panel h2 {
            margin: 0 0 12px;
            font-size: 27px;
        }

        .description {
            color: #c6b8d9;
            margin-bottom: 30px;
            line-height: 1.5;
        }

        label {
            display: block;
            margin: 18px 0 10px;
            color: #e4d8f5;
        }

        input {
            width: 100%;
            padding: 17px;
            border: 1px solid #69518a;
            border-radius: 13px;
            outline: none;
            background: #241a35;
            color: white;
            font-size: 16px;
        }

        input:focus {
            border-color: #b45cff;
            box-shadow: 0 0 12px #a855ff55;
        }

        input::placeholder {
            color: #9b8bad;
        }

        button {
            width: 100%;
            margin-top: 25px;
            padding: 17px;
            border: none;
            border-radius: 13px;
            background: linear-gradient(90deg, #922cff, #6416d6);
            color: white;
            font-size: 17px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.2s;
            box-shadow: 0 0 20px #8b2aff55;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 30px #a855ff99;
        }

        .message {
            margin: 25px 0;
            padding: 20px;
            overflow-wrap: anywhere;
            line-height: 1.5;
        }

        .error {
            border-color: #d94b75;
            color: #ffb5c8;
        }

        .balance-result {
            margin-top: 25px;
            padding: 22px;
            border: 1px solid #8242c4;
            border-radius: 15px;
            background: #211638;
        }

        .balance-label {
            color: #c5b5df;
        }

        .balance-value {
            margin-top: 10px;
            font-size: 30px;
            font-weight: bold;
            color: #b45cff;
            overflow-wrap: anywhere;
        }

        .wallet-address {
            margin-top: 12px;
            color: #b9a9ce;
            font-size: 12px;
            overflow-wrap: anywhere;
        }

        .notice {
            margin-top: 35px;
            padding: 22px;
            color: #d6c9e8;
            line-height: 1.6;
        }

        @media (max-width: 800px) {
            main {
                padding: 20px;
            }

            .panels {
                grid-template-columns: 1fr;
            }

            .panel {
                padding: 25px;
            }

            .brand {
                font-size: 20px;
            }
        }
    </style>
</head>

<body>
<main>

    <header>
        <div class="brand">
            <span class="logo">⬡</span>
            <span>MyToken</span>
            <span style="font-weight: normal; color: #c5b5df;">
                ERC-20
            </span>
        </div>

        <div class="network">
            ⚗ Сеть: Sepolia <span class="green">●</span>
        </div>
    </header>

    <section class="hero">
        <h1>Oguri Cap <span class="purple">(OGURI)</span></h1>
        <div class="subtitle">
            Веб-приложение для работы с ERC-20 токеном
            в тестовой сети Ethereum.
        </div>
    </section>

    {% if message %}
        <div class="message">{{ message }}</div>
    {% endif %}

    {% if error %}
        <div class="message error">{{ error }}</div>
    {% endif %}

    <section class="panels">

        <div class="panel">
            <h2>◈ Проверить баланс</h2>

            <p class="description">
                Вставь публичный адрес MetaMask-кошелька,
                чтобы узнать количество OGURI.
            </p>

            <form method="POST" action="/balance">
                <label>Адрес кошелька MetaMask</label>

                <input
                    type="text"
                    name="address"
                    placeholder="0x..."
                    value="{{ wallet_address or '' }}"
                    required
                >

                <button type="submit">
                    Проверить баланс
                </button>
            </form>

            {% if wallet_balance is not none %}
                <div class="balance-result">
                    <div class="balance-label">
                        Баланс твоего кошелька
                    </div>

                    <div class="balance-value">
                        {{ "{:,.8f}".format(wallet_balance) }} OGURI
                    </div>

                    <div class="wallet-address">
                        Кошелёк: {{ wallet_address }}
                    </div>
                </div>
            {% endif %}
        </div>

        <div class="panel">
            <h2>⇄ Перевести токены</h2>

            <p class="description">
                Отправь OGURI на другой Ethereum-кошелёк.
            </p>

            <form method="POST" action="/transfer">
                <label>Адрес получателя</label>

                <input
                    type="text"
                    name="recipient"
                    placeholder="0x..."
                    required
                >

                <label>Количество целых токенов</label>

                <input
                    type="number"
                    name="amount"
                    min="1"
                    step="1"
                    placeholder="Например, 100"
                    required
                >

                <button type="submit">
                    Отправить в Sepolia
                </button>
            </form>
        </div>

    </section>

    <div class="notice">
        ⓘ Учебное приложение. Работает с тестовой сетью Sepolia.
        Для отправки токенов необходим тестовый Sepolia ETH
        на кошельке отправителя для оплаты комиссии сети.
    </div>

</main>
</body>
</html>
"""


def get_client():
    return TokenClient()


def render_page(
    error=None,
    message=None,
    wallet_balance=None,
    wallet_address=None,
):
    return render_template_string(
        PAGE,
        error=error,
        message=message,
        wallet_balance=wallet_balance,
        wallet_address=wallet_address,
    )


@app.get("/")
def index():
    # При обычном открытии сайта баланс всегда скрыт.
    return render_page()


@app.post("/balance")
def balance():
    address = request.form.get("address", "").strip()

    try:
        client = get_client()

        address = validate_address(address)
        value = client.balance(address)

        return render_page(
            wallet_balance=value,
            wallet_address=address,
        )

    except (ValueError, TokenError) as exc:
        return render_page(
            error=str(exc),
            wallet_address=address,
        ), 400

    except Exception as exc:
        return render_page(
            error=f"Ошибка проверки баланса: {exc}",
            wallet_address=address,
        ), 502


@app.post("/transfer")
def transfer():
    try:
        recipient = validate_address(
            request.form.get("recipient", "")
        )

        amount = validate_positive_amount(
            request.form.get("amount", "")
        )

        client = get_client()
        tx_hash = client.transfer(recipient, amount)

        return render_page(
            message=f"Перевод отправлен! Хеш транзакции: {tx_hash}"
        )

    except (ValueError, TokenError) as exc:
        return render_page(error=str(exc)), 400

    except Exception as exc:
        return render_page(
            error=f"Ошибка отправки: {exc}"
        ), 502


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
    )
