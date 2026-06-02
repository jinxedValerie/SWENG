const int PIN_BTN_1 = 0;
const int PIN_BTN_2 = 1;
const int PIN_TRIAC = 3;
const int PIN_ZERO_CROSS = 6;
const int PIN_ZERO_CROSS_INT = 9;
const int PIN_LED_1 = 14;
const int PIN_LED_2 = 15;

volatile bool zeroCrossDetected = false;

typedef unsigned long millis_t;

millis_t prevBlink = 0;
const millis_t BLINK_INTERVAL = 1000;

millis_t prevButtonDebounce = 0;

const int FREQUENCY = 50;

int degree = 30;
const int MIN_DEGREE = 6;
const int MAX_DEGREE = 176;
const int DEGREE_STEP = 1;

bool lampActive = true;

void zeroCrossISR()
{
    zeroCrossDetected = true;
}

void setup()
{
    pinMode(PIN_BTN_1, INPUT);
    pinMode(PIN_BTN_2, INPUT);
    pinMode(PIN_TRIAC, OUTPUT);
    pinMode(PIN_LED_1, OUTPUT);

    attachInterrupt(digitalPinToInterrupt(PIN_ZERO_CROSS_INT), zeroCrossISR, RISING);
}

// puts the triac pins on high for 10us to ignite it
void igniteTriac()
{
    digitalWrite(PIN_TRIAC, HIGH);
    delayMicroseconds(10);
    digitalWrite(PIN_TRIAC, LOW);
}

// returns true and sets lastTrigger to now, if the delay was exceeded
// otherwise returns false
bool exceededDelay(millis_t *lastTrigger, millis_t delay)
{
    unsigned long current = millis();
    if (current - *lastTrigger > delay)
    {
        *lastTrigger = current;
        return true;
    }
    return false;
}

// adjusts the degree if buttons are pressed, only runs every 100us
// 10° shift per second pressed with DEGREE_STEP = 1
void checkButtons()
{
    if (!exceededDelay(&prevButtonDebounce, 100))
    {
        return;
    }

    if (digitalRead(PIN_BTN_1) == HIGH)
    {
        if (degree >= (MIN_DEGREE + DEGREE_STEP))
        {
            degree -= DEGREE_STEP;
        }
    }

    if (digitalRead(PIN_BTN_2) == HIGH)
    {
        if (degree <= (MAX_DEGREE - DEGREE_STEP))
        {
            degree += DEGREE_STEP;
        }
    }
}

void loop()
{
    checkButtons();

    if (exceededDelay(&prevBlink, BLINK_INTERVAL))
    {
        lampActive = !lampActive;
        digitalWrite(PIN_LED_1, lampActive ? HIGH : LOW); // trigger debug led
    }

    // act on zero cross detected
    if (zeroCrossDetected)
    {
        zeroCrossDetected = false;

        if (lampActive)
        {
            float delay_seconds = ((float)degree / (float)360) / (float)FREQUENCY;
            // alternative? unsigned long delay_us = (degree * 10000UL) / 180UL <=> (degree/180)*T/2
            delayMicroseconds(delay_seconds * 1000000);
            igniteTriac();
        }
    }
}