#include "uart_driver.h"

UARTDriver::UARTDriver() : listen_state(STATE_START), acquired(false) {
  this->start_bytes[0] = 0xff;
  this->start_bytes[1] = 0xee;
  this->start_bytes[2] = 0xdd;
}

UARTDriver::~UARTDriver(void) {}

void UARTDriver::listen(void) {

  bool failed_message = false;

  // Checks for available bytes in UART Buffer
  // While loop will break when there are no more bytes or
  // Messaged has failed because of unexpected byte
  while (Serial.available() && !failed_message) {

    switch (this->listen_state) {
    // Will read buffer, checking if first bytes equal start bytes
    // Otherwise, throwaway and cycle through state machine
    // if there are still bytes available
    case STATE_START:

      if (Serial.available() >= sizeof(this->start_bytes)) {

        for (size_t i = 0; i < sizeof(this->start_bytes); i++) {
          this->inc_start_bytes[i] = Serial.read();

          // Incorrect start byte breaks loop and triggers failed message
          if (this->inc_start_bytes[i] != this->start_bytes[i]) {
            failed_message = true;
            Serial.print("Incorrect Start Byte");
            break;
          }
        }

        if (!failed_message) {
          this->listen_state = STATE_PRE_DATA;
        }
      }

      break;

    case STATE_PRE_DATA:

      if (Serial.available() >=
          sizeof(this->inc_length_bytes) + sizeof(this->inc_command_code)) {

        this->inc_command_code = Serial.read();
        for (int i = 0; i < sizeof(inc_length_bytes); i++) {
          this->inc_length_bytes[i] = Serial.read();
        }

        // Convert two length bytes into integer value (16-bits)
        this->inc_data_length = *((uint16_t *)inc_length_bytes);
        this->listen_state = STATE_DATA;
      }

      break;

    case STATE_DATA:

      // Used data length calc'd in STATE_PRE_DATA to check for appropriate
      // amount of bytes + crc bytes
      if (Serial.available() >=
          this->inc_data_length + sizeof(this->inc_crc_bytes)) {

        for (int i = 0; i < this->inc_data_length; i++) {
          this->inc_data[i] = Serial.read();
        }
        for (int i = 0; i < 4; i++) {
          this->inc_crc_bytes[i] = Serial.read();
        }

        // Convert array of bytes to single uint32 type
        uint32_t inc_crc = *((uint32_t *)this->inc_crc_bytes);

        uint32_t true_crc =
            this->generate_crc32(this->inc_data, this->inc_data_length);

        this->listen_state = STATE_START;

        if (inc_crc != true_crc) {
          failed_message = true;
          break;
        }

        this->acquired = true;
      }
      break;
    }
  }
}

// Source: https://stackoverflow.com/questions/27939882/fast-crc-algorithm
uint32_t UARTDriver::generate_crc32(const uint8_t *buf, int len) {
  int k;
  uint32_t crc = 0;
  crc = ~crc;
  while (len--) {
    crc ^= *buf++;
    for (k = 0; k < 8; k++)
      // Using CRC-32 Polynomial in reversed bit order
      crc = crc & 1 ? (crc >> 1) ^ 0xedb88320 : crc >> 1;
  }
  return ~crc;
}

void UARTDriver::print_message(void) {

  Serial.write(inc_start_bytes, sizeof(inc_start_bytes));

  Serial.write(inc_length_bytes, sizeof(inc_length_bytes));

  Serial.write(inc_data, this->inc_data_length);

  Serial.write(inc_crc_bytes, sizeof(inc_crc_bytes));
}

bool UARTDriver::is_acquired() { return this->acquired; }

void UARTDriver::set_acquired(bool acquired) { this->acquired = acquired; }

uint8_t *UARTDriver::get_data() { return this->inc_data; }

int UARTDriver::get_data_length() { return this->inc_data_length; }

uint8_t UARTDriver::get_command_code() { return this->inc_command_code; }