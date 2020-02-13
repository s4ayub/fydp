#ifndef UART_DRIVER_H
#define UART_DRIVER_H

#include <Arduino.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>

#define MAX_DATA_LENGTH 255

typedef enum { STATE_START, STATE_PRE_DATA, STATE_DATA } listen_state_t;

// @class UARTDriver
class UARTDriver {
public:
  UARTDriver();

  virtual ~UARTDriver(void);

  // State machine to read and interpret incoming UART messages following comm.
  // protocol
  void listen(void);

  // Generates CRC-32 checksum given data buffer
  // @param buf Data buffer to be checksum'd
  // @param len Size of data buffer in bytes
  // @return The 32-bit crc value
  uint32_t generate_crc32(const uint8_t *buf, int len);

  // Sends stored message over UART
  void print_message(void);

  bool is_acquired();

  void set_acquired(bool acquired);

  uint8_t* get_data();

  int get_data_length();

  uint8_t get_command_code();


private:
  bool acquired;
  uint8_t start_bytes[3];
  listen_state_t listen_state;
  uint8_t inc_start_bytes[3];
  uint8_t inc_command_code;
  uint8_t inc_length_bytes[2];
  int inc_data_length;
  uint8_t inc_data[MAX_DATA_LENGTH];
  uint8_t inc_crc_bytes[4];
};

#endif
