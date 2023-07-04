let lastSensorValue = 0;
let sensorValue = 0;
serial.redirectToUSB();
basic.forever(function () {
  sensorValue = pins.analogReadPin(AnalogPin.P1);
  if (lastSensorValue != sensorValue) {
    serial.writeLine("");
    serial.writeNumber(sensorValue);
    lastSensorValue = sensorValue;
  }
});
