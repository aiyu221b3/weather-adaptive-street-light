# Weather-Adaptive Street Light

A small reinforcement learning project that uses **Q-learning** to adapt street-light brightness based on ambient light conditions.

The system combines an **Arduino**, a light sensor, and a PWM-controlled LED. The Arduino handles hardware I/O, while Python runs the Q-learning agent.

## How It Works

1. The Arduino periodically reads the ambient light sensor.
2. Python discretizes the reading into a light-level state and estimates the light trend.
3. The Q-learning agent selects one of five brightness levels.
4. The Arduino applies the corresponding PWM value to the LED.
5. A reward balances visibility against energy consumption, with an additional penalty for excessive brightness when ambient light is rapidly decreasing.
6. The Q-table is updated from the observed transition.

### State

```text
(light_level, light_trend)
```

Light level is discretized into five bins, while the trend represents whether ambient light is decreasing, stable, or increasing.

### Actions

Five brightness levels are available:

```text
0 → 0% PWM
1 → 25% PWM
2 → 50% PWM
3 → 75% PWM
4 → 100% PWM
```

## Hardware

* Arduino
* Ambient light sensor / op-amp sensor circuit
* PWM-capable LED output

## Running

Upload the Arduino sketch and connect the board over serial.

Install the Python dependency:

```bash
pip install pyserial
```

Then update the serial port in the Python script:

```python
env = StreetLightEnv(port="COM3", baud_r=115200)
```

and run:

```bash
python main.py
```

The agent trains online while interacting directly with the physical hardware.

## Project Structure

```text
.
├── main.py
└── street_light.ino
```

This is a compact hardware-RL demonstration rather than a production street-light controller for a microproject 4th sem.
