/*
 * Kibbly: stepper motor test for circuit 1 (DRV8825 on its carrier board)
 *
 * Board: NUCLEO-F439ZI. Make a new STM32CubeIDE project for the board, answer "No" to
 * "Initialize all peripherals with their default Mode?", then replace the whole
 * Core/Src/main.c with this file. No pin needs to be set in the .ioc: this file sets
 * its own clock and pins. Do not regenerate code from the .ioc afterwards, or this
 * file is overwritten.
 *
 * Wiring (hardware/04_wiring_list.md, section 6B):
 *   STEP  PE9  (D6, CN10 pin 4)   carrier S, through column 11
 *   DIR   PF13 (D7, CN10 pin 2)   carrier D, through column 10
 *   EN    PF15 (D2, CN10 pin 12)  carrier E, through column 9; low = motor on
 * Carrier switches 1 OFF, 2 OFF, 3 ON: 1/16 step, 3200 steps per turn.
 *
 * What it does, again and again:
 *   1. LD2 (blue) on, motor on, one turn forward in 4 s
 *   2. pause 1 s, one turn back
 *   3. motor off, LD2 off, LD1 (green) blinks for 2 s while the motor rests
 * If LD1 blinks but the motor does not move, the code runs: check the wiring and Vref.
 */
#include "main.h"

#define STEPS_PER_TURN 3200U  /* 200 full steps times 16 microsteps */
#define HALF_PERIOD_US 625U   /* 800 steps per second: one turn in 4 s; bigger is slower */

static void SystemClock_Config(void);
static void gpio_init(void);
static void delay_us(uint32_t us);
static void motor_enable(int on);
static void motor_steps(uint32_t steps, int forward);

int main(void)
{
  HAL_Init();
  SystemClock_Config();
  gpio_init();

  /* start the cycle counter used by delay_us */
  CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;
  DWT->CYCCNT = 0;
  DWT->CTRL |= DWT_CTRL_CYCCNTENA_Msk;

  motor_enable(0);
  HAL_Delay(2000);

  while (1)
  {
    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_7, GPIO_PIN_SET);    /* LD2 on: moving */
    motor_enable(1);
    motor_steps(STEPS_PER_TURN, 1);                        /* one turn forward */
    HAL_Delay(1000);
    motor_steps(STEPS_PER_TURN, 0);                        /* one turn back */
    motor_enable(0);                                       /* rest: motor free and cool */
    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_7, GPIO_PIN_RESET);

    for (int i = 0; i < 4; i++)                            /* 2 s rest, LD1 blinking */
    {
      HAL_GPIO_TogglePin(GPIOB, GPIO_PIN_0);
      HAL_Delay(500);
    }
  }
}

/* EN is active low: 0 V turns the motor on */
static void motor_enable(int on)
{
  HAL_GPIO_WritePin(GPIOF, GPIO_PIN_15, on ? GPIO_PIN_RESET : GPIO_PIN_SET);
}

static void motor_steps(uint32_t steps, int forward)
{
  HAL_GPIO_WritePin(GPIOF, GPIO_PIN_13, forward ? GPIO_PIN_SET : GPIO_PIN_RESET);
  delay_us(5);  /* let DIR settle before the first step */
  for (uint32_t i = 0; i < steps; i++)
  {
    HAL_GPIO_WritePin(GPIOE, GPIO_PIN_9, GPIO_PIN_SET);
    delay_us(HALF_PERIOD_US);
    HAL_GPIO_WritePin(GPIOE, GPIO_PIN_9, GPIO_PIN_RESET);
    delay_us(HALF_PERIOD_US);
  }
}

static void delay_us(uint32_t us)
{
  uint32_t start = DWT->CYCCNT;
  uint32_t ticks = us * (SystemCoreClock / 1000000U);
  while ((DWT->CYCCNT - start) < ticks)
  {
  }
}

static void gpio_init(void)
{
  GPIO_InitTypeDef g = {0};

  __HAL_RCC_GPIOB_CLK_ENABLE();
  __HAL_RCC_GPIOE_CLK_ENABLE();
  __HAL_RCC_GPIOF_CLK_ENABLE();

  /* levels set before the pins become outputs: EN high (motor off), STEP and DIR low, LEDs off */
  HAL_GPIO_WritePin(GPIOF, GPIO_PIN_15, GPIO_PIN_SET);
  HAL_GPIO_WritePin(GPIOF, GPIO_PIN_13, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(GPIOE, GPIO_PIN_9, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0 | GPIO_PIN_7, GPIO_PIN_RESET);

  g.Mode = GPIO_MODE_OUTPUT_PP;
  g.Pull = GPIO_NOPULL;
  g.Speed = GPIO_SPEED_FREQ_LOW;

  g.Pin = GPIO_PIN_9;                 /* STEP */
  HAL_GPIO_Init(GPIOE, &g);
  g.Pin = GPIO_PIN_13 | GPIO_PIN_15;  /* DIR, EN */
  HAL_GPIO_Init(GPIOF, &g);
  g.Pin = GPIO_PIN_0 | GPIO_PIN_7;    /* LD1 green, LD2 blue */
  HAL_GPIO_Init(GPIOB, &g);
}

/* 16 MHz from the internal HSI oscillator: no crystal setting needed, plenty for this test */
static void SystemClock_Config(void)
{
  RCC_OscInitTypeDef osc = {0};
  RCC_ClkInitTypeDef clk = {0};

  osc.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  osc.HSIState = RCC_HSI_ON;
  osc.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  osc.PLL.PLLState = RCC_PLL_NONE;
  if (HAL_RCC_OscConfig(&osc) != HAL_OK)
  {
    Error_Handler();
  }

  clk.ClockType = RCC_CLOCKTYPE_HCLK | RCC_CLOCKTYPE_SYSCLK | RCC_CLOCKTYPE_PCLK1 | RCC_CLOCKTYPE_PCLK2;
  clk.SYSCLKSource = RCC_SYSCLKSOURCE_HSI;
  clk.AHBCLKDivider = RCC_SYSCLK_DIV1;
  clk.APB1CLKDivider = RCC_HCLK_DIV1;
  clk.APB2CLKDivider = RCC_HCLK_DIV1;
  if (HAL_RCC_ClockConfig(&clk, FLASH_LATENCY_0) != HAL_OK)
  {
    Error_Handler();
  }
}

void Error_Handler(void)
{
  __disable_irq();
  while (1)
  {
  }
}
